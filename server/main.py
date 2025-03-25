# Project: UDP Interface Server
# SPDX-FileCopyrightText: 2025 Tamas Liszkai
# SPDX-License-Identifier: MIT

from udpinterface import UdpInterface

CFG = {
    "IP": "0.0.0.0",
    "PORT": 20001,
    "REFRESH_RATE_MS": 50,
    "TRACE_PERIOD_S": 0.005
}

def main():
    app = UdpInterface(CFG)
    app.mainloop()

if __name__ == "__main__":
    main()
