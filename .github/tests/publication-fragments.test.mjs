import assert from "node:assert/strict";
import test from "node:test";
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
