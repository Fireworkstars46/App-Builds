package com.fireworkstars46.appbatterylist;

import java.util.ArrayList;
import java.util.List;

final class GuidedReviewPlanner {
    private GuidedReviewPlanner() {}

    static List<String> buildUserQueue(List<AppEntry> apps, String ownPackage) {
        List<String> packages = new ArrayList<>();
        if (apps == null) return packages;
        for (AppEntry app : apps) {
            if (app == null || app.systemApp || !app.enabled) continue;
            if (app.packageName.equals(ownPackage)) continue;
            packages.add(app.packageName);
        }
        return packages;
    }
}
