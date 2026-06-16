(function () {
  var motionQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
  var transitionDuration = 220;
  var leavingClass = "is-page-leaving";
  var isTransitioning = false;

  function isModifiedEvent(event) {
    return event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || event.button !== 0;
  }

  function isPageLikeLink(link) {
    if (!link || !link.href || link.hasAttribute("download")) {
      return false;
    }

    var url = new URL(link.href, window.location.href);
    var target = link.getAttribute("target");

    if (target && target !== "_self") {
      return false;
    }

    if (url.origin !== window.location.origin) {
      return false;
    }

    if (url.pathname === window.location.pathname && url.search === window.location.search) {
      return false;
    }

    var fileName = url.pathname.split("/").pop();
    var extension = fileName.includes(".") ? fileName.split(".").pop() : "";

    return extension === "" || extension === "html";
  }

  document.documentElement.classList.add("has-page-transitions");

  window.addEventListener("pageshow", function () {
    document.body.classList.remove(leavingClass);
  });

  document.addEventListener("click", function (event) {
    var link = event.target.closest("a");

    if (isTransitioning || isModifiedEvent(event) || !isPageLikeLink(link)) {
      return;
    }

    if (motionQuery.matches) {
      return;
    }

    event.preventDefault();
    isTransitioning = true;
    document.body.classList.add(leavingClass);

    window.setTimeout(function () {
      window.location.href = link.href;
    }, transitionDuration);
  });
})();
