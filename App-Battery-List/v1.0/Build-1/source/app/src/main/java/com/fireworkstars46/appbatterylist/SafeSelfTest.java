package com.fireworkstars46.appbatterylist;

import android.content.Context;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.util.List;

final class SafeSelfTest {
    private SafeSelfTest() {}

    static String run(Context context, List<AppEntry> productionApps) {
        StringBuilder report = new StringBuilder();
        report.append("=== ").append(BuildConfig.PROJECT_NAME).append(" SAFE SELF-TEST v")
                .append(BuildConfig.VERSION_NAME).append(" Build ").append(BuildConfig.PROJECT_BUILD).append(" ===\n");
        int pass = 0, fail = 0, skipped = 0;

        try {
            boolean ok = productionApps != null && !productionApps.isEmpty();
            result(report, ok, "Installed-app production query", ok ? productionApps.size() + " visible apps" : "No apps returned");
            if (ok) pass++; else fail++;
        } catch (RuntimeException ex) {
            result(report, false, "Installed-app production query", ex.toString()); fail++;
        }

        boolean hasSelf = false;
        for (AppEntry app : productionApps) if (app.packageName.equals(context.getPackageName())) { hasSelf = true; break; }
        result(report, hasSelf, "Current package visible", context.getPackageName());
        if (hasSelf) pass++; else fail++;

        List<AppEntry> exact = AppFilter.apply(productionApps, context.getPackageName(), AppFilter.Type.ALL);
        boolean searchOk = exact.stream().anyMatch(a -> a.packageName.equals(context.getPackageName()));
        result(report, searchOk, "Search/filter production path", "Search for own package");
        if (searchOk) pass++; else fail++;

        try {
            String txt = ExportFormatter.toText(productionApps);
            ByteArrayOutputStream out = new ByteArrayOutputStream();
            ExportEngine.writeUtf8(out, txt);
            String roundTrip = out.toString(StandardCharsets.UTF_8);
            boolean ok = txt.equals(roundTrip) && roundTrip.contains(context.getPackageName());
            result(report, ok, "TXT export formatter -> production stream writer -> read/compare", "Bytes=" + out.size());
            if (ok) pass++; else fail++;
        } catch (Exception ex) {
            result(report, false, "TXT export formatter -> production stream writer -> read/compare", ex.toString()); fail++;
        }

        try {
            String sample = "Name, with comma and \"quote\"";
            String escaped = ExportFormatter.csv(sample);
            boolean ok = "\"Name, with comma and \"\"quote\"\"\"".equals(escaped);
            result(report, ok, "CSV escaping", "Special characters");
            if (ok) pass++; else fail++;
        } catch (RuntimeException ex) {
            result(report, false, "CSV escaping", ex.toString()); fail++;
        }

        try {
            File dir = new File(context.getCacheDir(), "safe-self-test-log");
            deleteTree(dir);
            BoundedLogger logger = new BoundedLogger(dir);
            String marker = "SELFTEST_MARKER_" + System.nanoTime();
            logger.log(marker);
            File log = new File(dir, "activity.log");
            String read = Files.readString(log.toPath(), StandardCharsets.UTF_8);
            boolean ok = read.contains(marker);
            result(report, ok, "Bounded logger write -> reload/read -> compare", log.getAbsolutePath());
            if (ok) pass++; else fail++;
            deleteTree(dir);
        } catch (Exception ex) {
            result(report, false, "Bounded logger write -> reload/read -> compare", ex.toString()); fail++;
        }

        report.append("SKIPPED/NOT TESTED - Physical Downloads export + Android share sheet | Requires interactive OS UI / external storage confirmation\n");
        skipped++;
        report.append("SKIPPED/NOT TESTED - App-info screen launch result | Requires interactive Android Settings UI\n");
        skipped++;
        report.append("SKIPPED/NOT TESTED - Secure Folder cross-profile visibility | Android/Knox profile isolation requires a real Secure Folder install\n");
        skipped++;

        report.append("\nTOTALS: PASS=").append(pass).append(" FAIL=").append(fail).append(" SKIPPED=").append(skipped).append('\n');
        report.append(fail == 0 ? "SELF-TEST RESULT: PASS (with listed interactive skips)\n" : "SELF-TEST RESULT: FAIL\n");
        return report.toString();
    }

    private static void result(StringBuilder report, boolean pass, String name, String detail) {
        report.append(pass ? "PASS" : "FAIL").append(" - ").append(name).append(" | ").append(detail).append('\n');
    }

    private static void deleteTree(File file) {
        if (file == null || !file.exists()) return;
        if (file.isDirectory()) {
            File[] children = file.listFiles();
            if (children != null) for (File child : children) deleteTree(child);
        }
        file.delete();
    }
}
