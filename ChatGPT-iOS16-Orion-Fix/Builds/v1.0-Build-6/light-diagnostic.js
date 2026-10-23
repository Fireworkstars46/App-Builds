(() => {
  "use strict";

  const VERSION = "1.0";
  const BUILD = 6;
  const ENABLE_KEY = "diagnosticsEnabled";
  const REPORT_KEY = "lightDiagnosticReport";
  const MAX_EVENTS = 12;
  const SNAPSHOT_DELAY_MS = 8000;

  const chromeApi = typeof chrome !== "undefined" ? chrome : null;
  const browserApi = typeof browser !== "undefined" ? browser : null;

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
    return clip(value, 900)
      .replace(/https?:\/\/[^\s)]+/g, (match) => sanitizeUrl(match));
  }

  function storageGet(defaults, callback) {
    if (chromeApi && chromeApi.storage && chromeApi.storage.local) {
      try {
        chromeApi.storage.local.get(defaults, (result) => {
          if (chromeApi.runtime && chromeApi.runtime.lastError) callback(defaults);
          else callback(result || defaults);
        });
        return;
      } catch (_) {}
    }
    if (browserApi && browserApi.storage && browserApi.storage.local) {
      try {
        Promise.resolve(browserApi.storage.local.get(defaults))
          .then((result) => callback(result || defaults))
          .catch(() => callback(defaults));
        return;
      } catch (_) {}
    }
    callback(defaults);
  }

  function storageSet(value) {
    if (chromeApi && chromeApi.storage && chromeApi.storage.local) {
      try { chromeApi.storage.local.set(value, () => {}); return; } catch (_) {}
    }
    if (browserApi && browserApi.storage && browserApi.storage.local) {
      try { Promise.resolve(browserApi.storage.local.set(value)).catch(() => {}); } catch (_) {}
    }
  }

  function start() {
    const state = {
      version: VERSION,
      build: BUILD,
      origin: window.location.origin,
      started: new Date().toISOString(),
      completed: false,
      events: [],
      snapshot: null
    };

    function addEvent(kind, detail) {
      state.events.push({
        time: new Date().toISOString(),
        kind: clip(kind, 40),
        detail: safeMessage(detail || "")
      });
      if (state.events.length > MAX_EVENTS) {
        state.events.splice(0, state.events.length - MAX_EVENTS);
      }
      persist();
    }

    function exists(selector) {
      try { return Boolean(document.querySelector && document.querySelector(selector)); }
      catch (_) { return false; }
    }

    function count(selector) {
      try { return document.querySelectorAll ? document.querySelectorAll(selector).length : -1; }
      catch (_) { return -1; }
    }

    function makeSnapshot() {
      return {
        captured: new Date().toISOString(),
        readyState: document.readyState || "unknown",
        bodyPresent: Boolean(document.body),
        rootPresent: exists("#root"),
        nextPresent: exists("#__next"),
        composerPresent: exists("#prompt-textarea, textarea, [contenteditable='true']"),
        sendControlPresent: exists("[data-testid='send-button'], button[aria-label='Send prompt'], button[aria-label='Send message']"),
        sidebarControlPresent: exists("button[aria-label*='sidebar' i], button[aria-label*='menu' i]"),
        buttonCount: count("button"),
        scriptCount: count("script"),
        externalScriptCount: count("script[src]"),
        moduleScriptCount: count("script[type='module']")
      };
    }

    function buildReport() {
      const s = state.snapshot;
      const lines = [
        "ChatGPT iOS 16 Orion Lightweight Diagnostic",
        "Version " + VERSION + " | Build " + BUILD,
        "Origin: " + state.origin,
        "Started: " + state.started,
        "Startup capture completed: " + (state.completed ? "yes" : "no"),
        "",
        "Startup/resource events (" + state.events.length + "):"
      ];

      if (!state.events.length) lines.push("- None captured");
      else state.events.forEach((item) => lines.push("- " + item.time + " [" + item.kind + "] " + item.detail));

      lines.push("");
      lines.push("8-second page snapshot:");
      if (!s) {
        lines.push("- Not reached. The page may have frozen/closed before the snapshot timer fired.");
      } else {
        lines.push("- readyState: " + s.readyState);
        lines.push("- body present: " + s.bodyPresent);
        lines.push("- #root present: " + s.rootPresent);
        lines.push("- #__next present: " + s.nextPresent);
        lines.push("- composer present: " + s.composerPresent);
        lines.push("- send control present: " + s.sendControlPresent);
        lines.push("- sidebar/menu control present: " + s.sidebarControlPresent);
        lines.push("- button count: " + s.buttonCount);
        lines.push("- script count: " + s.scriptCount);
        lines.push("- external script count: " + s.externalScriptCount);
        lines.push("- module script count: " + s.moduleScriptCount);
      }

      lines.push("");
      lines.push("Privacy: no message text, typed text, cookies, local/session storage contents, request bodies, clipboard contents, or page text are collected.");
      lines.push("Performance: no MutationObserver, PerformanceObserver, DOM polling, click tracking, or on-page diagnostic UI is used.");
      return lines.join("\n");
    }

    function persist() {
      storageSet({
        [REPORT_KEY]: {
          version: VERSION,
          build: BUILD,
          updated: new Date().toISOString(),
          report: buildReport()
        }
      });
    }

    persist();

    window.addEventListener("error", (event) => {
      if (event && event.target && event.target !== window) {
        const target = event.target;
        const tag = clip(target.tagName || "resource", 30);
        const url = target.src || target.href || "";
        if (url) addEvent("resource-error", tag + " " + sanitizeUrl(url));
        return;
      }
      const source = sanitizeUrl(event && event.filename ? event.filename : "");
      const message = safeMessage(event && event.message ? event.message : "JavaScript error");
      addEvent("javascript-error", message + (source ? " | " + source : ""));
    }, true);

    window.addEventListener("unhandledrejection", (event) => {
      const reason = event ? event.reason : null;
      let message = "Promise rejected";
      if (reason && typeof reason === "object") message = reason.message || reason.name || message;
      else if (typeof reason === "string") message = reason;
      addEvent("unhandled-rejection", message);
    }, true);

    document.addEventListener("DOMContentLoaded", () => addEvent("lifecycle", "DOMContentLoaded"), { once: true });
    window.addEventListener("load", () => addEvent("lifecycle", "window load"), { once: true });

    setTimeout(() => {
      state.snapshot = makeSnapshot();
      state.completed = true;
      addEvent("snapshot", "8-second startup snapshot saved");
      persist();
    }, SNAPSHOT_DELAY_MS);
  }

  storageGet({ [ENABLE_KEY]: false }, (settings) => {
    if (settings && settings[ENABLE_KEY] === true) start();
  });
})();
