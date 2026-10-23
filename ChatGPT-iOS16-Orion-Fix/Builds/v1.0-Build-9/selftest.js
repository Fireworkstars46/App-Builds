const fs = require('fs');
const vm = require('vm');
const path = require('path');
const root = __dirname;
let pass = 0, fail = 0;
function check(name, fn) { try { if (fn() === false) throw new Error('returned false'); console.log('PASS - ' + name); pass++; } catch (e) { console.log('FAIL - ' + name + ' | ' + e.message); fail++; } }
function read(name) { return fs.readFileSync(path.join(root, name), 'utf8'); }
function polyfillContext() { class TestURL extends URL {} const c={URL:TestURL,Object,Map,Number,TypeError,Symbol,console}; vm.createContext(c); vm.runInContext(read('polyfill.js'),c); return c; }

check('manifest JSON parses and identifies Version 1.0 Build 9 manifest 1.0.8',()=>{const m=JSON.parse(read('manifest.json'));return m.manifest_version===3&&m.version==='1.0.8'&&m.content_scripts.some(x=>x.js&&x.js.includes('main-probe.js')&&x.world==='MAIN');});
check('URL.canParse compatibility behavior preserved',()=>{const c=polyfillContext();return c.URL.canParse('https://example.com')===true&&c.URL.canParse('::::')===false&&c.URL.canParse('/a','https://example.com')===true;});
check('Object.groupBy compatibility behavior preserved',()=>{const c=polyfillContext();const r=c.Object.groupBy([1,2,3,4],v=>v%2?'odd':'even');return r.odd.join(',')==='1,3'&&r.even.join(',')==='2,4'&&Object.getPrototypeOf(r)===null;});
check('Map.groupBy compatibility behavior preserved',()=>{const c=polyfillContext();const k={};const r=c.Map.groupBy([1,2,3],v=>v===1?k:NaN);return r.get(k)[0]===1&&r.get(NaN).join(',')==='2,3';});
check('diagnostic has no heavy observer/polling/click architecture',()=>{const s=read('main-probe.js')+read('light-diagnostic.js');return !/new\s+MutationObserver\s*\(/.test(s)&&!/new\s+PerformanceObserver\s*\(/.test(s)&&!/setInterval\s*\(/.test(s)&&!/addEventListener\s*\(\s*["']click["']/.test(s);});
check('diagnostic creates no on-page UI',()=>{const s=read('main-probe.js')+read('light-diagnostic.js');return !/attachShadow\s*\(/.test(s)&&!/appendChild\s*\(/.test(s)&&!/createElement\s*\(/.test(s);});
check('page-world probe does not read page text or input values',()=>{const s=read('main-probe.js');return !/\.textContent\b/.test(s)&&!/\.innerText\b/.test(s)&&!/\.value\b/.test(s)&&!/getAttribute\s*\(\s*["']placeholder["']/.test(s);});
check('immediate early capture is attached before setting resolution',()=>{const s=read('main-probe.js');return s.indexOf('attachEarlyCapture();') < s.indexOf('document.addEventListener(RESOLVE_EVENT') && /window\.addEventListener\("error", onEarlyError, true\)/.test(s);});
check('OFF resolution removes listeners and clears buffer',()=>{const s=read('main-probe.js');return /detachEarlyCapture\(\)/.test(s)&&/errors\.splice\(0, errors\.length\)/.test(s)&&/removeEventListener\("error", onEarlyError, true\)/.test(s);});
check('resource timing remains one-time API read',()=>{const s=read('main-probe.js');return /getEntriesByType\s*\(\s*["']resource["']\s*\)/.test(s)&&!/PerformanceObserver/.test(s);});
check('CSP capture does not read CSP sample/code content',()=>{const s=read('main-probe.js');return /securitypolicyviolation/.test(s)&&/effectiveDirective/.test(s)&&/blockedURI/.test(s)&&!s.includes('event.sample')&&!s.includes('event["sample"]')&&!s.includes("event['sample']");});

class FakeCustomEvent extends Event { constructor(type, init={}) { super(type); this.detail=init.detail; } }
class FakeElement { constructor(tag='DIV', attrs={}) { this.tagName=tag; this.attrs={...attrs}; this.disabled=false; this.onclick=null; } getAttribute(n){return Object.prototype.hasOwnProperty.call(this.attrs,n)?this.attrs[n]:null;} setAttribute(n,v){this.attrs[n]=String(v);} removeAttribute(n){delete this.attrs[n];} }
function buildBase(enabled) {
  const tasks=[]; const saved={}; const document=new EventTarget();
  const rootEl=new FakeElement('DIV'); rootEl['__reactFiber$abc']={}; rootEl['__reactProps$abc']={}; rootEl['__reactContainer$abc']={}; rootEl['_reactListeningabc']=true;
  const composer=new FakeElement('TEXTAREA'); composer['__reactFiber$def']={}; composer['__reactProps$def']={};
  const sidebar=new FakeElement('BUTTON',{'aria-disabled':'false'}); sidebar['__reactFiber$ghi']={}; sidebar['__reactProps$ghi']={};
  const documentElement=new FakeElement('HTML');
  document.documentElement=documentElement; document.body={}; document.readyState='complete';
  document.querySelector=(sel)=>{if(sel==='#root')return rootEl;if(sel.includes('prompt-textarea'))return composer;if(sel.includes('send-button'))return null;if(sel.includes('sidebar'))return sidebar;return null;};
  document.querySelectorAll=(sel)=>new Array({'button':15,'script':11,'script[src]':0,"script[type='module']":1,"script[type='module']:not([src])":1,"script[type='module'][src]":0,"link[rel='modulepreload']":34,"link[rel='preload'][as='script']":0,"link[rel='stylesheet']":1}[sel]||0).fill({});
  document.createEvent=()=>({initCustomEvent(type,b,c,detail){this.type=type;this.detail=detail;}});
  const window=new EventTarget(); window.location={origin:'https://chatgpt.com'};
  window.performance={getEntriesByType(type){if(type==='resource')return [{initiatorType:'script',name:'https://chatgpt.com/cdn/assets/12345678901234567890123456789012.js?token=SECRET',duration:120}];if(type==='navigation')return [{domInteractive:500,domContentLoadedEventEnd:700,loadEventEnd:900}];return[];}};
  const navigator={userAgent:'Mozilla/5.0 iPhone OS 16_6 AppleWebKit/605.1.15',platform:'iPhone',vendor:'Apple Computer, Inc.'};
  const chrome={runtime:{lastError:null},storage:{local:{get(def,cb){cb({diagnosticsEnabled:enabled});},set(v,cb){Object.assign(saved,v);if(cb)cb();}}}};
  const context={window,document,navigator,chrome,URL,Event,EventTarget,CustomEvent:FakeCustomEvent,Object,Map,Array,Number,Promise,Date,console,setTimeout(fn,ms){tasks.push({fn,ms});return tasks.length;},clearTimeout(){}};
  vm.createContext(context);
  return {context,tasks,saved,window,document};
}
function fireInlineModuleError(h) {
  const script=new FakeElement('SCRIPT',{type:'module'});
  const e=new Event('error');
  Object.defineProperty(e,'target',{value:script});
  h.window.dispatchEvent(e);
}
function finish(h){h.tasks.sort((a,b)=>a.ms-b.ms).forEach(t=>t.fn());return h;}

check('early inline module failure before storage lookup is retained when diagnostics ON',()=>{
  const h=buildBase(true); vm.runInContext(read('main-probe.js'),h.context); fireInlineModuleError(h); vm.runInContext(read('light-diagnostic.js'),h.context); finish(h);
  const r=h.saved.lightDiagnosticReport&&h.saved.lightDiagnosticReport.report||'';
  return /Build 9/.test(r)&&/early buffered errors=1/.test(r)&&/inline-script-error/.test(r)&&/inline module script failed/.test(r);
});
check('early failure is discarded and no report saved when diagnostics OFF',()=>{
  const h=buildBase(false); vm.runInContext(read('main-probe.js'),h.context); fireInlineModuleError(h); vm.runInContext(read('light-diagnostic.js'),h.context); finish(h);
  return !Object.prototype.hasOwnProperty.call(h.saved,'lightDiagnosticReport');
});
check('diagnostics ON still produces completed one-time snapshot',()=>{const h=buildBase(true);vm.runInContext(read('main-probe.js'),h.context);vm.runInContext(read('light-diagnostic.js'),h.context);finish(h);const r=h.saved.lightDiagnosticReport&&h.saved.lightDiagnosticReport.report||'';return /Startup capture completed: yes/.test(r)&&/inline module script count: 1/.test(r)&&/modulepreload count: 34/.test(r);});
check('resource URL secrets and long IDs are redacted',()=>{const h=buildBase(true);vm.runInContext(read('main-probe.js'),h.context);vm.runInContext(read('light-diagnostic.js'),h.context);finish(h);const r=h.saved.lightDiagnosticReport.report;return !r.includes('SECRET')&&!r.includes('?token=')&&(r.includes(':hex')||r.includes(':token'));});
check('popup identifies Build 9 and default remains OFF',()=>{const h=read('popup.html'),j=read('popup.js');return /Light Diagnostics \(Build 9\)/.test(h)&&!/Build 8/.test(h)&&/\[ENABLE_KEY\]: false/.test(j);});
check('version/build strings are consistent across release docs',()=>['BUILD-INFO.txt','INSTALL.txt','RELEASE-NOTES.txt','RELEASE-EVIDENCE.txt'].every(n=>/Version[: ]+1\.0/i.test(read(n))&&/Build[: ]+9/i.test(read(n))));
check('polyfill source remains unchanged in behavior and contains only three targeted shims',()=>{const s=read('polyfill.js');return /URL\.canParse/.test(s)&&/Object\.groupBy/.test(s)&&/Map\.groupBy/.test(s)&&!/diagnostic/i.test(s);});
console.log('TOTAL: '+pass+' PASS / '+fail+' FAIL'); process.exit(fail?1:0);
