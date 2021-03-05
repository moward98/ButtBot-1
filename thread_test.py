import time 
from threading import Thread
from queue import Queue
import motor_driver
import smbus2

def motor_send(out_q, speed, duration, direction):
    data = [0,0,0]
    data[0] = speed
    data[1] = duration 
    data[2] = direction 
    out_q.put(data)

def consumer(in_q):
    while True:
        data = in_q.get()
        print("in here")
        mc.fwd_bwd(data[0], data[2])
        time.sleep(data[1])
        print("leaving")
        mc.stop()
        

bus = smbus2.SMBus(0)
mc = motor_driver.MotorDriver(bus)

q = Queue()
t1 = Thread(target = consumer, args = (q, ))
t1.start()

while True:
    info = input('Enter Speed and Time ')
    input_dims = info.split()
    speed = int(input_dims[0])
    dur = int(input_dims[1])
    print("speed is", speed)
    print("duration is", dur)
    motor_send(speed, dur, 'fwd')
    time.sleep(dur)

