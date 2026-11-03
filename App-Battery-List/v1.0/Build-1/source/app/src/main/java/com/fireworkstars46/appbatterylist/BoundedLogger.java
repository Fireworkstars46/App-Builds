package com.fireworkstars46.appbatterylist;

import android.content.Context;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.time.Instant;

final class BoundedLogger {
    private static final long MAX_BYTES = 256 * 1024;
    private final File logDir;
    private final File current;
    private final File previous;

    BoundedLogger(Context context) {
        this(new File(context.getFilesDir(), "logs"));
    }

    BoundedLogger(File root) {
        logDir = root;
        current = new File(logDir, "activity.log");
        previous = new File(logDir, "activity.1.log");
    }

    synchronized void log(String event) {
        try {
            if (!logDir.exists() && !logDir.mkdirs()) return;
            rotateIfNeeded();
            String line = Instant.now() + " | " + event + "\n";
            try (FileOutputStream out = new FileOutputStream(current, true)) {
                out.write(line.getBytes(StandardCharsets.UTF_8));
                out.flush();
            }
        } catch (IOException ignored) {
            // Logging must never break app functionality.
        }
    }

    private void rotateIfNeeded() {
        if (!current.exists() || current.length() < MAX_BYTES) return;
        if (previous.exists()) previous.delete();
        current.renameTo(previous);
    }
}
