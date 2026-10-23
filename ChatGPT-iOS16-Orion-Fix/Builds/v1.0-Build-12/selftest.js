const fs = require('fs');
const vm = require('vm');
const path = require('path');
const root = __dirname;
let pass = 0, fail = 0;
function check(name, fn) { try { if (fn() === false) throw new Error('returned false'); console.log('PASS - ' + name); pass++; } catch (e) { console.log('FAIL - ' + name + ' | ' + e.message); fail++; } }
function read(name) { return fs.readFileSync(path.join(root, name), 'utf8'); }
function polyfillContext() { class TestURL extends URL {} const c={URL:TestURL,Object,Map,Number,TypeError,Symbol,console}; vm.createContext(c); vm.runInContext(read('polyfill.js'),c); return c; }

check('manifest identifies Version 1.0 Build 12 manifest 1.0.11',()=>{const m=JSON.parse(read('manifest.json'));return m.manifest_version===3&&m.version==='1.0.11'&&m.content_scripts.some(x=>x.js&&x.js.includes('main-probe.js')&&x.world==='MAIN');});
check('URL.canParse compatibility behavior preserved',()=>{const c=polyfillContext();return c.URL.canParse('https://example.com')===true&&c.URL.canParse('::::')===false&&c.URL.canParse('/a','https://example.com')===true;});
check('Object.groupBy compatibility behavior preserved',()=>{const c=polyfillContext();const r=c.Object.groupBy([1,2,3,4],v=>v%2?'odd':'even');return r.odd.join(',')==='1,3'&&r.even.join(',')==='2,4'&&Object.getPrototypeOf(r)===null;});
check('Map.groupBy compatibility behavior preserved',()=>{const c=polyfillContext();const k={};const r=c.Map.groupBy([1,2,3],v=>v===1?k:NaN);return r.get(k)[0]===1&&r.get(NaN).join(',')==='2,3';});
check('diagnostic has no heavy observer/polling/click architecture',()=>{const s=read('main-probe.js')+read('light-diagnostic.js');return !/new\s+MutationObserver\s*\(/.test(s)&&!/new\s+PerformanceObserver\s*\(/.test(s)&&!/setInterval\s*\(/.test(s)&&!/addEventListener\s*\(\s*["']click["']/.test(s);});
check('diagnostic creates no on-page UI',()=>{const s=read('main-probe.js')+read('light-diagnostic.js');return !/attachShadow\s*\(/.test(s)&&!/appendChild\s*\(/.test(s)&&!/createElement\s*\(/.test(s);});
check('page-world probe does not read page text or input values',()=>{const s=read('main-probe.js');return !/\.textContent\b/.test(s)&&!/\.innerText\b/.test(s)&&!/\.value\b/.test(s)&&!/getAttribute\s*\(\s*["']placeholder["']/.test(s);});
check('CSP-invalid new Function syntax probes removed',()=>{const s=read('main-probe.js');return !/new\s+Function\s*\(/.test(s)&&!s.includes('syntax:')&&!s.includes('syntaxSupported(');});
check('API feature matrix still includes targeted modern capabilities',()=>{const s=read('main-probe.js');return ['Array.fromAsync','Promise.withResolvers','Promise.try','Set.prototype.union','Iterator.prototype.map','URLPattern','Intl.DurationFormat','ReadableStream.from','ArrayBuffer.prototype.transfer','Uint8Array.fromBase64','RegExp v flag','document.startViewTransition'].every(x=>s.includes(x));});
check('feature matrix remains diagnostic-only and defines no missing APIs',()=>{const s=read('main-probe.js');return !/Object\.defineProperty\s*\(/.test(s)&&!/prototype\.[A-Za-z0-9_$]+\s*=/.test(s)&&!/\bwindow\.[A-Za-z0-9_$]+\s*=/.test(s);});
check('early matrix captured before setting resolution',()=>{const s=read('main-probe.js');return s.indexOf('earlyFeatureMatrix = buildFeatureMatrix(') < s.indexOf('attachEarlyCapture();')&&s.includes('document_start before ChatGPT bootstrap');});
check('8-second matrix and early-vs-late comparison are produced',()=>{const s=read('main-probe.js');return s.includes('8-second snapshot after ChatGPT startup attempt')&&s.includes('compareFeatureMatrices(earlyFeatureMatrix, lateFeatureMatrix)')&&s.includes('becameSupported')&&s.includes('stillMissing')&&s.includes('becameMissing');});
check('OFF resolution removes listeners and clears early matrix/error buffer',()=>{const s=read('main-probe.js');return /detachEarlyCapture\(\)/.test(s)&&/errors\.splice\(0, errors\.length\)/.test(s)&&/earlyFeatureMatrix = null/.test(s);});
check('resource timing remains one-time API read',()=>{const s=read('main-probe.js');return /getEntriesByType\s*\(\s*["']resource["']\s*\)/.test(s)&&!/PerformanceObserver/.test(s);});

class FakeCustomEvent extends Event { constructor(type, init={}) { super(type); this.detail=init.detail; } }
class FakeElement { constructor(tag='DIV', attrs={}) { this.tagName=tag; this.attrs={...attrs}; this.disabled=false; this.onclick=null; } getAttribute(n){return Object.prototype.hasOwnProperty.call(this.attrs,n)?this.attrs[n]:null;} setAttribute(n,v){this.attrs[n]=String(v);} removeAttribute(n){delete this.attrs[n];} }
function buildBase(enabled) {
  const tasks=[]; const saved={}; const document=new EventTarget();
  const rootEl=new FakeElement('DIV'); rootEl['__reactFiber$abc']={};
  const composer=new FakeElement('TEXTAREA'); const sidebar=new FakeElement('BUTTON',{'aria-disabled':'false'}); const documentElement=new FakeElement('HTML');
  document.documentElement=documentElement; document.body={}; document.readyState='complete';
  document.querySelector=(sel)=>{if(sel==='#root')return rootEl;if(sel.includes('prompt-textarea'))return composer;if(sel.includes('send-button'))return null;if(sel.includes('sidebar'))return sidebar;return null;};
  document.querySelectorAll=(sel)=>new Array({'button':15,'script':11,'script[src]':0,"script[type='module']":1,"script[type='module']:not([src])":1,"script[type='module'][src]":0,"link[rel='modulepreload']":34,"link[rel='preload'][as='script']":0,"link[rel='stylesheet']":1}[sel]||0).fill({});
  document.createEvent=()=>({initCustomEvent(type,b,c,detail){this.type=type;this.detail=detail;}});
  const window=new EventTarget(); window.location={origin:'https://chatgpt.com'};
  window.performance={getEntriesByType(type){if(type==='resource')return [{initiatorType:'script',name:'https://chatgpt.com/cdn/assets/12345678901234567890123456789012.js?token=SECRET',duration:120}];if(type==='navigation')return [{domInteractive:500,domContentLoadedEventEnd:700,loadEventEnd:900}];return[];}};
  const navigator={userAgent:'Mozilla/5.0 iPhone OS 16_6 AppleWebKit/605.1.15',platform:'iPhone',vendor:'Apple Computer, Inc.'};
  class TestPromise extends Promise {}
  TestPromise.withResolvers = undefined;
  const chrome={runtime:{lastError:null},storage:{local:{get(def,cb){cb({diagnosticsEnabled:enabled});},set(v,cb){Object.assign(saved,v);if(cb)cb();}}}};
  const context={window,document,navigator,chrome,URL,Event,EventTarget,CustomEvent:FakeCustomEvent,Object,Map,Array,Set,ArrayBuffer,Uint8Array,Number,RegExp,Intl,ReadableStream:globalThis.ReadableStream,AbortSignal:globalThis.AbortSignal,Promise:TestPromise,Date,console,setTimeout(fn,ms){tasks.push({fn,ms});return tasks.length;},clearTimeout(){}};
  vm.createContext(context);
  return {context,tasks,saved,window,document,TestPromise};
}
function finish(h){h.tasks.sort((a,b)=>a.ms-b.ms).forEach(t=>t.fn());return h;}
check('early-vs-late comparison detects capability becoming supported during startup',()=>{
  const h=buildBase(true); vm.runInContext(read('main-probe.js'),h.context); h.TestPromise.withResolvers=()=>({promise:null,resolve(){},reject(){}}); vm.runInContext(read('light-diagnostic.js'),h.context); finish(h);
  const r=h.saved.lightDiagnosticReport&&h.saved.lightDiagnosticReport.report||'';
  return /Version 1.0 \| Build 12/.test(r)&&/Browser feature comparison:/.test(r)&&/Promise.withResolvers/.test(r)&&/became supported:/.test(r)&&/8-second matrix/.test(r)&&!/syntax: optional chaining/.test(r);
});
check('diagnostics OFF saves no report',()=>{const h=buildBase(false);vm.runInContext(read('main-probe.js'),h.context);vm.runInContext(read('light-diagnostic.js'),h.context);finish(h);return !Object.prototype.hasOwnProperty.call(h.saved,'lightDiagnosticReport');});
check('resource URL secrets and long IDs are redacted',()=>{const h=buildBase(true);vm.runInContext(read('main-probe.js'),h.context);vm.runInContext(read('light-diagnostic.js'),h.context);finish(h);const r=h.saved.lightDiagnosticReport.report;return !r.includes('SECRET')&&!r.includes('?token=')&&(r.includes(':hex')||r.includes(':token'));});
check('popup identifies Build 12 and default remains OFF',()=>{const h=read('popup.html'),j=read('popup.js');return /Light Diagnostics \(Build 12\)/.test(h)&&!/Build 11/.test(h)&&/\[ENABLE_KEY\]: false/.test(j);});
check('Copy Missing Features Only copies comparison section through production popup handler',()=>{
  class PopEl {constructor(){this.handlers={};this.checked=false;this.textContent='';this.value='';this.selection=null;}addEventListener(t,f){this.handlers[t]=f;}focus(){}select(){this.selection=[0,this.value.length];}setSelectionRange(a,b){this.selection=[a,b];}}
  const ids=['diagnostics','status','report','reportStatus','refresh','copy','copyMissing','clear']; const els=Object.fromEntries(ids.map(id=>[id,new PopEl()]));
  const sample=['Header','Browser feature comparison:','- syntax probes removed: CSP','Early matrix (document_start):','- missing/unsupported: 2','  - Promise.withResolvers','  - URLPattern','8-second matrix (after ChatGPT startup attempt):','- missing/unsupported: 1','  - URLPattern','Changes during ChatGPT startup:','- became supported: 1','  - Promise.withResolvers','- still missing at 8 seconds: 1','  - URLPattern','','Page-world errors/rejections (0):'].join('\n');
  let copied=''; const document={getElementById(id){return els[id];},execCommand(cmd){return cmd==='copy';}}; const navigator={clipboard:{writeText(text){copied=text;return {then(resolve){resolve();}};}}};
  const chrome={runtime:{lastError:null},storage:{local:{get(def,cb){cb({diagnosticsEnabled:true,lightDiagnosticReport:{updated:'now',report:sample}});},set(v,cb){if(cb)cb();}}}};
  const c={document,navigator,chrome,Promise,console,Object,Boolean,String};vm.createContext(c);vm.runInContext(read('popup.js'),c);els.copyMissing.handlers.click();
  return copied.startsWith('Browser feature comparison:')&&copied.includes('Promise.withResolvers')&&copied.includes('still missing at 8 seconds: 1')&&!copied.includes('Page-world errors');
});
check('Copy Missing Features Only fallback selects comparison section on older clipboard path',()=>{
  class PopEl {constructor(){this.handlers={};this.checked=false;this.textContent='';this.value='';this.selection=null;}addEventListener(t,f){this.handlers[t]=f;}focus(){}select(){this.selection=[0,this.value.length];}setSelectionRange(a,b){this.selection=[a,b];}}
  const ids=['diagnostics','status','report','reportStatus','refresh','copy','copyMissing','clear']; const els=Object.fromEntries(ids.map(id=>[id,new PopEl()]));
  const sample='x\nBrowser feature comparison:\n- missing/unsupported: 1\n  - URLPattern\n\nPage-world errors/rejections (0):\n'; let exec=false;
  const document={getElementById(id){return els[id];},execCommand(cmd){exec=cmd==='copy';return exec;}}; const chrome={runtime:{lastError:null},storage:{local:{get(def,cb){cb({diagnosticsEnabled:true,lightDiagnosticReport:{updated:'now',report:sample}});},set(v,cb){if(cb)cb();}}}};
  const c={document,navigator:{},chrome,Promise,console,Object,Boolean,String};vm.createContext(c);vm.runInContext(read('popup.js'),c);els.copyMissing.handlers.click(); const sel=els.report.selection; const selected=sel?els.report.value.slice(sel[0],sel[1]):'';
  return exec&&selected.startsWith('Browser feature comparison:')&&selected.includes('URLPattern')&&!selected.includes('Page-world errors');
});
check('version/build strings consistent across release docs',()=>['BUILD-INFO.txt','INSTALL.txt','RELEASE-NOTES.txt','RELEASE-EVIDENCE.txt'].every(n=>/Version[: ]+1\.0/i.test(read(n))&&/Build[: ]+12/i.test(read(n))));
check('polyfill contains only three targeted compatibility shims',()=>{const s=read('polyfill.js');return /URL\.canParse/.test(s)&&/Object\.groupBy/.test(s)&&/Map\.groupBy/.test(s)&&!/diagnostic/i.test(s);});
console.log('TOTAL: '+pass+' PASS / '+fail+' FAIL'); process.exit(fail?1:0);
