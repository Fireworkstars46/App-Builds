(() => {
  "use strict";

  const VERSION = "1.0";
  const BUILD = 23;
  const TARGET_UA = "Mozilla/5.0 (iPhone; CPU iPhone OS 18_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.7 Mobile/15E148 Safari/604.1";
  const api = typeof browser !== "undefined" ? browser : (typeof chrome !== "undefined" ? chrome : null);
  const patchMap = new Map();

  const status = {
    version: VERSION,
    build: BUILD,
    uaTransport: "webRequest.onBeforeSendHeaders",
    uaListenerInstalled: false,
    uaModifiedRequestCount: 0,
    targetUserAgent: TARGET_UA,
    patchTransport: "webRequest.onBeforeRequest redirectUrl=data:text/javascript",
    patchListenerInstalled: false,
    patchCacheCount: 0,
    patchStoreEvents: 0,
    patchRedirectCount: 0,
    lastError: ""
  };

  function isChatGptAssetUrl(value) {
    try {
      const u = new URL(String(value || ""));
      return u.origin === "https://chatgpt.com" && /^\/cdn\/assets\/[^/?#]+\.m?js$/i.test(u.pathname);
    } catch (_) {
      return false;
    }
  }

  function cleanAssetUrl(value) {
    try {
      const u = new URL(String(value || ""));
      if (!isChatGptAssetUrl(u.href)) return "";
      return u.origin + u.pathname;
    } catch (_) {
      return "";
    }
  }

  function copyStatus() {
    return {
      version: VERSION,
      build: BUILD,
      uaTransport: status.uaTransport,
      uaListenerInstalled: status.uaListenerInstalled === true,
      uaModifiedRequestCount: Number(status.uaModifiedRequestCount) || 0,
      targetUserAgent: status.targetUserAgent,
      patchTransport: status.patchTransport,
      patchListenerInstalled: status.patchListenerInstalled === true,
      patchCacheCount: patchMap.size,
      patchStoreEvents: Number(status.patchStoreEvents) || 0,
      patchRedirectCount: Number(status.patchRedirectCount) || 0,
      lastError: String(status.lastError || "").slice(0, 200)
    };
  }

  function rewriteUserAgent(details) {
    try {
      const headers = Array.isArray(details && details.requestHeaders)
        ? details.requestHeaders.map((h) => ({ name: h.name, value: h.value }))
        : [];
      let found = false;
      for (const header of headers) {
        if (String(header.name || "").toLowerCase() === "user-agent") {
          header.value = TARGET_UA;
          found = true;
          break;
        }
      }
      if (!found) headers.push({ name: "User-Agent", value: TARGET_UA });
      status.uaModifiedRequestCount += 1;
      return { requestHeaders: headers };
    } catch (error) {
      status.lastError = error && error.message ? String(error.message) : "request header rewrite failed";
      return {};
    }
  }

  function redirectPatchedAsset(details) {
    try {
      const key = cleanAssetUrl(details && details.url);
      if (!key) return {};
      const dataUrl = patchMap.get(key);
      if (!dataUrl) return {};
      status.patchRedirectCount += 1;
      return { redirectUrl: dataUrl };
    } catch (error) {
      status.lastError = error && error.message ? String(error.message) : "asset redirect failed";
      return {};
    }
  }

  function storePatches(message) {
    try {
      const patches = Array.isArray(message && message.patches) ? message.patches : [];
      let stored = 0;
      for (const item of patches.slice(0, 12)) {
        const url = cleanAssetUrl(item && item.url);
        const dataUrl = String(item && item.dataUrl ? item.dataUrl : "");
        if (!url || !dataUrl.startsWith("data:text/javascript;base64,")) continue;
        if (dataUrl.length > 12 * 1024 * 1024) continue;
        patchMap.set(url, dataUrl);
        stored += 1;
      }
      status.patchCacheCount = patchMap.size;
      status.patchStoreEvents += 1;
      return { ok: true, stored, cached: patchMap.size, status: copyStatus() };
    } catch (error) {
      status.lastError = error && error.message ? String(error.message) : "patch store failed";
      return { ok: false, stored: 0, cached: patchMap.size, status: copyStatus() };
    }
  }

  try {
    if (!api || !api.webRequest || !api.webRequest.onBeforeSendHeaders || typeof api.webRequest.onBeforeSendHeaders.addListener !== "function") {
      status.lastError = "webRequest.onBeforeSendHeaders unavailable";
    } else {
      api.webRequest.onBeforeSendHeaders.addListener(
        rewriteUserAgent,
        { urls: ["https://chatgpt.com/*"] },
        ["blocking", "requestHeaders"]
      );
      status.uaListenerInstalled = true;
    }
  } catch (error) {
    status.lastError = error && error.message ? String(error.message) : "UA listener install failed";
  }

  try {
    if (!api || !api.webRequest || !api.webRequest.onBeforeRequest || typeof api.webRequest.onBeforeRequest.addListener !== "function") {
      status.lastError = status.lastError || "webRequest.onBeforeRequest unavailable";
    } else {
      api.webRequest.onBeforeRequest.addListener(
        redirectPatchedAsset,
        { urls: ["https://chatgpt.com/cdn/assets/*"], types: ["script"] },
        ["blocking"]
      );
      status.patchListenerInstalled = true;
    }
  } catch (error) {
    status.lastError = error && error.message ? String(error.message) : "asset redirect listener install failed";
  }

  try {
    if (api && api.runtime && api.runtime.onMessage && typeof api.runtime.onMessage.addListener === "function") {
      api.runtime.onMessage.addListener((message) => {
        if (!message || typeof message !== "object") return undefined;
        if (message.type === "chatgpt-ios16-b23-status") return Promise.resolve(copyStatus());
        if (message.type === "chatgpt-ios16-b23-store-patches") return Promise.resolve(storePatches(message));
        return undefined;
      });
    }
  } catch (error) {
    status.lastError = error && error.message ? String(error.message) : status.lastError;
  }
})();
