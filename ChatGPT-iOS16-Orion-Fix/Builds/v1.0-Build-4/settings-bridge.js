(() => {
  "use strict";

  const KEY = "diagnosticsEnabled";
  const EVENT_ENABLE = "chatgpt-ios16-diag-enable";
  const EVENT_DISABLE = "chatgpt-ios16-diag-disable";
  const EVENT_READY = "chatgpt-ios16-diag-ready";
  const EVENT_REQUEST_OFF = "chatgpt-ios16-diag-request-off";

  const chromeApi = typeof chrome !== "undefined" ? chrome : null;
  const browserApi = typeof browser !== "undefined" ? browser : null;

  function emit(enabled) {
    document.dispatchEvent(new Event(enabled ? EVENT_ENABLE : EVENT_DISABLE));
  }

  function readSetting() {
    if (chromeApi && chromeApi.storage && chromeApi.storage.local) {
      try {
        chromeApi.storage.local.get({ [KEY]: false }, (result) => {
          if (chromeApi.runtime && chromeApi.runtime.lastError) {
            emit(false);
            return;
          }
          emit(Boolean(result && result[KEY] === true));
        });
        return;
      } catch (_) {
        // Fall through to browser.* or safe OFF.
      }
    }

    if (browserApi && browserApi.storage && browserApi.storage.local) {
      try {
        Promise.resolve(browserApi.storage.local.get({ [KEY]: false }))
          .then((result) => emit(Boolean(result && result[KEY] === true)))
          .catch(() => emit(false));
        return;
      } catch (_) {
        // Safe default below.
      }
    }

    emit(false);
  }

  function writeSetting(enabled) {
    const value = { [KEY]: Boolean(enabled) };
    if (chromeApi && chromeApi.storage && chromeApi.storage.local) {
      try {
        chromeApi.storage.local.set(value, () => {
          if (chromeApi.runtime && chromeApi.runtime.lastError) emit(false);
        });
        return;
      } catch (_) {
        // Fall through.
      }
    }

    if (browserApi && browserApi.storage && browserApi.storage.local) {
      try {
        Promise.resolve(browserApi.storage.local.set(value)).catch(() => emit(false));
      } catch (_) {
        emit(false);
      }
    }
  }

  document.addEventListener(EVENT_READY, readSetting);
  document.addEventListener(EVENT_REQUEST_OFF, () => writeSetting(false));

  const changed = chromeApi && chromeApi.storage && chromeApi.storage.onChanged
    ? chromeApi.storage.onChanged
    : browserApi && browserApi.storage && browserApi.storage.onChanged
      ? browserApi.storage.onChanged
      : null;

  if (changed && typeof changed.addListener === "function") {
    changed.addListener((changes, areaName) => {
      if (areaName !== "local" || !changes || !changes[KEY]) return;
      emit(changes[KEY].newValue === true);
    });
  }

  // Also read immediately in case the MAIN-world diagnostic was ready first.
  readSetting();
})();
