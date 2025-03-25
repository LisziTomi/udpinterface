# Project: UDP Interface Server
# SPDX-FileCopyrightText: 2025 Tamas Liszkai
# SPDX-License-Identifier: MIT

class TraceController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.model.controller = self

        self.bind_events()

    def bind_events(self):
        self.view.ctrl_panel.clear_btn.config(command=self.on_clear)
        self.view.ctrl_panel.entry.bind('<Return>', self.on_time_window_change)
        self.view.ctrl_panel.entry.bind('<FocusOut>', self.on_time_window_change)
        self.view.data_list.on_visibility_toggle_cb = self.on_visibility_toggle

    def periodic_update(self):
        self.model.fetch_data()
        self.view.update_data(self.model.t, self.model.data, self.model.visibility)

    def reconfigure(self, data_points):
        self.view.prepare(data_points)

    def on_clear(self):
        self.model.clear()
        self.view.update_data(self.model.t, self.model.data, self.model.visibility)

    def on_time_window_change(self, event):
        try:
            self.view.plot.time_window = int(self.view.ctrl_panel.time_window_var.get())
        except ValueError:
            self.view.ctrl_panel.time_window_var.set(str(self.view.plot.time_window ))

    def on_visibility_toggle(self, idx, en):
        if en:
            self.model.visibility.add(idx)
        else:
            self.model.visibility.remove(idx)
