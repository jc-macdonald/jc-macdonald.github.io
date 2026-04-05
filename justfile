set shell := ["bash", "-uc"]

# Ruby version matching CI (deploy.yml)
ruby_version := "3.3.5"

help:
	@just --list

# ── Validation (no Ruby needed) ──────────────────────────────────────

# Run all pre-push checks that don't require Ruby
check: check-yaml check-includes check-assets check-bib check-config check-cv check-rendercv check-fmt

# Validate YAML frontmatter in all pages and projects
check-yaml:
	#!/usr/bin/env bash
	set -euo pipefail
	ok=true
	for f in _pages/*.md _projects/*.md; do
		[[ -f "$f" ]] || continue
		# Must start with ---
		if ! head -1 "$f" | grep -q '^---$'; then
			echo "FAIL: $f missing opening frontmatter delimiter"
			ok=false
			continue
		fi
		# Must have closing ---
		if ! awk 'NR>1 && /^---$/{found=1; exit} END{exit !found}' "$f"; then
			echo "FAIL: $f missing closing frontmatter delimiter"
			ok=false
		fi
	done
	$ok && echo "✓ YAML frontmatter OK"

# Verify all include_relative references resolve to existing files
check-includes:
	#!/usr/bin/env bash
	set -euo pipefail
	err=0
	# Check profiles page content: references
	if [[ -f _pages/profiles.md ]]; then
		while IFS= read -r ref; do
			ref=$(echo "$ref" | tr -d '[:space:]')
			[[ -z "$ref" || "$ref" == "[]" ]] && continue
			if [[ ! -f "_pages/$ref" ]]; then
				echo "FAIL: _pages/profiles.md references '$ref' but _pages/$ref does not exist"
				err=1
			fi
		done < <(grep -E '^\s+content:\s+' _pages/profiles.md | sed 's/.*content:\s*//' || true)
	fi
	if [[ $err -eq 0 ]]; then echo "✓ Include references OK"; else exit 1; fi

# Verify referenced assets exist
check-assets:
	#!/usr/bin/env bash
	set -euo pipefail
	err=0
	# Profile images
	for f in _pages/about.md _pages/profiles.md; do
		[[ -f "$f" ]] || continue
		while IFS= read -r img; do
			img=$(echo "$img" | tr -d '[:space:]')
			[[ -z "$img" ]] && continue
			if [[ ! -f "assets/img/$img" ]]; then
				echo "WARN: $f references image '$img' but assets/img/$img not found"
			fi
		done < <(grep -E '^\s+image:\s+' "$f" | sed 's/.*image:\s*//' || true)
	done
	# CNAME must exist
	if [[ ! -f CNAME ]]; then
		echo "FAIL: CNAME file missing"
		err=1
	fi
	if [[ $err -eq 0 ]]; then echo "✓ Asset references OK"; else exit 1; fi

# Validate BibTeX entries have required fields
check-bib:
	#!/usr/bin/env bash
	set -euo pipefail
	ok=true
	bib="_bibliography/papers.bib"
	[[ -f "$bib" ]] || { echo "WARN: $bib not found"; exit 0; }
	# Check each entry has title and author
	awk '
		/^@/{
			if (key != "" && !has_title) { print "WARN: " key " missing title"; err=1 }
			if (key != "" && !has_author) { print "WARN: " key " missing author"; err=1 }
			key=$0; has_title=0; has_author=0
		}
		/^[ \t]*title[ \t]*=/{has_title=1}
		/^[ \t]*author[ \t]*=/{has_author=1}
		END{
			if (key != "" && !has_title) { print "WARN: " key " missing title"; err=1 }
			if (key != "" && !has_author) { print "WARN: " key " missing author"; err=1 }
		}
	' "$bib"
	$ok && echo "✓ BibTeX entries OK"

# Validate _config.yml plugin-consumed fields have correct types
check-config:
	#!/usr/bin/env bash
	set -euo pipefail
	err=0
	# external_sources must be empty or a proper list (not a bare hash with stray keys)
	# The external-posts plugin iterates it as an array; a hash/scalar crashes it.
	es_block=$(awk '/^external_sources:/{found=1; next} found && /^[^ \t#]/{exit} found && /^[ \t]+[^ \t#]/{print}' _config.yml)
	if [[ -n "$es_block" ]]; then
		# If the block has indented content but no lines starting with "  - ", it's not a list
		if ! echo "$es_block" | grep -qE '^\s+-\s'; then
			echo "FAIL: external_sources has content but is not a YAML list (plugin will crash)"
			echo "  Found: $es_block"
			err=1
		fi
	fi
	if [[ $err -eq 0 ]]; then echo "✓ Config validation OK"; else exit 1; fi

# Validate _data/cv.yml matches RenderCV schema (basic structural check)
check-cv:
	#!/usr/bin/env bash
	set -euo pipefail
	[[ -f _data/cv.yml ]] || { echo "SKIP: _data/cv.yml not found"; exit 0; }
	err=0
	# Must have top-level cv: key
	if ! grep -qE '^cv:' _data/cv.yml; then
		echo "FAIL: _data/cv.yml missing top-level cv: key"
		err=1
	fi
	# Must have cv.name
	if ! grep -qE '^\s+name:\s+\S' _data/cv.yml; then
		echo "FAIL: cv.name is required by RenderCV"
		err=1
	fi
	# Detect common al-folio field names that RenderCV rejects
	if grep -nE '^\s+studyType:' _data/cv.yml; then
		echo "FAIL: cv.yml uses 'studyType' — RenderCV expects 'degree'"
		err=1
	fi
	if grep -nE '^\s+awarder:' _data/cv.yml; then
		echo "FAIL: cv.yml uses 'awarder' — not a RenderCV field (use summary)"
		err=1
	fi
	# Skills should use label/details (OneLineEntry), not name/keywords
	if grep -nE '^\s+keywords:' _data/cv.yml | head -1 | grep -q .; then
		echo "FAIL: cv.yml uses 'keywords' — RenderCV OneLineEntry expects 'details'"
		err=1
	fi
	if [[ $err -eq 0 ]]; then echo "✓ CV schema validation OK"; else exit 1; fi

# Run Prettier check (matches CI prettier.yml workflow)
check-fmt:
	#!/usr/bin/env bash
	set -euo pipefail
	if ! command -v npx &>/dev/null; then
		echo "SKIP: npx not found — install Node.js to run Prettier checks"
		exit 0
	fi
	npx prettier . --check && echo "✓ Prettier formatting OK"

# Verify rendercv can render the CV without errors (matches CI render-cv.yml)
check-rendercv:
	#!/usr/bin/env bash
	set -euo pipefail
	if ! command -v rendercv &>/dev/null; then
		echo "SKIP: rendercv not found — pip install 'rendercv[full]'"
		exit 0
	fi
	[[ -f _data/cv.yml ]] || { echo "SKIP: _data/cv.yml not found"; exit 0; }
	if rendercv render _data/cv.yml --dont-generate-png --dont-generate-markdown --dont-generate-html >/dev/null 2>&1; then
		echo "✓ RenderCV build OK"
	else
		echo "FAIL: rendercv render failed"
		rendercv render _data/cv.yml 2>&1
		exit 1
	fi
	# Clean up render artifacts — CI is the source of truth for committed output
	rm -rf _data/rendercv_output

# ── Local build (requires Ruby + bundle) ─────────────────────────────

# Install Ruby dependencies
setup:
	bundle install

# Build site locally (catches Liquid/Jekyll errors)
build:
	JEKYLL_ENV=production bundle exec jekyll build

# Serve site locally for preview
serve:
	bundle exec jekyll serve --livereload

# Clean Jekyll build artifacts
clean:
	bundle exec jekyll clean
	rm -rf _site .jekyll-cache .jekyll-metadata

# ── Docker-based clean-room build (matches CI exactly) ───────────────

# Full CI-equivalent build in Docker — the gold standard pre-push check
docker-build:
	#!/usr/bin/env bash
	set -euo pipefail
	echo "Building site in Docker (Ruby {{ruby_version}}, matches CI)..."
	docker run --rm \
		-v "$PWD":/srv/jekyll \
		-w /srv/jekyll \
		ruby:{{ruby_version}}-slim \
		bash -c '
			set -euo pipefail
			apt-get update -qq && apt-get install -y -qq build-essential imagemagick >/dev/null 2>&1
			gem install bundler --no-document
			bundle install --jobs 4 --retry 3
			JEKYLL_ENV=production bundle exec jekyll build
			echo "✓ Docker clean-room build passed."
		'

# ── Pre-push gate ────────────────────────────────────────────────────

# Run before every push: structural checks + local build
pre-push: check build
	@echo "✓ Ready to push."

# Run before every push (Docker variant — no local Ruby needed)
pre-push-docker: check docker-build
	@echo "✓ Ready to push (Docker-verified)."

# ── Formatting ───────────────────────────────────────────────────────

# Format Liquid/HTML/Markdown with Prettier
fmt:
	npx prettier --write "**/*.{html,liquid,md,yml,yaml,json}" --ignore-path .gitignore

fmt-check:
	npx prettier --check "**/*.{html,liquid,md,yml,yaml,json}" --ignore-path .gitignore
