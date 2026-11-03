package com.fireworkstars46.appbatterylist;

import android.content.Context;
import android.graphics.Typeface;
import android.view.Gravity;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.List;

final class AppListAdapter extends BaseAdapter {
    private final Context context;
    private List<AppEntry> items = new ArrayList<>();

    AppListAdapter(Context context) {
        this.context = context;
    }

    void setItems(List<AppEntry> newItems) {
        items = new ArrayList<>(newItems);
        notifyDataSetChanged();
    }

    @Override public int getCount() { return items.size(); }
    @Override public AppEntry getItem(int position) { return items.get(position); }
    @Override public long getItemId(int position) { return position; }

    @Override
    public View getView(int position, View convertView, ViewGroup parent) {
        Holder holder;
        if (convertView == null) {
            LinearLayout row = new LinearLayout(context);
            row.setOrientation(LinearLayout.HORIZONTAL);
            row.setGravity(Gravity.CENTER_VERTICAL);
            int pad = dp(10);
            row.setPadding(pad, pad, pad, pad);

            ImageView icon = new ImageView(context);
            row.addView(icon, new LinearLayout.LayoutParams(dp(44), dp(44)));

            LinearLayout textBox = new LinearLayout(context);
            textBox.setOrientation(LinearLayout.VERTICAL);
            LinearLayout.LayoutParams textLp = new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f);
            textLp.setMarginStart(dp(12));
            row.addView(textBox, textLp);

            TextView label = new TextView(context);
            label.setTextSize(16);
            label.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
            textBox.addView(label);

            TextView pkg = new TextView(context);
            pkg.setTextSize(12);
            pkg.setSingleLine(true);
            textBox.addView(pkg);

            TextView meta = new TextView(context);
            meta.setTextSize(12);
            textBox.addView(meta);

            holder = new Holder(icon, label, pkg, meta);
            row.setTag(holder);
            convertView = row;
        } else {
            holder = (Holder) convertView.getTag();
        }

        AppEntry app = getItem(position);
        holder.icon.setImageDrawable(app.icon);
        holder.label.setText(app.label);
        holder.pkg.setText(app.packageName);
        holder.meta.setText(app.typeLabel() + (app.enabled ? " • Enabled" : " • Disabled"));
        return convertView;
    }

    private int dp(int dp) {
        return Math.round(dp * context.getResources().getDisplayMetrics().density);
    }

    private static final class Holder {
        final ImageView icon;
        final TextView label;
        final TextView pkg;
        final TextView meta;
        Holder(ImageView icon, TextView label, TextView pkg, TextView meta) {
            this.icon = icon;
            this.label = label;
            this.pkg = pkg;
            this.meta = meta;
        }
    }
}
