package com.fireworkstars46.appbatterylist;

import android.content.Context;
import android.content.SharedPreferences;

import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

final class GuidedReviewStore {
    static final String PRODUCTION_PREFS = "guided_review_v1";

    private static final String KEY_ACTIVE = "active";
    private static final String KEY_INDEX = "index";
    private static final String KEY_PACKAGES = "packages";
    private static final String KEY_SKIPPED = "skipped";

    static final class State {
        final boolean active;
        final int index;
        final List<String> packages;
        final Set<String> skipped;

        State(boolean active, int index, List<String> packages, Set<String> skipped) {
            this.active = active;
            this.index = index;
            this.packages = packages;
            this.skipped = skipped;
        }

        boolean isComplete() {
            return !packages.isEmpty() && index >= packages.size();
        }

        String currentPackage() {
            return active && index >= 0 && index < packages.size() ? packages.get(index) : null;
        }
    }

    private final SharedPreferences prefs;

    private GuidedReviewStore(SharedPreferences prefs) {
        this.prefs = prefs;
    }

    static GuidedReviewStore production(Context context) {
        return new GuidedReviewStore(context.getSharedPreferences(PRODUCTION_PREFS, Context.MODE_PRIVATE));
    }

    static GuidedReviewStore isolated(Context context, String name) {
        return new GuidedReviewStore(context.getSharedPreferences(name, Context.MODE_PRIVATE));
    }

    State load() {
        List<String> packages = split(prefs.getString(KEY_PACKAGES, ""));
        Set<String> skipped = new LinkedHashSet<>(split(prefs.getString(KEY_SKIPPED, "")));
        int storedIndex = prefs.getInt(KEY_INDEX, 0);
        int index = Math.max(0, Math.min(storedIndex, packages.size()));
        boolean active = prefs.getBoolean(KEY_ACTIVE, false) && !packages.isEmpty() && index < packages.size();
        return new State(active, index, packages, skipped);
    }

    boolean start(List<String> packages) {
        List<String> safe = packages == null ? new ArrayList<>() : new ArrayList<>(packages);
        boolean committed = prefs.edit()
                .putBoolean(KEY_ACTIVE, !safe.isEmpty())
                .putInt(KEY_INDEX, 0)
                .putString(KEY_PACKAGES, join(safe))
                .putString(KEY_SKIPPED, "")
                .commit();
        if (!committed) return false;
        State state = load();
        return state.packages.equals(safe) && state.index == 0 && state.active == !safe.isEmpty();
    }

    boolean advance(boolean skippedCurrent) {
        State state = load();
        if (!state.active) return false;
        Set<String> skipped = new LinkedHashSet<>(state.skipped);
        String current = state.currentPackage();
        if (skippedCurrent && current != null) skipped.add(current);
        if (!skippedCurrent && current != null) skipped.remove(current);
        int next = state.index + 1;
        boolean active = next < state.packages.size();
        return prefs.edit()
                .putBoolean(KEY_ACTIVE, active)
                .putInt(KEY_INDEX, next)
                .putString(KEY_SKIPPED, join(new ArrayList<>(skipped)))
                .commit();
    }

    boolean previous() {
        State state = load();
        if (state.packages.isEmpty()) return false;
        int previous = Math.max(0, state.index - 1);
        Set<String> skipped = new LinkedHashSet<>(state.skipped);
        if (previous < state.packages.size()) skipped.remove(state.packages.get(previous));
        return prefs.edit()
                .putBoolean(KEY_ACTIVE, true)
                .putInt(KEY_INDEX, previous)
                .putString(KEY_SKIPPED, join(new ArrayList<>(skipped)))
                .commit();
    }

    boolean clear() {
        return prefs.edit().clear().commit() && load().packages.isEmpty() && !load().active;
    }

    private static String join(List<String> values) {
        return String.join("\n", values);
    }

    private static List<String> split(String raw) {
        List<String> values = new ArrayList<>();
        if (raw == null || raw.isEmpty()) return values;
        String[] parts = raw.split("\\n");
        for (String part : parts) if (!part.isEmpty()) values.add(part);
        return values;
    }
}
