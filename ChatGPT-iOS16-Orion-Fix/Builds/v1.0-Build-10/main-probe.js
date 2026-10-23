(() => {
  "use strict";

  const VERSION = "1.0";
  const BUILD = 10;
  const ENABLE_ATTR = "data-chatgpt-ios16-lightdiag";
  const RESOLVE_EVENT = "chatgpt-ios16-lightdiag-resolved";
  const REPORT_EVENT = "chatgpt-ios16-lightdiag-main-report";
  const SNAPSHOT_DELAY_MS = 8000;
  const MAX_ERRORS = 8;
  let started = false;
  let settingResolved = false;
  let diagnosticsEnabled = false;
  const errors = [];
  let earlyFeatureMatrix = null;

  function hasFunction(value) {
    return typeof value === "function";
  }

  function syntaxSupported(source) {
    try {
      // Parse-only probe. The returned function is never invoked.
      new Function(source);
      return true;
    } catch (_) {
      return false;
    }
  }

  function regexpFlagSupported(flag) {
    try {
      new RegExp("", flag);
      return true;
    } catch (_) {
      return false;
    }
  }

  function buildEarlyFeatureMatrix() {
    const setProto = typeof Set !== "undefined" ? Set.prototype : null;
    const arrayBufferProto = typeof ArrayBuffer !== "undefined" ? ArrayBuffer.prototype : null;
    const uint8Proto = typeof Uint8Array !== "undefined" ? Uint8Array.prototype : null;
    const iteratorProto = typeof Iterator !== "undefined" && Iterator && Iterator.prototype ? Iterator.prototype : null;
    const intl = typeof Intl !== "undefined" ? Intl : null;
    const readableStreamCtor = typeof ReadableStream !== "undefined" ? ReadableStream : null;
    const abortSignalCtor = typeof AbortSignal !== "undefined" ? AbortSignal : null;
    const cryptoObj = typeof crypto !== "undefined" ? crypto : null;

    return {
      captured: new Date().toISOString(),
      phase: "document_start before ChatGPT bootstrap; after this extension's compatibility polyfill",
      features: {
        "Array.fromAsync": hasFunction(Array.fromAsync),
        "Promise.withResolvers": hasFunction(Promise.withResolvers),
        "Promise.try": hasFunction(Promise.try),
        "Object.groupBy": hasFunction(Object.groupBy),
        "Map.groupBy": hasFunction(Map.groupBy),
        "RegExp.escape": typeof RegExp !== "undefined" && hasFunction(RegExp.escape),
        "RegExp v flag": regexpFlagSupported("v"),
        "Set.prototype.union": Boolean(setProto && hasFunction(setProto.union)),
        "Set.prototype.intersection": Boolean(setProto && hasFunction(setProto.intersection)),
        "Set.prototype.difference": Boolean(setProto && hasFunction(setProto.difference)),
        "Set.prototype.symmetricDifference": Boolean(setProto && hasFunction(setProto.symmetricDifference)),
        "Set.prototype.isSubsetOf": Boolean(setProto && hasFunction(setProto.isSubsetOf)),
        "Set.prototype.isSupersetOf": Boolean(setProto && hasFunction(setProto.isSupersetOf)),
        "Set.prototype.isDisjointFrom": Boolean(setProto && hasFunction(setProto.isDisjointFrom)),
        "Iterator global": typeof Iterator !== "undefined",
        "Iterator.prototype.map": Boolean(iteratorProto && hasFunction(iteratorProto.map)),
        "Iterator.prototype.filter": Boolean(iteratorProto && hasFunction(iteratorProto.filter)),
        "Iterator.prototype.take": Boolean(iteratorProto && hasFunction(iteratorProto.take)),
        "Iterator.prototype.drop": Boolean(iteratorProto && hasFunction(iteratorProto.drop)),
        "Iterator.prototype.flatMap": Boolean(iteratorProto && hasFunction(iteratorProto.flatMap)),
        "Iterator.prototype.reduce": Boolean(iteratorProto && hasFunction(iteratorProto.reduce)),
        "Iterator.prototype.toArray": Boolean(iteratorProto && hasFunction(iteratorProto.toArray)),
        "URLPattern": typeof URLPattern === "function",
        "Intl.DurationFormat": Boolean(intl && hasFunction(intl.DurationFormat)),
        "ReadableStream.from": Boolean(readableStreamCtor && hasFunction(readableStreamCtor.from)),
        "ArrayBuffer.prototype.transfer": Boolean(arrayBufferProto && hasFunction(arrayBufferProto.transfer)),
        "ArrayBuffer.prototype.transferToFixedLength": Boolean(arrayBufferProto && hasFunction(arrayBufferProto.transferToFixedLength)),
        "Resizable ArrayBuffer": Boolean(arrayBufferProto && "resizable" in arrayBufferProto),
        "Uint8Array.fromBase64": hasFunction(Uint8Array.fromBase64),
        "Uint8Array.fromHex": hasFunction(Uint8Array.fromHex),
        "Uint8Array.prototype.toBase64": Boolean(uint8Proto && hasFunction(uint8Proto.toBase64)),
        "Uint8Array.prototype.toHex": Boolean(uint8Proto && hasFunction(uint8Proto.toHex)),
        "Uint8Array.prototype.setFromBase64": Boolean(uint8Proto && hasFunction(uint8Proto.setFromBase64)),
        "Uint8Array.prototype.setFromHex": Boolean(uint8Proto && hasFunction(uint8Proto.setFromHex)),
        "Array.prototype.toSorted": hasFunction(Array.prototype.toSorted),
        "Array.prototype.toReversed": hasFunction(Array.prototype.toReversed),
        "Array.prototype.toSpliced": hasFunction(Array.prototype.toSpliced),
        "Array.prototype.with": hasFunction(Array.prototype.with),
        "Object.hasOwn": hasFunction(Object.hasOwn),
        "WeakRef": typeof WeakRef === "function",
        "FinalizationRegistry": typeof FinalizationRegistry === "function",
        "Intl.Segmenter": Boolean(intl && hasFunction(intl.Segmenter)),
        "Intl.supportedValuesOf": Boolean(intl && hasFunction(intl.supportedValuesOf)),
        "URL.canParse": typeof URL !== "undefined" && hasFunction(URL.canParse),
        "CSS :has selector support": typeof CSS !== "undefined" && CSS && hasFunction(CSS.supports) ? Boolean(CSS.supports("selector(:has(*))")) : false,
        "scheduler.postTask": typeof scheduler !== "undefined" && scheduler && hasFunction(scheduler.postTask),
        "navigator.scheduling.isInputPending": typeof navigator !== "undefined" && navigator.scheduling && hasFunction(navigator.scheduling.isInputPending),
        "trustedTypes.createPolicy": typeof trustedTypes !== "undefined" && trustedTypes && hasFunction(trustedTypes.createPolicy),
        "document.startViewTransition": typeof document !== "undefined" && hasFunction(document.startViewTransition),
        "HTMLElement.prototype.showPopover": typeof HTMLElement !== "undefined" && hasFunction(HTMLElement.prototype.showPopover),
        "Navigation API": typeof navigation !== "undefined",
        "CompressionStream": typeof CompressionStream === "function",
        "DecompressionStream": typeof DecompressionStream === "function",
        "TextEncoderStream": typeof TextEncoderStream === "function",
        "TextDecoderStream": typeof TextDecoderStream === "function",
        "AbortSignal.any": Boolean(abortSignalCtor && hasFunction(abortSignalCtor.any)),
        "AbortSignal.timeout": Boolean(abortSignalCtor && hasFunction(abortSignalCtor.timeout)),
        "structuredClone": typeof structuredClone === "function",
        "crypto.randomUUID": Boolean(cryptoObj && hasFunction(cryptoObj.randomUUID)),
        "syntax: class static block": syntaxSupported("class X { static { this.x = 1; } }"),
        "syntax: private fields": syntaxSupported("class X { #x = 1; get(){ return this.#x; } }"),
        "syntax: ergonomic brand check": syntaxSupported("class X { #x; has(o){ return #x in o; } }"),
        "syntax: logical assignment": syntaxSupported("let x = 0; x ||= 1; x &&= 2; x ??= 3;"),
        "syntax: numeric separators": syntaxSupported("return 1_000_000;"),
        "syntax: optional chaining": syntaxSupported("const x = {}; return x?.a?.b;"),
        "syntax: nullish coalescing": syntaxSupported("return null ?? 1;")
      }
    };
  }

  earlyFeatureMatrix = buildEarlyFeatureMatrix();

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
    const result = {
      fiber: false,
      props: false,
      events: false,
      container: false,
      listeners: false,
      handles: false,
      listening: false,
      markerCount: 0
    };
    if (!element) return result;
    try {
      const names = Object.getOwnPropertyNames(element);
      for (const name of names) {
        if (name.indexOf("__reactFiber$") === 0) result.fiber = true;
        if (name.indexOf("__reactProps$") === 0) result.props = true;
        if (name.indexOf("__reactEvents$") === 0) result.events = true;
        if (name.indexOf("__reactContainer$") === 0) result.container = true;
        if (name.indexOf("__reactListeners$") === 0) result.listeners = true;
        if (name.indexOf("__reactHandles$") === 0) result.handles = true;
        if (name.indexOf("_reactListening") === 0) result.listening = true;
      }
      result.markerCount = Number(result.fiber) + Number(result.props) + Number(result.events) +
        Number(result.container) + Number(result.listeners) + Number(result.handles) + Number(result.listening);
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
        inlineModuleScriptCount: count("script[type='module']:not([src])"),
        externalModuleScriptCount: count("script[type='module'][src]"),
        modulePreloadCount: count("link[rel='modulepreload']"),
        preloadScriptCount: count("link[rel='preload'][as='script']"),
        stylesheetCount: count("link[rel='stylesheet']")
      },
      resources: resourceSummary(),
      navigation: navigationSummary(),
      featureMatrix: earlyFeatureMatrix,
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

  function onEarlyError(event) {
    if (event && event.target && event.target !== window) {
      const target = event.target;
      const tag = String(target && target.tagName ? target.tagName : "resource").toUpperCase();
      const url = target && (target.src || target.href) ? (target.src || target.href) : "";
      if (url) {
        addError("resource-error", tag, url);
      } else if (tag === "SCRIPT") {
        let type = "classic";
        try {
          const rawType = target.getAttribute && target.getAttribute("type");
          if (rawType) type = clip(rawType, 40);
        } catch (_) {}
        addError("inline-script-error", "inline " + type + " script failed", "");
      } else {
        addError("resource-error", tag + " failed without URL", "");
      }
      return;
    }
    addError("javascript-error", event && event.message ? event.message : "JavaScript error", event && event.filename ? event.filename : "");
  }

  function onEarlyCsp(event) {
    const directive = event && (event.effectiveDirective || event.violatedDirective) ?
      (event.effectiveDirective || event.violatedDirective) : "CSP";
    const blocked = event && event.blockedURI ? sanitizeUrl(event.blockedURI) : "";
    addError("csp-violation", clip(directive, 80) + (blocked ? " blocked " + blocked : ""), "");
  }

  function onEarlyRejection(event) {
    const reason = event ? event.reason : null;
    let message = "Promise rejected";
    if (reason && typeof reason === "object") message = reason.message || reason.name || message;
    else if (typeof reason === "string") message = reason;
    addError("unhandled-rejection", message, "");
  }

  function attachEarlyCapture() {
    window.addEventListener("error", onEarlyError, true);
    document.addEventListener("securitypolicyviolation", onEarlyCsp, true);
    window.addEventListener("unhandledrejection", onEarlyRejection, true);
  }

  function detachEarlyCapture() {
    window.removeEventListener("error", onEarlyError, true);
    document.removeEventListener("securitypolicyviolation", onEarlyCsp, true);
    window.removeEventListener("unhandledrejection", onEarlyRejection, true);
  }

  function start() {
    if (started || !diagnosticsEnabled) return;
    started = true;
    try { if (document.documentElement) document.documentElement.removeAttribute(ENABLE_ATTR); } catch (_) {}
    emit("started", {
      readyState: document.readyState || "unknown",
      earlyBufferedErrorCount: errors.length,
      earlyFeatureCount: earlyFeatureMatrix && earlyFeatureMatrix.features ? Object.keys(earlyFeatureMatrix.features).length : 0
    });
    setTimeout(() => emit("snapshot", makeSnapshot()), SNAPSHOT_DELAY_MS);
  }

  function resolveSetting() {
    if (settingResolved) return;
    settingResolved = true;
    try {
      diagnosticsEnabled = Boolean(document.documentElement && document.documentElement.getAttribute(ENABLE_ATTR) === "1");
    } catch (_) {
      diagnosticsEnabled = false;
    }

    if (diagnosticsEnabled) {
      start();
    } else {
      detachEarlyCapture();
      errors.splice(0, errors.length);
      earlyFeatureMatrix = null;
      try { if (document.documentElement) document.documentElement.removeAttribute(ENABLE_ATTR); } catch (_) {}
    }
  }

  // Attach immediately at document_start, before the isolated-world storage lookup can finish.
  // If diagnostics are OFF, the isolated-world script resolves the setting to OFF,
  // these listeners are removed, and the small in-memory buffer is cleared without persistence.
  attachEarlyCapture();
  document.addEventListener(RESOLVE_EVENT, resolveSetting, { once: true });

  function checkResolvedAttribute() {
    try {
      if (!document.documentElement) return;
      const value = document.documentElement.getAttribute(ENABLE_ATTR);
      if (value === "1" || value === "0") resolveSetting();
    } catch (_) {}
  }

  checkResolvedAttribute();
  if (!document.documentElement) document.addEventListener("DOMContentLoaded", checkResolvedAttribute, { once: true });

})();
