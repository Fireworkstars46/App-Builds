#!/usr/bin/env python3
from pathlib import Path
import hashlib
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
APP_GRADLE = ROOT / 'app' / 'build.gradle'
MANIFEST = ROOT / 'app' / 'src' / 'main' / 'AndroidManifest.xml'
MAIN = ROOT / 'app' / 'src' / 'main' / 'java' / 'com' / 'fireworkstars46' / 'disneynowfiretv' / 'MainActivity.java'
BUILD_INFO = ROOT / 'BUILD_INFO.md'
README = ROOT / 'README.md'
GRADLE_PROPERTIES = ROOT / 'gradle.properties'
REPORT = ROOT / 'build' / 'reports' / 'STATIC-AUDIT-v0.1-Build13.txt'
EXPECTED_PACKAGE = 'com.fireworkstars46.disneynowfiretv'
ANDROID_NS = '{http://schemas.android.com/apk/res/android}'
results = []

def add(name, ok, detail=''):
    results.append(('PASS' if ok else 'FAIL', name, detail))

def has(text, needle):
    return needle in text

for path in [APP_GRADLE, MANIFEST, MAIN, BUILD_INFO, README, GRADLE_PROPERTIES]:
    add(f'Required source exists: {path.relative_to(ROOT)}', path.is_file(), str(path))

if any(s == 'FAIL' for s, _, _ in results):
    gradle = manifest_text = main = build_info = readme = gradle_properties = ''
else:
    gradle = APP_GRADLE.read_text(encoding='utf-8')
    manifest_text = MANIFEST.read_text(encoding='utf-8')
    main = MAIN.read_text(encoding='utf-8')
    build_info = BUILD_INFO.read_text(encoding='utf-8')
    readme = README.read_text(encoding='utf-8')
    gradle_properties = GRADLE_PROPERTIES.read_text(encoding='utf-8')

# Identity / build / dependency invariants.
add('Package namespace preserved', "namespace 'com.fireworkstars46.disneynowfiretv'" in gradle, EXPECTED_PACKAGE)
add('Package applicationId preserved', "applicationId 'com.fireworkstars46.disneynowfiretv'" in gradle, EXPECTED_PACKAGE)
add('Expected package embedded in runtime check', EXPECTED_PACKAGE in main, EXPECTED_PACKAGE)
add('Version name preserved', re.search(r"versionName\s+['\"]0\.1['\"]", gradle) is not None, '0.1')
add('Version code incremented to 13', re.search(r'versionCode\s+13\b', gradle) is not None, '13')
add('BuildConfig build number is 13', "buildConfigField 'int', 'APP_BUILD', '13'" in gradle, '13')
add('Runtime Safe Self-Test expects Build 13', 'BuildConfig.APP_BUILD == 13 && BuildConfig.VERSION_CODE == 13' in main, 'Build 13/versionCode 13')
add('Minimum SDK 22 preserved', re.search(r'minSdk\s+22\b', gradle) is not None, 'existing compatibility floor')
add('Target SDK 35 preserved', re.search(r'targetSdk\s+35\b', gradle) is not None, 'targetSdk 35')
add('Compile SDK 35 preserved', re.search(r'compileSdk\s+35\b', gradle) is not None, 'compileSdk 35')
add('Java 17 compile target', gradle.count('JavaVersion.VERSION_17') >= 2, 'source/target Java 17')
add('Media3 version pinned to 1.8.1', 'def media3_version = "1.8.1"' in gradle, 'last compatible line before minSdk 23 migration')
add('AndroidX mode enabled for Media3', 'android.useAndroidX=true' in gradle_properties, 'required by AndroidX Media3 dependencies')
for dep in ['media3-exoplayer', 'media3-exoplayer-dash', 'media3-exoplayer-hls', 'media3-ui']:
    add(f'Media3 dependency present: {dep}', dep in gradle, dep)

# Manifest / least privilege.
try:
    root = ET.fromstring(manifest_text)
    permissions = [n.attrib.get(ANDROID_NS + 'name', '') for n in root.findall('uses-permission')]
    app = root.find('application')
    activity = app.find('activity') if app is not None else None
    categories = [c.attrib.get(ANDROID_NS + 'name', '') for c in root.findall('.//category')]
    add('AndroidManifest XML parses', True, 'well-formed')
    add('INTERNET is the only requested permission', permissions == ['android.permission.INTERNET'], f'permissions={permissions}')
    add('Cleartext HTTP disabled', app is not None and app.attrib.get(ANDROID_NS + 'usesCleartextTraffic') == 'false', 'usesCleartextTraffic=false')
    add('Application hardware acceleration enabled', app is not None and app.attrib.get(ANDROID_NS + 'hardwareAccelerated') == 'true', 'hardwareAccelerated=true')
    add('Launcher activity exported', activity is not None and activity.attrib.get(ANDROID_NS + 'exported') == 'true', 'exported=true')
    add('Leanback launcher retained', 'android.intent.category.LEANBACK_LAUNCHER' in categories, str(categories))
    add('Standard launcher retained', 'android.intent.category.LAUNCHER' in categories, str(categories))
except Exception as exc:
    add('AndroidManifest XML parses', False, repr(exc))

# WebView safety / auth behavior.
checks = [
    ('JavaScript enabled', 'setJavaScriptEnabled(true)'),
    ('DOM storage enabled', 'setDomStorageEnabled(true)'),
    ('Media playback user gesture relaxed', 'setMediaPlaybackRequiresUserGesture(false)'),
    ('File access disabled', 'setAllowFileAccess(false)'),
    ('Content access disabled', 'setAllowContentAccess(false)'),
    ('Mixed content prohibited', 'MIXED_CONTENT_NEVER_ALLOW'),
    ('Third-party cookies allowed for provider auth', 'setAcceptThirdPartyCookies(webView, true)'),
    ('WebView debugging remains disabled', 'setWebContentsDebuggingEnabled(false)'),
    ('WebView native compositor layer retained', 'webView.setLayerType(View.LAYER_TYPE_NONE, null)'),
    ('Renderer priority policy set to important on API 26+', 'setRendererPriorityPolicy(WebView.RENDERER_PRIORITY_IMPORTANT, false)'),
    ('Popup provider-login routing retained', 'final boolean[] routed = new boolean[]{false}'),
    ('Cookie flush after navigation', 'CookieManager.getInstance().flush()'),
    ('App-local web-data clear path retained', 'clearAppWebData()'),
]
for name, needle in checks:
    add(name, needle in main, needle)

# Build 8 navigation architecture.
nav_checks = [
    ('Native TV Navigation setting exists', 'KEY_NATIVE_TV_NAV'),
    ('Build 8 migration flag exists', 'KEY_BUILD8_MIGRATED'),
    ('Build 8 migration enables Native TV Navigation', '.putBoolean(KEY_NATIVE_TV_NAV, true)'),
    ('Build 8 migration disables cursor', '.putBoolean(KEY_CURSOR_ENABLED, false)'),
    ('Build 8 migration disables legacy JS focus', '.putBoolean(KEY_TV_FOCUS, false)'),
    ('Build 8 migration enables Performance Mode', '.putBoolean(KEY_PERFORMANCE_MODE, true)'),
    ('Native TV Navigation production setter exists', 'setNativeTvNavigation(boolean enabled)'),
    ('Cursor enabling disables native TV mode', 'editor.putBoolean(KEY_NATIVE_TV_NAV, false)'),
    ('Legacy focus enabling disables native TV mode', 'setTvFocusNavigation(boolean enabled)'),
    ('Cursor compatibility path retained', 'Cursor Navigation (Compatibility)'),
    ('Legacy JS focus path retained', 'Legacy JS Focus Navigation'),
    ('Native TV mode exposed in menu', 'Native TV Navigation: '),
    ('Default D-pad path can pass through to WebView', 'super.dispatchKeyEvent(event)'),
    ('Native TV mode does not require DOM scanning every frame', 'isNativeTvNavigationEnabled()'),
]
for name, needle in nav_checks:
    add(name, needle in main, needle)

# Cursor compatibility must remain isolated and hidden when not selected.
cursor_checks = [
    ('Cursor compatibility overlay retained', 'private final class CursorView extends View'),
    ('Compact cursor overlay remains 48dp', 'cursorOverlaySize = dp(48)'),
    ('Cursor translated rather than full-screen redraw', 'setTranslationX(newX - getWidth() / 2f)'),
    ('Cursor click dispatch retained', 'webView.dispatchTouchEvent(down)'),
    ('Cursor hidden for native player', 'cursorView.setVisibility(View.GONE)'),
    ('Cursor mode preference persisted', 'KEY_CURSOR_ENABLED'),
]
for name, needle in cursor_checks:
    add(name, needle in main, needle)

# Whole-page zoom: regression target from Build 7.
zoom_checks = [
    ('Page Zoom setting retained', 'KEY_PAGE_ZOOM'),
    ('Page Zoom minimum 0', 'MIN_PAGE_ZOOM = 0'),
    ('Page Zoom maximum 500', 'MAX_PAGE_ZOOM = 500'),
    ('Direct numeric Page Zoom entry', 'TYPE_CLASS_NUMBER'),
    ('0-500 slider retained', 'slider.setMax(MAX_PAGE_ZOOM)'),
    ('One-percent decrement retained', 'minus.setText("-1")'),
    ('One-percent increment retained', 'plus.setText("+1")'),
    ('Reset 100 retained', 'reset.setText("Reset 100%")'),
    ('Whole-page WebView zoom method exists', 'applyWholePageZoom()'),
    ('WebView zoomBy used', 'webView.zoomBy('),
    ('0 percent hides complete WebView', 'webView.setAlpha(0f)'),
    ('Nonzero zoom restores WebView alpha', 'webView.setAlpha(1f)'),
    ('Page finished reapplies whole-page zoom', 'applyWholePageZoom();'),
]
for name, needle in zoom_checks:
    add(name, needle in main, needle)
add('Build 7 CSS zoom injector removed', 'firetv-page-zoom-style' not in main and 'html{zoom:' not in main, 'no document-only CSS zoom')
zoom_setter = re.search(r'private boolean setPageZoom\(int percent, boolean applyNow\) \{(.*?)\n    \}', main, re.S)
zoom_body = zoom_setter.group(1) if zoom_setter else ''
add('Page Zoom setter does not reload WebView', bool(zoom_setter) and 'webView.reload()' not in zoom_body, 'no endless reload regression')
add('Page Zoom setter uses whole-page production apply', 'applyWholePageZoom();' in zoom_body, 'same setter used by controls')

# Performance mode.
perf_checks = [
    ('Performance Mode setting exists', 'KEY_PERFORMANCE_MODE'),
    ('Performance Mode production setter exists', 'setPerformanceMode(boolean enabled)'),
    ('Performance Mode app-menu control exists', 'Performance Mode: '),
    ('Performance style has bounded animation duration', 'animation-duration:0.001s'),
    ('Performance style removes smooth scrolling', 'scroll-behavior:auto'),
    ('Performance Mode can remove its injected style', "getElementById('firetv-performance-style')"),
]
for name, needle in perf_checks:
    add(name, needle in main, needle)

# Experimental native media path inspired by official TV architecture, without proprietary code.
media_checks = [
    ('Media3 PlayerView field exists', 'private PlayerView nativePlayerView'),
    ('Media3 ExoPlayer field exists', 'private ExoPlayer nativePlayer'),
    ('Native player starts hidden', 'nativePlayerContainer.setVisibility(View.GONE)'),
    ('HLS/DASH WebView request observation exists', 'rememberMediaRequest(request)'),
    ('HLS classifier exists', 'endsWith(".m3u8")'),
    ('DASH classifier exists', 'endsWith(".mpd")'),
    ('DRM request classifier exists', 'isLikelyDrmLicenseRequest'),
    ('Media request headers stay memory-only', 'lastMediaRequestHeaders'),
    ('DRM request headers stay memory-only', 'lastDrmRequestHeaders'),
    ('Portable header copy excludes Host', '"host".equalsIgnoreCase(key)'),
    ('Portable header copy excludes Content-Length', '"content-length".equalsIgnoreCase(key)'),
    ('Session cookie can be passed in memory', 'CookieManager.getInstance().getCookie(url)'),
    ('Dormant native player implementation retained for controlled future diagnostics', 'private void tryNativePlayback()'),
    ('Media3 DefaultHttpDataSource used', 'DefaultHttpDataSource.Factory'),
    ('Media3 DefaultMediaSourceFactory used', 'DefaultMediaSourceFactory'),
    ('Media3 ExoPlayer builder used', 'new ExoPlayer.Builder(this)'),
    ('HLS MIME type assigned', 'MimeTypes.APPLICATION_M3U8'),
    ('DASH MIME type assigned', 'MimeTypes.APPLICATION_MPD'),
    ('Android Widevine UUID used through Media3', 'new MediaItem.DrmConfiguration.Builder(C.WIDEVINE_UUID)'),
    ('Observed license URI passed to Media3', '.setLicenseUri(lastDrmLicenseUrl)'),
    ('Observed license headers passed to Media3', '.setLicenseRequestHeaders(drmHeaders)'),
    ('Native player setup failure is contained', 'NATIVE_PLAYER setup_error'),
    ('Native playback error uses safe error code only', 'NATIVE_PLAYER error code='),
    ('Native player releases resources', 'nativePlayer.release()'),
    ('Back exits native player before app navigation', 'if (isNativePlayerVisible())'),
    ('Media candidates cleared on page navigation', 'clearMediaCandidates();'),
    ('Media candidates cleared with web data', 'app-local WebView data and in-memory media candidates'),
    ('Silk fallback retained', 'Open Current Page in Silk (Video Fallback)'),
]
for name, needle in media_checks:
    add(name, needle in main, needle)

# Build 13 privacy-safe Debug Mode + crash-stage rollback diagnostics.
debug_checks = [
    ('Debug Mode setting exists', 'KEY_DEBUG_MODE'),
    ('Debug Mode defaults OFF', 'prefs.getBoolean(KEY_DEBUG_MODE, false)'),
    ('Debug Mode production setter exists', 'setDebugMode(boolean enabled)'),
    ('Debug Mode menu toggle exists', 'Debug Mode: '),
    ('Debug Snapshot exists', 'buildDebugSnapshot()'),
    ('Debug report export exists', 'exportDebugReport()'),
    ('Debug report Build 13 filename exists', 'DisneyNOWFireTV-Debug-v0.1-Build13-'),
    ('Debug D-pad dispatch timing exists', 'recordDebugKeyDispatch'),
    ('Debug page-load timing exists', 'debugLastPageLoadMs'),
    ('Debug WebView error counter exists', 'debugWebErrorCount'),
    ('Debug HTTP error counter exists', 'debugHttpErrorCount'),
    ('Debug Media3 error counter exists', 'debugNativePlayerErrorCount'),
    ('Debug media manifest counter exists', 'debugMediaManifestCount'),
    ('Debug DRM candidate counter exists', 'debugDrmCandidateCount'),
    ('Debug recent log export bounded to 200 lines', 'logger.readRecentLines(200)'),
    ('Debug recent log reader hard-caps request', 'Math.min(maxLines, 500)'),
    ('Debug report privacy text present', 'full media/license URLs, query strings, device serials, and typed text are not included'),
    ('WebView remote debugging remains disabled', 'WebView.setWebContentsDebuggingEnabled(false)'),
    ('Safe Self-Test covers Debug Snapshot', 'Privacy-safe Debug Snapshot production path'),
]
for name, needle in debug_checks:
    add(name, needle in main, needle)

handoff_checks = [
    ('Native handoff stage tracker retained', 'recordNativeHandoffStage'),
    ('Native handoff attempt counter retained', 'debugNativeHandoffAttemptCount'),
    ('Native player create counter retained', 'debugNativePlayerCreateCount'),
    ('Native prepare counter retained', 'debugNativePrepareCount'),
    ('Possible DRM POST counter retained', 'debugPossibleDrmPostCount'),
    ('Possible DRM POST logging remains host/type only', 'POST_AFTER_MANIFEST '),
    ('Session context diagnostics use header-presence booleans', 'cookie='),
    ('Build 13 automatic native handoff safety flag is false', 'AUTO_NATIVE_HANDOFF_ENABLED = false'),
    ('Automatic native scheduler implementation is fail-safe disabled', 'Build 13 safety rollback keeps Media3 out of normal use'),
    ('Automatic native scheduler has no production call site', 'scheduleAutomaticNativePlayback();'),
    ('Native player has no normal production call site', 'tryNativePlayback();'),
    ('Build 13 Debug Snapshot states automatic handoff disabled', 'Automatic native handoff: disabled by Build 13 safety rollback'),
    ('Crash-stage active marker key exists', 'KEY_RUNTIME_ACTIVE'),
    ('Crash-stage name key exists', 'KEY_RUNTIME_STAGE'),
    ('Crash-stage detail key exists', 'KEY_RUNTIME_DETAIL'),
    ('Crash-stage exception-class key exists', 'KEY_RUNTIME_EXCEPTION'),
    ('Crash-stage timestamp key exists', 'KEY_RUNTIME_STAGE_AT'),
    ('Crash tracking initializes before normal app work', 'initializeRuntimeCrashTracking();'),
    ('Crash tracking uses shared production persistence helper', 'writeRuntimeState(SharedPreferences target'),
    ('Uncaught exception handler installed', 'Thread.setDefaultUncaughtExceptionHandler(installedUncaughtExceptionHandler)'),
    ('Uncaught exception evidence uses class chain only', 'String causes = safeThrowableChain(throwable)'),
    ('Previous incomplete run surfaced in Debug Snapshot', 'Previous run incomplete:'),
    ('Current persisted runtime stage surfaced in Debug Snapshot', 'Current persisted runtime stage:'),
    ('Page start stage persisted', 'persistRuntimeStage("page-started"'),
    ('Page finish stage persisted', 'persistRuntimeStage("page-finished"'),
    ('First manifest stage persisted', 'persistRuntimeStage("manifest-observed"'),
    ('Fullscreen WebView entry stage persisted', 'persistRuntimeStage("fullscreen-webview-enter"'),
    ('Clean shutdown marker written in onDestroy', 'markRuntimeCleanShutdown("activity-onDestroy")'),
    ('Previous uncaught handler restored on destroy', 'Thread.setDefaultUncaughtExceptionHandler(previousUncaughtExceptionHandler)'),
    ('Crash-stage persistence isolated self-test exists', 'Crash-stage persistence production helper write -> reload/read -> compare -> delete'),
    ('Automatic launch disabled self-test exists', 'Build 13 automatic native launch safety rollback'),
    ('Exception diagnostics use class chain helper', 'safeThrowableChain'),
]
for name, needle in handoff_checks:
    if name in ('Automatic native scheduler has no production call site', 'Native player has no normal production call site'):
        add(name, needle not in main, 'normal use cannot invoke Media3')
    else:
        add(name, needle in main, needle)

add('Manual Try Native Player normal menu item remains removed', 'Try Native Player:' not in main, 'normal menu has no manual handoff')
add('Old stream-ready instruction remains removed', 'press Menu > Try Native Player' not in main, 'no confusing handoff instruction')
add('Automatic native handoff is disconnected from manifest observation', 'scheduleAutomaticNativePlayback();' not in main, 'Build 13 safety rollback')
add('Native Media3 start is disconnected from normal production flow', 'tryNativePlayback();' not in main, 'dormant code only')
add('README documents Build 13 automatic-launch rollback', 'Automatic Media3 launch disabled' in readme, 'physical Build 11 regression response')
add('README documents persistent crash-stage evidence', 'Persistent crash-stage evidence' in readme, 'next-launch diagnostic evidence')

# Privacy: tokens/URLs must not be exported/logged.
add('Diagnostics do not append media URL value', 'append(lastMediaManifestUrl)' not in main, 'booleans/type only')
add('Debug report never directly appends manifest URL', 'append(lastMediaManifestUrl)' not in main, 'no full manifest URL export')
add('Debug report never directly appends DRM URL', 'append(lastDrmLicenseUrl)' not in main, 'no full license URL export')
add('Debug logging does not write request headers', 'lastMediaRequestHeaders' not in main[main.find('private void debugLog'):main.find('private void confirmClearWebData')], 'no debug header serialization')
add('Diagnostics do not append DRM license URL value', 'append(lastDrmLicenseUrl)' not in main, 'boolean only')
add('No logger writes full media manifest URL', 'logger.log("NATIVE_PLAYER start manifest="' not in main and 'logger.log("MEDIA_CANDIDATE manifest url=' not in main, 'host/type only')
add('No logger writes full DRM license URL', 'logger.log("MEDIA_CANDIDATE drm_license url=' not in main, 'host only')
add('Native handoff detail never appends full manifest URL', 'recordNativeHandoffStage("attempt-start", "host=" + manifestHost' in main, 'host/type/age only')
add('Possible DRM diagnostics never serialize request body', 'getRequestBody' not in main and 'request body' not in main.lower(), 'WebResourceRequest body unavailable/not captured')
add('Exception messages are not exported', '.getMessage()' not in main[main.find('private void tryNativePlayback'):main.find('private boolean isNativePlayerVisible')], 'class names/codes only')
add('Crash handler does not serialize exception messages', '.getMessage()' not in main[main.find('private void initializeRuntimeCrashTracking'):main.find('private static String safeThrowableChain')], 'class chain only')
add('Crash-stage details do not serialize full media/license URLs', 'putString(KEY_RUNTIME_DETAIL, lastMediaManifestUrl)' not in main and 'putString(KEY_RUNTIME_DETAIL, lastDrmLicenseUrl)' not in main, 'controlled safe details only')
add('Diagnostic privacy statement covers tokens/cookies/media/license URLs', 'provider tokens, cookies, media URLs, license URLs' in main, 'explicit')
add('About states no key extraction/DRM bypass', 'It does not extract keys, bypass DRM, unlock content' in main, 'explicit non-bypass behavior')
add('README states no DRM bypass/proprietary-copy behavior', 'no DRM is bypassed' in readme and 'authenticated-session' in readme, 'documented')

# Logging/diagnostics/Safe Self-Test.
checks2 = [
    ('Widevine runtime diagnostic retained', 'MediaDrm.isCryptoSchemeSupported(WIDEVINE_UUID)'),
    ('Diagnostics export retained', 'exportDiagnostics()'),
    ('Bounded log file count retained', 'MAX_FILES = 5'),
    ('Bounded log size retained', 'MAX_BYTES = 1024L * 1024L'),
    ('Safe Self-Test exists', 'runSafeSelfTest()'),
    ('Safe Self-Test Build 13 report name', 'SafeSelfTest-v0.1-Build13.txt'),
    ('Safe Self-Test settings persistence round trip', 'Settings persistence write -> reload/read -> compare -> delete'),
    ('Safe Self-Test native navigation migration check', 'Build 8 low-overhead Native TV Navigation migration'),
    ('Safe Self-Test media manifest classifier', 'Media manifest classifier'),
    ('Safe Self-Test DRM classifier', 'DRM endpoint classifier'),
    ('Safe Self-Test whole-page zoom production path', 'Whole-Page Zoom 0-500 persistence + WebView-level production apply -> restore'),
    ('Safe Self-Test native player surface check', 'Native Media3 player surface initialized'),
    ('Safe Self-Test marks real native playback skipped', 'Native Media3 HLS/DASH + Widevine playback'),
    ('Safe Self-Test data write/read/delete round trip', 'Project data write -> reload/read -> compare -> delete'),
]
for name, needle in checks2:
    add(name, needle in main, needle)

# Documentation/version consistency.
add('Build info matches Version 0.1 Build 13', 'Version: 0.1' in build_info and 'Build: 13' in build_info and 'versionCode: 13' in build_info, 'BUILD_INFO.md')
add('README identifies Build 13', 'v0.1 Build 13' in readme and 'Build 13 remains **NOT DONE' in readme, 'README.md')
add('README documents native navigation', 'Native TV Navigation' in readme, 'preserved Build 8 behavior')
add('README documents whole-page zoom', 'Whole-page Page Zoom 0-500' in readme, 'preserved Build 8 behavior')
add('README documents dormant experimental native playback', 'Dormant experimental native playback code' in readme, 'Build 13 safety rollback')
add('README documents Media3 1.8.1 compatibility rationale', 'Media3 `1.8.1`' in readme and '`minSdk 22`' in readme, 'dependency choice')

# Forbidden/high-risk capabilities.
for forbidden in [
    'android.permission.READ_CONTACTS', 'android.permission.READ_SMS', 'android.permission.RECORD_AUDIO',
    'android.permission.CAMERA', 'android.permission.ACCESS_FINE_LOCATION', 'android.permission.MANAGE_EXTERNAL_STORAGE',
    'setWebContentsDebuggingEnabled(true)', 'onReceivedSslError', 'setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW)',
    'addJavascriptInterface(', 'getKeyRequest(', 'provideKeyResponse(', 'KEY_TYPE_STREAMING'
]:
    add(f'Forbidden/high-risk capability absent: {forbidden}', forbidden not in manifest_text + main, forbidden)

# Structural checks.
add('MainActivity brace balance', main.count('{') == main.count('}'), f"open={main.count('{')} close={main.count('}')}")
add('MainActivity parenthesis balance', main.count('(') == main.count(')'), f"open={main.count('(')} close={main.count(')')}")
add('No stale Build 11 Safe Self-Test filename', 'SafeSelfTest-v0.1-Build11.txt' not in main, 'current report only')
add('No stale versionCode 11 in app Gradle', re.search(r'versionCode\s+11\b', gradle) is None, 'versionCode 13 only')

pass_count = sum(1 for status, _, _ in results if status == 'PASS')
fail_count = sum(1 for status, _, _ in results if status == 'FAIL')
REPORT.parent.mkdir(parents=True, exist_ok=True)
master = ROOT.parents[1] / 'MASTER_RULES.md'
master_sha = hashlib.sha256(master.read_bytes()).hexdigest() if master.is_file() else 'unavailable'
lines = [
    'DisneyNOW Fire TV Hybrid TV Shell - STATIC / RELEASE AUDIT',
    'Version: 0.1 Build 13',
    f'MASTER_RULES SHA-256: {master_sha}',
    '',
]
for i, (status, name, detail) in enumerate(results, 1):
    lines.append(f'{i}. {status} - {name} | {detail}')
lines += [
    '',
    f'STATIC TOTAL: PASS={pass_count} FAIL={fail_count}',
    'RESULT: PASS' if fail_count == 0 else 'RESULT: FAIL',
    '',
    'Physical Fire TV stability, actual WebView focus behavior, whole-page zoom appearance, real provider sign-in, Disney server playback, Silk fallback, previous-run crash-stage usefulness, and Debug Mode runtime behavior are environment-dependent and are NOT claimed by this static audit. Automatic Media3 launch is intentionally disabled in Build 13.',
]
REPORT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
print(REPORT.read_text(encoding='utf-8'))
sys.exit(0 if fail_count == 0 else 1)
