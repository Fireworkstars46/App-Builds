(() => {
  "use strict";

  const ENABLE_KEY = "diagnosticsEnabled";
  const REPORT_KEY = "lightDiagnosticReport";
  const checkbox = document.getElementById("diagnostics");
  const status = document.getElementById("status");
  const report = document.getElementById("report");
  const reportStatus = document.getElementById("reportStatus");
  const chromeApi = typeof chrome !== "undefined" ? chrome : null;
  const browserApi = typeof browser !== "undefined" ? browser : null;

  function getStorage(defaults, callback) {
    if (chromeApi && chromeApi.storage && chromeApi.storage.local) {
      try {
        chromeApi.storage.local.get(defaults, (result) => {
          if (chromeApi.runtime && chromeApi.runtime.lastError) callback(defaults, false);
          else callback(result || defaults, true);
        });
        return;
      } catch (_) {}
    }
    if (browserApi && browserApi.storage && browserApi.storage.local) {
      try {
        Promise.resolve(browserApi.storage.local.get(defaults))
          .then((result) => callback(result || defaults, true))
          .catch(() => callback(defaults, false));
        return;
      } catch (_) {}
    }
    callback(defaults, false);
  }

  function setStorage(value, callback) {
    if (chromeApi && chromeApi.storage && chromeApi.storage.local) {
      try {
        chromeApi.storage.local.set(value, () => {
          callback(!(chromeApi.runtime && chromeApi.runtime.lastError));
        });
        return;
      } catch (_) {}
    }
    if (browserApi && browserApi.storage && browserApi.storage.local) {
      try {
        Promise.resolve(browserApi.storage.local.set(value)).then(() => callback(true)).catch(() => callback(false));
        return;
      } catch (_) {}
    }
    callback(false);
  }

  function loadSetting() {
    getStorage({ [ENABLE_KEY]: false }, (result, ok) => {
      checkbox.checked = Boolean(result && result[ENABLE_KEY] === true);
      status.textContent = ok
        ? (checkbox.checked ? "Light diagnostics ON — reload ChatGPT to capture startup." : "Light diagnostics OFF")
        : "Could not read setting; using OFF.";
    });
  }

  function loadReport() {
    getStorage({ [REPORT_KEY]: null }, (result, ok) => {
      if (!ok) {
        report.value = "Could not read saved diagnostic report.";
        return;
      }
      const saved = result ? result[REPORT_KEY] : null;
      report.value = saved && saved.report
        ? saved.report
        : "No saved report yet. Turn Light Diagnostics ON, reload ChatGPT once, then come back here. If ChatGPT freezes, you can close the ChatGPT tab first and open this popup from a blank tab.";
      reportStatus.textContent = saved && saved.updated ? "Saved: " + saved.updated : "";
    });
  }

  checkbox.addEventListener("change", () => {
    const wanted = checkbox.checked;
    status.textContent = "Saving…";
    setStorage({ [ENABLE_KEY]: wanted }, (ok) => {
      if (!ok) {
        checkbox.checked = !wanted;
        status.textContent = "Save failed.";
        return;
      }
      status.textContent = wanted
        ? "Light diagnostics ON — reload ChatGPT to capture startup."
        : "Light diagnostics OFF";
    });
  });

  document.getElementById("refresh").addEventListener("click", loadReport);
  document.getElementById("clear").addEventListener("click", () => {
    setStorage({ [REPORT_KEY]: null }, (ok) => {
      reportStatus.textContent = ok ? "Saved report cleared." : "Could not clear report.";
      if (ok) loadReport();
    });
  });
  document.getElementById("copy").addEventListener("click", () => {
    const text = report.value;
    function fallback() {
      try {
        report.focus(); report.select(); report.setSelectionRange(0, report.value.length);
        const ok = document.execCommand("copy");
        reportStatus.textContent = ok ? "Copied." : "Copy failed — select the report manually.";
      } catch (_) {
        reportStatus.textContent = "Copy failed — select the report manually.";
      }
    }
    if (navigator.clipboard && typeof navigator.clipboard.writeText === "function") {
      navigator.clipboard.writeText(text).then(() => { reportStatus.textContent = "Copied."; }, fallback);
    } else fallback();
  });

  loadSetting();
  loadReport();
})();
