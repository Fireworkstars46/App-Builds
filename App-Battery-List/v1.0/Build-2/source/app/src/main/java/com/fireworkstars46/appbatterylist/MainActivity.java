package com.fireworkstars46.appbatterylist;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.provider.Settings;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.HorizontalScrollView;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.ProgressBar;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public final class MainActivity extends Activity {
    private final ExecutorService executor = Executors.newSingleThreadExecutor();
    private final List<AppEntry> allApps = new ArrayList<>();
    private final List<AppEntry> visibleApps = new ArrayList<>();
    private AppListAdapter adapter;
    private EditText search;
    private Spinner filterSpinner;
    private TextView status;
    private ProgressBar progress;
    private LinearLayout reviewPanel;
    private TextView reviewStatus;
    private BoundedLogger logger;
    private GuidedReviewStore reviewStore;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        logger = new BoundedLogger(this);
        reviewStore = GuidedReviewStore.production(this);
        logger.log("START | " + BuildConfig.PROJECT_NAME + " v" + BuildConfig.VERSION_NAME + " Build " + BuildConfig.PROJECT_BUILD);
        buildUi();
        loadApps();
    }

    @Override
    protected void onResume() {
        super.onResume();
        syncGuidedReviewUi();
    }

    @Override
    protected void onDestroy() {
        logger.log("STOP");
        executor.shutdownNow();
        super.onDestroy();
    }

    private void buildUi() {
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(dp(12), dp(10), dp(12), dp(8));
        setContentView(root);

        TextView title = new TextView(this);
        title.setText(BuildConfig.PROJECT_NAME + "  v" + BuildConfig.VERSION_NAME + "  Build " + BuildConfig.PROJECT_BUILD);
        title.setTextSize(21);
        title.setGravity(Gravity.CENTER_VERTICAL);
        title.setTypeface(android.graphics.Typeface.DEFAULT, android.graphics.Typeface.BOLD);
        root.addView(title, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        TextView note = new TextView(this);
        note.setText("Lists apps visible to this Android profile. Secure Folder is separate. Tap an app for App Info, or use Guided Review to walk through user-app battery settings one app at a time.");
        note.setTextSize(12);
        note.setPadding(0, dp(4), 0, dp(8));
        root.addView(note);

        search = new EditText(this);
        search.setHint("Search app name or package...");
        search.setSingleLine(true);
        root.addView(search, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        filterSpinner = new Spinner(this);
        String[] filters = {"All apps", "User apps", "System apps"};
        filterSpinner.setAdapter(new ArrayAdapter<>(this, android.R.layout.simple_spinner_dropdown_item, filters));
        root.addView(filterSpinner, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        HorizontalScrollView scroller = new HorizontalScrollView(this);
        scroller.setHorizontalScrollBarEnabled(false);
        LinearLayout buttons = new LinearLayout(this);
        buttons.setOrientation(LinearLayout.HORIZONTAL);
        scroller.addView(buttons);
        root.addView(scroller, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        addButton(buttons, "Refresh", v -> loadApps());
        addButton(buttons, "Guided Review", v -> guidedReviewMenu());
        addButton(buttons, "Copy", v -> copyVisible());
        addButton(buttons, "Save TXT", v -> saveVisible(false));
        addButton(buttons, "Save CSV", v -> saveVisible(true));
        addButton(buttons, "Share TXT", v -> shareVisible());
        addButton(buttons, "Safe Self-Test", v -> runSelfTest());
        addButton(buttons, "Diagnostics", v -> showDiagnostics());

        LinearLayout statusRow = new LinearLayout(this);
        statusRow.setOrientation(LinearLayout.HORIZONTAL);
        statusRow.setGravity(Gravity.CENTER_VERTICAL);
        progress = new ProgressBar(this);
        progress.setIndeterminate(true);
        statusRow.addView(progress, new LinearLayout.LayoutParams(dp(28), dp(28)));
        status = new TextView(this);
        status.setPadding(dp(8), 0, 0, 0);
        statusRow.addView(status, new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f));
        root.addView(statusRow);

        reviewPanel = new LinearLayout(this);
        reviewPanel.setOrientation(LinearLayout.VERTICAL);
        reviewPanel.setPadding(0, dp(6), 0, dp(6));
        reviewPanel.setVisibility(View.GONE);
        reviewStatus = new TextView(this);
        reviewStatus.setTextSize(14);
        reviewStatus.setTypeface(android.graphics.Typeface.DEFAULT, android.graphics.Typeface.BOLD);
        reviewPanel.addView(reviewStatus, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));

        TextView reviewHelp = new TextView(this);
        reviewHelp.setText("In App Info, tap Battery and choose the setting you want. Press Back here, then Done & Next. App Battery List opens the next app for you.");
        reviewHelp.setTextSize(12);
        reviewHelp.setPadding(0, dp(2), 0, dp(2));
        reviewPanel.addView(reviewHelp);

        HorizontalScrollView reviewScroller = new HorizontalScrollView(this);
        reviewScroller.setHorizontalScrollBarEnabled(false);
        LinearLayout reviewButtons = new LinearLayout(this);
        reviewButtons.setOrientation(LinearLayout.HORIZONTAL);
        reviewScroller.addView(reviewButtons);
        reviewPanel.addView(reviewScroller, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));
        addButton(reviewButtons, "Open Current", v -> openGuidedCurrent());
        addButton(reviewButtons, "Previous", v -> previousGuided());
        addButton(reviewButtons, "Done & Next", v -> advanceGuided(false));
        addButton(reviewButtons, "Skip & Next", v -> advanceGuided(true));
        addButton(reviewButtons, "End Review", v -> endGuidedReview());
        root.addView(reviewPanel);

        ListView list = new ListView(this);
        adapter = new AppListAdapter(this);
        list.setAdapter(adapter);
        list.setOnItemClickListener((parent, view, position, id) -> openAppInfo(adapter.getItem(position)));
        root.addView(list, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, 0, 1f));

        search.addTextChangedListener(new TextWatcher() {
            @Override public void beforeTextChanged(CharSequence s, int start, int count, int after) {}
            @Override public void onTextChanged(CharSequence s, int start, int before, int count) { applyFilter(); }
            @Override public void afterTextChanged(Editable s) {}
        });
        filterSpinner.setOnItemSelectedListener(new AdapterView.OnItemSelectedListener() {
            @Override public void onItemSelected(AdapterView<?> parent, View view, int position, long id) { applyFilter(); }
            @Override public void onNothingSelected(AdapterView<?> parent) {}
        });
    }

    private Button addButton(LinearLayout parent, String label, View.OnClickListener listener) {
        Button button = new Button(this);
        button.setText(label);
        button.setAllCaps(false);
        button.setOnClickListener(listener);
        parent.addView(button, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));
        return button;
    }

    private void loadApps() {
        setBusy(true, "Loading installed apps...");
        executor.execute(() -> {
            try {
                List<AppEntry> loaded = AppRepository.loadApps(this);
                runOnUiThread(() -> {
                    allApps.clear();
                    allApps.addAll(loaded);
                    applyFilter();
                    syncGuidedReviewUi();
                    setBusy(false, "Loaded " + allApps.size() + " apps visible to this profile");
                    logger.log("REFRESH_OK | count=" + allApps.size());
                });
            } catch (RuntimeException ex) {
                runOnUiThread(() -> {
                    setBusy(false, "Load failed: " + ex.getClass().getSimpleName());
                    logger.log("REFRESH_FAIL | " + ex);
                    showMessage("Could not load apps", ex.toString());
                });
            }
        });
    }

    private void applyFilter() {
        if (adapter == null || search == null || filterSpinner == null) return;
        AppFilter.Type type;
        switch (filterSpinner.getSelectedItemPosition()) {
            case 1: type = AppFilter.Type.USER; break;
            case 2: type = AppFilter.Type.SYSTEM; break;
            default: type = AppFilter.Type.ALL;
        }
        List<AppEntry> filtered = AppFilter.apply(allApps, search.getText().toString(), type);
        visibleApps.clear();
        visibleApps.addAll(filtered);
        adapter.setItems(filtered);
        if (status != null && progress != null && progress.getVisibility() != View.VISIBLE) {
            status.setText(filtered.size() + " shown / " + allApps.size() + " total");
        }
    }

    private void openAppInfo(AppEntry app) {
        if (app == null) return;
        openAppInfoPackage(app.packageName, "OPEN_APP_INFO");
    }

    private boolean openAppInfoPackage(String packageName, String logTag) {
        try {
            Intent intent = new Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.parse("package:" + packageName));
            startActivity(intent);
            logger.log(logTag + " | " + packageName);
            return true;
        } catch (RuntimeException ex) {
            logger.log(logTag + "_FAIL | " + packageName + " | " + ex);
            showMessage("Could not open App Info", ex.toString());
            return false;
        }
    }

    private void guidedReviewMenu() {
        GuidedReviewStore.State state = reviewStore.load();
        if (state.active) {
            new AlertDialog.Builder(this)
                    .setTitle("Guided Review")
                    .setMessage("A review is already in progress at " + (state.index + 1) + " of " + state.packages.size() + ".")
                    .setPositiveButton("Resume", (d, w) -> openGuidedCurrent())
                    .setNeutralButton("Restart", (d, w) -> confirmStartNewGuidedReview())
                    .setNegativeButton("Cancel", null)
                    .show();
        } else {
            confirmStartNewGuidedReview();
        }
    }

    private void confirmStartNewGuidedReview() {
        List<String> queue = GuidedReviewPlanner.buildUserQueue(allApps, getPackageName());
        if (queue.isEmpty()) {
            showMessage("Guided Review", "No enabled user-installed apps are available to review in this Android profile.");
            return;
        }
        new AlertDialog.Builder(this)
                .setTitle("Start Guided Battery Review")
                .setMessage("Review " + queue.size() + " enabled user apps. For each app, App Info opens. Tap Battery, choose Optimized/Unrestricted/Restricted, then press Back and use Done & Next. Progress is remembered if you leave the app.")
                .setPositiveButton("Start", (d, w) -> {
                    if (!reviewStore.start(queue)) {
                        showMessage("Guided Review", "Could not save the review session. Nothing was changed.");
                        return;
                    }
                    logger.log("GUIDED_START | count=" + queue.size());
                    syncGuidedReviewUi();
                    openGuidedCurrent();
                })
                .setNegativeButton("Cancel", null)
                .show();
    }

    private void syncGuidedReviewUi() {
        if (reviewPanel == null || reviewStatus == null || reviewStore == null) return;
        GuidedReviewStore.State state = reviewStore.load();
        if (!state.active) {
            reviewPanel.setVisibility(View.GONE);
            return;
        }
        String pkg = state.currentPackage();
        AppEntry app = findApp(pkg);
        String label = app == null ? pkg : app.label;
        reviewStatus.setText("Guided Review  " + (state.index + 1) + " / " + state.packages.size()
                + "  •  " + label + "\n" + pkg
                + (state.skipped.isEmpty() ? "" : "\nSkipped so far: " + state.skipped.size()));
        reviewPanel.setVisibility(View.VISIBLE);
    }

    private void openGuidedCurrent() {
        GuidedReviewStore.State state = reviewStore.load();
        int safety = state.packages.size() + 1;
        while (state.active && safety-- > 0) {
            String pkg = state.currentPackage();
            AppEntry app = findApp(pkg);
            if (app != null) {
                syncGuidedReviewUi();
                openAppInfoPackage(pkg, "GUIDED_OPEN");
                return;
            }
            logger.log("GUIDED_MISSING_SKIP | " + pkg);
            if (!reviewStore.advance(true)) {
                showMessage("Guided Review", "Could not advance past an app that is no longer installed.");
                return;
            }
            state = reviewStore.load();
        }
        if (state.isComplete()) showGuidedComplete(state);
        else syncGuidedReviewUi();
    }

    private void advanceGuided(boolean skipped) {
        GuidedReviewStore.State before = reviewStore.load();
        if (!before.active) {
            syncGuidedReviewUi();
            return;
        }
        String current = before.currentPackage();
        if (!reviewStore.advance(skipped)) {
            showMessage("Guided Review", "Could not save review progress. The current position was not changed.");
            return;
        }
        logger.log((skipped ? "GUIDED_SKIP" : "GUIDED_DONE") + " | " + current);
        GuidedReviewStore.State after = reviewStore.load();
        if (after.isComplete()) {
            showGuidedComplete(after);
            return;
        }
        syncGuidedReviewUi();
        openGuidedCurrent();
    }

    private void previousGuided() {
        GuidedReviewStore.State state = reviewStore.load();
        if (state.packages.isEmpty()) return;
        if (state.index <= 0) {
            Toast.makeText(this, "Already at the first app", Toast.LENGTH_SHORT).show();
            return;
        }
        if (!reviewStore.previous()) {
            showMessage("Guided Review", "Could not save the previous position.");
            return;
        }
        logger.log("GUIDED_PREVIOUS");
        syncGuidedReviewUi();
        openGuidedCurrent();
    }

    private void endGuidedReview() {
        GuidedReviewStore.State state = reviewStore.load();
        if (!state.active && state.packages.isEmpty()) return;
        new AlertDialog.Builder(this)
                .setTitle("End Guided Review?")
                .setMessage("This clears the saved review position. It does not change any app battery settings.")
                .setPositiveButton("End", (d, w) -> {
                    if (reviewStore.clear()) {
                        logger.log("GUIDED_END");
                        syncGuidedReviewUi();
                    } else {
                        showMessage("Guided Review", "Could not clear the saved review session.");
                    }
                })
                .setNegativeButton("Cancel", null)
                .show();
    }

    private void showGuidedComplete(GuidedReviewStore.State state) {
        syncGuidedReviewUi();
        logger.log("GUIDED_COMPLETE | total=" + state.packages.size() + " | skipped=" + state.skipped.size());
        new AlertDialog.Builder(this)
                .setTitle("Guided Review Complete")
                .setMessage("Reached the end of " + state.packages.size() + " user apps. Skipped: " + state.skipped.size() + ".\n\nYou can start a new review any time.")
                .setPositiveButton("OK", null)
                .show();
    }

    private AppEntry findApp(String packageName) {
        if (packageName == null) return null;
        for (AppEntry app : allApps) if (packageName.equals(app.packageName)) return app;
        return null;
    }

    private void copyVisible() {
        String text = ExportFormatter.toText(visibleApps);
        ClipboardManager clipboard = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
        clipboard.setPrimaryClip(ClipData.newPlainText("App Battery List", text));
        logger.log("COPY | count=" + visibleApps.size());
        Toast.makeText(this, "Copied " + visibleApps.size() + " apps", Toast.LENGTH_SHORT).show();
    }

    private void saveVisible(boolean csv) {
        String stamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd-HHmmss", Locale.US));
        String name = "App-Battery-List-v" + BuildConfig.VERSION_NAME + "-Build-" + BuildConfig.PROJECT_BUILD + "-" + stamp + (csv ? ".csv" : ".txt");
        String mime = csv ? "text/csv" : "text/plain";
        String content = csv ? ExportFormatter.toCsv(visibleApps) : ExportFormatter.toText(visibleApps);
        setBusy(true, "Saving " + name + "...");
        executor.execute(() -> {
            try {
                Uri uri = ExportEngine.saveToDownloads(this, name, mime, content);
                runOnUiThread(() -> {
                    setBusy(false, visibleApps.size() + " apps exported");
                    logger.log("EXPORT_OK | " + name + " | " + uri);
                    Toast.makeText(this, "Saved in Downloads/App Battery List", Toast.LENGTH_LONG).show();
                });
            } catch (Exception ex) {
                runOnUiThread(() -> {
                    setBusy(false, "Export failed");
                    logger.log("EXPORT_FAIL | " + ex);
                    showMessage("Export failed", ex.toString());
                });
            }
        });
    }

    private void shareVisible() {
        String stamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyyMMdd-HHmmss", Locale.US));
        String name = "App-Battery-List-v" + BuildConfig.VERSION_NAME + "-Build-" + BuildConfig.PROJECT_BUILD + "-" + stamp + ".txt";
        String content = ExportFormatter.toText(visibleApps);
        setBusy(true, "Preparing share file...");
        executor.execute(() -> {
            try {
                Uri uri = ExportEngine.saveToDownloads(this, name, "text/plain", content);
                runOnUiThread(() -> {
                    setBusy(false, visibleApps.size() + " apps ready to share");
                    Intent share = new Intent(Intent.ACTION_SEND);
                    share.setType("text/plain");
                    share.putExtra(Intent.EXTRA_STREAM, uri);
                    share.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
                    startActivity(Intent.createChooser(share, "Share app list"));
                    logger.log("SHARE | count=" + visibleApps.size());
                });
            } catch (Exception ex) {
                runOnUiThread(() -> {
                    setBusy(false, "Share preparation failed");
                    showMessage("Share failed", ex.toString());
                });
            }
        });
    }

    private void runSelfTest() {
        setBusy(true, "Safe Self-Test running...");
        List<AppEntry> snapshot = new ArrayList<>(allApps);
        executor.execute(() -> {
            String report = SafeSelfTest.run(this, snapshot);
            runOnUiThread(() -> {
                setBusy(false, "Safe Self-Test finished");
                logger.log("SELF_TEST_COMPLETE");
                new AlertDialog.Builder(this)
                        .setTitle("Safe Self-Test")
                        .setMessage(report)
                        .setPositiveButton("Copy", (d, w) -> {
                            ClipboardManager clipboard = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
                            clipboard.setPrimaryClip(ClipData.newPlainText("Safe Self-Test", report));
                        })
                        .setNegativeButton("Close", null)
                        .show();
            });
        });
    }

    private void showDiagnostics() {
        int user = 0;
        int system = 0;
        for (AppEntry app : allApps) {
            if (app.systemApp) system++; else user++;
        }
        GuidedReviewStore.State review = reviewStore.load();
        String reviewText = review.active
                ? (review.index + 1) + "/" + review.packages.size() + " active; skipped=" + review.skipped.size()
                : (review.isComplete() ? "Complete; total=" + review.packages.size() + "; skipped=" + review.skipped.size() : "Not active");
        String text = BuildConfig.PROJECT_NAME + " v" + BuildConfig.VERSION_NAME + " Build " + BuildConfig.PROJECT_BUILD
                + "\nPackage: " + getPackageName()
                + "\nAndroid SDK: " + android.os.Build.VERSION.SDK_INT
                + "\nVisible apps: " + allApps.size()
                + "\nUser apps: " + user
                + "\nSystem apps: " + system
                + "\nGuided review: " + reviewText
                + "\nPermissions used: QUERY_ALL_PACKAGES only"
                + "\nInternet permission: No"
                + "\nStorage permission: No"
                + "\nProfile scope: Current Android profile only";
        new AlertDialog.Builder(this)
                .setTitle("Diagnostics")
                .setMessage(text)
                .setPositiveButton("OK", null)
                .show();
    }

    private void setBusy(boolean busy, String message) {
        if (progress != null) progress.setVisibility(busy ? View.VISIBLE : View.GONE);
        if (status != null) status.setText(message);
    }

    private void showMessage(String title, String message) {
        new AlertDialog.Builder(this).setTitle(title).setMessage(message).setPositiveButton("OK", null).show();
    }

    private int dp(int dp) {
        return Math.round(dp * getResources().getDisplayMetrics().density);
    }
}
