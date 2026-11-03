package com.fireworkstars46.appbatterylist;

import java.time.Instant;
import java.util.List;

final class ExportFormatter {
    private ExportFormatter() {}

    static String toText(List<AppEntry> apps) {
        StringBuilder sb = new StringBuilder();
        sb.append(BuildConfig.PROJECT_NAME).append(" v").append(BuildConfig.VERSION_NAME)
                .append(" Build ").append(BuildConfig.PROJECT_BUILD).append('\n');
        sb.append("Package ID: ").append(BuildConfig.APPLICATION_ID).append('\n');
        sb.append("Exported: ").append(Instant.now()).append('\n');
        sb.append("Scope: apps visible to the current Android profile only. Secure Folder is a separate profile.\n");
        sb.append("Count: ").append(apps.size()).append("\n\n");
        for (AppEntry app : apps) {
            sb.append(app.label).append(" | ")
                    .append(app.packageName).append(" | ")
                    .append(app.typeLabel()).append(" | ")
                    .append(app.enabled ? "Enabled" : "Disabled")
                    .append('\n');
        }
        return sb.toString();
    }

    static String toCsv(List<AppEntry> apps) {
        StringBuilder sb = new StringBuilder("App Name,Package Name,Type,Enabled,Recommended Battery Setting\n");
        for (AppEntry app : apps) {
            sb.append(csv(app.label)).append(',')
                    .append(csv(app.packageName)).append(',')
                    .append(csv(app.typeLabel())).append(',')
                    .append(csv(Boolean.toString(app.enabled))).append(',')
                    .append(csv(""))
                    .append('\n');
        }
        return sb.toString();
    }

    static String csv(String value) {
        String safe = value == null ? "" : value.replace("\"", "\"\"");
        return "\"" + safe + "\"";
    }
}
