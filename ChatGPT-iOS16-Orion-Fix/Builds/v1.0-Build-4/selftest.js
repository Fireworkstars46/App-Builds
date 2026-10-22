const fs = require('fs');
const vm = require('vm');
const path = require('path');

const root = __dirname;
let pass = 0, fail = 0;
function check(name, fn) {
  try {
    const ok = fn();
    if (ok === false) throw new Error('returned false');
    console.log('PASS - ' + name);
    pass++;
  } catch (e) {
    console.log('FAIL - ' + name + ' | ' + e.message);
    fail++;
  }
}

// Polyfill regression tests.
function polyfillContext(preseed = {}) {
  class TestURL extends URL {}
  const ctx = { URL: TestURL, Object, Map, Number, TypeError, Symbol, console, ...preseed };
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(root, 'polyfill.js'), 'utf8'), ctx);
  return ctx;
}

check('URL.canParse valid/invalid/base behavior', () => {
  const c = polyfillContext();
  if (c.URL.canParse('https://example.com/a') !== true) return false;
  if (c.URL.canParse('::::') !== false) return false;
  if (c.URL.canParse('/a', 'https://example.com') !== true) return false;
  return true;
});
check('Object.groupBy groups and callback indexes', () => {
  const c = polyfillContext();
  const seen = [];
  const r = c.Object.groupBy([1,2,3,4], (v,i) => { seen.push(i); return v % 2 ? 'odd' : 'even'; });
  return seen.join(',') === '0,1,2,3' && r.odd.join(',') === '1,3' && r.even.join(',') === '2,4' && Object.getPrototypeOf(r) === null;
});
check('Object.groupBy handles __proto__ and Symbol keys', () => {
  const c = polyfillContext();
  const s = Symbol('k');
  const r1 = c.Object.groupBy([1], () => '__proto__');
  const r2 = c.Object.groupBy([2], () => s);
  return r1['__proto__'][0] === 1 && r2[s][0] === 2;
});
check('Map.groupBy preserves key identity and NaN grouping', () => {
  const c = polyfillContext();
  const obj = {};
  const r = c.Map.groupBy([1,2,3], (v) => v === 1 ? obj : NaN);
  return r.get(obj)[0] === 1 && r.get(NaN).join(',') === '2,3';
});
check('Polyfills do not overwrite native implementations', () => {
  function a(){return 'native-url';}
  function b(){return 'native-object';}
  function d(){return 'native-map';}
  class TestURL extends URL {}
  Object.defineProperty(TestURL, 'canParse', {value:a, configurable:true, writable:true});
  const OldObjectGroupBy = Object.groupBy;
  const OldMapGroupBy = Map.groupBy;
  try {
    Object.defineProperty(Object, 'groupBy', {value:b, configurable:true, writable:true});
    Object.defineProperty(Map, 'groupBy', {value:d, configurable:true, writable:true});
    const ctx = { URL: TestURL, Object, Map, Number, TypeError, Symbol, console };
    vm.createContext(ctx);
    vm.runInContext(fs.readFileSync(path.join(root, 'polyfill.js'), 'utf8'), ctx);
    return ctx.URL.canParse === a && ctx.Object.groupBy === b && ctx.Map.groupBy === d;
  } finally {
    if (OldObjectGroupBy === undefined) delete Object.groupBy; else Object.defineProperty(Object,'groupBy',{value:OldObjectGroupBy,configurable:true,writable:true});
    if (OldMapGroupBy === undefined) delete Map.groupBy; else Object.defineProperty(Map,'groupBy',{value:OldMapGroupBy,configurable:true,writable:true});
  }
});

function makeDoc() {
  const doc = new EventTarget();
  doc.documentElement = null;
  return doc;
}
function makeWin() {
  const win = new EventTarget();
  win.location = { origin: 'https://chatgpt.com' };
  return win;
}
function runDiagAndBridge(initial) {
  const document = makeDoc();
  const window = makeWin();
  let stored = initial;
  const changeListeners = [];
  const chrome = {
    runtime: { lastError: null },
    storage: {
      local: {
        get(defaults, cb) { cb({ diagnosticsEnabled: stored === undefined ? defaults.diagnosticsEnabled : stored }); },
        set(obj, cb) {
          const oldValue = stored;
          stored = obj.diagnosticsEnabled;
          const changes = { diagnosticsEnabled: { oldValue, newValue: stored } };
          for (const fn of changeListeners) fn(changes, 'local');
          if (cb) cb();
        }
      },
      onChanged: { addListener(fn) { changeListeners.push(fn); } }
    }
  };
  const common = { document, Event, EventTarget, console, chrome, URL, Promise, Object, Map, Array, AbortSignal, structuredClone, crypto: globalThis.crypto, CSS: {supports(){return true;}}, Number, navigator: {}, setTimeout, clearTimeout };
  const main = {...common, window};
  vm.createContext(main);
  vm.runInContext(fs.readFileSync(path.join(root,'diagnostic.js'),'utf8'), main);
  const isolated = {...common, window: {}};
  vm.createContext(isolated);
  vm.runInContext(fs.readFileSync(path.join(root,'settings-bridge.js'),'utf8'), isolated);
  return {document, window, chrome, getStored:()=>stored};
}

check('Diagnostics default OFF with no saved setting', () => {
  const h = runDiagAndBridge(undefined);
  return h.window.__CHATGPT_IOS16_DIAG__.enabled === false && h.getStored() === undefined;
});
check('Persisted Diagnostics ON is read and applied', () => {
  const h = runDiagAndBridge(true);
  return h.window.__CHATGPT_IOS16_DIAG__.enabled === true;
});
check('Storage change ON/OFF immediately syncs to page diagnostic state', () => {
  const h = runDiagAndBridge(false);
  h.chrome.storage.local.set({diagnosticsEnabled:true}, ()=>{});
  if (h.window.__CHATGPT_IOS16_DIAG__.enabled !== true) return false;
  h.chrome.storage.local.set({diagnosticsEnabled:false}, ()=>{});
  return h.window.__CHATGPT_IOS16_DIAG__.enabled === false;
});
check('Diagnostic Turn Off request writes OFF and disables immediately', () => {
  const h = runDiagAndBridge(true);
  h.document.dispatchEvent(new Event('chatgpt-ios16-diag-request-off'));
  return h.getStored() === false && h.window.__CHATGPT_IOS16_DIAG__.enabled === false;
});
check('Setting persistence write -> reload/read -> compare', () => {
  const h1 = runDiagAndBridge(false);
  h1.chrome.storage.local.set({diagnosticsEnabled:true}, ()=>{});
  const persisted = h1.getStored();
  const h2 = runDiagAndBridge(persisted);
  return persisted === true && h2.window.__CHATGPT_IOS16_DIAG__.enabled === true;
});

function runPopup(initial) {
  let stored = initial;
  const checkbox = { checked:false, disabled:false, handlers:{}, addEventListener(type, fn){this.handlers[type]=fn;} };
  const status = { textContent:'' };
  const document = { getElementById(id){ return id === 'diagnostics' ? checkbox : status; } };
  const chrome = { runtime:{lastError:null}, storage:{ local:{
    get(defaults, cb){ cb({diagnosticsEnabled: stored === undefined ? defaults.diagnosticsEnabled : stored}); },
    set(obj, cb){ stored = obj.diagnosticsEnabled; if(cb) cb(); }
  }}};
  const ctx = {document, chrome, console};
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(root,'popup.js'),'utf8'),ctx);
  return {checkbox,status,getStored:()=>stored};
}
check('Popup loads default OFF and reflects status', () => {
  const p = runPopup(undefined);
  return p.checkbox.checked === false && /OFF/.test(p.status.textContent);
});
check('Popup toggle saves ON and updates status', () => {
  const p = runPopup(false);
  p.checkbox.checked = true;
  p.checkbox.handlers.change();
  return p.getStored() === true && p.checkbox.checked === true && /ON/.test(p.status.textContent);
});


check('Diagnostic UI mounts when enabled and is removed when disabled', () => {
  class FakeButton { constructor(){ this.handlers={}; this.textContent=''; } addEventListener(t,f){ this.handlers[t]=f; } }
  class FakeShadow {
    constructor(){ this.nodes={panel:{hidden:true},count:{textContent:''},report:{value:'',focus(){},select(){},setSelectionRange(){}},status:{textContent:''},bubble:new FakeButton(),close:new FakeButton(),copy:new FakeButton(),disable:new FakeButton(),clear:new FakeButton()}; this._html=''; }
    set innerHTML(v){this._html=v;} get innerHTML(){return this._html;} getElementById(id){return this.nodes[id]||null;}
  }
  class FakeHost { constructor(){this.style={};this.parentNode=null;this.id='';} attachShadow(){this.shadow=new FakeShadow();return this.shadow;} }
  const htmlRoot={children:[],appendChild(el){this.children.push(el);el.parentNode=this;},removeChild(el){this.children=this.children.filter(x=>x!==el);el.parentNode=null;}};
  const doc=new EventTarget(); doc.documentElement=htmlRoot; doc.createElement=()=>new FakeHost(); doc.execCommand=()=>true;
  const win=makeWin();
  const ctx={document:doc,window:win,Event,EventTarget,console,URL,Promise,Object,Map,Array,AbortSignal,structuredClone,crypto:globalThis.crypto,CSS:{supports(){return true;}},Number,navigator:{},setTimeout,clearTimeout};
  vm.createContext(ctx); vm.runInContext(fs.readFileSync(path.join(root,'diagnostic.js'),'utf8'),ctx);
  if (htmlRoot.children.length !== 0) return false;
  doc.dispatchEvent(new Event('chatgpt-ios16-diag-enable'));
  if (htmlRoot.children.length !== 1 || win.__CHATGPT_IOS16_DIAG__.enabled !== true) return false;
  doc.dispatchEvent(new Event('chatgpt-ios16-diag-disable'));
  return htmlRoot.children.length === 0 && win.__CHATGPT_IOS16_DIAG__.enabled === false;
});

console.log(`TOTAL: ${pass} PASS / ${fail} FAIL`);
process.exit(fail ? 1 : 0);
