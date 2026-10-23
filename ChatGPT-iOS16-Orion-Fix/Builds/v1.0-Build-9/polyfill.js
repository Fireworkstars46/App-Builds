(() => {
  "use strict";

  if (typeof URL !== "undefined" && typeof URL.canParse !== "function") {
    Object.defineProperty(URL, "canParse", {
      configurable: true,
      writable: true,
      value(url, base) {
        try {
          if (arguments.length >= 2) {
            new URL(url, base);
          } else {
            new URL(url);
          }
          return true;
        } catch (_) {
          return false;
        }
      }
    });
  }

  if (typeof Object.groupBy !== "function") {
    Object.defineProperty(Object, "groupBy", {
      configurable: true,
      writable: true,
      value(items, callbackFn) {
        if (items == null) {
          throw new TypeError("Object.groupBy requires an iterable");
        }
        if (typeof callbackFn !== "function") {
          throw new TypeError("Object.groupBy callback must be a function");
        }

        const groups = Object.create(null);
        let index = 0;
        for (const item of items) {
          if (index >= Number.MAX_SAFE_INTEGER) {
            throw new TypeError("Object.groupBy exceeded the maximum safe index");
          }
          const key = callbackFn(item, index);
          if (Object.prototype.hasOwnProperty.call(groups, key)) {
            groups[key].push(item);
          } else {
            groups[key] = [item];
          }
          index += 1;
        }
        return groups;
      }
    });
  }

  if (typeof Map.groupBy !== "function") {
    Object.defineProperty(Map, "groupBy", {
      configurable: true,
      writable: true,
      value(items, callbackFn) {
        if (items == null) {
          throw new TypeError("Map.groupBy requires an iterable");
        }
        if (typeof callbackFn !== "function") {
          throw new TypeError("Map.groupBy callback must be a function");
        }

        const groups = new Map();
        let index = 0;
        for (const item of items) {
          if (index >= Number.MAX_SAFE_INTEGER) {
            throw new TypeError("Map.groupBy exceeded the maximum safe index");
          }
          const key = callbackFn(item, index);
          const existing = groups.get(key);
          if (existing) {
            existing.push(item);
          } else {
            groups.set(key, [item]);
          }
          index += 1;
        }
        return groups;
      }
    });
  }
})();
