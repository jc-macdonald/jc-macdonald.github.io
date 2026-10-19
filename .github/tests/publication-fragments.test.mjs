import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";
import { runInNewContext } from "node:vm";
import { publicationSearchTerm } from "../../assets/js/publication-fragment.mjs";

const targets = new Set(["main-content", "published", "under-review", "preprints", "in-preparation", "macdonald2024austronesian"]);
const hasTarget = (id) => targets.has(id);

test("section, paper and skip links retain the full bibliography", () => {
  for (const target of targets) {
    assert.equal(publicationSearchTerm(`#${target}`, hasTarget), "");
  }
});

test("legacy search links decode text and search without case sensitivity", () => {
  assert.equal(publicationSearchTerm("#Austronesian", hasTarget), "austronesian");
  assert.equal(publicationSearchTerm("#Foot%20and%20Mouth", hasTarget), "foot and mouth");
  assert.equal(publicationSearchTerm("#P%C3%A9rez", hasTarget), "pérez");
});

test("empty and malformed fragments do not hide the bibliography or throw", () => {
  assert.equal(publicationSearchTerm("", hasTarget), "");
  assert.equal(publicationSearchTerm("#", hasTarget), "");
  assert.equal(publicationSearchTerm("#%E0%A4%A", hasTarget), "");
});

test("section navigation cancels pending typed input before it can hide papers", () => {
  // Exercise the actual browser event handler with controlled timers. DOM
  // filtering/visibility is also checked in the production browser review.
  const calls = [];
  const events = {};
  const pending = new Map();
  let sequence = 0;
  const input = { value: "", addEventListener: (name, callback) => (events[name] = callback) };
  const window = { location: { hash: "" }, addEventListener: (name, callback) => (events[name] = callback) };
  const document = {
    addEventListener: (name, callback) => (events[name] = callback),
    getElementById: (id) => (id === "bibsearch" ? input : hasTarget(id) ? {} : null),
    querySelectorAll: () => [],
  };
  const script = readFileSync(new URL("../../assets/js/bibsearch.js", import.meta.url), "utf8").replace(/^import .*;$/gm, "");
  runInNewContext(script, {
    document,
    window,
    CSS: { highlights: {} },
    publicationSearchTerm,
    highlightSearchTerm: ({ search }) => {
      calls.push(search);
      return [];
    },
    setTimeout: (callback) => {
      pending.set(++sequence, callback);
      return sequence;
    },
    clearTimeout: (id) => pending.delete(id),
  });
  events.DOMContentLoaded();
  input.value = "Austronesian";
  events.input.call(input);
  assert.deepEqual(calls, [""]);
  window.location.hash = "#under-review";
  events.hashchange();
  for (const callback of pending.values()) callback();
  assert.equal(input.value, "");
  assert.deepEqual(calls, ["", ""]);
});
