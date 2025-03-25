# Project: UDP Interface Server
# SPDX-FileCopyrightText: 2025 Tamas Liszkai
# SPDX-License-Identifier: MIT

class TraceModel:
    def __init__(self, queue, period):
        self.queue = queue
        self.period = period
        self.t = []
        self.data = []
        self.controller = None
        self.data_points = 0
        self.visibility = set()

    def fetch_data(self):
        while self.queue.qsize():
            try:
                data = self.queue.get(0)
                if self.data_points != len(data):
                    self.reconfigure(len(data))
                self.t.append(data[0] * self.period)
                self.data.append(data[1:])
            except queue.Empty:
                pass

    def reconfigure(self, data_points):
        self.clear()
        self.data_points = data_points
        self.visibility = set(range(data_points - 1))
        if self.controller is not None:
            self.controller.reconfigure(data_points - 1)

    def clear(self):
        self.t = []
        self.data = []
