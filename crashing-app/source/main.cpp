#include "mbed-drivers/mbed.h"

static void blinky(void) {
    static DigitalOut led(LED1);
    led = !led;
    printf("LED = %d \r\n",led.read());
}

static void crash(void) {
    *(uint32_t * )NULL = 0xDEADBEEF;
}

void app_start(int, char**) {
    minar::Scheduler::postCallback(blinky).period(minar::milliseconds(500));
    
    minar::Scheduler::postCallback(crash).delay(minar::milliseconds(2300));
}
