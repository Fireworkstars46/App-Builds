(() => {
  "use strict";

  const VERSION = "1.0";
  const BUILD = 8;
  const ENABLE_KEY = "diagnosticsEnabled";
  const REPORT_KEY = "lightDiagnosticReport";
  const ENABLE_ATTR = "data-chatgpt-ios16-lightdiag";
  const ENABLE_EVENT = "chatgpt-ios16-lightdiag-enable";
  const REPORT_EVENT = "chatgpt-ios16-lightdiag-main-report";
  const FALLBACK_DELAY_MS = 9500;
  const MAX_EVENTS = 12;

  const chromeApi = typeof chrome !== "undefined" ? chrome : null;
  const browserApi = typeof browser !== "undefined" ? browser : null;

  function clip(value, maxLength) {
    const text = String(value == null ? "" : value);
    return text.length > maxLength ? text.slice(0, maxLength) + "…" : text;
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
      state.events.push({ time: new Date().toISOString(), kind: clip(kind, 40), detail: clip(detail || "", 500) });
      if (state.events.length > MAX_EVENTS) state.events.splice(0, state.events.length - MAX_EVENTS);
      persist();
    }

    function bool(value) { return value === true ? "true" : value === false ? "false" : "unknown"; }

    function elementLines(label, item) {
      if (!item || !item.present) return ["- " + label + " present: false"];
      const react = item.react || {};
      return [
        "- " + label + " present: true",
        "- " + label + " tag: " + (item.tag || "unknown"),
        "- " + label + " React fiber marker: " + bool(react.fiber),
        "- " + label + " React props marker: " + bool(react.props),
        "- " + label + " React events marker: " + bool(react.events),
        "- " + label + " React container marker: " + bool(react.container),
        "- " + label + " React listeners marker: " + bool(react.listeners),
        "- " + label + " React handles marker: " + bool(react.handles),
        "- " + label + " React listening marker: " + bool(react.listening),
        "- " + label + " disabled: " + bool(item.disabled),
        "- " + label + " aria-disabled: " + (item.ariaDisabled || "unknown"),
        "- " + label + " contenteditable: " + (item.contentEditable || "unknown"),
        "- " + label + " direct onclick: " + bool(item.directOnClick)
      ];
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
      lines.push("8-second page-world snapshot:");
      if (!s) {
        lines.push("- Not received. The page may have frozen/closed before the page-world probe completed.");
      } else {
        const b = s.browser || {};
        const d = s.document || {};
        lines.push("- readyState: " + (d.readyState || "unknown"));
        lines.push("- body present: " + bool(d.bodyPresent));
        lines.push("- user agent: " + (b.userAgent || "unavailable"));
        lines.push("- platform: " + (b.platform || "unavailable"));
        lines.push("- vendor: " + (b.vendor || "unavailable"));
        lines.push(...elementLines("root", d.root));
        lines.push(...elementLines("composer", d.composer));
        lines.push(...elementLines("send", d.send));
        lines.push(...elementLines("sidebar/menu", d.sidebar));
        lines.push("- button count: " + d.buttonCount);
        lines.push("- script count: " + d.scriptCount);
        lines.push("- external script count: " + d.externalScriptCount);
        lines.push("- module script count: " + d.moduleScriptCount);
        lines.push("- inline module script count: " + d.inlineModuleScriptCount);
        lines.push("- external module script count: " + d.externalModuleScriptCount);
        lines.push("- modulepreload count: " + d.modulePreloadCount);
        lines.push("- preload-as-script count: " + d.preloadScriptCount);
        lines.push("- stylesheet count: " + d.stylesheetCount);

        const r = s.resources || {};
        lines.push("");
        lines.push("One-time resource timing summary:");
        lines.push("- supported: " + bool(r.supported));
        lines.push("- total resources: " + (r.total == null ? "unknown" : r.total));
        lines.push("- JS-like resources: " + (r.jsLike == null ? "unknown" : r.jsLike));
        const initiators = r.byInitiator || {};
        const keys = Object.keys(initiators).sort();
        lines.push("- initiator counts: " + (keys.length ? keys.map((key) => key + "=" + initiators[key]).join(", ") : "none"));
        const samples = Array.isArray(r.samples) ? r.samples : [];
        lines.push("- selected resource samples (" + samples.length + "):");
        if (!samples.length) lines.push("  - none");
        else samples.forEach((item) => lines.push("  - [" + item.initiator + "] " + item.url + " | " + item.durationMs + " ms"));

        const n = s.navigation || {};
        lines.push("");
        lines.push("Navigation timing:");
        lines.push("- supported: " + bool(n.supported));
        if (n.supported) {
          lines.push("- DOM interactive: " + n.domInteractiveMs + " ms");
          lines.push("- DOMContentLoaded end: " + n.domContentLoadedEventEndMs + " ms");
          lines.push("- load event end: " + n.loadEventEndMs + " ms");
        }

        const errs = Array.isArray(s.errors) ? s.errors : [];
        lines.push("");
        lines.push("Page-world errors/rejections (" + errs.length + "):");
        if (!errs.length) lines.push("- None captured");
        else errs.forEach((item) => lines.push("- " + item.time + " [" + item.kind + "] " + item.message + (item.source ? " | " + item.source : "")));
      }

      lines.push("");
      lines.push("Privacy: no message text, typed text, cookies, local/session storage contents, request bodies, clipboard contents, placeholders, labels, or page text are collected.");
      lines.push("Performance: no MutationObserver, PerformanceObserver, DOM polling, click tracking, or on-page diagnostic UI is used; resource timing is read once at the 8-second snapshot.");
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

    function onMainReport(event) {
      let data = null;
      try { data = JSON.parse(event && typeof event.detail === "string" ? event.detail : ""); } catch (_) {}
      if (!data || data.build !== BUILD) return;
      if (data.kind === "started") {
        addEvent("page-probe", "page-world probe started");
      } else if (data.kind === "snapshot" && data.payload) {
        state.snapshot = data.payload;
        state.completed = true;
        addEvent("snapshot", "8-second page-world snapshot saved");
      }
    }

    document.addEventListener(REPORT_EVENT, onMainReport);
    persist();

    function signalMainProbe() {
      try { if (document.documentElement) document.documentElement.setAttribute(ENABLE_ATTR, "1"); } catch (_) {}
      try { document.dispatchEvent(new Event(ENABLE_EVENT)); } catch (_) {}
    }

    signalMainProbe();
    if (!document.documentElement) document.addEventListener("DOMContentLoaded", signalMainProbe, { once: true });

    document.addEventListener("DOMContentLoaded", () => addEvent("lifecycle", "DOMContentLoaded"), { once: true });
    window.addEventListener("load", () => addEvent("lifecycle", "window load"), { once: true });

    setTimeout(() => {
      if (!state.completed) addEvent("probe-timeout", "No page-world snapshot received by 9.5 seconds");
      persist();
    }, FALLBACK_DELAY_MS);
  }

  storageGet({ [ENABLE_KEY]: false }, (settings) => {
    if (settings && settings[ENABLE_KEY] === true) start();
  });
})();
