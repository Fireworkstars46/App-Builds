package com.fireworkstars46.disneynowfiretv;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.ActivityNotFoundException;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageInfo;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.media.MediaDrm;
import android.media.UnsupportedSchemeException;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Message;
import android.os.SystemClock;
import android.text.InputType;
import android.view.KeyEvent;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.view.WindowManager;
import android.webkit.CookieManager;
import android.webkit.GeolocationPermissions;
import android.webkit.PermissionRequest;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebStorage;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebViewDatabase;
import android.widget.Button;
import android.widget.EditText;
import android.widget.FrameLayout;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.SeekBar;
import android.widget.TextView;
import android.widget.Toast;

import androidx.media3.common.C;
import androidx.media3.common.MediaItem;
import androidx.media3.common.MimeTypes;
import androidx.media3.common.PlaybackException;
import androidx.media3.common.Player;
import androidx.media3.common.util.UnstableApi;
import androidx.media3.datasource.DefaultHttpDataSource;
import androidx.media3.exoplayer.ExoPlayer;
import androidx.media3.exoplayer.source.DefaultMediaSourceFactory;
import androidx.media3.ui.PlayerView;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Locale;
import java.util.UUID;

@UnstableApi
public final class MainActivity extends Activity {
    private static final String HOME_URL = "https://disneynow.com/";
    private static final String SILK_PACKAGE = "com.amazon.cloud9";
    private static final String EXPECTED_PACKAGE_ID = "com.fireworkstars46.disneynowfiretv";
    private static final String PREFS_NAME = "settings";
    private static final String KEY_UA_PROFILE = "ua_profile";
    private static final String KEY_TV_FOCUS = "tv_focus_navigation";
    private static final String KEY_CURSOR_ENABLED = "cursor_enabled";
    private static final String KEY_NATIVE_TV_NAV = "native_tv_navigation";
    private static final String KEY_PERFORMANCE_MODE = "performance_mode";
    private static final String KEY_DEBUG_MODE = "debug_mode";
    private static final String KEY_PAGE_ZOOM = "page_zoom_percent";
    private static final String KEY_BUILD2_MIGRATED = "build2_navigation_migrated";
    private static final String KEY_BUILD8_MIGRATED = "build8_native_shell_migrated";
    private static final String KEY_FIRST_RUN_SHOWN = "first_run_shown";
    private static final String KEY_RUNTIME_ACTIVE = "build12_runtime_active";
    private static final String KEY_RUNTIME_STAGE = "build12_runtime_stage";
    private static final String KEY_RUNTIME_DETAIL = "build12_runtime_detail";
    private static final String KEY_RUNTIME_EXCEPTION = "build12_runtime_exception";
    private static final String KEY_RUNTIME_STAGE_AT = "build12_runtime_stage_at_ms";

    private static final int DEFAULT_PAGE_ZOOM = 75;
    private static final int MIN_PAGE_ZOOM = 0;
    private static final int MAX_PAGE_ZOOM = 500;

    private static final String UA_ANDROID = "android";
    private static final String UA_WEBVIEW = "webview";
    private static final String UA_DESKTOP = "desktop";

    private static final UUID WIDEVINE_UUID = new UUID(
            0xedef8ba979d64aceL,
            0xa3c827dcd51d21edL
    );

    private FrameLayout root;
    private WebView webView;
    private CursorView cursorView;
    private float cursorX;
    private float cursorY;
    private boolean cursorPositionInitialized;
    private static final long CURSOR_ACCELERATION_DELAY_MS = 220L;
    private static final long CURSOR_ACCELERATION_RAMP_MS = 1100L;
    private static final float CURSOR_TAP_NUDGE_PIXELS = 2f;
    private static final float CURSOR_START_PIXELS_PER_SECOND = 180f;
    private static final float CURSOR_MAX_PIXELS_PER_SECOND = 720f;
    private static final boolean AUTO_NATIVE_HANDOFF_ENABLED = false;
    private static final long AUTO_NATIVE_FALLBACK_TIMEOUT_MS = 20000L;
    private boolean cursorLeftHeld, cursorRightHeld, cursorUpHeld, cursorDownHeld, cursorMovementFrameScheduled;
    private long cursorMovementStartedAt;
    private long cursorLastFrameAt;
    private boolean videoFallbackHintShown;
    private FrameLayout customViewContainer;
    private FrameLayout nativePlayerContainer;
    private PlayerView nativePlayerView;
    private ExoPlayer nativePlayer;
    private volatile String lastMediaManifestUrl;
    private volatile Map<String, String> lastMediaRequestHeaders = Collections.emptyMap();
    private volatile long lastMediaCapturedAt;
    private volatile String lastDrmLicenseUrl;
    private volatile Map<String, String> lastDrmRequestHeaders = Collections.emptyMap();
    private volatile long lastDrmCapturedAt;
    private int appliedWholePageZoomPercent = 100;
    private long debugPageStartedAt;
    private long debugLastPageLoadMs;
    private long debugKeyEventCount;
    private long debugKeyDispatchTotalNanos;
    private long debugKeyDispatchMaxNanos;
    private int debugWebErrorCount;
    private int debugHttpErrorCount;
    private int debugNativePlayerErrorCount;
    private int debugMediaManifestCount;
    private int debugDrmCandidateCount;
    private int debugNativeHandoffReadyCount;
    private int debugNativeHandoffAttemptCount;
    private int debugNativePlayerCreateCount;
    private int debugNativePrepareCount;
    private int debugPossibleDrmPostCount;
    private String debugLastWebError = "none";
    private String debugLastHttpError = "none";
    private String debugLastNativePlayerError = "none";
    private String debugLastNativeHandoffStage = "idle";
    private String debugLastNativeHandoffDetail = "none";
    private String debugLastPossibleDrmPost = "none";
    private boolean nativeReadyHintShown;
    private volatile int autoNativeScheduleToken;
    private volatile boolean autoNativeAttemptScheduled;
    private volatile boolean autoNativeAttemptedForPage;
    private int nativePlaybackAttemptToken;
    private boolean nativePlaybackStarted;
    private View customView;
    private WebChromeClient.CustomViewCallback customViewCallback;
    private SharedPreferences prefs;
    private AppLogger logger;
    private boolean previousRunIncomplete;
    private String previousRunStage = "none";
    private String previousRunDetail = "none";
    private String previousRunException = "none";
    private long previousRunStageAt;
    private String currentRuntimeStage = "uninitialized";
    private String currentRuntimeDetail = "none";
    private long currentRuntimeStageAt;
    private boolean runtimeManifestStagePersisted;
    private Thread.UncaughtExceptionHandler previousUncaughtExceptionHandler;
    private Thread.UncaughtExceptionHandler installedUncaughtExceptionHandler;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
        enterImmersiveMode();

        prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
        logger = new AppLogger(this);
        initializeRuntimeCrashTracking();
        migrateBuild2Settings();
        migrateBuild8Settings();
        logger.log("START version=" + versionLabel() + " sdk=" + Build.VERSION.SDK_INT);

        root = new FrameLayout(this);
        root.setBackgroundColor(Color.BLACK);

        webView = new WebView(this);
        webView.setBackgroundColor(Color.BLACK);
        webView.setFocusable(true);
        webView.setFocusableInTouchMode(true);
        root.addView(webView, new FrameLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT
        ));

        cursorView = new CursorView(this);
        cursorView.setVisibility(isCursorEnabled() ? View.VISIBLE : View.GONE);
        int cursorOverlaySize = dp(48);
        root.addView(cursorView, new FrameLayout.LayoutParams(cursorOverlaySize, cursorOverlaySize));

        customViewContainer = new FrameLayout(this);
        customViewContainer.setBackgroundColor(Color.TRANSPARENT);
        customViewContainer.setVisibility(View.GONE);
        root.addView(customViewContainer, new FrameLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT
        ));

        nativePlayerContainer = new FrameLayout(this);
        nativePlayerContainer.setBackgroundColor(Color.BLACK);
        nativePlayerContainer.setVisibility(View.GONE);
        nativePlayerView = new PlayerView(this);
        nativePlayerView.setUseController(true);
        nativePlayerView.setShowBuffering(PlayerView.SHOW_BUFFERING_WHEN_PLAYING);
        nativePlayerContainer.addView(nativePlayerView, new FrameLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT
        ));
        root.addView(nativePlayerContainer, new FrameLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT
        ));

        setContentView(root);
        configureWebView();
        webView.loadUrl(HOME_URL);
        webView.requestFocus();
        cursorView.post(this::resetCursorToCenter);

        if (!prefs.getBoolean(KEY_FIRST_RUN_SHOWN, false)) {
            boolean saved = prefs.edit().putBoolean(KEY_FIRST_RUN_SHOWN, true).commit();
            if (!saved) {
                logger.log("WARN first-run flag persistence failed");
            }
            logger.log("FIRST_RUN notice=Build13 native automatic launch disabled; crash-stage tracking enabled");
        }
    }

    private void configureWebView() {
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setMediaPlaybackRequiresUserGesture(false);
        settings.setAllowFileAccess(false);
        settings.setAllowContentAccess(false);
        settings.setBuiltInZoomControls(false);
        settings.setDisplayZoomControls(false);
        settings.setLoadWithOverviewMode(true);
        settings.setUseWideViewPort(true);
        settings.setSupportZoom(true);
        settings.setCacheMode(WebSettings.LOAD_DEFAULT);
        settings.setSupportMultipleWindows(true);
        settings.setJavaScriptCanOpenWindowsAutomatically(true);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        settings.setUserAgentString(resolveUserAgent(currentUaProfile()));
        webView.setInitialScale(100);
        webView.setOverScrollMode(View.OVER_SCROLL_NEVER);
        // Keep application/window hardware acceleration enabled, but do not force the WebView
        // into an offscreen hardware layer. Let WebView/SurfaceView choose the compositor path so
        // Fire TV ad/protected-video surfaces are less likely to render audio with a black picture.
        webView.setLayerType(View.LAYER_TYPE_NONE, null);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            webView.setRendererPriorityPolicy(WebView.RENDERER_PRIORITY_IMPORTANT, false);
        }

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            settings.setSafeBrowsingEnabled(true);
        }

        WebView.setWebContentsDebuggingEnabled(false);

        CookieManager cookies = CookieManager.getInstance();
        cookies.setAcceptCookie(true);
        cookies.setAcceptThirdPartyCookies(webView, true);

        webView.setWebViewClient(new DisneyWebViewClient());
        webView.setWebChromeClient(new DisneyWebChromeClient());
    }

    private final class DisneyWebViewClient extends WebViewClient {
        @Override
        public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
            return handleUri(request.getUrl());
        }

        @SuppressWarnings("deprecation")
        @Override
        public boolean shouldOverrideUrlLoading(WebView view, String url) {
            return handleUri(Uri.parse(url));
        }

        @SuppressWarnings("deprecation")
        @Override
        public void onReceivedError(WebView view, int errorCode, String description, String failingUrl) {
            if (isDebugModeEnabled()) {
                debugWebErrorCount++;
                debugLastWebError = "code=" + errorCode + " host=" + safeHost(failingUrl);
            }
            logger.log("WEB_ERROR code=" + errorCode + " host=" + safeHost(failingUrl));
            debugLog("WEB_ERROR_DETAIL code=" + errorCode + " host=" + safeHost(failingUrl));
            super.onReceivedError(view, errorCode, description, failingUrl);
        }

        @Override
        public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
            rememberMediaRequest(request);
            return super.shouldInterceptRequest(view, request);
        }

        @Override
        public void onReceivedHttpError(WebView view, WebResourceRequest request, WebResourceResponse errorResponse) {
            if (request.isForMainFrame()) {
                if (isDebugModeEnabled()) {
                    debugHttpErrorCount++;
                    debugLastHttpError = "status=" + errorResponse.getStatusCode() + " host=" + safeHost(request.getUrl());
                }
                logger.log("HTTP_ERROR status=" + errorResponse.getStatusCode() + " host=" + safeHost(request.getUrl()));
                debugLog("HTTP_ERROR_DETAIL status=" + errorResponse.getStatusCode() + " host=" + safeHost(request.getUrl()));
            }
            super.onReceivedHttpError(view, request, errorResponse);
        }

        @Override
        public void onPageStarted(WebView view, String url, android.graphics.Bitmap favicon) {
            super.onPageStarted(view, url, favicon);
            debugPageStartedAt = isDebugModeEnabled() ? SystemClock.uptimeMillis() : 0L;
            String host = safeHost(url);
            debugLog("PAGE_STARTED host=" + host);
            persistRuntimeStage("page-started", "host=" + host);
            clearMediaCandidates();
        }

        @Override
        public void onPageFinished(WebView view, String url) {
            super.onPageFinished(view, url);
            CookieManager.getInstance().flush();
            applyWholePageZoom();
            applyPerformanceModeToCurrentDocument();
            if (isDebugModeEnabled() && debugPageStartedAt > 0L) {
                debugLastPageLoadMs = Math.max(0L, SystemClock.uptimeMillis() - debugPageStartedAt);
            }
            String host = safeHost(url);
            logger.log("PAGE_FINISHED host=" + host);
            debugLog("PAGE_FINISHED_DETAIL host=" + host + " loadMs=" + debugLastPageLoadMs);
            persistRuntimeStage("page-finished", "host=" + host + " loadMs=" + debugLastPageLoadMs);
            if (prefs.getBoolean(KEY_TV_FOCUS, false) || isNativeTvNavigationEnabled()) {
                injectFocusHighlight();
            }
            view.requestFocus();
        }
    }

    private final class DisneyWebChromeClient extends WebChromeClient {
        @Override
        public void onShowCustomView(View view, CustomViewCallback callback) {
            if (customView != null) {
                callback.onCustomViewHidden();
                return;
            }
            customView = view;
            customViewCallback = callback;
            persistRuntimeStage("fullscreen-webview-enter", "custom video view shown");
            customViewContainer.removeAllViews();
            customViewContainer.addView(view, new FrameLayout.LayoutParams(
                    ViewGroup.LayoutParams.MATCH_PARENT,
                    ViewGroup.LayoutParams.MATCH_PARENT
            ));
            // Keep WebView attached but not drawing under the fullscreen media surface. This avoids
            // a full-page WebView composition pass competing with protected/ad video on Fire TV.
            webView.setVisibility(View.INVISIBLE);
            customViewContainer.setVisibility(View.VISIBLE);
            customViewContainer.bringToFront();
            view.requestFocus();
            stopAllCursorDirections();
            if (cursorView != null) {
                cursorView.setVisibility(View.GONE);
            }
            if (!videoFallbackHintShown) {
                videoFallbackHintShown = true;
                Toast.makeText(MainActivity.this, "If video is still black: Menu > Open Current Page in Silk.", Toast.LENGTH_LONG).show();
            }
            enterImmersiveMode();
            logger.log("FULLSCREEN enter compositor=webview_invisible");
        }

        @Override
        public void onHideCustomView() {
            hideCustomView();
        }

        @Override
        public boolean onCreateWindow(WebView view, boolean isDialog, boolean isUserGesture, Message resultMsg) {
            final WebView popup = new WebView(MainActivity.this);
            WebSettings popupSettings = popup.getSettings();
            popupSettings.setJavaScriptEnabled(true);
            popupSettings.setDomStorageEnabled(true);
            popupSettings.setMediaPlaybackRequiresUserGesture(false);
            popupSettings.setAllowFileAccess(false);
            popupSettings.setAllowContentAccess(false);
            popupSettings.setSupportMultipleWindows(true);
            popupSettings.setJavaScriptCanOpenWindowsAutomatically(true);
            popupSettings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
            popupSettings.setUserAgentString(resolveUserAgent(currentUaProfile()));
            CookieManager popupCookies = CookieManager.getInstance();
            popupCookies.setAcceptCookie(true);
            popupCookies.setAcceptThirdPartyCookies(popup, true);
            final boolean[] routed = new boolean[]{false};
            popup.setWebViewClient(new WebViewClient() {
                private boolean routeOnce(WebView child, Uri uri) {
                    if (uri == null) return false;
                    if (!isHttpOrHttps(uri)) return handleUri(uri);
                    if (routed[0]) return true;
                    routed[0] = true;
                    CookieManager.getInstance().flush();
                    webView.loadUrl(uri.toString());
                    child.post(() -> {
                        child.stopLoading();
                        child.setWebViewClient(null);
                        child.destroy();
                    });
                    return true;
                }

                @Override
                public boolean shouldOverrideUrlLoading(WebView child, WebResourceRequest request) {
                    return routeOnce(child, request == null ? null : request.getUrl());
                }

                @SuppressWarnings("deprecation")
                @Override
                public boolean shouldOverrideUrlLoading(WebView child, String url) {
                    return routeOnce(child, url == null ? null : Uri.parse(url));
                }

                @Override
                public void onPageStarted(WebView child, String url, android.graphics.Bitmap favicon) {
                    super.onPageStarted(child, url, favicon);
                    if (!routed[0] && url != null) routeOnce(child, Uri.parse(url));
                }
            });
            WebView.WebViewTransport transport = (WebView.WebViewTransport) resultMsg.obj;
            transport.setWebView(popup);
            resultMsg.sendToTarget();
            return true;
        }

        @Override
        public void onPermissionRequest(PermissionRequest request) {
            logger.log("WEB_PERMISSION denied resources=" + request.getResources().length);
            request.deny();
        }

        @Override
        public void onGeolocationPermissionsShowPrompt(String origin, GeolocationPermissions.Callback callback) {
            logger.log("GEOLOCATION denied host=" + safeHost(origin));
            callback.invoke(origin, false, false);
        }
    }

    private void clearMediaCandidates() {
        lastMediaManifestUrl = null;
        lastMediaRequestHeaders = Collections.emptyMap();
        lastMediaCapturedAt = 0L;
        lastDrmLicenseUrl = null;
        lastDrmRequestHeaders = Collections.emptyMap();
        lastDrmCapturedAt = 0L;
        nativeReadyHintShown = false;
        autoNativeScheduleToken++;
        autoNativeAttemptScheduled = false;
        autoNativeAttemptedForPage = false;
        runtimeManifestStagePersisted = false;
        recordNativeHandoffStage("waiting-for-manifest", "media candidates cleared; automatic native launch disabled in Build 13");
    }

    private void rememberMediaRequest(WebResourceRequest request) {
        if (request == null || request.getUrl() == null || !isHttpOrHttps(request.getUrl())) return;
        String url = request.getUrl().toString();
        String method = safeText(request.getMethod());
        long now = SystemClock.uptimeMillis();
        if (isMediaManifestUrl(url)) {
            lastMediaManifestUrl = url;
            lastMediaRequestHeaders = copyPortableRequestHeaders(request.getRequestHeaders());
            lastMediaCapturedAt = now;
            if (isDebugModeEnabled()) {
                debugMediaManifestCount++;
                debugNativeHandoffReadyCount++;
            }
            String host = safeHost(request.getUrl());
            String type = mediaManifestType(url);
            String detail = "manifest host=" + host + " type=" + type
                    + " capturedHeaders=" + lastMediaRequestHeaders.size()
                    + " referer=" + containsHeaderIgnoreCase(lastMediaRequestHeaders, "Referer")
                    + " origin=" + containsHeaderIgnoreCase(lastMediaRequestHeaders, "Origin")
                    + " cookieAvailable=" + hasSessionCookie(url);
            logger.log("MEDIA_CANDIDATE manifest host=" + host + " type=" + type);
            debugLog("MEDIA_CANDIDATE_DETAIL " + detail);
            recordNativeHandoffStage("manifest-ready", detail + " automaticLaunch=false");
            nativeReadyHintShown = true;
            if (!runtimeManifestStagePersisted) {
                runtimeManifestStagePersisted = true;
                persistRuntimeStage("manifest-observed", "host=" + host + " type=" + type + " automaticLaunch=false");
            }
        }

        boolean nonGetSubresourceNearMedia = !request.isForMainFrame()
                && !"GET".equalsIgnoreCase(method)
                && lastMediaCapturedAt > 0L
                && now - lastMediaCapturedAt >= 0L
                && now - lastMediaCapturedAt <= 120000L;
        if (nonGetSubresourceNearMedia && isDebugModeEnabled()) {
            debugPossibleDrmPostCount++;
            debugLastPossibleDrmPost = "host=" + safeHost(request.getUrl())
                    + " method=" + method
                    + " contentType=" + safeContentTypeCategory(request.getRequestHeaders());
            debugLog("POST_AFTER_MANIFEST " + debugLastPossibleDrmPost);
        }

        if (isLikelyDrmLicenseRequest(url, method)) {
            lastDrmLicenseUrl = url;
            lastDrmRequestHeaders = copyPortableRequestHeaders(request.getRequestHeaders());
            lastDrmCapturedAt = now;
            if (isDebugModeEnabled()) debugDrmCandidateCount++;
            logger.log("MEDIA_CANDIDATE drm_license host=" + safeHost(request.getUrl()));
            debugLog("MEDIA_CANDIDATE_DETAIL drm_license host=" + safeHost(request.getUrl())
                    + " capturedHeaders=" + lastDrmRequestHeaders.size()
                    + " contentType=" + safeContentTypeCategory(request.getRequestHeaders()));
        }
    }

    private static boolean isMediaManifestUrl(String url) {
        if (url == null) return false;
        String lower = url.toLowerCase(Locale.US);
        int q = lower.indexOf('?');
        if (q >= 0) lower = lower.substring(0, q);
        return lower.endsWith(".m3u8") || lower.endsWith(".mpd");
    }

    private static String mediaManifestType(String url) {
        if (url == null) return "unknown";
        String lower = url.toLowerCase(Locale.US);
        return lower.contains(".m3u8") ? "hls" : (lower.contains(".mpd") ? "dash" : "unknown");
    }

    private static boolean isLikelyDrmLicenseRequest(String url, String method) {
        if (url == null) return false;
        String lower = url.toLowerCase(Locale.US);
        boolean marker = lower.contains("widevine") || lower.contains("license") || lower.contains("drm");
        return marker && (method == null || !"GET".equalsIgnoreCase(method));
    }

    private static Map<String, String> copyPortableRequestHeaders(Map<String, String> headers) {
        if (headers == null || headers.isEmpty()) return Collections.emptyMap();
        Map<String, String> out = new HashMap<>();
        for (Map.Entry<String, String> entry : headers.entrySet()) {
            if (entry.getKey() == null || entry.getValue() == null) continue;
            String key = entry.getKey();
            if ("host".equalsIgnoreCase(key)
                    || "content-length".equalsIgnoreCase(key)
                    || "connection".equalsIgnoreCase(key)
                    || "accept-encoding".equalsIgnoreCase(key)) continue;
            out.put(key, entry.getValue());
        }
        return Collections.unmodifiableMap(out);
    }

    private Map<String, String> requestHeadersWithSession(Map<String, String> captured, String url) {
        Map<String, String> out = new HashMap<>();
        if (captured != null) out.putAll(captured);
        if (!containsHeaderIgnoreCase(out, "User-Agent")) {
            out.put("User-Agent", webView.getSettings().getUserAgentString());
        }
        if (!containsHeaderIgnoreCase(out, "Cookie")) {
            String cookie = CookieManager.getInstance().getCookie(url);
            if (cookie != null && !cookie.trim().isEmpty()) out.put("Cookie", cookie);
        }
        return out;
    }

    private static boolean containsHeaderIgnoreCase(Map<String, String> headers, String wanted) {
        if (headers == null) return false;
        for (String key : headers.keySet()) if (wanted.equalsIgnoreCase(key)) return true;
        return false;
    }

    private static String headerValueIgnoreCase(Map<String, String> headers, String wanted) {
        if (headers == null) return null;
        for (Map.Entry<String, String> entry : headers.entrySet()) {
            if (wanted.equalsIgnoreCase(entry.getKey())) return entry.getValue();
        }
        return null;
    }

    private static String safeContentTypeCategory(Map<String, String> headers) {
        String value = headerValueIgnoreCase(headers, "Content-Type");
        if (value == null || value.trim().isEmpty()) return "none";
        String lower = value.toLowerCase(Locale.US);
        if (lower.contains("protobuf") || lower.contains("octet-stream")) return "binary";
        if (lower.contains("json")) return "json";
        if (lower.contains("form")) return "form";
        if (lower.contains("xml")) return "xml";
        if (lower.contains("text")) return "text";
        return "other";
    }

    private boolean hasSessionCookie(String url) {
        if (url == null) return false;
        try {
            String cookie = CookieManager.getInstance().getCookie(url);
            return cookie != null && !cookie.trim().isEmpty();
        } catch (RuntimeException ex) {
            return false;
        }
    }

    private static long ageMs(long capturedAt) {
        if (capturedAt <= 0L) return -1L;
        return Math.max(0L, SystemClock.uptimeMillis() - capturedAt);
    }

    private void recordNativeHandoffStage(String stage, String detail) {
        String safeStage = safeText(stage);
        String safeDetail = safeText(detail);
        debugLastNativeHandoffStage = safeStage;
        debugLastNativeHandoffDetail = safeDetail;
        debugLog("NATIVE_HANDOFF stage=" + safeStage + " detail=" + safeDetail);
    }

    private boolean writeRuntimeState(SharedPreferences target, boolean active, String stage, String detail, String exceptionClassChain, long atMs) {
        if (target == null) return false;
        return target.edit()
                .putBoolean(KEY_RUNTIME_ACTIVE, active)
                .putString(KEY_RUNTIME_STAGE, safeText(stage))
                .putString(KEY_RUNTIME_DETAIL, safeText(detail))
                .putString(KEY_RUNTIME_EXCEPTION, safeText(exceptionClassChain))
                .putLong(KEY_RUNTIME_STAGE_AT, Math.max(0L, atMs))
                .commit();
    }

    private void initializeRuntimeCrashTracking() {
        previousRunIncomplete = prefs.getBoolean(KEY_RUNTIME_ACTIVE, false);
        previousRunStage = safeText(prefs.getString(KEY_RUNTIME_STAGE, "none"));
        previousRunDetail = safeText(prefs.getString(KEY_RUNTIME_DETAIL, "none"));
        previousRunException = safeText(prefs.getString(KEY_RUNTIME_EXCEPTION, "none"));
        previousRunStageAt = prefs.getLong(KEY_RUNTIME_STAGE_AT, 0L);
        if (previousRunIncomplete) {
            logger.log("PREVIOUS_RUN incomplete stage=" + previousRunStage
                    + " exception=" + previousRunException);
        }
        persistRuntimeStage("startup", "Build 13 startup; automatic native launch disabled");

        previousUncaughtExceptionHandler = Thread.getDefaultUncaughtExceptionHandler();
        installedUncaughtExceptionHandler = (thread, throwable) -> {
            String causes = safeThrowableChain(throwable);
            try {
                long now = System.currentTimeMillis();
                currentRuntimeStage = "uncaught-exception";
                currentRuntimeDetail = "causes=" + causes;
                currentRuntimeStageAt = now;
                writeRuntimeState(prefs, true, currentRuntimeStage, currentRuntimeDetail, causes, now);
                logger.log("UNCAUGHT_EXCEPTION causes=" + causes);
            } catch (Throwable ignored) {
                // Crash evidence must never replace the platform's normal crash handling.
            }
            Thread.UncaughtExceptionHandler previous = previousUncaughtExceptionHandler;
            if (previous != null) {
                previous.uncaughtException(thread, throwable);
            } else {
                android.os.Process.killProcess(android.os.Process.myPid());
                System.exit(10);
            }
        };
        Thread.setDefaultUncaughtExceptionHandler(installedUncaughtExceptionHandler);
    }

    private void persistRuntimeStage(String stage, String detail) {
        currentRuntimeStage = safeText(stage);
        currentRuntimeDetail = safeText(detail);
        currentRuntimeStageAt = System.currentTimeMillis();
        boolean saved = writeRuntimeState(prefs, true, currentRuntimeStage, currentRuntimeDetail, "none", currentRuntimeStageAt);
        if (!saved && logger != null) logger.log("WARN runtime stage persistence failed stage=" + currentRuntimeStage);
    }

    private void markRuntimeCleanShutdown(String reason) {
        String safeReason = safeText(reason);
        currentRuntimeStage = "clean-stop";
        currentRuntimeDetail = safeReason;
        currentRuntimeStageAt = System.currentTimeMillis();
        boolean saved = writeRuntimeState(prefs, false, currentRuntimeStage, currentRuntimeDetail, "none", currentRuntimeStageAt);
        if (!saved && logger != null) logger.log("WARN clean shutdown marker persistence failed");
    }

    private static String safeThrowableChain(Throwable throwable) {
        if (throwable == null) return "none";
        StringBuilder out = new StringBuilder();
        Throwable current = throwable;
        int depth = 0;
        while (current != null && depth < 4) {
            if (depth > 0) out.append("->");
            out.append(current.getClass().getSimpleName());
            current = current.getCause();
            depth++;
        }
        return out.toString();
    }

    private void scheduleAutomaticNativePlayback() {
        autoNativeAttemptScheduled = false;
        recordNativeHandoffStage("auto-disabled", "Build 13 safety rollback keeps Media3 out of normal use");
        debugLog("AUTO_NATIVE_HANDOFF disabled");
    }

    private void scheduleNativeFallbackWatchdog(final int attemptToken) {
        if (nativePlayerContainer == null) return;
        nativePlayerContainer.postDelayed(() -> {
            if (attemptToken != nativePlaybackAttemptToken || !isNativePlayerVisible()) return;
            ExoPlayer player = nativePlayer;
            if (player == null || player.isPlaying()) return;
            recordNativeHandoffStage("auto-timeout", "native player did not start within " + AUTO_NATIVE_FALLBACK_TIMEOUT_MS + "ms");
            fallbackToWebPlayback("startup-timeout");
        }, AUTO_NATIVE_FALLBACK_TIMEOUT_MS);
    }

    private void fallbackToWebPlayback(String reason) {
        String safeReason = safeText(reason);
        recordNativeHandoffStage("auto-fallback", safeReason);
        logger.log("NATIVE_PLAYER auto_fallback reason=" + safeReason);
        stopNativePlayback();
        if (isDebugModeEnabled()) {
            Toast.makeText(this, "Native playback did not start; returned to the normal DisneyNOW player.", Toast.LENGTH_SHORT).show();
        }
    }

    private void tryNativePlayback() {
        if (isDebugModeEnabled()) debugNativeHandoffAttemptCount++;
        final String manifest = lastMediaManifestUrl;
        if (manifest == null || !isMediaManifestUrl(manifest)) {
            recordNativeHandoffStage("blocked-no-manifest", "automatic handoff had no HLS/DASH candidate");
            logger.log("NATIVE_PLAYER no_manifest_candidate");
            return;
        }
        String manifestHost = safeHost(manifest);
        String manifestType = mediaManifestType(manifest);
        long manifestAge = ageMs(lastMediaCapturedAt);
        recordNativeHandoffStage("attempt-start", "host=" + manifestHost + " type=" + manifestType + " ageMs=" + manifestAge);
        if (customView != null) hideCustomView();
        releaseNativePlayer();
        nativePlaybackStarted = false;
        final int playbackAttemptToken = ++nativePlaybackAttemptToken;
        try {
            Map<String, String> mediaHeaders = requestHeadersWithSession(lastMediaRequestHeaders, manifest);
            recordNativeHandoffStage("session-context",
                    "headers=" + mediaHeaders.size()
                            + " cookie=" + containsHeaderIgnoreCase(mediaHeaders, "Cookie")
                            + " referer=" + containsHeaderIgnoreCase(mediaHeaders, "Referer")
                            + " origin=" + containsHeaderIgnoreCase(mediaHeaders, "Origin"));
            DefaultHttpDataSource.Factory httpFactory = new DefaultHttpDataSource.Factory()
                    .setAllowCrossProtocolRedirects(true)
                    .setUserAgent(webView.getSettings().getUserAgentString())
                    .setDefaultRequestProperties(mediaHeaders);
            DefaultMediaSourceFactory mediaSourceFactory = new DefaultMediaSourceFactory(httpFactory);
            nativePlayer = new ExoPlayer.Builder(this)
                    .setMediaSourceFactory(mediaSourceFactory)
                    .build();
            if (isDebugModeEnabled()) debugNativePlayerCreateCount++;
            recordNativeHandoffStage("player-created", "Media3 ExoPlayer created");
            nativePlayer.addListener(new Player.Listener() {
                @Override
                public void onPlaybackStateChanged(int playbackState) {
                    String state = playbackStateLabel(playbackState);
                    debugLog("NATIVE_PLAYER state=" + state);
                    recordNativeHandoffStage("player-state", state);
                }

                @Override
                public void onIsPlayingChanged(boolean isPlaying) {
                    debugLog("NATIVE_PLAYER isPlaying=" + isPlaying);
                    if (isPlaying) {
                        nativePlaybackStarted = true;
                        recordNativeHandoffStage("playing", "Media3 reports isPlaying=true");
                    }
                }

                @Override
                public void onPlayerError(PlaybackException error) {
                    String causes = safeThrowableChain(error);
                    if (isDebugModeEnabled()) {
                        debugNativePlayerErrorCount++;
                        debugLastNativePlayerError = "code=" + error.errorCode + " type=" + error.getClass().getSimpleName() + " causes=" + causes;
                    }
                    logger.log("NATIVE_PLAYER error code=" + error.errorCode + " type=" + error.getClass().getSimpleName() + " causes=" + causes);
                    debugLog("NATIVE_PLAYER_DETAIL error code=" + error.errorCode + " type=" + error.getClass().getSimpleName() + " causes=" + causes);
                    recordNativeHandoffStage("player-error", "code=" + error.errorCode + " type=" + error.getClass().getSimpleName() + " causes=" + causes);
                    if (nativePlayerContainer != null) {
                        nativePlayerContainer.post(() -> fallbackToWebPlayback("player-error-" + error.errorCode));
                    }
                }
            });

            MediaItem.Builder item = new MediaItem.Builder().setUri(manifest);
            if ("hls".equals(manifestType)) item.setMimeType(MimeTypes.APPLICATION_M3U8);
            else if ("dash".equals(manifestType)) item.setMimeType(MimeTypes.APPLICATION_MPD);

            long drmAge = lastDrmCapturedAt == 0L ? Long.MAX_VALUE : Math.abs(lastDrmCapturedAt - lastMediaCapturedAt);
            boolean useDrm = lastDrmLicenseUrl != null && drmAge <= 120000L;
            if (useDrm) {
                Map<String, String> drmHeaders = requestHeadersWithSession(lastDrmRequestHeaders, lastDrmLicenseUrl);
                MediaItem.DrmConfiguration drm = new MediaItem.DrmConfiguration.Builder(C.WIDEVINE_UUID)
                        .setLicenseUri(lastDrmLicenseUrl)
                        .setLicenseRequestHeaders(drmHeaders)
                        .build();
                item.setDrmConfiguration(drm);
            }
            recordNativeHandoffStage("media-item-configured", "type=" + manifestType + " drmCandidate=" + useDrm + " drmAgeMs=" + (drmAge == Long.MAX_VALUE ? -1L : drmAge));

            nativePlayerView.setPlayer(nativePlayer);
            nativePlayerContainer.setVisibility(View.VISIBLE);
            nativePlayerContainer.bringToFront();
            webView.setVisibility(View.INVISIBLE);
            stopAllCursorDirections();
            cursorView.setVisibility(View.GONE);
            nativePlayer.setMediaItem(item.build());
            nativePlayer.prepare();
            if (isDebugModeEnabled()) debugNativePrepareCount++;
            recordNativeHandoffStage("prepare-called", "Media3 prepare invoked");
            nativePlayer.play();
            recordNativeHandoffStage("play-called", "Media3 play invoked");
            scheduleNativeFallbackWatchdog(playbackAttemptToken);
            nativePlayerView.requestFocus();
            logger.log("NATIVE_PLAYER start manifest_host=" + manifestHost
                    + " type=" + manifestType
                    + " drmCandidate=" + useDrm);
        } catch (RuntimeException ex) {
            String causes = safeThrowableChain(ex);
            logger.log("NATIVE_PLAYER setup_error type=" + ex.getClass().getSimpleName() + " causes=" + causes);
            recordNativeHandoffStage("setup-error", "type=" + ex.getClass().getSimpleName() + " causes=" + causes);
            fallbackToWebPlayback("setup-error-" + ex.getClass().getSimpleName());
        }
    }

    private boolean isNativePlayerVisible() {
        return nativePlayerContainer != null && nativePlayerContainer.getVisibility() == View.VISIBLE;
    }

    private void stopNativePlayback() {
        nativePlaybackAttemptToken++;
        nativePlaybackStarted = false;
        releaseNativePlayer();
        if (nativePlayerContainer != null) nativePlayerContainer.setVisibility(View.GONE);
        if (webView != null) webView.setVisibility(View.VISIBLE);
        if (cursorView != null) cursorView.setVisibility(isCursorEnabled() && customView == null ? View.VISIBLE : View.GONE);
        if (webView != null) webView.requestFocus();
        enterImmersiveMode();
        logger.log("NATIVE_PLAYER stop");
    }

    private void releaseNativePlayer() {
        if (nativePlayerView != null) nativePlayerView.setPlayer(null);
        if (nativePlayer != null) {
            nativePlayer.stop();
            nativePlayer.release();
            nativePlayer = null;
        }
    }

    private void openCurrentPageInSilk() {
        if (isNativePlayerVisible()) stopNativePlayback();
        String current = webView == null ? null : webView.getUrl();
        if (current == null || current.trim().isEmpty()) current = HOME_URL;
        Uri uri = Uri.parse(current);
        if (!isHttpOrHttps(uri)) uri = Uri.parse(HOME_URL);
        if (customView != null) hideCustomView();
        Intent silk = new Intent(Intent.ACTION_VIEW, uri);
        silk.setPackage(SILK_PACKAGE);
        try {
            startActivity(silk);
            logger.log("SILK_FALLBACK opened host=" + safeHost(uri));
            return;
        } catch (ActivityNotFoundException ex) {
            logger.log("SILK_FALLBACK package_unavailable");
        }
        try {
            startActivity(new Intent(Intent.ACTION_VIEW, uri));
            logger.log("BROWSER_FALLBACK opened host=" + safeHost(uri));
        } catch (ActivityNotFoundException ex) {
            logger.log("BROWSER_FALLBACK unavailable");
            Toast.makeText(this, "No browser is installed to open DisneyNOW.", Toast.LENGTH_LONG).show();
        }
    }

    private boolean handleUri(Uri uri) {
        if (uri == null) {
            return false;
        }
        if (isHttpOrHttps(uri)) {
            return false;
        }

        try {
            Intent intent = new Intent(Intent.ACTION_VIEW, uri);
            startActivity(intent);
            logger.log("EXTERNAL_SCHEME opened scheme=" + safeText(uri.getScheme()));
        } catch (ActivityNotFoundException ex) {
            logger.log("EXTERNAL_SCHEME unavailable scheme=" + safeText(uri.getScheme()));
            Toast.makeText(this, "No app is installed to open that link.", Toast.LENGTH_SHORT).show();
        }
        return true;
    }

    private static boolean isHttpOrHttps(Uri uri) {
        if (uri == null) {
            return false;
        }
        String scheme = uri.getScheme();
        return "http".equalsIgnoreCase(scheme) || "https".equalsIgnoreCase(scheme);
    }

    private void hideCustomView() {
        if (customView == null) {
            return;
        }
        customViewContainer.removeAllViews();
        customViewContainer.setVisibility(View.GONE);
        customView = null;
        webView.setVisibility(View.VISIBLE);
        if (cursorView != null) {
            cursorView.setVisibility(isCursorEnabled() ? View.VISIBLE : View.GONE);
        }
        if (customViewCallback != null) {
            customViewCallback.onCustomViewHidden();
            customViewCallback = null;
        }
        webView.requestFocus();
        enterImmersiveMode();
        logger.log("FULLSCREEN exit");
    }

    @Override
    public boolean dispatchKeyEvent(KeyEvent event) {
        final long debugStarted = isDebugModeEnabled() ? System.nanoTime() : 0L;
        boolean result;
        if (event != null) {
            int keyCode = event.getKeyCode();
            int action = event.getAction();

            if (keyCode == KeyEvent.KEYCODE_MENU) {
                if (action == KeyEvent.ACTION_DOWN && event.getRepeatCount() == 0) {
                    showAppMenu();
                }
                result = true;
                recordDebugKeyDispatch(debugStarted);
                return result;
            }

            if (isNativePlayerVisible()) {
                result = super.dispatchKeyEvent(event);
                recordDebugKeyDispatch(debugStarted);
                return result;
            }

            if (customView == null && isCursorEnabled() && isCursorNavigationKey(keyCode)) {
                if (isCursorDirectionKey(keyCode)) {
                    if (action == KeyEvent.ACTION_DOWN && event.getRepeatCount() == 0) startCursorDirection(keyCode);
                    else if (action == KeyEvent.ACTION_UP) stopCursorDirection(keyCode);
                } else if (action == KeyEvent.ACTION_DOWN && event.getRepeatCount() == 0) performCursorClick();
                // Consume both DOWN and UP before WebView; repeated DOWN is ignored because our frame loop moves smoothly.
                result = true;
                recordDebugKeyDispatch(debugStarted);
                return result;
            }
        }
        result = super.dispatchKeyEvent(event);
        recordDebugKeyDispatch(debugStarted);
        return result;
    }

    private static boolean isCursorDirectionKey(int keyCode) {
        return keyCode == KeyEvent.KEYCODE_DPAD_LEFT
                || keyCode == KeyEvent.KEYCODE_DPAD_RIGHT
                || keyCode == KeyEvent.KEYCODE_DPAD_UP
                || keyCode == KeyEvent.KEYCODE_DPAD_DOWN;
    }

    private static boolean isCursorNavigationKey(int keyCode) {
        return isCursorDirectionKey(keyCode)
                || keyCode == KeyEvent.KEYCODE_DPAD_CENTER
                || keyCode == KeyEvent.KEYCODE_ENTER
                || keyCode == KeyEvent.KEYCODE_NUMPAD_ENTER;
    }

    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_MENU) {
            showAppMenu();
            return true;
        }

        if (customView == null && isCursorEnabled()) {
            if (keyCode == KeyEvent.KEYCODE_DPAD_LEFT
                    || keyCode == KeyEvent.KEYCODE_DPAD_RIGHT
                    || keyCode == KeyEvent.KEYCODE_DPAD_UP
                    || keyCode == KeyEvent.KEYCODE_DPAD_DOWN) {
                moveCursor(keyCode, event == null ? 0 : event.getRepeatCount());
                return true;
            }
            if (keyCode == KeyEvent.KEYCODE_DPAD_CENTER || keyCode == KeyEvent.KEYCODE_ENTER || keyCode == KeyEvent.KEYCODE_NUMPAD_ENTER) {
                performCursorClick();
                return true;
            }
        }

        if (customView == null && prefs.getBoolean(KEY_TV_FOCUS, false)) {
            if (keyCode == KeyEvent.KEYCODE_DPAD_RIGHT || keyCode == KeyEvent.KEYCODE_DPAD_DOWN) {
                moveWebFocus(true);
                return true;
            }
            if (keyCode == KeyEvent.KEYCODE_DPAD_LEFT || keyCode == KeyEvent.KEYCODE_DPAD_UP) {
                moveWebFocus(false);
                return true;
            }
            if (keyCode == KeyEvent.KEYCODE_DPAD_CENTER || keyCode == KeyEvent.KEYCODE_ENTER || keyCode == KeyEvent.KEYCODE_NUMPAD_ENTER) {
                sendEnterToWebView();
                return true;
            }
        }

        return super.onKeyDown(keyCode, event);
    }

    private void startCursorDirection(int keyCode) {
        boolean wasMoving=anyCursorDirectionHeld(); setCursorDirectionHeld(keyCode,true);
        if(!wasMoving&&anyCursorDirectionHeld()){long now=SystemClock.uptimeMillis();cursorMovementStartedAt=now;cursorLastFrameAt=now;moveCursorByDirection(keyCode,CURSOR_TAP_NUDGE_PIXELS);}
        scheduleCursorMovementFrame();
    }
    private void stopCursorDirection(int keyCode){setCursorDirectionHeld(keyCode,false);if(!anyCursorDirectionHeld()){if(cursorView!=null)cursorView.removeCallbacks(cursorMovementFrame);cursorMovementFrameScheduled=false;}}
    private void stopAllCursorDirections(){cursorLeftHeld=cursorRightHeld=cursorUpHeld=cursorDownHeld=false;if(cursorView!=null)cursorView.removeCallbacks(cursorMovementFrame);cursorMovementFrameScheduled=false;}
    private void setCursorDirectionHeld(int k,boolean v){if(k==KeyEvent.KEYCODE_DPAD_LEFT)cursorLeftHeld=v;else if(k==KeyEvent.KEYCODE_DPAD_RIGHT)cursorRightHeld=v;else if(k==KeyEvent.KEYCODE_DPAD_UP)cursorUpHeld=v;else if(k==KeyEvent.KEYCODE_DPAD_DOWN)cursorDownHeld=v;}
    private boolean anyCursorDirectionHeld(){return cursorLeftHeld||cursorRightHeld||cursorUpHeld||cursorDownHeld;}
    private void scheduleCursorMovementFrame(){if(!cursorMovementFrameScheduled&&anyCursorDirectionHeld()&&cursorView!=null){cursorMovementFrameScheduled=true;cursorView.postOnAnimation(cursorMovementFrame);}}
    private final Runnable cursorMovementFrame=new Runnable(){@Override public void run(){
        cursorMovementFrameScheduled=false;if(!isCursorEnabled()||customView!=null||!anyCursorDirectionHeld()){stopAllCursorDirections();return;}
        long now=SystemClock.uptimeMillis();long held=Math.max(0L,now-cursorMovementStartedAt);float ramp=clamp((held-CURSOR_ACCELERATION_DELAY_MS)/(float)CURSOR_ACCELERATION_RAMP_MS,0f,1f);ramp*=ramp;
        float speed=CURSOR_START_PIXELS_PER_SECOND+(CURSOR_MAX_PIXELS_PER_SECOND-CURSOR_START_PIXELS_PER_SECOND)*ramp;
        float dt=clamp((now-cursorLastFrameAt)/1000f,0f,0.05f);cursorLastFrameAt=now;
        float dx=(cursorRightHeld?1f:0f)-(cursorLeftHeld?1f:0f),dy=(cursorDownHeld?1f:0f)-(cursorUpHeld?1f:0f);
        if(dx!=0f||dy!=0f){if(dx!=0f&&dy!=0f){dx*=0.70710677f;dy*=0.70710677f;}moveCursorBy(dx*speed*dt,dy*speed*dt);}scheduleCursorMovementFrame();}};
    private void moveCursor(int keyCode,int repeatCount){moveCursorByDirection(keyCode,CURSOR_TAP_NUDGE_PIXELS);}
    private void moveCursorByDirection(int k,float px){float dx=0f,dy=0f;if(k==KeyEvent.KEYCODE_DPAD_LEFT)dx=-px;else if(k==KeyEvent.KEYCODE_DPAD_RIGHT)dx=px;else if(k==KeyEvent.KEYCODE_DPAD_UP)dy=-px;else if(k==KeyEvent.KEYCODE_DPAD_DOWN)dy=px;moveCursorBy(dx,dy);}
    private void moveCursorBy(float dx,float dy){
        if(cursorView==null||webView==null)return;ensureCursorPosition();float radius=cursorView.cursorRadius(),minX=radius,minY=radius,maxX=Math.max(minX,webView.getWidth()-radius),maxY=Math.max(minY,webView.getHeight()-radius);
        float x=cursorX+dx,y=cursorY+dy;boolean top=y<minY,bottom=y>maxY;cursorX=clamp(x,minX,maxX);cursorY=clamp(y,minY,maxY);cursorView.setCursorPosition(cursorX,cursorY);
        if(top)webView.scrollBy(0,-dp(10));else if(bottom)webView.scrollBy(0,dp(10));
    }

    private void performCursorClick() {
        if (webView == null) {
            return;
        }
        ensureCursorPosition();
        long now = android.os.SystemClock.uptimeMillis();
        MotionEvent down = MotionEvent.obtain(now, now, MotionEvent.ACTION_DOWN, cursorX, cursorY, 0);
        MotionEvent up = MotionEvent.obtain(now, now + 24L, MotionEvent.ACTION_UP, cursorX, cursorY, 0);
        try {
            webView.dispatchTouchEvent(down);
            webView.dispatchTouchEvent(up);
            if (cursorView != null) {
                cursorView.showClickPulse();
            }
        } finally {
            down.recycle();
            up.recycle();
        }
    }

    private void ensureCursorPosition() {
        if (cursorPositionInitialized || webView == null || webView.getWidth() <= 0 || webView.getHeight() <= 0) {
            return;
        }
        resetCursorToCenter();
    }

    private void resetCursorToCenter() {
        if (webView == null || cursorView == null || webView.getWidth() <= 0 || webView.getHeight() <= 0) {
            return;
        }
        cursorX = webView.getWidth() / 2f;
        cursorY = webView.getHeight() / 2f;
        cursorPositionInitialized = true;
        cursorView.setCursorPosition(cursorX, cursorY);
    }

    private static float clamp(float value, float min, float max) {
        return Math.max(min, Math.min(max, value));
    }

    private void moveWebFocus(boolean forward) {
        String delta = forward ? "1" : "-1";
        String js = "(function(){"
                + "var q='a[href],button:not([disabled]),input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex=\\\"-1\\\"]),video';"
                + "var a=Array.prototype.slice.call(document.querySelectorAll(q)).filter(function(e){"
                + "var r=e.getBoundingClientRect(),s=getComputedStyle(e);return r.width>0&&r.height>0&&s.visibility!==\"hidden\"&&s.display!==\"none\";});"
                + "if(!a.length)return;var cur=document.activeElement,i=a.indexOf(cur);"
                + "if(i<0){i=" + (forward ? "0" : "a.length-1") + ";}else{i=(i+" + delta + "+a.length)%a.length;}"
                + "a[i].focus();a[i].scrollIntoView({block:'center',inline:'center'});"
                + "})();";
        webView.evaluateJavascript(js, null);
    }

    private void sendEnterToWebView() {
        long now = android.os.SystemClock.uptimeMillis();
        webView.dispatchKeyEvent(new KeyEvent(now, now, KeyEvent.ACTION_DOWN, KeyEvent.KEYCODE_ENTER, 0));
        webView.dispatchKeyEvent(new KeyEvent(now, now, KeyEvent.ACTION_UP, KeyEvent.KEYCODE_ENTER, 0));
    }

    private void injectFocusHighlight() {
        String js = "(function(){if(document.getElementById('firetv-focus-style'))return;"
                + "var s=document.createElement('style');s.id='firetv-focus-style';"
                + "s.textContent='*:focus{outline:4px solid white !important;outline-offset:3px !important;}';"
                + "(document.head||document.documentElement).appendChild(s);})();";
        webView.evaluateJavascript(js, null);
    }

    private void showAppMenu() {
        final boolean cursorEnabled = isCursorEnabled();
        final boolean nativeTv = isNativeTvNavigationEnabled();
        final boolean legacyFocus = prefs.getBoolean(KEY_TV_FOCUS, false);
        final boolean performance = isPerformanceModeEnabled();
        final boolean debug = isDebugModeEnabled();
        final String[] items = new String[]{
                "Home",
                "Reload",
                "Open Current Page in Silk (Video Fallback)",
                "Page Zoom: " + currentPageZoom() + "%",
                "Native TV Navigation: " + (nativeTv ? "On" : "Off"),
                "Cursor Navigation (Compatibility): " + (cursorEnabled ? "On" : "Off"),
                "Legacy JS Focus Navigation: " + (legacyFocus ? "On" : "Off"),
                "Performance Mode: " + (performance ? "On" : "Off"),
                "Debug Mode: " + (debug ? "On" : "Off"),
                "Debug Snapshot",
                "Export Debug Report",
                "Reset Debug Counters",
                "User Agent: " + profileLabel(currentUaProfile()),
                "Clear DisneyNOW App Web Data",
                "Diagnostics",
                "Export Diagnostic Report",
                "Safe Self-Test",
                "About",
                "Exit"
        };

        new AlertDialog.Builder(this)
                .setTitle("DisneyNOW TV Shell — " + versionLabel())
                .setItems(items, (dialog, which) -> {
                    switch (which) {
                        case 0:
                            if (isNativePlayerVisible()) stopNativePlayback();
                            webView.loadUrl(HOME_URL);
                            break;
                        case 1:
                            if (isNativePlayerVisible()) stopNativePlayback();
                            webView.reload();
                            break;
                        case 2:
                            openCurrentPageInSilk();
                            break;
                        case 3:
                            showPageZoomDialog();
                            break;
                        case 4:
                            setNativeTvNavigation(!nativeTv);
                            break;
                        case 5:
                            setCursorEnabled(!cursorEnabled);
                            break;
                        case 6:
                            setTvFocusNavigation(!legacyFocus);
                            break;
                        case 7:
                            setPerformanceMode(!performance);
                            break;
                        case 8:
                            setDebugMode(!debug);
                            break;
                        case 9:
                            showTextDialog("Debug Snapshot", buildDebugSnapshot());
                            break;
                        case 10:
                            exportDebugReport();
                            break;
                        case 11:
                            resetDebugCounters();
                            Toast.makeText(this, "Debug counters reset.", Toast.LENGTH_SHORT).show();
                            break;
                        case 12:
                            showUserAgentDialog();
                            break;
                        case 13:
                            confirmClearWebData();
                            break;
                        case 14:
                            showTextDialog("Diagnostics", buildDiagnostics());
                            break;
                        case 15:
                            exportDiagnostics();
                            break;
                        case 16:
                            runSafeSelfTest();
                            break;
                        case 17:
                            showAbout();
                            break;
                        case 18:
                            logger.log("EXIT menu");
                            finish();
                            break;
                        default:
                            break;
                    }
                })
                .show();
    }

    private void showPageZoomDialog() {
        final int current = currentPageZoom();
        final LinearLayout panel = new LinearLayout(this);
        panel.setOrientation(LinearLayout.VERTICAL);
        int pad = dp(20);
        panel.setPadding(pad, dp(8), pad, 0);

        TextView help = new TextView(this);
        help.setText("Whole-Page Zoom: 0-500%. Uses WebView-level zoom so the complete rendered page scales together. 0% intentionally hides the page; Menu remains available to restore it. Changes apply without reloading.");
        panel.addView(help, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        final EditText input = new EditText(this);
        input.setSingleLine(true);
        input.setInputType(InputType.TYPE_CLASS_NUMBER);
        input.setText(String.valueOf(current));
        input.setSelectAllOnFocus(true);
        input.setContentDescription("Page Zoom percent from 0 to 500");
        panel.addView(input, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        final SeekBar slider = new SeekBar(this);
        slider.setMax(MAX_PAGE_ZOOM);
        slider.setProgress(current);
        slider.setContentDescription("Page Zoom slider 0 to 500 percent");
        panel.addView(slider, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        Button minus = new Button(this); minus.setText("-1");
        Button plus = new Button(this); plus.setText("+1");
        Button reset = new Button(this); reset.setText("Reset 100%");
        row.addView(minus, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
        row.addView(plus, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
        row.addView(reset, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1.5f));
        panel.addView(row, new LinearLayout.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        final boolean[] syncing = new boolean[]{false};
        slider.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                if (!fromUser || syncing[0]) return;
                syncing[0] = true;
                input.setText(String.valueOf(progress));
                input.setSelection(input.getText().length());
                syncing[0] = false;
            }
            @Override public void onStartTrackingTouch(SeekBar seekBar) {}
            @Override public void onStopTrackingTouch(SeekBar seekBar) {
                int value = seekBar.getProgress();
                input.setText(String.valueOf(value));
                input.setSelection(input.getText().length());
                setPageZoom(value, true);
            }
        });

        View.OnClickListener adjust = v -> {
            Integer parsed = parseZoomInput(input);
            int value = parsed == null ? slider.getProgress() : parsed;
            if (v == minus) value--;
            else if (v == plus) value++;
            else value = 100;
            value = Math.max(MIN_PAGE_ZOOM, Math.min(MAX_PAGE_ZOOM, value));
            slider.setProgress(value);
            input.setText(String.valueOf(value));
            input.setSelection(input.getText().length());
            setPageZoom(value, true);
        };
        minus.setOnClickListener(adjust);
        plus.setOnClickListener(adjust);
        reset.setOnClickListener(adjust);

        final AlertDialog dialog = new AlertDialog.Builder(this)
                .setTitle("Page Zoom: " + current + "%")
                .setView(panel)
                .setPositiveButton("Apply", null)
                .setNegativeButton("Close", null)
                .create();
        dialog.setOnShowListener(ignored -> dialog.getButton(AlertDialog.BUTTON_POSITIVE).setOnClickListener(v -> {
            Integer value = parseZoomInput(input);
            if (value == null || value < MIN_PAGE_ZOOM || value > MAX_PAGE_ZOOM) {
                input.setError("Enter a whole number from 0 to 500.");
                return;
            }
            slider.setProgress(value);
            if (setPageZoom(value, true)) dialog.dismiss();
        }));
        dialog.show();
    }

    private Integer parseZoomInput(EditText input) {
        if (input == null) return null;
        String raw = input.getText() == null ? "" : input.getText().toString().trim();
        if (raw.isEmpty()) return null;
        try {
            return Integer.parseInt(raw);
        } catch (NumberFormatException ex) {
            return null;
        }
    }

    private void showUserAgentDialog() {
        final String[] values = new String[]{UA_ANDROID, UA_WEBVIEW, UA_DESKTOP};
        final String[] labels = new String[]{
                "Android Chrome-compatible (recommended)",
                "Device WebView original",
                "Desktop Edge-compatible"
        };
        String current = currentUaProfile();
        int checked = 0;
        for (int i = 0; i < values.length; i++) {
            if (values[i].equals(current)) {
                checked = i;
                break;
            }
        }

        final int initialChecked = checked;
        new AlertDialog.Builder(this)
                .setTitle("User Agent")
                .setSingleChoiceItems(labels, initialChecked, (dialog, which) -> {
                    setUserAgentProfile(values[which]);
                    dialog.dismiss();
                })
                .setNegativeButton("Cancel", null)
                .show();
    }

    private void setUserAgentProfile(String profile) {
        if (!isValidUaProfile(profile)) {
            Toast.makeText(this, "Invalid user-agent profile.", Toast.LENGTH_SHORT).show();
            return;
        }
        boolean saved = prefs.edit().putString(KEY_UA_PROFILE, profile).commit();
        if (!saved) {
            logger.log("ERROR ua profile persistence failed profile=" + profile);
            Toast.makeText(this, "Could not save the user-agent setting.", Toast.LENGTH_LONG).show();
            return;
        }
        webView.getSettings().setUserAgentString(resolveUserAgent(profile));
        logger.log("SETTING ua_profile=" + profile);
        webView.reload();
    }

    private void setTvFocusNavigation(boolean enabled) {
        SharedPreferences.Editor editor = prefs.edit().putBoolean(KEY_TV_FOCUS, enabled);
        if (enabled) {
            editor.putBoolean(KEY_CURSOR_ENABLED, false);
            editor.putBoolean(KEY_NATIVE_TV_NAV, false);
            stopAllCursorDirections();
        }
        boolean saved = editor.commit();
        if (!saved) {
            logger.log("ERROR legacy focus persistence failed");
            Toast.makeText(this, "Could not save Legacy Focus Navigation.", Toast.LENGTH_LONG).show();
            return;
        }
        if (cursorView != null) {
            cursorView.setVisibility(isCursorEnabled() ? View.VISIBLE : View.GONE);
        }
        logger.log("SETTING legacy_focus_navigation=" + enabled);
        if (enabled) {
            injectFocusHighlight();
        }
        Toast.makeText(this, "Legacy Focus Navigation " + (enabled ? "enabled" : "disabled") + ".", Toast.LENGTH_SHORT).show();
    }

    private boolean isCursorEnabled() {
        return prefs.getBoolean(KEY_CURSOR_ENABLED, true);
    }

    private boolean isNativeTvNavigationEnabled() {
        return prefs.getBoolean(KEY_NATIVE_TV_NAV, true);
    }

    private void setNativeTvNavigation(boolean enabled) {
        SharedPreferences.Editor editor = prefs.edit().putBoolean(KEY_NATIVE_TV_NAV, enabled);
        if (enabled) {
            editor.putBoolean(KEY_CURSOR_ENABLED, false);
            editor.putBoolean(KEY_TV_FOCUS, false);
            stopAllCursorDirections();
        }
        boolean saved = editor.commit();
        if (!saved) {
            logger.log("ERROR native TV navigation persistence failed");
            Toast.makeText(this, "Could not save Native TV Navigation.", Toast.LENGTH_LONG).show();
            return;
        }
        if (cursorView != null) cursorView.setVisibility(isCursorEnabled() && customView == null && !isNativePlayerVisible() ? View.VISIBLE : View.GONE);
        if (enabled) {
            injectFocusHighlight();
            webView.requestFocus();
        }
        logger.log("SETTING native_tv_navigation=" + enabled);
        Toast.makeText(this, "Native TV Navigation " + (enabled ? "enabled" : "disabled") + ".", Toast.LENGTH_SHORT).show();
    }

    private boolean isPerformanceModeEnabled() {
        return prefs.getBoolean(KEY_PERFORMANCE_MODE, true);
    }

    private void setPerformanceMode(boolean enabled) {
        boolean saved = prefs.edit().putBoolean(KEY_PERFORMANCE_MODE, enabled).commit();
        if (!saved) {
            logger.log("ERROR performance mode persistence failed");
            Toast.makeText(this, "Could not save Performance Mode.", Toast.LENGTH_LONG).show();
            return;
        }
        applyPerformanceModeToCurrentDocument();
        logger.log("SETTING performance_mode=" + enabled);
        Toast.makeText(this, "Performance Mode " + (enabled ? "enabled" : "disabled") + ".", Toast.LENGTH_SHORT).show();
    }

    private void setCursorEnabled(boolean enabled) {
        SharedPreferences.Editor editor = prefs.edit().putBoolean(KEY_CURSOR_ENABLED, enabled);
        if (enabled) {
            editor.putBoolean(KEY_TV_FOCUS, false);
            editor.putBoolean(KEY_NATIVE_TV_NAV, false);
        }
        boolean saved = editor.commit();
        if (!saved) {
            logger.log("ERROR cursor persistence failed");
            Toast.makeText(this, "Could not save Cursor Navigation.", Toast.LENGTH_LONG).show();
            return;
        }
        if (!enabled) stopAllCursorDirections();
        if (cursorView != null) {
            cursorView.setVisibility(enabled && customView == null ? View.VISIBLE : View.GONE);
        }
        if (enabled) {
            resetCursorToCenter();
        }
        logger.log("SETTING cursor_navigation=" + enabled);
        Toast.makeText(this, "Cursor Navigation " + (enabled ? "enabled" : "disabled") + ".", Toast.LENGTH_SHORT).show();
    }

    private int currentPageZoom() {
        int zoom = prefs.getInt(KEY_PAGE_ZOOM, DEFAULT_PAGE_ZOOM);
        if (zoom < MIN_PAGE_ZOOM || zoom > MAX_PAGE_ZOOM) {
            return DEFAULT_PAGE_ZOOM;
        }
        return zoom;
    }

    private boolean setPageZoom(int percent, boolean applyNow) {
        if (percent < MIN_PAGE_ZOOM || percent > MAX_PAGE_ZOOM) {
            return false;
        }
        boolean saved = prefs.edit().putInt(KEY_PAGE_ZOOM, percent).commit();
        if (!saved) {
            logger.log("ERROR page zoom persistence failed percent=" + percent);
            if (applyNow) {
                Toast.makeText(this, "Could not save Page Zoom.", Toast.LENGTH_LONG).show();
            }
            return false;
        }
        if (applyNow) {
            applyWholePageZoom();
        }
        logger.log("SETTING page_zoom=" + percent);
        return true;
    }

    private void applyWholePageZoom() {
        if (webView == null) return;
        int target = currentPageZoom();
        if (target == 0) {
            webView.setAlpha(0f);
            logger.log("PAGE_ZOOM applied percent=0 mode=whole_webview_hidden");
            return;
        }
        webView.setAlpha(1f);
        int from = Math.max(1, appliedWholePageZoomPercent);
        float ratio = target / (float) from;
        applyWebViewZoomRatio(ratio);
        appliedWholePageZoomPercent = target;
        logger.log("PAGE_ZOOM applied percent=" + target + " mode=webview_zoomBy");
    }

    private void applyWebViewZoomRatio(float ratio) {
        if (webView == null || ratio <= 0f || Float.isNaN(ratio) || Float.isInfinite(ratio)) return;
        while (ratio > 100f) {
            webView.zoomBy(100f);
            ratio /= 100f;
        }
        while (ratio < 0.01f) {
            webView.zoomBy(0.01f);
            ratio /= 0.01f;
        }
        if (Math.abs(ratio - 1f) > 0.0001f) webView.zoomBy(ratio);
    }

    private void applyPerformanceModeToCurrentDocument() {
        if (webView == null) return;
        String js;
        if (isPerformanceModeEnabled()) {
            js = "(function(){var id='firetv-performance-style',s=document.getElementById(id);"
                    + "if(!s){s=document.createElement('style');s.id=id;(document.head||document.documentElement).appendChild(s);}"
                    + "s.textContent='*,*::before,*::after{animation-duration:0.001s !important;animation-delay:0s !important;transition-duration:0.001s !important;scroll-behavior:auto !important;}';"
                    + "})();";
        } else {
            js = "(function(){var s=document.getElementById('firetv-performance-style');if(s)s.remove();})();";
        }
        webView.evaluateJavascript(js, null);
    }

    private void migrateBuild8Settings() {
        if (prefs.getBoolean(KEY_BUILD8_MIGRATED, false)) return;
        boolean saved = prefs.edit()
                .putBoolean(KEY_NATIVE_TV_NAV, true)
                .putBoolean(KEY_CURSOR_ENABLED, false)
                .putBoolean(KEY_TV_FOCUS, false)
                .putBoolean(KEY_PERFORMANCE_MODE, true)
                .putBoolean(KEY_BUILD8_MIGRATED, true)
                .commit();
        if (!saved && logger != null) logger.log("WARN Build 8 navigation migration persistence failed");
    }

    private void migrateBuild2Settings() {
        if (prefs.getBoolean(KEY_BUILD2_MIGRATED, false)) {
            return;
        }
        boolean saved = prefs.edit()
                .putBoolean(KEY_CURSOR_ENABLED, true)
                .putBoolean(KEY_TV_FOCUS, false)
                .putInt(KEY_PAGE_ZOOM, DEFAULT_PAGE_ZOOM)
                .putBoolean(KEY_BUILD2_MIGRATED, true)
                .commit();
        if (!saved && logger != null) {
            logger.log("WARN Build 2 settings migration persistence failed");
        }
    }

    private String currentUaProfile() {
        String profile = prefs.getString(KEY_UA_PROFILE, UA_ANDROID);
        return isValidUaProfile(profile) ? profile : UA_ANDROID;
    }

    private static boolean isValidUaProfile(String profile) {
        return UA_ANDROID.equals(profile) || UA_WEBVIEW.equals(profile) || UA_DESKTOP.equals(profile);
    }

    private String resolveUserAgent(String profile) {
        String original = WebSettings.getDefaultUserAgent(this);
        if (UA_WEBVIEW.equals(profile)) {
            return original;
        }
        if (UA_DESKTOP.equals(profile)) {
            return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    + "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0";
        }

        String sanitized = original
                .replace("; wv", "")
                .replace(" Version/4.0", "")
                .replace("Version/4.0 ", "");
        return sanitized;
    }

    private static String profileLabel(String profile) {
        if (UA_WEBVIEW.equals(profile)) {
            return "Device WebView";
        }
        if (UA_DESKTOP.equals(profile)) {
            return "Desktop Edge";
        }
        return "Android Chrome-compatible";
    }

    private boolean isDebugModeEnabled() {
        return prefs.getBoolean(KEY_DEBUG_MODE, false);
    }

    private void setDebugMode(boolean enabled) {
        boolean saved = prefs.edit().putBoolean(KEY_DEBUG_MODE, enabled).commit();
        if (!saved) {
            Toast.makeText(this, "Could not save Debug Mode.", Toast.LENGTH_LONG).show();
            logger.log("ERROR debug mode persistence failed");
            return;
        }
        logger.log("DEBUG_MODE " + (enabled ? "enabled" : "disabled"));
        Toast.makeText(this, "Debug Mode " + (enabled ? "enabled" : "disabled") + ".", Toast.LENGTH_SHORT).show();
    }

    private void debugLog(String message) {
        if (isDebugModeEnabled()) logger.log("DEBUG " + message);
    }

    private void recordDebugKeyDispatch(long startedNanos) {
        if (startedNanos == 0L || !isDebugModeEnabled()) return;
        long elapsed = Math.max(0L, System.nanoTime() - startedNanos);
        debugKeyEventCount++;
        debugKeyDispatchTotalNanos += elapsed;
        if (elapsed > debugKeyDispatchMaxNanos) debugKeyDispatchMaxNanos = elapsed;
    }

    private static String playbackStateLabel(int state) {
        if (state == Player.STATE_IDLE) return "IDLE";
        if (state == Player.STATE_BUFFERING) return "BUFFERING";
        if (state == Player.STATE_READY) return "READY";
        if (state == Player.STATE_ENDED) return "ENDED";
        return "UNKNOWN(" + state + ")";
    }

    private void resetDebugCounters() {
        debugPageStartedAt = 0L;
        debugLastPageLoadMs = 0L;
        debugKeyEventCount = 0L;
        debugKeyDispatchTotalNanos = 0L;
        debugKeyDispatchMaxNanos = 0L;
        debugWebErrorCount = 0;
        debugHttpErrorCount = 0;
        debugNativePlayerErrorCount = 0;
        debugMediaManifestCount = 0;
        debugDrmCandidateCount = 0;
        debugNativeHandoffReadyCount = 0;
        debugNativeHandoffAttemptCount = 0;
        debugNativePlayerCreateCount = 0;
        debugNativePrepareCount = 0;
        debugPossibleDrmPostCount = 0;
        debugLastWebError = "none";
        debugLastHttpError = "none";
        debugLastNativePlayerError = "none";
        debugLastNativeHandoffStage = "idle";
        debugLastNativeHandoffDetail = "none";
        debugLastPossibleDrmPost = "none";
        logger.log("DEBUG counters reset");
    }

    private String buildDebugSnapshot() {
        Runtime runtime = Runtime.getRuntime();
        long usedBytes = runtime.totalMemory() - runtime.freeMemory();
        double avgKeyMs = debugKeyEventCount == 0L ? 0.0 : (debugKeyDispatchTotalNanos / 1_000_000.0) / debugKeyEventCount;
        double maxKeyMs = debugKeyDispatchMaxNanos / 1_000_000.0;
        String playerState = "not-created";
        if (nativePlayer != null) playerState = playbackStateLabel(nativePlayer.getPlaybackState()) + "; isPlaying=" + nativePlayer.isPlaying();
        StringBuilder out = new StringBuilder();
        out.append("DisneyNOW Fire TV Debug Snapshot\n");
        out.append("Version: ").append(versionLabel()).append('\n');
        out.append("Debug Mode: ").append(isDebugModeEnabled()).append('\n');
        out.append("Current main-frame host: ").append(webView == null ? "unavailable" : safeHost(webView.getUrl())).append('\n');
        out.append("Last page load: ").append(debugLastPageLoadMs).append(" ms\n");
        out.append("WebView errors: ").append(debugWebErrorCount).append("; last=").append(debugLastWebError).append('\n');
        out.append("Main-frame HTTP errors: ").append(debugHttpErrorCount).append("; last=").append(debugLastHttpError).append('\n');
        out.append("Native-player errors: ").append(debugNativePlayerErrorCount).append("; last=").append(debugLastNativePlayerError).append('\n');
        out.append("Media manifests observed: ").append(debugMediaManifestCount).append("; currentType=").append(mediaManifestType(lastMediaManifestUrl)).append("; ageMs=").append(ageMs(lastMediaCapturedAt)).append('\n');
        out.append("DRM candidates observed: ").append(debugDrmCandidateCount).append("; currentDetected=").append(lastDrmLicenseUrl != null).append("; ageMs=").append(ageMs(lastDrmCapturedAt)).append('\n');
        out.append("Possible post-manifest non-GET requests: ").append(debugPossibleDrmPostCount).append("; last=").append(debugLastPossibleDrmPost).append('\n');
        out.append("Native handoff: readyEvents=").append(debugNativeHandoffReadyCount)
                .append(" attempts=").append(debugNativeHandoffAttemptCount)
                .append(" playerCreates=").append(debugNativePlayerCreateCount)
                .append(" prepares=").append(debugNativePrepareCount).append('\n');
        out.append("Automatic native handoff: disabled by Build 13 safety rollback").append('\n');
        out.append("Previous run incomplete: ").append(previousRunIncomplete)
                .append("; stage=").append(previousRunStage)
                .append("; detail=").append(previousRunDetail)
                .append("; exception=").append(previousRunException)
                .append("; atMs=").append(previousRunStageAt).append('\n');
        out.append("Current persisted runtime stage: ").append(currentRuntimeStage)
                .append("; detail=").append(currentRuntimeDetail)
                .append("; atMs=").append(currentRuntimeStageAt).append('\n');
        out.append("Native handoff last stage: ").append(debugLastNativeHandoffStage).append("; detail=").append(debugLastNativeHandoffDetail).append('\n');
        out.append("Native player: ").append(playerState).append('\n');
        out.append("Fullscreen WebView video: ").append(customView != null).append('\n');
        out.append("Navigation: nativeTV=").append(isNativeTvNavigationEnabled())
                .append(" cursor=").append(isCursorEnabled())
                .append(" legacyFocus=").append(prefs.getBoolean(KEY_TV_FOCUS, false)).append('\n');
        out.append("Performance Mode: ").append(isPerformanceModeEnabled()).append('\n');
        out.append("Whole-Page Zoom: ").append(currentPageZoom()).append("%\n");
        out.append(String.format(Locale.US, "D-pad dispatch samples: %d; avg=%.3f ms; max=%.3f ms\n", debugKeyEventCount, avgKeyMs, maxKeyMs));
        out.append("Java heap used: ").append(usedBytes / (1024L * 1024L)).append(" MiB; total=")
                .append(runtime.totalMemory() / (1024L * 1024L)).append(" MiB; max=")
                .append(runtime.maxMemory() / (1024L * 1024L)).append(" MiB\n");
        out.append("Log folder: ").append(logger.getLogDirectory().getAbsolutePath()).append('\n');
        out.append("\nPrivacy: passwords, cookies, authorization headers, provider tokens, full media/license URLs, query strings, device serials, and typed text are not included. WebView remote debugging remains disabled.\n");
        return out.toString();
    }

    private void exportDebugReport() {
        String report = buildDiagnostics() + "\n\n" + buildDebugSnapshot() + "\n\nRecent privacy-safe app log:\n" + logger.readRecentLines(200);
        File folder = new File(appStorageRoot(), "debug");
        if (!folder.exists() && !folder.mkdirs()) {
            Toast.makeText(this, "Could not create the debug folder.", Toast.LENGTH_LONG).show();
            logger.log("ERROR debug report folder create failed");
            return;
        }
        String stamp = new SimpleDateFormat("yyyyMMdd-HHmmss", Locale.US).format(new Date());
        File file = new File(folder, "DisneyNOWFireTV-Debug-v0.1-Build13-" + stamp + ".txt");
        if (writeUtf8(file, report)) {
            logger.log("DEBUG_REPORT exported file=" + file.getName());
            showTextDialog("Debug Report Exported", "Saved to:\n" + file.getAbsolutePath());
        } else {
            logger.log("ERROR debug report export failed");
            Toast.makeText(this, "Debug report export failed.", Toast.LENGTH_LONG).show();
        }
    }

    private void confirmClearWebData() {
        new AlertDialog.Builder(this)
                .setTitle("Clear DisneyNOW App Web Data?")
                .setMessage("This clears cookies, cache, Web Storage, form data, and HTTP auth saved only inside this app. You may need to sign into your TV provider again.")
                .setPositiveButton("Clear", (dialog, which) -> clearAppWebData())
                .setNegativeButton("Cancel", null)
                .show();
    }

    private void clearAppWebData() {
        CookieManager cookies = CookieManager.getInstance();
        cookies.removeAllCookies(value -> {
            cookies.flush();
            webView.clearCache(true);
            webView.clearHistory();
            webView.clearFormData();
            webView.clearSslPreferences();
            WebStorage.getInstance().deleteAllData();
            WebViewDatabase.getInstance(MainActivity.this).clearHttpAuthUsernamePassword();
            clearMediaCandidates();
            logger.log("WEB_DATA cleared app-local WebView data and in-memory media candidates");
            webView.loadUrl(HOME_URL);
            Toast.makeText(MainActivity.this, "App web data cleared.", Toast.LENGTH_SHORT).show();
        });
    }

    private String buildDiagnostics() {
        StringBuilder out = new StringBuilder();
        out.append("Project: DisneyNOW Fire TV Hybrid TV Shell\n");
        out.append("Version: ").append(versionLabel()).append('\n');
        out.append("Package: ").append(getPackageName()).append('\n');
        out.append("Device: ").append(safeText(Build.MANUFACTURER)).append(' ').append(safeText(Build.MODEL)).append('\n');
        out.append("Android SDK: ").append(Build.VERSION.SDK_INT).append('\n');
        out.append("OS display: ").append(safeText(Build.DISPLAY)).append('\n');
        out.append("WebView: ").append(webViewPackageSummary()).append('\n');
        out.append("UA profile: ").append(profileLabel(currentUaProfile())).append('\n');
        out.append("User agent: ").append(webView.getSettings().getUserAgentString()).append('\n');
        out.append("JavaScript: ").append(webView.getSettings().getJavaScriptEnabled()).append('\n');
        out.append("DOM storage: ").append(webView.getSettings().getDomStorageEnabled()).append('\n');
        out.append("Third-party cookies: enabled for this app WebView\n");
        out.append("Native TV Navigation: ").append(isNativeTvNavigationEnabled()).append('\n');
        out.append("Cursor Navigation: ").append(isCursorEnabled()).append('\n');
        out.append("Legacy Focus Navigation: ").append(prefs.getBoolean(KEY_TV_FOCUS, false)).append('\n');
        out.append("Performance Mode: ").append(isPerformanceModeEnabled()).append('\n');
        out.append("Debug Mode: ").append(isDebugModeEnabled()).append('\n');
        out.append("Whole-Page Zoom: ").append(currentPageZoom()).append("%\n");
        out.append("Native manifest detected: ").append(lastMediaManifestUrl != null).append(" (type=").append(mediaManifestType(lastMediaManifestUrl)).append(")\n");
        out.append("DRM license endpoint detected: ").append(lastDrmLicenseUrl != null).append('\n');
        out.append("Automatic native launch: disabled in Build 13 after physical crash/regression").append('\n');
        out.append("Previous run incomplete: ").append(previousRunIncomplete)
                .append("; stage=").append(previousRunStage)
                .append("; detail=").append(previousRunDetail)
                .append("; exception=").append(previousRunException).append('\n');
        out.append("Current runtime stage: ").append(currentRuntimeStage)
                .append("; detail=").append(currentRuntimeDetail).append('\n');
        out.append("WebView hardware acceleration: ").append(webView.isHardwareAccelerated()).append('\n');
        out.append("Widevine: ").append(widevineSummary()).append('\n');
        out.append("Home: ").append(HOME_URL).append('\n');
        out.append("Log folder: ").append(logger.getLogDirectory().getAbsolutePath()).append('\n');
        out.append("\nNo passwords, provider tokens, cookies, media URLs, license URLs, device serials, browsing text, or private input are collected by this diagnostic report.\n");
        return out.toString();
    }

    private String webViewPackageSummary() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            PackageInfo info = WebView.getCurrentWebViewPackage();
            if (info == null) {
                return "unavailable";
            }
            return safeText(info.packageName) + " " + safeText(info.versionName);
        }
        return "package query unavailable below API 26";
    }

    private String widevineSummary() {
        if (!MediaDrm.isCryptoSchemeSupported(WIDEVINE_UUID)) {
            return "not supported";
        }
        MediaDrm drm = null;
        try {
            drm = new MediaDrm(WIDEVINE_UUID);
            String vendor = safeDrmProperty(drm, MediaDrm.PROPERTY_VENDOR);
            String version = safeDrmProperty(drm, MediaDrm.PROPERTY_VERSION);
            String security = safeDrmProperty(drm, "securityLevel");
            return "supported; vendor=" + vendor + "; version=" + version + "; security=" + security;
        } catch (UnsupportedSchemeException | RuntimeException ex) {
            return "reported supported but could not open: " + ex.getClass().getSimpleName();
        } finally {
            if (drm != null) {
                drm.release();
            }
        }
    }

    private static String safeDrmProperty(MediaDrm drm, String key) {
        try {
            String value = drm.getPropertyString(key);
            return value == null || value.trim().isEmpty() ? "unknown" : value.trim();
        } catch (RuntimeException ex) {
            return "unknown";
        }
    }

    private void exportDiagnostics() {
        String diagnostics = buildDiagnostics();
        File folder = new File(appStorageRoot(), "diagnostics");
        if (!folder.exists() && !folder.mkdirs()) {
            Toast.makeText(this, "Could not create the diagnostics folder.", Toast.LENGTH_LONG).show();
            logger.log("ERROR diagnostics folder create failed");
            return;
        }
        String stamp = new SimpleDateFormat("yyyyMMdd-HHmmss", Locale.US).format(new Date());
        File file = new File(folder, "DisneyNOWFireTV-Diagnostics-" + stamp + ".txt");
        if (writeUtf8(file, diagnostics)) {
            logger.log("DIAGNOSTICS exported file=" + file.getName());
            showTextDialog("Diagnostic Report Exported", "Saved to:\n" + file.getAbsolutePath());
        } else {
            logger.log("ERROR diagnostics export failed");
            Toast.makeText(this, "Diagnostic export failed.", Toast.LENGTH_LONG).show();
        }
    }

    private void runSafeSelfTest() {
        List<TestResult> results = new ArrayList<>();

        addResult(results, "Project package identity",
                EXPECTED_PACKAGE_ID.equals(getPackageName()),
                "expected=" + EXPECTED_PACKAGE_ID + " actual=" + getPackageName());

        boolean versionOk = "0.1".equals(BuildConfig.VERSION_NAME) && BuildConfig.APP_BUILD == 13 && BuildConfig.VERSION_CODE == 13;
        addResult(results, "Version + Build identity", versionOk,
                "versionName=" + BuildConfig.VERSION_NAME + " versionCode=" + BuildConfig.VERSION_CODE + " Build=" + BuildConfig.APP_BUILD);

        String tempKey = "__selftest_" + System.nanoTime();
        String tempValue = "write-reload-compare";
        boolean settingWritten = prefs.edit().putString(tempKey, tempValue).commit();
        SharedPreferences reloadedPrefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
        boolean settingMatches = settingWritten && tempValue.equals(reloadedPrefs.getString(tempKey, null));
        boolean settingCleaned = reloadedPrefs.edit().remove(tempKey).commit();
        addResult(results, "Settings persistence write -> reload/read -> compare -> delete",
                settingMatches && settingCleaned,
                "write=" + settingWritten + " compare=" + settingMatches + " cleanup=" + settingCleaned);

        boolean webSettingsOk = webView.getSettings().getJavaScriptEnabled()
                && webView.getSettings().getDomStorageEnabled()
                && !webView.getSettings().getAllowFileAccess()
                && !webView.getSettings().getAllowContentAccess()
                && CookieManager.getInstance().acceptCookie();
        addResult(results, "WebView production settings", webSettingsOk,
                "JavaScript/DOM enabled; file/content access disabled; cookies accepted");

        String ua = webView.getSettings().getUserAgentString();
        boolean uaOk = ua != null && !ua.trim().isEmpty() && isValidUaProfile(currentUaProfile());
        addResult(results, "User-agent production path", uaOk,
                "profile=" + currentUaProfile() + " uaLength=" + (ua == null ? 0 : ua.length()));

        addResult(results, "Hardware-accelerated WebView runtime", webView.isHardwareAccelerated(),
                "isHardwareAccelerated=" + webView.isHardwareAccelerated());

        addResult(results, "Build 8 low-overhead Native TV Navigation migration",
                prefs.getBoolean(KEY_BUILD8_MIGRATED, false) && (isNativeTvNavigationEnabled() || isCursorEnabled() || prefs.getBoolean(KEY_TV_FOCUS, false)),
                "migrated=" + prefs.getBoolean(KEY_BUILD8_MIGRATED, false) + " nativeTv=" + isNativeTvNavigationEnabled() + " cursor=" + isCursorEnabled() + " legacy=" + prefs.getBoolean(KEY_TV_FOCUS, false));

        addResult(results, "Media manifest classifier",
                isMediaManifestUrl("https://example.invalid/a.m3u8?token=redacted")
                        && isMediaManifestUrl("https://example.invalid/a.mpd")
                        && !isMediaManifestUrl("https://example.invalid/a.mp4"),
                "HLS/DASH detected; ordinary MP4 is not misclassified as a manifest");

        addResult(results, "DRM endpoint classifier",
                isLikelyDrmLicenseRequest("https://example.invalid/widevine/license", "POST")
                        && !isLikelyDrmLicenseRequest("https://example.invalid/widevine/license", "GET"),
                "license POST detected; GET not treated as a license transaction");

        boolean cursorStateOk = cursorView != null
                && ((isCursorEnabled() && cursorView.getVisibility() == View.VISIBLE)
                || (!isCursorEnabled() && cursorView.getVisibility() != View.VISIBLE));
        addResult(results, "Cursor visibility matches navigation setting", cursorStateOk,
                "enabled=" + isCursorEnabled() + " visibility=" + (cursorView == null ? -1 : cursorView.getVisibility()));

        ViewGroup.LayoutParams cursorParams = cursorView == null ? null : cursorView.getLayoutParams();
        boolean compactCursorOverlay = cursorParams != null && cursorParams.width == dp(48) && cursorParams.height == dp(48);
        addResult(results, "Compact cursor overlay production geometry", compactCursorOverlay,
                cursorParams == null ? "no layout params" : "width=" + cursorParams.width + " height=" + cursorParams.height);

        ensureCursorPosition();
        float beforeX = cursorX;
        float beforeY = cursorY;
        if (isCursorEnabled() && webView.getWidth() > dp(160)) {
            moveCursor(KeyEvent.KEYCODE_DPAD_RIGHT, 0);
            boolean cursorMoved = cursorX > beforeX || (beforeX >= webView.getWidth() - cursorView.cursorRadius());
            cursorX = beforeX;
            cursorY = beforeY;
            cursorView.setCursorPosition(cursorX, cursorY);
            addResult(results, "Cursor compatibility production movement path", cursorMoved,
                    "beforeX=" + beforeX + " after/restoreX=" + cursorX);
        } else {
            results.add(TestResult.skipped("Cursor compatibility production movement path",
                    "Cursor mode is disabled or WebView geometry is not ready; no page click is performed by Safe Self-Test."));
        }

        if (isCursorEnabled() && webView.getWidth() > dp(160)) {
            ensureCursorPosition();
            float dispatchBeforeX = cursorX;
            float dispatchBeforeY = cursorY;
            long now = android.os.SystemClock.uptimeMillis();
            boolean dispatchConsumed = dispatchKeyEvent(new KeyEvent(now, now, KeyEvent.ACTION_DOWN, KeyEvent.KEYCODE_DPAD_RIGHT, 0));
            boolean dispatchMoved = cursorX > dispatchBeforeX || (dispatchBeforeX >= webView.getWidth() - cursorView.cursorRadius());
            boolean upConsumed = dispatchKeyEvent(new KeyEvent(now, now + 1L, KeyEvent.ACTION_UP, KeyEvent.KEYCODE_DPAD_RIGHT, 0));
            cursorX = dispatchBeforeX;
            cursorY = dispatchBeforeY;
            cursorView.setCursorPosition(cursorX, cursorY);
            addResult(results, "Activity pre-WebView D-pad dispatch interception",
                    dispatchConsumed && dispatchMoved && upConsumed,
                    "downConsumed=" + dispatchConsumed + " moved=" + dispatchMoved + " upConsumed=" + upConsumed);
        } else {
            results.add(TestResult.skipped("Activity pre-WebView D-pad dispatch interception",
                    "Cursor mode is disabled or WebView geometry is not ready; no page click is performed by Safe Self-Test."));
        }

        int originalZoom = currentPageZoom();
        boolean zoomMinSet = setPageZoom(MIN_PAGE_ZOOM, false);
        SharedPreferences zoomMinReload = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
        boolean zoomMinReloaded = zoomMinSet && zoomMinReload.getInt(KEY_PAGE_ZOOM, -1) == MIN_PAGE_ZOOM;
        boolean zoomMaxSet = setPageZoom(MAX_PAGE_ZOOM, false);
        SharedPreferences zoomMaxReload = getSharedPreferences(PREFS_NAME, MODE_PRIVATE);
        boolean zoomMaxReloaded = zoomMaxSet && zoomMaxReload.getInt(KEY_PAGE_ZOOM, -1) == MAX_PAGE_ZOOM;
        boolean invalidLowRejected = !setPageZoom(MIN_PAGE_ZOOM - 1, false);
        boolean invalidHighRejected = !setPageZoom(MAX_PAGE_ZOOM + 1, false);
        boolean zoomRestored = setPageZoom(originalZoom, true);
        addResult(results, "Whole-Page Zoom 0-500 persistence + WebView-level production apply -> restore",
                zoomMinReloaded && zoomMaxReloaded && invalidLowRejected && invalidHighRejected && zoomRestored && currentPageZoom() == originalZoom,
                "min=" + zoomMinReloaded + " max=" + zoomMaxReloaded + " invalidLow=" + invalidLowRejected + " invalidHigh=" + invalidHighRejected + " restored=" + zoomRestored);

        if (customView == null && customViewContainer != null && webView != null) {
            View testFullscreenView = new View(this);
            final boolean[] callbackCalled = new boolean[]{false};
            DisneyWebChromeClient testChrome = new DisneyWebChromeClient();
            testChrome.onShowCustomView(testFullscreenView, () -> callbackCalled[0] = true);
            boolean fullscreenOverlayOk = customView == testFullscreenView
                    && customViewContainer.getVisibility() == View.VISIBLE
                    && webView.getVisibility() == View.INVISIBLE;
            testChrome.onHideCustomView();
            boolean fullscreenRestored = customView == null
                    && customViewContainer.getVisibility() == View.GONE
                    && webView.getVisibility() == View.VISIBLE
                    && callbackCalled[0];
            addResult(results, "Fullscreen overlay compositor production path",
                    fullscreenOverlayOk && fullscreenRestored,
                    "overlay=" + fullscreenOverlayOk + " restored=" + fullscreenRestored + " callback=" + callbackCalled[0]);
        } else {
            results.add(TestResult.skipped("Fullscreen overlay compositor production path",
                    "A real fullscreen custom view is already active or required views are unavailable; Safe Self-Test will not interrupt it."));
        }

        File internalTest = new File(getFilesDir(), "selftest.tmp");
        boolean internalRoundTrip = writeReadCompareDelete(internalTest, "DisneyNOWFireTV-selftest");
        addResult(results, "Project data write -> reload/read -> compare -> delete", internalRoundTrip,
                internalTest.getAbsolutePath());

        File externalRoot = getExternalFilesDir(null);
        if (externalRoot == null) {
            results.add(TestResult.skipped("App-specific external diagnostics storage", "External app-specific storage is unavailable on this device."));
        } else {
            File externalTest = new File(externalRoot, "selftest-external.tmp");
            boolean externalRoundTrip = writeReadCompareDelete(externalTest, "diagnostic-storage-selftest");
            addResult(results, "App-specific diagnostic storage write -> reload/read -> compare -> delete", externalRoundTrip,
                    externalTest.getAbsolutePath());
        }

        boolean widevineSupported = MediaDrm.isCryptoSchemeSupported(WIDEVINE_UUID);
        addResult(results, "Widevine DRM scheme availability", widevineSupported,
                widevineSupported ? widevineSummary() : "Widevine is unavailable; protected Disney playback is unlikely to work.");

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            PackageInfo packageInfo = WebView.getCurrentWebViewPackage();
            addResult(results, "WebView runtime package detection", packageInfo != null,
                    packageInfo == null ? "No current WebView package reported." : safeText(packageInfo.packageName) + " " + safeText(packageInfo.versionName));
        } else {
            results.add(TestResult.skipped("WebView runtime package detection", "Android API is below 26; this package-query API is unavailable."));
        }

        boolean homeUrlOk = HOME_URL.startsWith("https://") && "disneynow.com".equalsIgnoreCase(Uri.parse(HOME_URL).getHost());
        addResult(results, "DisneyNOW home URL safety invariant", homeUrlOk, HOME_URL);

        addResult(results, "Native handoff privacy-safe stage tracker",
                "none".equals(safeThrowableChain(null))
                        && "binary".equals(safeContentTypeCategory(Collections.singletonMap("Content-Type", "application/octet-stream")))
                        && "json".equals(safeContentTypeCategory(Collections.singletonMap("content-type", "application/json"))),
                "stage/error helpers classify without exposing URL/header values");

        addResult(results, "Native Media3 player surface initialized",
                nativePlayerContainer != null && nativePlayerView != null && nativePlayerContainer.getVisibility() == View.GONE,
                "PlayerView exists and starts hidden; no external media request is started by Safe Self-Test.");

        addResult(results, "Build 13 automatic native launch safety rollback",
                !AUTO_NATIVE_HANDOFF_ENABLED && !autoNativeAttemptScheduled,
                "Normal DisneyNOW use does not automatically create/start Media3 after the Build 11 crash regression.");

        SharedPreferences crashTrackingTest = getSharedPreferences(PREFS_NAME + "_build12_crash_selftest", MODE_PRIVATE);
        crashTrackingTest.edit().clear().commit();
        boolean crashTrackingRoundTrip = writeRuntimeState(crashTrackingTest, true, "self-test-stage", "self-test-detail", "none", 12345L)
                && crashTrackingTest.getBoolean(KEY_RUNTIME_ACTIVE, false)
                && "self-test-stage".equals(crashTrackingTest.getString(KEY_RUNTIME_STAGE, ""))
                && "self-test-detail".equals(crashTrackingTest.getString(KEY_RUNTIME_DETAIL, ""))
                && "none".equals(crashTrackingTest.getString(KEY_RUNTIME_EXCEPTION, ""))
                && crashTrackingTest.getLong(KEY_RUNTIME_STAGE_AT, 0L) == 12345L;
        boolean crashTrackingCleanup = crashTrackingTest.edit().clear().commit();
        addResult(results, "Crash-stage persistence production helper write -> reload/read -> compare -> delete",
                crashTrackingRoundTrip && crashTrackingCleanup,
                "isolated SharedPreferences self-test; real user settings/crash marker untouched");

        String debugSnapshot = buildDebugSnapshot();
        addResult(results, "Privacy-safe Debug Snapshot production path",
                debugSnapshot.contains("Debug Mode:")
                        && debugSnapshot.contains("D-pad dispatch samples:")
                        && debugSnapshot.contains("full media/license URLs")
                        && !debugSnapshot.contains("Cookie:")
                        && !debugSnapshot.contains("Authorization:"),
                "snapshot generated without cookies/auth headers/full media URLs");

        results.add(TestResult.skipped(
                "Native Media3 HLS/DASH + Widevine playback",
                "Requires a legitimate stream/DRM request exposed by the user's authenticated DisneyNOW session; Safe Self-Test does not manufacture tokens, licenses, or media URLs."
        ));

        results.add(TestResult.skipped(
                "Live DisneyNOW authentication + protected video playback",
                "Requires the user's real provider session, Disney servers, device DRM negotiation, and an interactive Fire TV playback check."
        ));
        results.add(TestResult.skipped(
                "Physical Fire TV navigation/click behavior and fullscreen video",
                "Requires actual Fire TV hardware interaction; Safe Self-Test can exercise surrounding code but cannot judge real remote responsiveness, page focus quality, or protected playback."
        ));

        String report = formatSelfTestReport(results);
        File folder = new File(appStorageRoot(), "selftest");
        boolean folderReady = folder.exists() || folder.mkdirs();
        File reportFile = new File(folder, "SafeSelfTest-v0.1-Build13.txt");
        boolean reportSaved = folderReady && writeUtf8(reportFile, report);
        logger.log("SELF_TEST complete " + selfTestTotals(results) + " reportSaved=" + reportSaved);

        String shown = report + "\nReport saved: " + (reportSaved ? reportFile.getAbsolutePath() : "FAILED TO SAVE");
        showTextDialog("Safe Self-Test — " + versionLabel(), shown);
    }

    private static void addResult(List<TestResult> results, String name, boolean pass, String detail) {
        results.add(pass ? TestResult.pass(name, detail) : TestResult.fail(name, detail));
    }

    private String formatSelfTestReport(List<TestResult> results) {
        StringBuilder out = new StringBuilder();
        out.append("DisneyNOW Fire TV Hybrid TV Shell SAFE SELF-TEST\n");
        out.append("Version: ").append(versionLabel()).append('\n');
        out.append("Package: ").append(getPackageName()).append('\n');
        out.append("Device: ").append(safeText(Build.MANUFACTURER)).append(' ').append(safeText(Build.MODEL)).append('\n');
        out.append("Android SDK: ").append(Build.VERSION.SDK_INT).append("\n\n");

        int index = 1;
        for (TestResult result : results) {
            out.append(index++)
                    .append(". ")
                    .append(result.status)
                    .append(" - ")
                    .append(result.name)
                    .append(" | ")
                    .append(result.detail)
                    .append('\n');
        }
        out.append("\nTOTALS: ").append(selfTestTotals(results)).append('\n');
        out.append("\nBuild remains NOT DONE until physical Fire TV stability, navigation responsiveness, whole-page zoom, provider login, WebView playback, Silk fallback, Debug Mode/report usefulness, and previous-run crash-stage evidence are tested and any failures are resolved. Automatic Media3 launch is intentionally disabled in Build 13.\n");
        return out.toString();
    }

    private static String selfTestTotals(List<TestResult> results) {
        int pass = 0;
        int fail = 0;
        int skipped = 0;
        for (TestResult result : results) {
            if ("PASS".equals(result.status)) {
                pass++;
            } else if ("FAIL".equals(result.status)) {
                fail++;
            } else {
                skipped++;
            }
        }
        return "PASS=" + pass + " FAIL=" + fail + " SKIPPED/NOT TESTED=" + skipped;
    }

    private boolean writeReadCompareDelete(File file, String value) {
        boolean write = writeUtf8(file, value);
        String loaded = write ? readUtf8(file) : null;
        boolean compare = value.equals(loaded);
        boolean deleted = !file.exists() || file.delete();
        return write && compare && deleted;
    }

    private static boolean writeUtf8(File file, String value) {
        try (FileOutputStream out = new FileOutputStream(file, false)) {
            out.write(value.getBytes(StandardCharsets.UTF_8));
            out.flush();
            return true;
        } catch (Exception ex) {
            return false;
        }
    }

    private static String readUtf8(File file) {
        StringBuilder out = new StringBuilder();
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(file), StandardCharsets.UTF_8))) {
            char[] buffer = new char[2048];
            int count;
            while ((count = reader.read(buffer)) != -1) {
                out.append(buffer, 0, count);
            }
            return out.toString();
        } catch (Exception ex) {
            return null;
        }
    }

    private File appStorageRoot() {
        File external = getExternalFilesDir(null);
        return external != null ? external : getFilesDir();
    }

    private void showAbout() {
        String text = "DisneyNOW Fire TV Hybrid TV Shell\n"
                + versionLabel() + "\n\n"
                + "Unofficial personal-use compatibility app. Not affiliated with or endorsed by Disney.\n\n"
                + "Build 13 keeps Native TV Navigation, Performance Mode, whole-WebView zoom, privacy-safe Debug Mode, the dormant experimental Media3/ExoPlayer HLS/DASH/Widevine code path, and Silk fallback.\n\n"
                + "Build 13 rolls back the unstable Build 11 automatic Media3 launch after physical Fire TV testing showed glitchy behavior and an app restart/crash. HLS/DASH observations remain privacy-safe diagnostics only during normal use. Build 13 also persists a bounded safe runtime stage and exception class chain so the next launch/report can show where an unexpected process end occurred without storing URLs, cookies, tokens, typed text, or exception messages.\n\n"
                + "The dormant native implementation is restricted to legitimately observed authenticated-session media and Android Widevine when applicable. It does not extract keys, bypass DRM, unlock content, or copy Disney proprietary player/auth code. Build 13 preserves the permanent release-signing identity for in-place updates and remains NOT DONE until physically tested on the Fire TV Stick.";
        showTextDialog("About", text);
    }

    private void showTextDialog(String title, String text) {
        ScrollView scroll = new ScrollView(this);
        TextView textView = new TextView(this);
        int pad = dp(20);
        textView.setPadding(pad, pad, pad, pad);
        textView.setTextColor(Color.WHITE);
        textView.setTextSize(16f);
        textView.setTextIsSelectable(true);
        textView.setText(text);
        scroll.addView(textView);

        new AlertDialog.Builder(this)
                .setTitle(title)
                .setView(scroll)
                .setPositiveButton("Close", null)
                .show();
    }

    private int dp(int value) {
        float density = getResources().getDisplayMetrics().density;
        return Math.round(value * density);
    }

    private String versionLabel() {
        return "v" + BuildConfig.VERSION_NAME + " Build " + BuildConfig.APP_BUILD;
    }

    private void enterImmersiveMode() {
        getWindow().getDecorView().setSystemUiVisibility(
                View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                        | View.SYSTEM_UI_FLAG_FULLSCREEN
                        | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                        | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                        | View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                        | View.SYSTEM_UI_FLAG_LAYOUT_STABLE
        );
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) {
            enterImmersiveMode();
        }
    }

    @Override
    public void onBackPressed() {
        if (isNativePlayerVisible()) {
            stopNativePlayback();
            return;
        }
        if (customView != null) {
            hideCustomView();
            return;
        }
        if (webView != null && webView.canGoBack()) {
            webView.goBack();
            return;
        }
        logger.log("EXIT back");
        super.onBackPressed();
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (webView != null) {
            webView.onResume();
        }
        if (customView != null && customViewContainer != null) {
            customViewContainer.setVisibility(View.VISIBLE);
            customViewContainer.bringToFront();
            customView.requestFocus();
        }
        enterImmersiveMode();
    }

    @Override
    protected void onPause() {
        stopAllCursorDirections();
        if (webView != null) {
            webView.onPause();
        }
        super.onPause();
    }

    @Override
    protected void onDestroy() {
        markRuntimeCleanShutdown("activity-onDestroy");
        if (installedUncaughtExceptionHandler != null
                && Thread.getDefaultUncaughtExceptionHandler() == installedUncaughtExceptionHandler) {
            Thread.setDefaultUncaughtExceptionHandler(previousUncaughtExceptionHandler);
        }
        stopAllCursorDirections();
        releaseNativePlayer();
        if (webView != null) {
            root.removeView(webView);
            webView.stopLoading();
            webView.setWebChromeClient(null);
            webView.setWebViewClient(null);
            webView.destroy();
            webView = null;
        }
        cursorView = null;
        logger.log("STOP version=" + versionLabel());
        super.onDestroy();
    }

    private static String safeHost(String url) {
        if (url == null) {
            return "unknown";
        }
        try {
            return safeHost(Uri.parse(url));
        } catch (RuntimeException ex) {
            return "unknown";
        }
    }

    private static String safeHost(Uri uri) {
        if (uri == null || uri.getHost() == null) {
            return "unknown";
        }
        return uri.getHost();
    }

    private static String safeText(String value) {
        if (value == null || value.trim().isEmpty()) {
            return "unknown";
        }
        return value.replace('\n', ' ').replace('\r', ' ').trim();
    }

    private final class CursorView extends View {
        private final Paint fill = new Paint(Paint.ANTI_ALIAS_FLAG);
        private final Paint stroke = new Paint(Paint.ANTI_ALIAS_FLAG);
        private final Paint cross = new Paint(Paint.ANTI_ALIAS_FLAG);
        private long pulseUntil;

        CursorView(Context context) {
            super(context);
            setFocusable(false);
            setClickable(false);
            fill.setStyle(Paint.Style.FILL);
            fill.setColor(Color.WHITE);
            stroke.setStyle(Paint.Style.STROKE);
            stroke.setStrokeWidth(dp(3));
            stroke.setColor(Color.BLACK);
            cross.setStyle(Paint.Style.STROKE);
            cross.setStrokeWidth(dp(2));
            cross.setColor(Color.BLACK);
        }

        float cursorRadius() {
            return dp(16);
        }

        void setCursorPosition(float newX, float newY) {
            setTranslationX(newX - getWidth() / 2f);
            setTranslationY(newY - getHeight() / 2f);
        }

        void showClickPulse() {
            pulseUntil = android.os.SystemClock.uptimeMillis() + 120L;
            invalidate();
            postDelayed(this::invalidate, 130L);
        }

        @Override
        protected void onDraw(Canvas canvas) {
            super.onDraw(canvas);
            float radius = cursorRadius();
            if (android.os.SystemClock.uptimeMillis() < pulseUntil) {
                radius *= 1.35f;
            }
            float x = getWidth() / 2f;
            float y = getHeight() / 2f;
            canvas.drawCircle(x, y, radius, fill);
            canvas.drawCircle(x, y, radius, stroke);
            float arm = radius * 0.55f;
            canvas.drawLine(x - arm, y, x + arm, y, cross);
            canvas.drawLine(x, y - arm, x, y + arm, cross);
        }
    }

    private static final class TestResult {
        final String status;
        final String name;
        final String detail;

        private TestResult(String status, String name, String detail) {
            this.status = status;
            this.name = name;
            this.detail = detail;
        }

        static TestResult pass(String name, String detail) {
            return new TestResult("PASS", name, detail);
        }

        static TestResult fail(String name, String detail) {
            return new TestResult("FAIL", name, detail);
        }

        static TestResult skipped(String name, String detail) {
            return new TestResult("SKIPPED/NOT TESTED", name, detail);
        }
    }

    private static final class AppLogger {
        private static final long MAX_BYTES = 1024L * 1024L;
        private static final int MAX_FILES = 5;
        private final File logDir;

        AppLogger(Context context) {
            File external = context.getExternalFilesDir(null);
            File root = external != null ? external : context.getFilesDir();
            logDir = new File(root, "logs");
            if (!logDir.exists()) {
                //noinspection ResultOfMethodCallIgnored
                logDir.mkdirs();
            }
        }

        File getLogDirectory() {
            return logDir;
        }

        synchronized void log(String message) {
            try {
                rotateIfNeeded();
                File current = new File(logDir, "app-0.log");
                String stamp = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss.SSS", Locale.US).format(new Date());
                String line = stamp + " | " + safeText(message) + "\n";
                try (FileOutputStream out = new FileOutputStream(current, true)) {
                    out.write(line.getBytes(StandardCharsets.UTF_8));
                    out.flush();
                }
            } catch (Exception ignored) {
                // Logging must never break normal app behavior.
            }
        }

        synchronized String readRecentLines(int maxLines) {
            File current = new File(logDir, "app-0.log");
            String loaded = readUtf8(current);
            if (loaded == null || loaded.isEmpty()) return "(no log entries)\n";
            String[] lines = loaded.split("\n");
            int safeMax = Math.max(1, Math.min(maxLines, 500));
            int start = Math.max(0, lines.length - safeMax);
            StringBuilder out = new StringBuilder();
            for (int i = start; i < lines.length; i++) {
                if (!lines[i].isEmpty()) out.append(lines[i]).append('\n');
            }
            return out.length() == 0 ? "(no log entries)\n" : out.toString();
        }

        private void rotateIfNeeded() {
            File current = new File(logDir, "app-0.log");
            if (!current.exists() || current.length() < MAX_BYTES) {
                return;
            }
            File oldest = new File(logDir, "app-" + (MAX_FILES - 1) + ".log");
            if (oldest.exists()) {
                //noinspection ResultOfMethodCallIgnored
                oldest.delete();
            }
            for (int i = MAX_FILES - 2; i >= 0; i--) {
                File from = new File(logDir, "app-" + i + ".log");
                File to = new File(logDir, "app-" + (i + 1) + ".log");
                if (from.exists()) {
                    //noinspection ResultOfMethodCallIgnored
                    from.renameTo(to);
                }
            }
        }
    }
}
