package com.fireworkstars46.appbatterylist;

import android.content.Context;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageManager;
import android.os.Build;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;

final class AppRepository {
    private AppRepository() {}

    static List<AppEntry> loadApps(Context context) {
        PackageManager pm = context.getPackageManager();
        List<ApplicationInfo> installed;
        if (Build.VERSION.SDK_INT >= 33) {
            installed = pm.getInstalledApplications(PackageManager.ApplicationInfoFlags.of(PackageManager.MATCH_ALL));
        } else {
            installed = pm.getInstalledApplications(PackageManager.MATCH_ALL);
        }

        List<AppEntry> result = new ArrayList<>(installed.size());
        for (ApplicationInfo info : installed) {
            String label;
            try {
                CharSequence cs = pm.getApplicationLabel(info);
                label = cs == null ? info.packageName : cs.toString();
            } catch (RuntimeException ex) {
                label = info.packageName;
            }

            boolean system = (info.flags & ApplicationInfo.FLAG_SYSTEM) != 0
                    || (info.flags & ApplicationInfo.FLAG_UPDATED_SYSTEM_APP) != 0;

            result.add(new AppEntry(
                    label,
                    info.packageName,
                    system,
                    info.enabled,
                    safeIcon(pm, info)
            ));
        }

        Collections.sort(result, Comparator
                .comparing((AppEntry a) -> a.label.toLowerCase(Locale.ROOT))
                .thenComparing(a -> a.packageName.toLowerCase(Locale.ROOT)));
        return result;
    }

    private static android.graphics.drawable.Drawable safeIcon(PackageManager pm, ApplicationInfo info) {
        try {
            return pm.getApplicationIcon(info);
        } catch (RuntimeException ex) {
            return pm.getDefaultActivityIcon();
        }
    }
}
