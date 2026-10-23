(() => {
  "use strict";

  const VERSION = "1.0";
  const BUILD = 23;
  const STATUS_KEY = "build23AssetCompatStatus";
  const RELOAD_KEY = "chatgpt_ios16_b23_reload_count";
  const MAX_ASSETS = 60;
  const MAX_BYTES = 8 * 1024 * 1024;
  const FETCH_TIMEOUT_MS = 4500;
  const YIELD_MS = 12;
  const api = typeof browser !== "undefined" ? browser : (typeof chrome !== "undefined" ? chrome : null);

  function delay(ms) { return new Promise((resolve) => setTimeout(resolve, ms)); }

  function storageSet(value) {
    try {
      if (!api || !api.storage || !api.storage.local) return Promise.resolve();
      const result = api.storage.local.set(value);
      return result && typeof result.then === "function" ? result.catch(() => {}) : Promise.resolve();
    } catch (_) { return Promise.resolve(); }
  }

  function sendMessage(message) {
    return new Promise((resolve) => {
      try {
        if (!api || !api.runtime || typeof api.runtime.sendMessage !== "function") return resolve(null);
        const maybe = api.runtime.sendMessage(message, (result) => {
          try {
            if (api.runtime && api.runtime.lastError) resolve(null);
            else resolve(result || null);
          } catch (_) { resolve(result || null); }
        });
        if (maybe && typeof maybe.then === "function") maybe.then(resolve).catch(() => resolve(null));
      } catch (_) { resolve(null); }
    });
  }

  function fileName(url) {
    try { return new URL(url).pathname.split("/").pop() || "asset.js"; } catch (_) { return "asset.js"; }
  }

  function collectAssetUrls() {
    const out = [];
    const seen = new Set();
    try {
      const entries = performance && typeof performance.getEntriesByType === "function" ? performance.getEntriesByType("resource") : [];
      for (const entry of entries || []) {
        if (out.length >= MAX_ASSETS) break;
        try {
          const u = new URL(String(entry && entry.name ? entry.name : ""), location.origin);
          if (u.origin !== location.origin) continue;
          if (!/^\/cdn\/assets\/[^/?#]+\.m?js$/i.test(u.pathname)) continue;
          const clean = u.origin + u.pathname;
          if (!seen.has(clean)) { seen.add(clean); out.push(clean); }
        } catch (_) {}
      }
    } catch (_) {}
    return out;
  }

  async function fetchText(url) {
    const controller = typeof AbortController === "function" ? new AbortController() : null;
    let timer = null;
    try {
      if (controller) timer = setTimeout(() => controller.abort(), FETCH_TIMEOUT_MS);
      const response = await fetch(url, {
        credentials: "omit",
        cache: "force-cache",
        redirect: "error",
        referrerPolicy: "no-referrer",
        signal: controller ? controller.signal : undefined
      });
      if (!response || !response.ok) return null;
      const len = response.headers && response.headers.get ? Number(response.headers.get("content-length") || 0) : 0;
      if (Number.isFinite(len) && len > MAX_BYTES) return null;
      const text = await response.text();
      if (text.length > MAX_BYTES) return null;
      return text;
    } catch (_) { return null; }
    finally { if (timer != null) clearTimeout(timer); }
  }

  function isIdentStart(ch) { return /[A-Za-z_$]/.test(ch); }
  function isIdentPart(ch) { return /[A-Za-z0-9_$]/.test(ch); }

  function skipQuoted(source, i, quote) {
    i += 1;
    while (i < source.length) {
      const ch = source[i++];
      if (ch === "\\") { i += 1; continue; }
      if (ch === quote) break;
    }
    return i;
  }

  function skipTemplate(source, i) {
    i += 1;
    while (i < source.length) {
      const ch = source[i++];
      if (ch === "\\") { i += 1; continue; }
      if (ch === "`") break;
    }
    return i;
  }

  function scanVRegexLiterals(source) {
    const found = [];
    const prefixWords = new Set(["return", "throw", "case", "delete", "void", "typeof", "new", "in", "instanceof", "yield", "await", "else", "do"]);
    let i = 0;
    let canStartRegex = true;
    while (i < source.length) {
      const ch = source[i];
      if (/\s/.test(ch)) { i += 1; continue; }
      if (ch === "'" || ch === '"') { i = skipQuoted(source, i, ch); canStartRegex = false; continue; }
      if (ch === "`") { i = skipTemplate(source, i); canStartRegex = false; continue; }
      if (ch === "/" && source[i + 1] === "/") {
        i += 2; while (i < source.length && source[i] !== "\n" && source[i] !== "\r") i += 1; continue;
      }
      if (ch === "/" && source[i + 1] === "*") {
        i += 2; while (i + 1 < source.length && !(source[i] === "*" && source[i + 1] === "/")) i += 1; i = Math.min(source.length, i + 2); continue;
      }
      if (ch === "/" && canStartRegex) {
        const start = i;
        i += 1;
        let inClass = false;
        let closed = false;
        while (i < source.length) {
          const c = source[i++];
          if (c === "\\") { i += 1; continue; }
          if (c === "[" && !inClass) { inClass = true; continue; }
          if (c === "]" && inClass) { inClass = false; continue; }
          if (c === "/" && !inClass) { closed = true; break; }
          if (c === "\n" || c === "\r") break;
        }
        if (closed) {
          const slashEnd = i - 1;
          const flagsStart = i;
          while (i < source.length && /[A-Za-z]/.test(source[i])) i += 1;
          const flags = source.slice(flagsStart, i);
          if (flags.includes("v")) {
            found.push({ start, slashEnd, flagsStart, end: i, pattern: source.slice(start + 1, slashEnd), flags });
          }
          canStartRegex = false;
          continue;
        }
        i = start + 1;
        canStartRegex = true;
        continue;
      }
      if (ch === "/") { i += source[i + 1] === "=" ? 2 : 1; canStartRegex = true; continue; }
      if (isIdentStart(ch)) {
        const start = i++;
        while (i < source.length && isIdentPart(source[i])) i += 1;
        const word = source.slice(start, i);
        canStartRegex = prefixWords.has(word);
        continue;
      }
      if (/[0-9]/.test(ch)) {
        i += 1; while (i < source.length && /[0-9A-Fa-f_xXobOBn.eE+-]/.test(source[i])) i += 1;
        canStartRegex = false; continue;
      }
      const two = source.slice(i, i + 2);
      if (two === "++" || two === "--") { i += 2; canStartRegex = false; continue; }
      if (ch === ")" || ch === "]" || ch === "}") { i += 1; canStartRegex = false; continue; }
      if (ch === ".") { i += 1; canStartRegex = false; continue; }
      i += 1;
      canStartRegex = "([{,;:?=<>!~+-*%&|^".includes(ch);
    }
    return found;
  }

  function flagsWithoutV(flags, addU) {
    let out = "";
    for (const f of flags) if (f !== "v" && !out.includes(f)) out += f;
    if (addU && !out.includes("u")) out += "u";
    return out;
  }

  function patternNeedsVSemantics(pattern) {
    const value = String(pattern || "");
    return value.includes("&&") || value.includes("--") || /\\q\s*\{/.test(value) || /\\[pP]\{(?:RGI_|Basic_Emoji|Emoji_Keycap_Sequence|RGI_Emoji)/.test(value);
  }

  function testRegExp(pattern, flags) {
    try { new RegExp(pattern, flags); return true; } catch (_) { return false; }
  }

  function rewriteModuleSpecifiers(source, baseUrl) {
    function absolute(spec) {
      try {
        if (!(spec.startsWith("./") || spec.startsWith("../") || spec.startsWith("/"))) return spec;
        return new URL(spec, baseUrl).href;
      } catch (_) { return spec; }
    }
    let out = source.replace(/((?:\bfrom\s*|\bimport\s*\(\s*|\bimport\s*)["'])(\.{1,2}\/[^"']+|\/[^"']+)(["'])/g,
      (m, a, spec, q) => a + absolute(spec) + q);
    out = out.replace(/((?:\bexport\s+[^;]{0,300}?\bfrom\s*)["'])(\.{1,2}\/[^"']+|\/[^"']+)(["'])/g,
      (m, a, spec, q) => a + absolute(spec) + q);
    out = out.replace(/\bimport\.meta\.url\b/g, JSON.stringify(baseUrl));
    return out;
  }

  function transformSource(source, baseUrl) {
    const spans = scanVRegexLiterals(source);
    if (!spans.length) return { changed: false, source, literalCount: 0, safeCount: 0, fallbackCount: 0 };
    let out = source;
    let safeCount = 0;
    let fallbackCount = 0;
    for (let n = spans.length - 1; n >= 0; n--) {
      const item = spans[n];
      let replacement;
      const uFlags = flagsWithoutV(item.flags, true);
      const plainFlags = flagsWithoutV(item.flags, false);
      if (!patternNeedsVSemantics(item.pattern) && testRegExp(item.pattern, uFlags)) {
        replacement = out.slice(item.start, item.flagsStart) + uFlags;
        safeCount += 1;
      } else if (!patternNeedsVSemantics(item.pattern) && testRegExp(item.pattern, plainFlags)) {
        replacement = out.slice(item.start, item.flagsStart) + plainFlags;
        safeCount += 1;
      } else {
        const fallbackFlags = flagsWithoutV(item.flags, true);
        replacement = "/(?!) /";
        replacement = "/(?!)/" + fallbackFlags;
        fallbackCount += 1;
      }
      out = out.slice(0, item.start) + replacement + out.slice(item.end);
    }
    out = rewriteModuleSpecifiers(out, baseUrl);
    return { changed: true, source: out, literalCount: spans.length, safeCount, fallbackCount };
  }

  function toBase64Utf8(text) {
    const bytes = new TextEncoder().encode(text);
    let binary = "";
    const CHUNK = 0x8000;
    for (let i = 0; i < bytes.length; i += CHUNK) {
      binary += String.fromCharCode.apply(null, bytes.subarray(i, Math.min(bytes.length, i + CHUNK)));
    }
    return btoa(binary);
  }

  function getReloadCount() {
    try { return Math.max(0, Math.min(2, Number(sessionStorage.getItem(RELOAD_KEY) || 0) || 0)); } catch (_) { return 0; }
  }
  function setReloadCount(value) { try { sessionStorage.setItem(RELOAD_KEY, String(value)); } catch (_) {} }

  async function run() {
    const status = {
      version: VERSION, build: BUILD, captured: new Date().toISOString(),
      discoveredAssets: 0, fetchedAssets: 0, failedAssets: 0,
      trueVLiteralCount: 0, patchedAssetCount: 0, safeDowngradeCount: 0, fallbackLiteralCount: 0,
      patchedAssets: [], backgroundStored: 0, backgroundCached: 0, backgroundRedirectsBeforeStore: 0,
      reloadCountBefore: getReloadCount(), autoReloadIssued: false, lastError: ""
    };
    try {
      const before = await sendMessage({ type: "chatgpt-ios16-b23-status" });
      if (before && Number.isFinite(Number(before.patchRedirectCount))) status.backgroundRedirectsBeforeStore = Number(before.patchRedirectCount);
      const urls = collectAssetUrls();
      status.discoveredAssets = urls.length;
      const patches = [];
      for (const url of urls) {
        const text = await fetchText(url);
        if (text == null) { status.failedAssets += 1; await delay(YIELD_MS); continue; }
        status.fetchedAssets += 1;
        const transformed = transformSource(text, url);
        if (transformed.changed) {
          status.trueVLiteralCount += transformed.literalCount;
          status.safeDowngradeCount += transformed.safeCount;
          status.fallbackLiteralCount += transformed.fallbackCount;
          status.patchedAssetCount += 1;
          if (status.patchedAssets.length < 8) status.patchedAssets.push(fileName(url));
          patches.push({ url, dataUrl: "data:text/javascript;base64," + toBase64Utf8(transformed.source) });
        }
        await delay(YIELD_MS);
      }
      if (patches.length) {
        const stored = await sendMessage({ type: "chatgpt-ios16-b23-store-patches", patches });
        if (stored) {
          status.backgroundStored = Number(stored.stored) || 0;
          status.backgroundCached = Number(stored.cached) || 0;
        }
      }
      const reloadCount = getReloadCount();
      if (status.backgroundStored > 0 && reloadCount < 2) {
        status.autoReloadIssued = true;
        setReloadCount(reloadCount + 1);
        await storageSet({ [STATUS_KEY]: status });
        setTimeout(() => location.reload(), 80);
        return;
      }
    } catch (error) {
      status.lastError = error && error.message ? String(error.message).slice(0, 200) : "asset compatibility pass failed";
    }
    await storageSet({ [STATUS_KEY]: status });
  }

  function schedule() {
    if (document.readyState === "complete") setTimeout(run, 350);
    else window.addEventListener("load", () => setTimeout(run, 350), { once: true });
  }

  schedule();
})();
