(() => {
  "use strict";

  const VERSION = "1.0";
  const BUILD = 7;
  const ENABLE_ATTR = "data-chatgpt-ios16-lightdiag";
  const ENABLE_EVENT = "chatgpt-ios16-lightdiag-enable";
  const REPORT_EVENT = "chatgpt-ios16-lightdiag-main-report";
  const SNAPSHOT_DELAY_MS = 8000;
  const MAX_ERRORS = 8;
  let started = false;
  const errors = [];

  function clip(value, maxLength) {
    const text = String(value == null ? "" : value);
    return text.length > maxLength ? text.slice(0, maxLength) + "…" : text;
  }

  function redactPath(pathname) {
    return String(pathname || "")
      .replace(/[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}/ig, ":uuid")
      .replace(/\b[0-9a-f]{24,}\b/ig, ":hex")
      .replace(/\b[A-Za-z0-9_-]{32,}\b/g, ":token")
      .replace(/\/\d{9,}(?=\/|$)/g, "/:id");
  }

  function sanitizeUrl(value) {
    const text = clip(value, 1400);
    if (!text) return "";
    try {
      const parsed = new URL(text, window.location.origin);
      if (parsed.protocol === "http:" || parsed.protocol === "https:") {
        return parsed.origin + redactPath(parsed.pathname);
      }
    } catch (_) {}
    return clip(redactPath(text.replace(/[?#].*$/, "")), 500);
  }

  function safeMessage(value) {
    return clip(value, 900).replace(/https?:\/\/[^\s)]+/g, (match) => sanitizeUrl(match));
  }

  function emit(kind, payload) {
    const detail = JSON.stringify({
      version: VERSION,
      build: BUILD,
      kind,
      time: new Date().toISOString(),
      payload: payload || null
    });
    try {
      document.dispatchEvent(new CustomEvent(REPORT_EVENT, { detail }));
    } catch (_) {
      try {
        const event = document.createEvent("CustomEvent");
        event.initCustomEvent(REPORT_EVENT, false, false, detail);
        document.dispatchEvent(event);
      } catch (_) {}
    }
  }

  function reactMarkers(element) {
    const result = { fiber: false, props: false, events: false, markerCount: 0 };
    if (!element) return result;
    try {
      const names = Object.getOwnPropertyNames(element);
      for (const name of names) {
        if (name.indexOf("__reactFiber$") === 0) result.fiber = true;
        if (name.indexOf("__reactProps$") === 0) result.props = true;
        if (name.indexOf("__reactEvents$") === 0) result.events = true;
      }
      result.markerCount = Number(result.fiber) + Number(result.props) + Number(result.events);
    } catch (_) {}
    return result;
  }

  function getAttributeState(element, name) {
    if (!element || typeof element.getAttribute !== "function") return "unavailable";
    try {
      const value = element.getAttribute(name);
      return value == null ? "absent" : clip(value, 40);
    } catch (_) {
      return "unavailable";
    }
  }

  function elementState(element) {
    if (!element) return { present: false };
    const state = {
      present: true,
      tag: clip(element.tagName || "unknown", 20),
      react: reactMarkers(element),
      disabled: Boolean(element.disabled),
      ariaDisabled: getAttributeState(element, "aria-disabled"),
      contentEditable: getAttributeState(element, "contenteditable"),
      directOnClick: false
    };
    try { state.directOnClick = typeof element.onclick === "function"; } catch (_) {}
    return state;
  }

  function query(selector) {
    try { return document.querySelector ? document.querySelector(selector) : null; }
    catch (_) { return null; }
  }

  function count(selector) {
    try { return document.querySelectorAll ? document.querySelectorAll(selector).length : -1; }
    catch (_) { return -1; }
  }

  function resourceSummary() {
    const summary = {
      supported: false,
      total: 0,
      jsLike: 0,
      byInitiator: {},
      samples: []
    };
    try {
      if (!window.performance || typeof window.performance.getEntriesByType !== "function") return summary;
      const entries = window.performance.getEntriesByType("resource") || [];
      summary.supported = true;
      summary.total = entries.length;
      for (const entry of entries) {
        const type = clip(entry.initiatorType || "unknown", 30);
        summary.byInitiator[type] = (summary.byInitiator[type] || 0) + 1;
        const url = sanitizeUrl(entry.name || "");
        const jsLike = type === "script" || /\.m?js(?:$|[?#])/i.test(String(entry.name || ""));
        if (jsLike) summary.jsLike += 1;
        if (summary.samples.length < 20 && (jsLike || type === "link" || type === "fetch" || type === "xmlhttprequest")) {
          summary.samples.push({
            initiator: type,
            url,
            durationMs: Number.isFinite(Number(entry.duration)) ? Math.round(Number(entry.duration)) : -1
          });
        }
      }
    } catch (_) {}
    return summary;
  }

  function navigationSummary() {
    const result = { supported: false };
    try {
      if (!window.performance || typeof window.performance.getEntriesByType !== "function") return result;
      const nav = (window.performance.getEntriesByType("navigation") || [])[0];
      if (!nav) return result;
      result.supported = true;
      for (const key of ["domInteractive", "domContentLoadedEventEnd", "loadEventEnd"]) {
        const value = Number(nav[key]);
        result[key + "Ms"] = Number.isFinite(value) ? Math.round(value) : -1;
      }
    } catch (_) {}
    return result;
  }

  function makeSnapshot() {
    const root = query("#root");
    const composer = query("#prompt-textarea, textarea, [contenteditable='true']");
    const send = query("[data-testid='send-button'], button[aria-label='Send prompt'], button[aria-label='Send message']");
    const sidebar = query("button[aria-label*='sidebar' i], button[aria-label*='menu' i]");

    return {
      captured: new Date().toISOString(),
      browser: {
        userAgent: clip(navigator.userAgent || "", 320),
        platform: clip(navigator.platform || "", 80),
        vendor: clip(navigator.vendor || "", 80)
      },
      document: {
        readyState: document.readyState || "unknown",
        bodyPresent: Boolean(document.body),
        root: elementState(root),
        composer: elementState(composer),
        send: elementState(send),
        sidebar: elementState(sidebar),
        buttonCount: count("button"),
        scriptCount: count("script"),
        externalScriptCount: count("script[src]"),
        moduleScriptCount: count("script[type='module']"),
        modulePreloadCount: count("link[rel='modulepreload']"),
        preloadScriptCount: count("link[rel='preload'][as='script']"),
        stylesheetCount: count("link[rel='stylesheet']")
      },
      resources: resourceSummary(),
      navigation: navigationSummary(),
      errors: errors.slice()
    };
  }

  function addError(kind, message, source) {
    errors.push({
      time: new Date().toISOString(),
      kind: clip(kind, 40),
      message: safeMessage(message || ""),
      source: sanitizeUrl(source || "")
    });
    if (errors.length > MAX_ERRORS) errors.splice(0, errors.length - MAX_ERRORS);
  }

  function start() {
    if (started) return;
    started = true;
    try { if (document.documentElement) document.documentElement.removeAttribute(ENABLE_ATTR); } catch (_) {}
    emit("started", { readyState: document.readyState || "unknown" });

    window.addEventListener("error", (event) => {
      if (event && event.target && event.target !== window) {
        const target = event.target;
        const url = target && (target.src || target.href) ? (target.src || target.href) : "";
        if (url) addError("resource-error", target.tagName || "resource", url);
        return;
      }
      addError("javascript-error", event && event.message ? event.message : "JavaScript error", event && event.filename ? event.filename : "");
    }, true);

    window.addEventListener("unhandledrejection", (event) => {
      const reason = event ? event.reason : null;
      let message = "Promise rejected";
      if (reason && typeof reason === "object") message = reason.message || reason.name || message;
      else if (typeof reason === "string") message = reason;
      addError("unhandled-rejection", message, "");
    }, true);

    setTimeout(() => emit("snapshot", makeSnapshot()), SNAPSHOT_DELAY_MS);
  }

  document.addEventListener(ENABLE_EVENT, start);

  function checkAttribute() {
    try {
      if (document.documentElement && document.documentElement.getAttribute(ENABLE_ATTR) === "1") start();
    } catch (_) {}
  }

  checkAttribute();
  if (!document.documentElement) document.addEventListener("DOMContentLoaded", checkAttribute, { once: true });
})();
