#include "mbed-drivers/mbed.h"

static void my_loop_function(void) {
    uint8_t turns = 20;

    while(turns-- > -1) {
        wait_ms(5);
    }
}


void app_start(int, char**) {
    minar::Scheduler::postCallback(my_loop_function).delay(minar::milliseconds(500));
}
