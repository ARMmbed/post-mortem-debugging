# Debugging a crashed device with mbed OS and uVision 5

When it comes to programming microcontrollers the one scenario that you never want to face is a device that suddenly hangs. It's already very frustrating while you're developing software, and tracing down these bugs can be very time-consuming; it's even worse when the device is already deployed in the field. Replicating the exact conditions in which the device failed can be almost impossible in the lab, especially when the failure manifestates itself after months.

Fortunately mbed-enabled hardware ships with [CMSIS-DAP](https://developer.mbed.org/handbook/CMSIS-DAP) or it's successor DAPLink, which allows you to directly hook into devices via the built-in USB ports (on developer boards), or via a debugging probe like [SWDAP](https://developer.mbed.org/teams/mbed/wiki/SWDAP). CMSIS-DAP is responsible for mounting your mbed OS board as a mass-storage device for easy flashing, but it can also be used to dump the RAM and ROM of a running device, thus enabling you to do post-mortem debugging on a crashed device.

In this blog post we'll show you how to install all dependencies, crash a device, and subsequently do a post-mortem debug session. To follow along you'll need:

1. [A development board](https://www.mbed.com/en/development/hardware/boards/) capable of running mbed OS.
1. [yotta](http://yottadocs.mbed.com/#installing) - to build faulty firmware.
1. [ARM KEIL uVision 5](http://www2.keil.com/mdk5/install/) - to load the debug session.

This article assumes knowledge of building applications for mbed OS. If you're unfamiliar with mbed OS, read [Running your first mbed OS application](https://docs.mbed.com/docs/getting-started-mbed-os/en/latest/FirstProjectmbedOS/) first.

## Creating a program that crashes

Here's an application that writes to a pointer at address 0x0 when the button at `SW2` is triggered. In most devices the ROM starts at address 0x0, and writing to ROM is not allowed, so the core hard faults.

```cpp
#include "mbed-drivers/mbed.h"

// change this to reflect a button on your own board
static InterruptIn btn(SW2);

static void blinky(void) {
    static DigitalOut led(LED1);
    led = !led;
}

static void btn_interrupt() {
    *(uint16_t*)0 = 0xDEAD;
}

void app_start(int, char**) {
    minar::Scheduler::postCallback(blinky).period(minar::milliseconds(500));

    btn.fall(&btn_interrupt);
}
```

Build this application with debug symbols enabled (via `yt build -d`) and flash it on your device. The LED should start blinking until you hit `SW2` and the device freezes.

## Starting a post-mortem debug session

For convenience we created a Python script which can pull the data off the device, and create a uVision 5 project in a single command. Download [dump-firmware.py](https://github.com/janjongboom/mbed-post-mortem-debugging/blob/master/crashing-app/dump_firmware.py) and store it in the same directory as your mbed OS project.

> If you use virtualenv to run yotta, run this script in the same virtualenv environment. On Windows, run this script from 'Run yotta' in your start menu.
