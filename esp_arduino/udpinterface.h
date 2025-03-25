// Project: UDP Interface Server
// SPDX-FileCopyrightText: 2025 Tamas Liszkai
// SPDX-License-Identifier: MIT

#pragma once

#ifdef UDP_INTERFACE

#include "cfg.h"

#include <cstdint>
#include <cstddef>
#include <type_traits>
#include <WiFi.h>
#include <AsyncUDP.h>

template <typename... Ts> class cxpr_string;

#endif // UDP_INTERFACE

class UdpInterface {
public:
    UdpInterface() = delete;

    static void init() {
#ifdef UDP_INTERFACE
        WiFi.mode(WIFI_STA);
        WiFi.begin(CFG::UDP::ssid, CFG::UDP::pswd);
        while (WiFi.status() != WL_CONNECTED) {
            delay(1000);
        }
        if (!udp.connect(IPAddress(CFG::UDP::server_ip), CFG::UDP::server_port)) {
            // TODO assert
        }
#endif // UDP_INTERFACE
    }

    template <typename... Ts>
    static inline void trace(Ts&&... arg) {
#ifdef UDP_INTERFACE
        trace_impl(cnt++, std::forward<Ts>(arg)...);
#endif // UDP_INTERFACE
    }

private:
#ifdef UDP_INTERFACE
    inline static AsyncUDP udp;
    inline static uint32_t cnt;

    template <typename... Ts>
    static inline void trace_impl(Ts&&... arg) {
        udp.printf(cxpr_string<Ts...>::value, std::forward<Ts>(arg)...);
    }
#endif // UDP_INTERFACE
};

#ifdef UDP_INTERFACE
// Source: https://stackoverflow.com/questions/72472069/wrap-cstdio-print-function-with-c-variadic-template
template<class T> struct format;
template<> struct format<int>                { static constexpr char const * spec = "%d ";  };
template<> struct format<short>              { static constexpr char const * spec = "%d ";  };
template<> struct format<long>               { static constexpr char const * spec = "%ld "; };
template<> struct format<long long>          { static constexpr char const * spec = "%lld "; };
template<> struct format<unsigned int>       { static constexpr char const * spec = "%u ";  };
template<> struct format<unsigned long>      { static constexpr char const * spec = "%lu "; };
template<> struct format<unsigned long long> { static constexpr char const * spec = "%llu "; };
template<> struct format<float>              { static constexpr char const * spec = "%f ";};
template<> struct format<double>             { static constexpr char const * spec = "%f ";};

template <typename... Ts>
class cxpr_string
{
public:
    constexpr cxpr_string() : buf_{}, size_{0}  {
        size_t i=0;
        ( [&]() {
            using T = std::remove_cv_t<std::remove_reference_t<Ts>>;
            const size_t max = size(format<T>::spec);
            for (int i=0; i < max; ++i) {
                buf_[size_++] = format<T>::spec[i];
            }
        }(), ...);
        buf_[size_++] = 0;
    }

    static constexpr size_t size(const char* s)
    {
        size_t i=0;
        for (; *s != 0; ++s) ++i;
        return i;
    }

    template <typename... Is>
    static constexpr size_t calc_size() {
        return (0 + ... + size(format<std::remove_cv_t<std::remove_reference_t<Is>>>::spec));
    }

    constexpr const char* get() const {
        return buf_;
    }

    static constexpr cxpr_string<Ts...> ref{};
    static constexpr const char* value = ref.get();
private:
    char buf_[calc_size<Ts...>()+1] = { 0 };
    size_t size_;
};

#endif // UDP_INTERFACE
