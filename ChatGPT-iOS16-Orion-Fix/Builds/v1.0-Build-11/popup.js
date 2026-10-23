(() => {
  "use strict";

  const ENABLE_KEY = "diagnosticsEnabled";
  const REPORT_KEY = "lightDiagnosticReport";
  const checkbox = document.getElementById("diagnostics");
  const status = document.getElementById("status");
  const report = document.getElementById("report");
  const reportStatus = document.getElementById("reportStatus");
  const copyMissing = document.getElementById("copyMissing");
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
  function extractMissingFeatures(text) {
    const source = String(text || "");
    const start = source.indexOf("Early browser feature matrix:");
    if (start < 0) return "";
    let end = source.indexOf("\n- full feature results:", start);
    if (end < 0) end = source.indexOf("\nPage-world errors/rejections", start);
    if (end < 0) end = source.length;
    return source.slice(start, end).trim();
  }

  function fallbackCopy(text) {
    try {
      const full = report.value;
      const start = full.indexOf(text);
      if (start < 0) throw new Error("text not found");
      report.focus();
      report.setSelectionRange(start, start + text.length);
      const ok = document.execCommand("copy");
      reportStatus.textContent = ok ? "Copied." : "Copy failed — select the report manually.";
    } catch (_) {
      reportStatus.textContent = "Copy failed — select the report manually.";
    }
  }

  function copyText(text) {
    if (navigator.clipboard && typeof navigator.clipboard.writeText === "function") {
      navigator.clipboard.writeText(text).then(() => { reportStatus.textContent = "Copied."; }, () => fallbackCopy(text));
    } else fallbackCopy(text);
  }

  document.getElementById("copy").addEventListener("click", () => copyText(report.value));
  copyMissing.addEventListener("click", () => {
    const text = extractMissingFeatures(report.value);
    if (!text) {
      reportStatus.textContent = "Missing-features section not available yet. Refresh after the 8-second snapshot.";
      return;
    }
    copyText(text);
  });

  loadSetting();
  loadReport();
})();
