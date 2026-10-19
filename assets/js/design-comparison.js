// Progressive enhancement: the full checked CSV table is visible without JS.
document.querySelectorAll("[data-design-comparison]").forEach((comparison) => {
  const tbody = comparison.querySelector("tbody");
  const rows = Array.from(tbody.rows);
  const frontOnly = comparison.querySelector("[data-front-only]");
  const order = comparison.querySelector("[data-design-order]");
  const count = comparison.querySelector("[data-design-count]");
  const update = () => {
    rows.sort((a, b) => Number(a.dataset[order.value]) - Number(b.dataset[order.value]));
    let visible = 0;
    rows.forEach((row) => {
      row.hidden = frontOnly.checked && row.dataset.front !== "1";
      if (!row.hidden) visible += 1;
      tbody.append(row);
    });
    count.textContent = `${visible} of ${rows.length} designs`;
  };
  frontOnly.addEventListener("change", update);
  order.addEventListener("change", update);
  comparison.querySelector(".design-controls").hidden = false;
  update();
});
