(() => {
  if (typeof URL === "undefined" || typeof URL.canParse === "function") {
    return;
  }

  Object.defineProperty(URL, "canParse", {
    configurable: true,
    writable: true,
    value(url, base) {
      try {
        if (arguments.length >= 2) {
          new URL(url, base);
        } else {
          new URL(url);
        }
        return true;
      } catch (_) {
        return false;
      }
    }
  });
})();
