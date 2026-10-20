import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import test from "node:test";
import vm from "node:vm";

const site = process.env.SITE_DIR || "_site";
const html = (page) => fs.readFileSync(path.join(site, page, "index.html"), "utf8");
const readSearch = () => {
  const widget = { data: [] };
  const location = { href: "" };
  const opened = [];
  vm.runInNewContext(fs.readFileSync(path.join(site, "assets/js/search-data.js"), "utf8"), {
    document: { querySelector: () => widget },
    window: { location, open: (url) => opened.push(url) },
    setThemeSetting: () => {},
  });
  return { entries: widget.data, location, opened };
};

test("search includes maintained secondary pages and actionable news", () => {
  const { entries, location } = readSearch();
  for (const title of ["Computed software examples", "Research figures", "Modeling in practice", "repositories", "Outside work"]) {
    const entry = entries.find((entry) => entry.title === title);
    assert.ok(entry, `Missing search destination: ${title}`);
    assert.equal(typeof entry.handler, "function");
    entry.handler();
    assert.ok(fs.existsSync(path.join(site, new URL(location.href, "https://example.org").pathname, "index.html")));
  }
  const news = entries.filter((entry) => entry.section === "News");
  assert.ok(news.length > 0);
  for (const entry of news) {
    assert.equal(typeof entry.handler, "function");
    entry.handler();
    assert.ok(fs.existsSync(path.join(site, new URL(location.href, "https://example.org").pathname, "index.html")));
  }
  assert.equal(new Set(entries.map((entry) => entry.id)).size, entries.length);
  assert.ok(entries.some((entry) => entry.title === "Download CV (PDF)"));
  assert.ok(entries.some((entry) => entry.title === "Web of Science"));
});

test("empty template pages are absent from output and sitemap", () => {
  const sitemap = fs.readFileSync(path.join(site, "sitemap.xml"), "utf8");
  for (const page of ["people", "blog", "_pages/dropdown"]) {
    assert.ok(!fs.existsSync(path.join(site, page, "index.html")), page);
    assert.ok(!sitemap.includes(`/${page}/`), page);
  }
});

test("home previews identify the author and supply an absolute image URL", () => {
  const home = html("");
  assert.match(home, /property="og:title" content="Joshua C\. Macdonald"/);
  assert.match(home, /name="twitter:title" content="Joshua C\. Macdonald"/);
  assert.ok(
    /property="og:image" content="https:\/\/jcmacdonald\.dev\/assets\/img\/prof_pic\.jpg"/.test(home),
    "Missing absolute Open Graph portrait URL"
  );
  assert.ok(home.indexOf("Selected publications") < home.indexOf("Research in progress"));
});

test("academic pages retain current teaching and separate workshop presentations", () => {
  assert.match(html("teaching"), /Summer 2025 and Summer 2026/);
  assert.match(html("talks"), /Workshop presentations/);
  const publications = html("publications");
  assert.ok(!publications.includes('id="macdonald2026structeval"'));
  assert.doesNotMatch(publications.replace(/<[^>]+>/g, " "), /and\s+et al\./);
});

// Folded YAML descriptions and quoted titles must remain valid structured data.
test("page structured metadata is valid JSON with concrete profile links", () => {
  for (const page of ["", "cv", "publications", "projects"]) {
    const scripts = [...html(page).matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)];
    assert.ok(scripts.length);
    for (const [, script] of scripts) {
      const record = JSON.parse(script);
      if (record.sameAs) assert.ok(record.sameAs.every((url) => typeof url === "string" && url.startsWith("https://")));
      if (page === "" && record["@type"] === "WebSite") assert.equal(record.headline, "Joshua C. Macdonald");
    }
  }
});
