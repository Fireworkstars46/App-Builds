package com.fireworkstars46.appbatterylist;

import android.content.ContentResolver;
import android.content.ContentValues;
import android.content.Context;
import android.net.Uri;
import android.os.Environment;
import android.provider.MediaStore;

import java.io.IOException;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;

final class ExportEngine {
    private ExportEngine() {}

    static Uri saveToDownloads(Context context, String displayName, String mimeType, String content) throws IOException {
        ContentValues values = new ContentValues();
        values.put(MediaStore.Downloads.DISPLAY_NAME, displayName);
        values.put(MediaStore.Downloads.MIME_TYPE, mimeType);
        values.put(MediaStore.Downloads.RELATIVE_PATH, Environment.DIRECTORY_DOWNLOADS + "/App Battery List");
        values.put(MediaStore.Downloads.IS_PENDING, 1);

        ContentResolver resolver = context.getContentResolver();
        Uri uri = resolver.insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, values);
        if (uri == null) throw new IOException("MediaStore insert returned null");

        boolean success = false;
        try (OutputStream out = resolver.openOutputStream(uri, "w")) {
            if (out == null) throw new IOException("Could not open output stream");
            writeUtf8(out, content);
            success = true;
        } finally {
            if (!success) {
                resolver.delete(uri, null, null);
            }
        }

        ContentValues done = new ContentValues();
        done.put(MediaStore.Downloads.IS_PENDING, 0);
        resolver.update(uri, done, null, null);
        return uri;
    }

    static void writeUtf8(OutputStream out, String content) throws IOException {
        out.write(content.getBytes(StandardCharsets.UTF_8));
        out.flush();
    }
}
