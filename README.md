# UDP Interface

A simple interface and python tool (UDP server) to trace and control an ESP32 device with Arduino framework over WiFI.

## Getting Started

### Dependencies

* python
* esp32 project with Arduino framework

### Usage

* In the ESP32 firmware code create a cfg.h file to configure the WiFI and server parameters.

``` c++
#include <cstdint>

namespace CFG {

namespace UDP {
    constexpr const char* ssid = "SSID";
    constexpr const char* pswd = "PASSWORD";
    constexpr const uint8_t server_ip[] = {192, 168, 0, 1};
    constexpr uint32_t server_port = 20001;
}
```

* In your code you can then initialize the interface and can trace any variable.

``` c++
#include "udpinterface.h"

uint8_t var1;
float var2;
int32_t var3;

void setup()
{
    UdpInterface::init();
}

void loop()
{
    UdpInterface::trace(var1, var2, var3);
    delay(10);
}

```

* On your PC just start the server with main.py

``` sh
python main.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details
