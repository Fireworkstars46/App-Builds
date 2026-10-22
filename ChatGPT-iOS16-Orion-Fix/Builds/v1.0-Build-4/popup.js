(() => {
  "use strict";

  const KEY = "diagnosticsEnabled";
  const checkbox = document.getElementById("diagnostics");
  const status = document.getElementById("status");
  const chromeApi = typeof chrome !== "undefined" ? chrome : null;
  const browserApi = typeof browser !== "undefined" ? browser : null;

  function showStatus(text) {
    status.textContent = text;
  }

  function apply(value) {
    checkbox.checked = value === true;
    showStatus(checkbox.checked ? "Diagnostics ON" : "Diagnostics OFF");
  }

  function load() {
    if (chromeApi && chromeApi.storage && chromeApi.storage.local) {
      try {
        chromeApi.storage.local.get({ [KEY]: false }, (result) => {
          if (chromeApi.runtime && chromeApi.runtime.lastError) {
            apply(false);
            showStatus("Could not read setting; using OFF.");
            return;
          }
          apply(Boolean(result && result[KEY] === true));
        });
        return;
      } catch (_) {
        // Fall through.
      }
    }

    if (browserApi && browserApi.storage && browserApi.storage.local) {
      Promise.resolve(browserApi.storage.local.get({ [KEY]: false }))
        .then((result) => apply(Boolean(result && result[KEY] === true)))
        .catch(() => {
          apply(false);
          showStatus("Could not read setting; using OFF.");
        });
        return;
    }

    checkbox.disabled = true;
    apply(false);
    showStatus("Storage API unavailable; diagnostics stay OFF.");
  }

  function save(value) {
    showStatus("Saving…");
    const payload = { [KEY]: Boolean(value) };

    if (chromeApi && chromeApi.storage && chromeApi.storage.local) {
      try {
        chromeApi.storage.local.set(payload, () => {
          if (chromeApi.runtime && chromeApi.runtime.lastError) {
            checkbox.checked = !value;
            showStatus("Save failed.");
            return;
          }
          apply(value);
        });
        return;
      } catch (_) {
        // Fall through.
      }
    }

    if (browserApi && browserApi.storage && browserApi.storage.local) {
      Promise.resolve(browserApi.storage.local.set(payload))
        .then(() => apply(value))
        .catch(() => {
          checkbox.checked = !value;
          showStatus("Save failed.");
        });
        return;
    }

    checkbox.checked = !value;
    showStatus("Save failed: storage unavailable.");
  }

  checkbox.addEventListener("change", () => save(checkbox.checked));
  load();
})();
