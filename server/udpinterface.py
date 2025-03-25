# Project: UDP Interface Server
# SPDX-FileCopyrightText: 2025 Tamas Liszkai
# SPDX-License-Identifier: MIT

import tkinter as tk
from services.udpserver import UdpServer
from models.tracemodel import TraceModel
from views.traceview import TraceView
from controllers.tracecontroller import TraceController

class UdpInterface(tk.Tk):
    def __init__(self, cfg, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cfg = cfg

        self.wm_title("UDP Interface")

        self.udpserver = UdpServer(self.cfg["IP"], self.cfg["PORT"])
        self.trace_model = TraceModel(self.udpserver.queue, self.cfg["TRACE_PERIOD_S"])
        self.trace_view = TraceView()
        self.trace_controller = TraceController(self.trace_model, self.trace_view)

        self.trace_view.pack(fill=tk.BOTH, expand=1)

        self._start()


    def _start(self):
        self.udpserver.run()
        self._update()


    def _update(self):
        self._update_impl()
        self.after(self.cfg["REFRESH_RATE_MS"], self._update)


    def _update_impl(self):
        self.trace_controller.periodic_update()
