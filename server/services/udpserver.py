# Project: UDP Interface Server
# SPDX-FileCopyrightText: 2025 Tamas Liszkai
# SPDX-License-Identifier: MIT

import socket
import threading
import queue

BUFFER_SIZE = 4096

class UdpServer:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.queue = queue.Queue()

        self.socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.socket.bind((ip, port))

    def run(self):
        self.thread = threading.Thread(target=self._worker_thread, daemon=True)
        self.thread.start()

    def _worker_thread(self):
        while True:
            message, address = self.socket.recvfrom(BUFFER_SIZE)
            data = list(map(float, message.decode('utf-8').split()))
            self.queue.put(data)
