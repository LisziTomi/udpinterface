# Project: UDP Interface Server
# SPDX-FileCopyrightText: 2025 Tamas Liszkai
# SPDX-License-Identifier: MIT

import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.widgets import Cursor

class TraceView(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ctrl_panel = ControlFrame(self)
        self.ctrl_panel.pack(side=tk.TOP, fill=tk.X)

        self.panes = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.panes.pack(fill=tk.BOTH, expand=1)

        self.data_list = DataFrame(self.panes)
        self.panes.add(self.data_list, width=300, minsize=100)

        self.plot = PlotFrame(self.panes)
        self.panes.add(self.plot, minsize=100)

    def prepare(self, nb_lines):
        self.plot.prepare(nb_lines)
        self.data_list.prepare(nb_lines)

    def update_data(self, t, data, visibility):
        self.plot.update_data(t, data, visibility)
        if len(t) > 0:
            self.data_list.update_data(t[-1], data[-1])
        else:
            self.data_list.clear_data()

    def clear(self):
        self.plot.clear()
        self.data_list.clear()


class ControlFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.clear_btn = tk.Button(self, text="Clear data")
        self.clear_btn.pack(side=tk.LEFT, padx=5, pady=5)

        validate = (self.register(self.validate_entry))
        tk.Label(self, text=" s").pack(side=tk.RIGHT, pady=10)
        self.time_window_var = tk.StringVar()
        self.time_window_var.set("5") #TODO

        self.entry = tk.Entry(self, textvariable=self.time_window_var, justify='right', validate='all', validatecommand=(validate, '%P'))
        self.entry.pack(side=tk.RIGHT)

        tk.Label(self, text="Time window:").pack(side=tk.RIGHT, pady=10)

    def validate_entry(self, P):
        return str.isdigit(P) or P == ""


class PlotFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.time_window = 5 # TODO

        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.grid()
        self.lines = []

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()

        self.cursor = Cursor(self.ax, useblit=True, color='red', linewidth=1)

        self.refresh()

    def prepare(self, nb_lines):
        self.clear()
        for i in range(nb_lines):
            self.lines.extend(self.ax.plot([], []))

    def update_data(self, t, data, visibility):
        for i, line in enumerate(self.lines):
            line.set_xdata(t)
            line.set_ydata([row[i] for row in data])
            line.set_visible(i in visibility)

        self.rescale(t)
        self.refresh()

    def rescale(self, t):
        self.ax.relim(True)
        self.ax.autoscale()
        if len(t) > 0:
            x_min = max(t[0], t[-1] - self.time_window)
            x_max = max(x_min + self.time_window, t[-1])
            self.ax.set_xlim(x_min, x_max)


    def refresh(self):
        self.canvas.draw()
        self.fig.canvas.flush_events()

    def clear(self):
        for line in self.lines:
            line.remove()
        self.lines = []


class DataFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_entries = []
        self.time_entry = TimeEntry(self, height=300)
        self.time_entry.pack(fill=tk.X, padx=5, pady=2)
        self.on_visibility_toggle_cb = None

    def prepare(self, nb_lines):
        self.clear()
        for i in range(nb_lines):
            entry = DataEntry(self, i, self.on_visibility_toggle, height=300)
            entry.pack(fill=tk.X, padx=5, pady=2)
            self.data_entries.append(entry)

    def update_data(self, t, data):
        self.time_entry.set_value(t)
        for i, entry in enumerate(self.data_entries):
            entry.set_value(data[i])

    def clear(self):
        for entry in self.data_entries:
            entry.destroy()
        self.data_entries = []
        self.time_entry.set_value(0)

    def clear_data(self):
        self.time_entry.set_value(0)
        for entry in self.data_entries:
            entry.set_value(0)

    def on_visibility_toggle(self, idx, en):
        if self.on_visibility_toggle_cb is not None:
            self.on_visibility_toggle_cb(idx, en)



class TimeEntry(tk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(borderwidth=1, relief=tk.SOLID, padx=5)

        self.text = tk.StringVar()
        self.text.set("0 s")
        tk.Label(self, text="t:").pack(side=tk.LEFT)
        label = tk.Label(self, textvariable=self.text, anchor='w')
        label.pack(side=tk.LEFT, fill=tk.X, expand=1)

    def set_value(self, value):
        self.text.set("{:.2f} s".format(value))


class DataEntry(tk.Frame):
    def __init__(self, parent, idx, cb, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.idx = idx
        self.config(borderwidth=2, relief=tk.RIDGE)
        self.cb = cb

        tk.Label(self, text="{}:".format(idx)).pack(side=tk.LEFT)
        self.text = tk.StringVar()
        self.text.set("....")
        label = tk.Label(self, textvariable=self.text, anchor='w')
        label.pack(side=tk.LEFT, fill=tk.X, expand=1)

        self.enabled = tk.BooleanVar(value=True)
        self.checkbox = tk.Checkbutton(self, variable=self.enabled, command=self.on_checkbox_toggle)
        self.checkbox.pack(side=tk.RIGHT)

    def set_value(self, value):
        self.text.set("{:.4f}".format(value))

    def on_checkbox_toggle(self):
        if self.cb is not None:
            self.cb(self.idx, self.enabled.get())
