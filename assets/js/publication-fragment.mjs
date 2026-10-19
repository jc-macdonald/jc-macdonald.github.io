// Real page anchors navigate; other fragments retain legacy bibliography search.
export function publicationSearchTerm(fragment, hasTarget) {
  let value;
  try {
    value = decodeURIComponent(fragment.replace(/^#/, ""));
  } catch {
    return "";
  }
  return hasTarget(value) ? "" : value.toLowerCase();
}
