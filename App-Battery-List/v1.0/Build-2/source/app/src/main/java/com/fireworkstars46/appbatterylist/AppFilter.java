package com.fireworkstars46.appbatterylist;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

final class AppFilter {
    enum Type { ALL, USER, SYSTEM }

    private AppFilter() {}

    static List<AppEntry> apply(List<AppEntry> source, String query, Type type) {
        String q = query == null ? "" : query.trim().toLowerCase(Locale.ROOT);
        List<AppEntry> out = new ArrayList<>();
        for (AppEntry app : source) {
            if (type == Type.USER && app.systemApp) continue;
            if (type == Type.SYSTEM && !app.systemApp) continue;
            if (!q.isEmpty()) {
                String label = app.label.toLowerCase(Locale.ROOT);
                String pkg = app.packageName.toLowerCase(Locale.ROOT);
                if (!label.contains(q) && !pkg.contains(q)) continue;
            }
            out.add(app);
        }
        return out;
    }
}
