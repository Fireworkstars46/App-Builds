(() => {
  "use strict";

  const VERSION = "1.0";
  const BUILD = 4;
  const MAX_ERRORS = 25;
  const GLOBAL_KEY = "__CHATGPT_IOS16_DIAG__";
  const EVENT_ENABLE = "chatgpt-ios16-diag-enable";
  const EVENT_DISABLE = "chatgpt-ios16-diag-disable";
  const EVENT_READY = "chatgpt-ios16-diag-ready";
  const EVENT_REQUEST_OFF = "chatgpt-ios16-diag-request-off";

  if (window[GLOBAL_KEY] && window[GLOBAL_KEY].build >= BUILD) {
    return;
  }

  const errors = [];
  let diagnosticsEnabled = false;
  let host = null;
  let shadow = null;
  let panel = null;
  let counter = null;
  let reportBox = null;
  let copyStatus = null;

  function clip(value, maxLength) {
    const text = String(value == null ? "" : value);
    return text.length > maxLength ? text.slice(0, maxLength) + "…" : text;
  }

  function sanitizeUrl(value) {
    const text = clip(value, 1200);
    if (!text) return "";
    try {
      const parsed = new URL(text, window.location.origin);
      if (parsed.protocol === "http:" || parsed.protocol === "https:") {
        return parsed.origin + parsed.pathname;
      }
    } catch (_) {
      // Keep a shortened non-URL value below.
    }
    return clip(text.replace(/[?#].*$/, ""), 500);
  }

  function sanitizeStack(value) {
    return clip(value, 3500).replace(/https?:\/\/[^\s)]+/g, (match) => sanitizeUrl(match));
  }

  function safeErrorMessage(value) {
    // Capture only the browser/runtime error text. Never inspect page inputs,
    // message DOM, cookies, storage, request bodies, or clipboard contents.
    return clip(value, 1200);
  }

  function addError(type, message, source, line, column, stack) {
    if (!diagnosticsEnabled) return;
    errors.push({
      time: new Date().toISOString(),
      type: clip(type || "error", 40),
      message: safeErrorMessage(message || "(no error message)"),
      source: sanitizeUrl(source || ""),
      line: Number.isFinite(Number(line)) ? Number(line) : 0,
      column: Number.isFinite(Number(column)) ? Number(column) : 0,
      stack: sanitizeStack(stack || "")
    });

    if (errors.length > MAX_ERRORS) {
      errors.splice(0, errors.length - MAX_ERRORS);
    }
    refreshUi();
  }

  function check(name, test) {
    let ok = false;
    try {
      ok = Boolean(test());
    } catch (_) {
      ok = false;
    }
    return { name, ok };
  }

  function getFeatures() {
    return [
      check("URL.canParse", () => typeof URL !== "undefined" && typeof URL.canParse === "function"),
      check("Promise.withResolvers", () => typeof Promise.withResolvers === "function"),
      check("Object.groupBy", () => typeof Object.groupBy === "function"),
      check("Map.groupBy", () => typeof Map.groupBy === "function"),
      check("Array.prototype.toSorted", () => typeof Array.prototype.toSorted === "function"),
      check("Array.prototype.toReversed", () => typeof Array.prototype.toReversed === "function"),
      check("Array.prototype.toSpliced", () => typeof Array.prototype.toSpliced === "function"),
      check("Array.prototype.with", () => typeof Array.prototype.with === "function"),
      check("AbortSignal.any", () => typeof AbortSignal !== "undefined" && typeof AbortSignal.any === "function"),
      check("AbortSignal.timeout", () => typeof AbortSignal !== "undefined" && typeof AbortSignal.timeout === "function"),
      check("structuredClone", () => typeof structuredClone === "function"),
      check("crypto.randomUUID", () => typeof crypto !== "undefined" && typeof crypto.randomUUID === "function"),
      check("CSS.supports", () => typeof CSS !== "undefined" && typeof CSS.supports === "function")
    ];
  }

  function buildReport() {
    const features = getFeatures();
    const missing = features.filter((item) => !item.ok).map((item) => item.name);
    const lines = [
      "ChatGPT iOS 16 Orion Compatibility Diagnostic",
      "Version " + VERSION + " | Build " + BUILD,
      "Origin: " + window.location.origin,
      "Generated: " + new Date().toISOString(),
      "Diagnostics: " + (diagnosticsEnabled ? "enabled" : "disabled"),
      "",
      "Missing checked browser features (" + missing.length + "):",
      missing.length ? missing.map((name) => "- " + name).join("\n") : "- None of the checked features are missing",
      "",
      "Captured JavaScript errors/rejections (" + errors.length + "):"
    ];

    if (!errors.length) {
      lines.push("- None captured yet. Reproduce the broken action, then open DIAG again.");
    } else {
      errors.forEach((entry, index) => {
        lines.push("");
        lines.push("#" + (index + 1) + " " + entry.time + " [" + entry.type + "]");
        lines.push("Message: " + entry.message);
        if (entry.source) {
          lines.push("Source: " + entry.source + (entry.line ? ":" + entry.line + ":" + entry.column : ""));
        }
        if (entry.stack) {
          lines.push("Stack: " + entry.stack);
        }
      });
    }

    lines.push("");
    lines.push("Privacy: this diagnostic does not inspect message text, typed text, cookies, local/session storage, request bodies, or clipboard contents.");
    return lines.join("\n");
  }

  function refreshUi() {
    if (counter) counter.textContent = String(errors.length);
    if (reportBox && panel && panel.hidden === false) reportBox.value = buildReport();
  }

  function setPanelVisible(visible) {
    if (!panel) return;
    panel.hidden = !visible;
    if (visible && reportBox) {
      reportBox.value = buildReport();
      if (copyStatus) copyStatus.textContent = "";
    }
  }

  function copyReport() {
    const text = buildReport();
    const showResult = (ok) => {
      if (copyStatus) copyStatus.textContent = ok ? "Copied." : "Copy failed — select the report text manually.";
    };

    if (navigator.clipboard && typeof navigator.clipboard.writeText === "function") {
      navigator.clipboard.writeText(text).then(() => showResult(true), () => fallbackCopy(text));
    } else {
      fallbackCopy(text);
    }
  }

  function fallbackCopy(text) {
    try {
      if (!reportBox) throw new Error("report box unavailable");
      reportBox.value = text;
      reportBox.focus();
      reportBox.select();
      reportBox.setSelectionRange(0, reportBox.value.length);
      showLegacyCopyResult(document.execCommand("copy"));
    } catch (_) {
      showLegacyCopyResult(false);
    }
  }

  function showLegacyCopyResult(ok) {
    if (copyStatus) copyStatus.textContent = ok ? "Copied." : "Copy failed — select the report text manually.";
  }

  function mountUi() {
    if (host || !document.documentElement) return;

    host = document.createElement("div");
    host.id = "chatgpt-ios16-diag-host";
    host.style.position = "fixed";
    host.style.right = "8px";
    host.style.bottom = "8px";
    host.style.zIndex = "2147483647";
    host.style.pointerEvents = "auto";
    document.documentElement.appendChild(host);

    shadow = host.attachShadow({ mode: "open" });
    shadow.innerHTML = `
      <style>
        :host { all: initial; }
        * { box-sizing: border-box; }
        button, textarea, div, span { font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
        #bubble {
          border: 1px solid rgba(0,0,0,.25); border-radius: 999px; padding: 8px 10px;
          background: #fff; color: #111; font-size: 13px; font-weight: 700;
          box-shadow: 0 2px 10px rgba(0,0,0,.22); min-width: 64px;
        }
        #panel {
          position: fixed; left: 8px; right: 8px; top: 8px; bottom: 8px;
          background: #fff; color: #111; border: 1px solid rgba(0,0,0,.28);
          border-radius: 14px; padding: 12px; box-shadow: 0 6px 30px rgba(0,0,0,.30);
          display: flex; flex-direction: column; gap: 8px;
        }
        #panel[hidden] { display: none; }
        #title { font-size: 16px; font-weight: 700; }
        #help { font-size: 13px; line-height: 1.35; }
        #report { width: 100%; flex: 1; min-height: 180px; resize: none; font-size: 12px; line-height: 1.35; }
        #row { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
        .action { font-size: 14px; padding: 9px 12px; border: 1px solid #777; border-radius: 9px; background: #f5f5f5; color: #111; }
        #status { font-size: 12px; }
      </style>
      <button id="bubble" type="button">DIAG <span id="count">0</span></button>
      <div id="panel" hidden>
        <div id="title">ChatGPT iOS 16 Diagnostic — v1.0 Build 4</div>
        <div id="help">Try the broken Send or sidebar button first. Then return here and copy this report. It does not read your messages or typed text.</div>
        <textarea id="report" readonly spellcheck="false"></textarea>
        <div id="row">
          <button class="action" id="copy" type="button">Copy Report</button>
          <button class="action" id="clear" type="button">Clear Errors</button>
          <button class="action" id="disable" type="button">Turn Diagnostics Off</button>
          <button class="action" id="close" type="button">Close</button>
          <span id="status"></span>
        </div>
      </div>`;

    panel = shadow.getElementById("panel");
    counter = shadow.getElementById("count");
    reportBox = shadow.getElementById("report");
    copyStatus = shadow.getElementById("status");

    shadow.getElementById("bubble").addEventListener("click", () => setPanelVisible(true));
    shadow.getElementById("close").addEventListener("click", () => setPanelVisible(false));
    shadow.getElementById("copy").addEventListener("click", copyReport);
    shadow.getElementById("disable").addEventListener("click", () => {
      document.dispatchEvent(new Event(EVENT_REQUEST_OFF));
      disableDiagnostics();
    });
    shadow.getElementById("clear").addEventListener("click", () => {
      errors.splice(0, errors.length);
      refreshUi();
      if (copyStatus) copyStatus.textContent = "Errors cleared.";
    });

    refreshUi();
  }

  function unmountUi() {
    if (host && host.parentNode) host.parentNode.removeChild(host);
    host = null;
    shadow = null;
    panel = null;
    counter = null;
    reportBox = null;
    copyStatus = null;
  }

  function enableDiagnostics() {
    diagnosticsEnabled = true;
    if (document.documentElement) {
      mountUi();
    } else {
      document.addEventListener("DOMContentLoaded", mountUi, { once: true });
    }
  }

  function disableDiagnostics() {
    diagnosticsEnabled = false;
    errors.splice(0, errors.length);
    unmountUi();
  }

  document.addEventListener(EVENT_ENABLE, enableDiagnostics);
  document.addEventListener(EVENT_DISABLE, disableDiagnostics);

  window.addEventListener("error", (event) => {
    if (!diagnosticsEnabled) return;
    if (event.target && event.target !== window) return;
    const err = event.error;
    addError(
      "error",
      event.message || (err && err.message) || "JavaScript error",
      event.filename || "",
      event.lineno || 0,
      event.colno || 0,
      err && err.stack ? err.stack : ""
    );
  }, true);

  window.addEventListener("unhandledrejection", (event) => {
    if (!diagnosticsEnabled) return;
    const reason = event.reason;
    if (reason && typeof reason === "object") {
      addError("unhandledrejection", reason.message || reason.name || "Promise rejected", "", 0, 0, reason.stack || "");
    } else {
      addError("unhandledrejection", typeof reason === "string" ? reason : "Promise rejected", "", 0, 0, "");
    }
  }, true);

  window[GLOBAL_KEY] = {
    version: VERSION,
    build: BUILD,
    get enabled() { return diagnosticsEnabled; },
    get errors() { return errors.slice(); },
    report: buildReport,
    show: () => { if (diagnosticsEnabled) setPanelVisible(true); }
  };

  // Diagnostics are OFF by default. The isolated settings bridge will answer
  // this ready event with the persisted extension-owned setting.
  document.dispatchEvent(new Event(EVENT_READY));
})();
