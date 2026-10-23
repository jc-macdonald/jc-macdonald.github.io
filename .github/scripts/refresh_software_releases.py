"""Refresh and validate deterministic software-release data for the site and CV."""

from __future__ import annotations

import argparse
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import tomllib

ROOT = Path(__file__).resolve().parents[2]
SOURCES = ROOT / "_data/software_release_sources.json"
MANIFEST = ROOT / "_data/software_releases.json"
EDITORIAL = ROOT / "_data/software.yml"
CV = ROOT / "_data/cv.yml"
MATURITY_PREFIX = "Development Status :: "
SCHEMA_VERSION = 1
PRIVATE_CONFIG_FIELDS = (
    "version",
    "repository",
    "package",
    "docs_url",
    "docs_url_template",
    "docs_label",
    "concept_doi",
    "citation_url",
    "source_url",
    "pypi_url",
    "release_archive_doi",
    "release_archive_url",
)
PRIVATE_RECORD_FIELDS = PRIVATE_CONFIG_FIELDS + ("display_version",)
UPSTREAM_FIELDS_BY_SOURCE = {
    "pypi": frozenset(
        {
            "version",
            "maturity",
            "published",
            "published_at",
            "release_archive_doi",
            "release_archive_source",
        }
    ),
    "github-main": frozenset(
        {"version", "maturity", "published", "source_ref", "source_revision"}
    ),
    "manual": frozenset(
        {"version", "maturity", "published", "source_revision", "reviewed_at"}
    ),
}
DOI_PATTERN = re.compile(r"10\.5281/zenodo\.\d+")


def read_url(url: str, *, accept: str) -> bytes:
    """Read an HTTPS resource with bounded retries for transient failures."""
    headers = {
        "Accept": accept,
        "User-Agent": "jcmacdonald.dev-release-refresh",
    }
    if url.startswith("https://api.github.com/") and os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    request = urllib.request.Request(
        url,
        headers=headers,
    )
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return response.read()
        except (TimeoutError, urllib.error.URLError):
            if attempt == 2:
                raise
            time.sleep(2**attempt)
    raise AssertionError("retry loop ended unexpectedly")


def read_json_url(url: str) -> dict[str, object]:
    """Read a JSON object over HTTPS."""
    value = json.loads(read_url(url, accept="application/json"))
    if not isinstance(value, dict):
        raise TypeError(f"Expected a JSON object from {url}")
    return value


def maturity_from_classifiers(classifiers: list[object]) -> str:
    """Return the single declared package-maturity label."""
    matches = [
        str(value) for value in classifiers if str(value).startswith(MATURITY_PREFIX)
    ]
    if len(matches) != 1:
        raise ValueError(
            "Each package must declare exactly one Development Status classifier"
        )
    return matches[0].split(" - ", maxsplit=1)[-1].lower()


def normalized_release_version(value: object) -> str:
    """Normalize the optional ``v`` prefix used in release metadata."""
    return str(value or "").removeprefix("v")


def zenodo_release_doi(config: dict[str, object], version: str) -> str | None:
    """Find the exact Zenodo archive for a public package release.

    A concept DOI is stable across releases. The refresh resolves that concept
    through Zenodo's public API, then requires both an exact version match and
    the GitHub tag relation for the configured repository. This prevents an
    unrelated record with a similar title or version from entering the CV.
    """
    concept_doi = config.get("concept_doi")
    repository = config.get("repository")
    if not concept_doi or not repository:
        return None
    concept_match = DOI_PATTERN.fullmatch(str(concept_doi))
    if not concept_match:
        raise ValueError(f"Invalid Zenodo concept DOI: {concept_doi!r}")
    concept_id = str(concept_doi).rsplit(".", maxsplit=1)[-1]
    hits: list[object] = []
    page = 1
    total = None
    while total is None or len(hits) < total:
        query = urllib.parse.urlencode(
            {
                "q": f"conceptrecid:{concept_id}",
                "all_versions": "true",
                "sort": "newest",
                "size": 25,
                "page": page,
            }
        )
        payload = read_json_url(f"https://zenodo.org/api/records?{query}")
        hits_container = payload.get("hits")
        if not isinstance(hits_container, dict):
            raise ValueError("Zenodo response lacks a hits object")
        page_hits = hits_container.get("hits")
        page_total = hits_container.get("total")
        if not isinstance(page_hits, list) or type(page_total) is not int:
            raise ValueError("Zenodo response has invalid hits or total")
        if page_total < 0 or (total is not None and page_total != total):
            raise ValueError("Zenodo response has an inconsistent hit total")
        total = page_total
        if not page_hits and len(hits) < total:
            raise ValueError("Zenodo pagination ended before the reported total")
        hits.extend(page_hits)
        page += 1
    if len(hits) != total:
        raise ValueError("Zenodo pagination returned an unexpected number of hits")
    expected_source = f"https://github.com/{repository}/tree/v{version}"
    version_hits: list[dict[str, object]] = []
    for hit in hits:
        if not isinstance(hit, dict):
            raise ValueError("Zenodo returned a non-object record")
        if hit.get("conceptdoi") != concept_doi:
            raise ValueError("Zenodo returned a record outside the configured concept")
        metadata = hit.get("metadata")
        if not isinstance(metadata, dict):
            raise ValueError("Zenodo record lacks metadata")
        if normalized_release_version(metadata.get("version")) != version:
            continue
        version_hits.append(hit)
    matches: list[str] = []
    for hit in version_hits:
        metadata = hit["metadata"]
        assert isinstance(metadata, dict)
        resource_type = metadata.get("resource_type")
        if (
            not isinstance(resource_type, dict)
            or resource_type.get("type") != "software"
        ):
            raise ValueError("Zenodo exact-version record is not software")
        if hit.get("status") != "published":
            raise ValueError("Zenodo exact-version record is not published")
        related = metadata.get("related_identifiers", [])
        source_matches = any(
            isinstance(item, dict)
            and item.get("relation") == "isSupplementTo"
            and item.get("identifier") == expected_source
            and item.get("scheme") == "url"
            and item.get("resource_type") == "software"
            for item in related
        )
        doi = str(hit.get("doi", ""))
        if not source_matches:
            raise ValueError("Zenodo exact-version record has the wrong source relation")
        if not DOI_PATTERN.fullmatch(doi) or metadata.get("doi") != doi:
            raise ValueError("Zenodo exact-version record has inconsistent DOI metadata")
        matches.append(doi)
    if len(matches) > 1:
        raise ValueError(
            f"Zenodo returned multiple exact archives for {repository} v{version}"
        )
    return matches[0] if matches else None


def release_phase(version: str, *, published: bool) -> str:
    """Classify distribution phase separately from package maturity."""
    if not published or ".dev" in version:
        return "development"
    match = re.search(r"(a|b|rc)\d+$", version)
    return (
        {"a": "alpha", "b": "beta", "rc": "release candidate"}[match.group(1)]
        if match
        else "final"
    )


def github_project(config: dict[str, object]) -> dict[str, object]:
    """Read version and classifiers from a resolved public GitHub revision."""
    repository = str(config["repository"])
    ref = str(config.get("ref", "main"))
    path = str(config.get("pyproject_path", "pyproject.toml"))
    commit = read_json_url(f"https://api.github.com/repos/{repository}/commits/{ref}")
    revision = str(commit.get("sha", ""))
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError(f"GitHub did not return a commit SHA for {repository}@{ref}")
    url = f"https://raw.githubusercontent.com/{repository}/{revision}/{path}"
    project = tomllib.loads(read_url(url, accept="text/plain").decode())["project"]
    return {
        "version": str(project["version"]),
        "maturity": maturity_from_classifiers(list(project.get("classifiers", []))),
        "published": False,
        "source_ref": ref,
        "source_revision": revision,
    }


def pypi_project(config: dict[str, object]) -> dict[str, object]:
    """Read the current public release and classifier from PyPI."""
    package = str(config["package"])
    payload = read_json_url(f"https://pypi.org/pypi/{package}/json")
    info = payload["info"]
    if not isinstance(info, dict):
        raise TypeError(f"PyPI returned invalid project metadata for {package}")
    version = str(info["version"])
    files = payload.get("releases", {})
    uploads = files.get(version, []) if isinstance(files, dict) else []
    published_at = None
    if uploads and isinstance(uploads[0], dict):
        published_at = uploads[0].get("upload_time_iso_8601")
    configured_archives = config.get("release_archives", {})
    configured_archive = (
        configured_archives.get(version)
        if isinstance(configured_archives, dict)
        else None
    )
    resolved_archive = None
    if configured_archive is None:
        resolved_archive = zenodo_release_doi(config, version)
    archive_doi = configured_archive or resolved_archive
    return {
        "version": version,
        "maturity": maturity_from_classifiers(list(info.get("classifiers", []))),
        "published": True,
        "published_at": published_at,
        "release_archive_doi": archive_doi,
        "release_archive_source": (
            "reviewed registry"
            if configured_archive
            else ("Zenodo concept lookup" if resolved_archive else None)
        ),
    }


def manual_project(config: dict[str, object]) -> dict[str, object]:
    """Return an explicitly reviewed record for a private project."""
    return {
        "version": config.get("version"),
        "maturity": str(config["maturity"]),
        "published": False,
        "source_revision": "manual review",
        "reviewed_at": str(config["reviewed_at"]),
    }


def validate_private_config(slug: str, config: dict[str, object]) -> None:
    """Prevent reviewed private entries from carrying publishable metadata."""
    exposed = [key for key in PRIVATE_CONFIG_FIELDS if config.get(key)]
    if config.get("release_archives"):
        exposed.append("release_archives")
    if exposed:
        raise ValueError(
            f"Private release source {slug} exposes metadata: {sorted(exposed)}"
        )


def configured_docs_url(config: dict[str, object], version: str | None) -> str | None:
    """Resolve a stable or development documentation URL from reviewed config."""
    template = config.get("docs_url_template")
    if template:
        match = re.match(r"^(\d+)\.(\d+)", version or "")
        if not match:
            raise ValueError(f"Cannot derive a major.minor docs path from {version!r}")
        return str(template).format(
            version=version,
            major_minor=f"{match.group(1)}.{match.group(2)}",
        )
    return str(config["docs_url"]) if config.get("docs_url") else None


def decorate_record(
    slug: str, config: dict[str, object], upstream: dict[str, object]
) -> dict[str, object]:
    """Combine reviewed configuration with one upstream metadata snapshot."""
    source = str(config["source"])
    if config.get("visibility") == "Private":
        validate_private_config(slug, config)
    record = dict(upstream)
    version = str(record["version"]) if record.get("version") is not None else None
    published = bool(record["published"])
    visibility = str(config["visibility"])
    maturity = str(record["maturity"])
    phase = release_phase(version or "0.0.0.dev0", published=published)
    status = f"{visibility}; package maturity: {maturity}"
    if not published:
        status = f"{status}; {config.get('unreleased_label', 'unreleased')}"
    repository = str(config["repository"]) if config.get("repository") else None
    package = config.get("package")
    docs_url = configured_docs_url(config, version)
    record.update(
        {
            "slug": slug,
            "source": source,
            "repository": repository,
            "package": package,
            "visibility": visibility,
            "release_phase": phase,
            "display_status": status,
            "display_version": version
            if published
            else (f"{version} development" if version else None),
            "source_url": f"https://github.com/{repository}" if repository else None,
            "pypi_url": f"https://pypi.org/project/{package}/{version}/"
            if published
            else None,
            "docs_url": docs_url,
            "docs_label": (
                str(config["docs_label"])
                if config.get("docs_label")
                else (
                    "Release documentation"
                    if config.get("docs_url_template")
                    else ("Development documentation" if docs_url else None)
                )
            ),
        }
    )
    concept_doi = config.get("concept_doi")
    citation_ref = (
        f"v{version}"
        if published
        else record.get("source_revision", config.get("ref", "main"))
    )
    record["concept_doi"] = concept_doi
    record["citation_url"] = (
        f"https://doi.org/{concept_doi}"
        if concept_doi
        else (
            f"https://github.com/{repository}/blob/{citation_ref}/CITATION.cff"
            if repository
            else None
        )
    )
    archives = config.get("release_archives", {})
    configured_archive = archives.get(version) if isinstance(archives, dict) else None
    archive_doi = record.get("release_archive_doi") or configured_archive
    record["release_archive_doi"] = archive_doi
    record["release_archive_url"] = (
        f"https://doi.org/{archive_doi}" if archive_doi else None
    )
    record["archive_pending"] = bool(published and not archive_doi)
    if published:
        cv_status = (
            f"Release status: {visibility}; package maturity: {maturity}; "
            f"latest released version: v{version} ({phase})."
        )
    else:
        cv_status = (
            f"Release status: {status} (development version {version})."
            if version
            else f"Release status: {status}."
        )
    cv_links: list[str] = []
    if record["pypi_url"]:
        cv_links.append(f"[PyPI]({record['pypi_url']})")
    if record["release_archive_url"]:
        cv_links.append(f"[Release archive]({record['release_archive_url']})")
    if concept_doi:
        cv_links.append(f"[All versions]({record['citation_url']})")
    elif record["citation_url"]:
        cv_links.append(f"[Citation metadata]({record['citation_url']})")
    record["cv_status"] = (
        f"{cv_status} {' · '.join(cv_links)}" if cv_links else cv_status
    )
    return record


def build_record(slug: str, config: dict[str, object]) -> dict[str, object]:
    """Build one display-ready release record."""
    loaders = {
        "pypi": pypi_project,
        "github-main": github_project,
        "manual": manual_project,
    }
    source = str(config["source"])
    if source not in loaders:
        raise ValueError(f"Unsupported release source for {slug}: {source}")
    return decorate_record(slug, config, loaders[source](config))


def build_manifest(sources: dict[str, object]) -> dict[str, object]:
    """Build all records in reviewed registry order."""
    packages = sources.get("packages")
    if not isinstance(packages, dict):
        raise TypeError("Release sources must contain a packages mapping")
    return {
        "schema_version": SCHEMA_VERSION,
        "packages": {
            slug: build_record(slug, config) for slug, config in packages.items()
        },
    }


def expected_cv_line(slug: str, record: dict[str, object], indent: str) -> str:
    """Render one generated RenderCV highlight line."""
    return f'{indent}- "{record["cv_status"]}" # software-release: {slug}'


def sync_cv(manifest: dict[str, object], *, write: bool) -> None:
    """Synchronize marker-delimited release lines in the CV."""
    text = CV.read_text(encoding="utf-8")
    packages = manifest["packages"]
    if not isinstance(packages, dict):
        raise TypeError("Release manifest must contain a packages mapping")
    seen: set[str] = set()

    def replace(match: re.Match[str]) -> str:
        slug = match.group("slug")
        if slug not in packages:
            raise ValueError(f"Unknown CV software-release marker: {slug}")
        if slug in seen:
            raise ValueError(f"Duplicate CV software-release marker: {slug}")
        seen.add(slug)
        return expected_cv_line(slug, packages[slug], match.group("indent"))

    updated = re.sub(
        r'^(?P<indent>\s*)- ".*" # software-release: (?P<slug>[a-z0-9_]+)$',
        replace,
        text,
        flags=re.MULTILINE,
    )
    missing = set(packages) - seen
    if missing:
        raise ValueError(f"CV is missing software-release markers: {sorted(missing)}")
    if write:
        CV.write_text(updated, encoding="utf-8")
    elif updated != text:
        raise ValueError("CV release lines are stale; run the refresh command")


def validate_manifest(manifest: dict[str, object], sources: dict[str, object]) -> None:
    """Require aligned registry, lockfile, editorial data, and CV markers."""
    if (
        type(sources.get("schema_version")) is not int
        or sources["schema_version"] != SCHEMA_VERSION
    ):
        raise ValueError("Unsupported release-source schema_version")
    if (
        type(manifest.get("schema_version")) is not int
        or manifest["schema_version"] != SCHEMA_VERSION
    ):
        raise ValueError("Unsupported release-manifest schema_version")
    source_packages = sources.get("packages")
    manifest_packages = manifest.get("packages")
    if not isinstance(source_packages, dict) or not isinstance(manifest_packages, dict):
        raise TypeError("Source and release data must contain package mappings")
    if list(source_packages) != list(manifest_packages):
        raise ValueError("Release manifest keys/order differ from the source registry")
    upstream_keys = {
        "version",
        "maturity",
        "published",
        "published_at",
        "source_ref",
        "source_revision",
        "reviewed_at",
    }
    for slug, config in source_packages.items():
        if not isinstance(config, dict):
            raise TypeError(f"Release source for {slug} must be an object")
        record = manifest_packages[slug]
        if not isinstance(record, dict):
            raise TypeError(f"Release record for {slug} must be an object")
        source = config.get("source")
        if config.get("visibility") == "Private":
            validate_private_config(slug, config)
        if source not in UPSTREAM_FIELDS_BY_SOURCE:
            raise ValueError(f"Unsupported release source for {slug}: {source}")
        allowed_upstream = UPSTREAM_FIELDS_BY_SOURCE[source]
        unexpected_upstream = (set(record) & upstream_keys) - allowed_upstream
        if unexpected_upstream:
            raise ValueError(
                f"{source} release record has unexpected upstream fields for "
                f"{slug}: {sorted(unexpected_upstream)}"
            )
        if source == "pypi":
            if (
                record.get("published") is not True
                or not record.get("version")
                or not record.get("maturity")
                or not record.get("published_at")
            ):
                raise ValueError(
                    f"PyPI release record lacks upstream fields for {slug}"
                )
        elif source == "github-main":
            if (
                record.get("published") is not False
                or not record.get("version")
                or not record.get("maturity")
                or not record.get("source_ref")
                or not re.fullmatch(
                    r"[0-9a-f]{40}", str(record.get("source_revision", ""))
                )
            ):
                raise ValueError(
                    f"GitHub release record lacks upstream fields for {slug}"
                )
        elif source == "manual":
            reviewed_at = str(config.get("reviewed_at", ""))
            if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", reviewed_at):
                raise ValueError(f"Manual release source {slug} needs reviewed_at")
            expected_upstream = manual_project(config)
            actual_upstream = {key: record.get(key) for key in expected_upstream}
            if actual_upstream != expected_upstream:
                raise ValueError(f"Manual release record is stale for {slug}")
        upstream = {key: record[key] for key in allowed_upstream}
        expected = decorate_record(slug, config, upstream)
        if expected != record:
            raise ValueError(f"Release record is stale or invalid for {slug}")
        if record["visibility"] == "Private" and any(
            record.get(key) for key in PRIVATE_RECORD_FIELDS
        ):
            raise ValueError(f"Private release record {slug} exposes public metadata")
        if record["visibility"] == "Private" and any(
            (record.get("release_archives"), record.get("archive_pending"))
        ):
            raise ValueError(f"Private release record {slug} exposes archive metadata")
    editorial_slugs = re.findall(
        r"(?m)^- slug: ([a-z0-9_]+)$", EDITORIAL.read_text(encoding="utf-8")
    )
    if editorial_slugs != list(source_packages):
        raise ValueError(
            "Editorial software keys/order differ from the release registry"
        )
    sync_cv(manifest, write=False)


def main() -> None:
    """Refresh from upstream services or validate the committed lockfile."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    sources = json.loads(SOURCES.read_text(encoding="utf-8"))
    if args.refresh:
        manifest = build_manifest(sources)
        MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        sync_cv(manifest, write=True)
    else:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    validate_manifest(manifest, sources)
    print("Software release manifest and CV markers are consistent")


if __name__ == "__main__":
    main()
