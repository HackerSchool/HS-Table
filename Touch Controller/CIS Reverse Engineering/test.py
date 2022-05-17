import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)

PIN_CLK = 21    # Clock Pin (Yellow)
PIN_PS = 26     # Pulse Pin (Orange)
N_PIXELS = 1400  # Number of Pixels in sensor
PS_CYCLES = 5  # Number of clock cycles the pulse signal stays on
# CLK_TIME = .1  # Period of clock signal (seconds)
CLK_TIME = .01  # Period of clock signal (seconds)
CLK_DUTY = .5 # Clock duty cicle


GPIO.setup(PIN_CLK, GPIO.OUT)
GPIO.setup(PIN_PS, GPIO.OUT)

while True:
    GPIO.output(PIN_CLK, GPIO.HIGH)
    GPIO.output(PIN_PS, GPIO.HIGH)
    # print("pulse on")
    sleep(CLK_TIME*CLK_DUTY)

    GPIO.output(PIN_CLK, GPIO.LOW)
    sleep(CLK_TIME*(1-CLK_DUTY))

    for i in range(N_PIXELS):

        if PS_CYCLES - 1 == i:
            GPIO.output(PIN_PS, GPIO.LOW)
            # print("pulse off")

        GPIO.output(PIN_CLK, GPIO.HIGH)
        sleep(CLK_TIME*CLK_DUTY)

        GPIO.output(PIN_CLK, GPIO.LOW)
        sleep(CLK_TIME*(1-CLK_DUTY))

