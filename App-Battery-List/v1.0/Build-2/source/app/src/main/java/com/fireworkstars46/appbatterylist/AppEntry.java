package com.fireworkstars46.appbatterylist;

import android.graphics.drawable.Drawable;

final class AppEntry {
    final String label;
    final String packageName;
    final boolean systemApp;
    final boolean enabled;
    final Drawable icon;

    AppEntry(String label, String packageName, boolean systemApp, boolean enabled, Drawable icon) {
        this.label = label;
        this.packageName = packageName;
        this.systemApp = systemApp;
        this.enabled = enabled;
        this.icon = icon;
    }

    String typeLabel() {
        return systemApp ? "System" : "User";
    }
}
