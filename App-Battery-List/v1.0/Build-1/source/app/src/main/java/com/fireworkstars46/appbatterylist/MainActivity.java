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
    private BoundedLogger logger;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        logger = new BoundedLogger(this);
        logger.log("START | " + BuildConfig.PROJECT_NAME + " v" + BuildConfig.VERSION_NAME + " Build " + BuildConfig.PROJECT_BUILD);
        buildUi();
        loadApps();
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
        note.setText("Lists apps visible to this Android profile. Secure Folder is separate; install/open a copy there to list Secure Folder apps. Tap an app to open App Info.");
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

    private void addButton(LinearLayout parent, String label, View.OnClickListener listener) {
        Button button = new Button(this);
        button.setText(label);
        button.setAllCaps(false);
        button.setOnClickListener(listener);
        parent.addView(button, new LinearLayout.LayoutParams(ViewGroup.LayoutParams.WRAP_CONTENT, ViewGroup.LayoutParams.WRAP_CONTENT));
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
        try {
            Intent intent = new Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.parse("package:" + app.packageName));
            startActivity(intent);
            logger.log("OPEN_APP_INFO | " + app.packageName);
        } catch (RuntimeException ex) {
            showMessage("Could not open App Info", ex.toString());
        }
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
        String text = BuildConfig.PROJECT_NAME + " v" + BuildConfig.VERSION_NAME + " Build " + BuildConfig.PROJECT_BUILD
                + "\nPackage: " + getPackageName()
                + "\nAndroid SDK: " + android.os.Build.VERSION.SDK_INT
                + "\nVisible apps: " + allApps.size()
                + "\nUser apps: " + user
                + "\nSystem apps: " + system
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
        progress.setVisibility(busy ? View.VISIBLE : View.GONE);
        status.setText(message);
    }

    private void showMessage(String title, String message) {
        new AlertDialog.Builder(this).setTitle(title).setMessage(message).setPositiveButton("OK", null).show();
    }

    private int dp(int dp) {
        return Math.round(dp * getResources().getDisplayMetrics().density);
    }
}
