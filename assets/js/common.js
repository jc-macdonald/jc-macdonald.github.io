$(document).ready(function () {
  // Toggle publication details while keeping button and panel state available
  // to assistive technology. Opening one panel closes the others in that entry.
  $(".publication-toggle").click(function () {
    const button = this;
    const target = document.getElementById(button.getAttribute("aria-controls"));
    if (!target) return;

    const entry = button.closest("[data-publication-status]");
    const shouldOpen = !target.classList.contains("open");

    $(entry)
      .find(".publication-details.hidden")
      .each(function () {
        const isOpen = this === target && shouldOpen;
        $(this).toggleClass("open", isOpen).attr("aria-hidden", String(!isOpen)).prop("inert", !isOpen);
      });
    $(entry).find(".publication-toggle").attr("aria-expanded", "false");
    if (shouldOpen) button.setAttribute("aria-expanded", "true");
  });
  $("a").removeClass("waves-effect waves-light");

  // bootstrap-toc
  if ($("#toc-sidebar").length) {
    // remove related publications years from the TOC
    $(".publications h2").each(function () {
      $(this).attr("data-toc-skip", "");
    });
    var navSelector = "#toc-sidebar";
    var $myNav = $(navSelector);
    Toc.init($myNav);
    $("body").scrollspy({
      target: navSelector,
      offset: 100,
    });
  }

  // add css to jupyter notebooks
  const cssLink = document.createElement("link");
  cssLink.href = "../css/jupyter.css";
  cssLink.rel = "stylesheet";
  cssLink.type = "text/css";

  let jupyterTheme = determineComputedTheme();

  $(".jupyter-notebook-iframe-container iframe").each(function () {
    $(this).contents().find("head").append(cssLink);

    if (jupyterTheme == "dark") {
      $(this).bind("load", function () {
        $(this).contents().find("body").attr({
          "data-jp-theme-light": "false",
          "data-jp-theme-name": "JupyterLab Dark",
        });
      });
    }
  });

  // trigger popovers
  $('[data-toggle="popover"]').popover({
    trigger: "hover",
  });
});
