import time
import zmq
import math

# ZeroMQ Context
context = zmq.Context()

# Define the socket using the "Context"
game1 = context.socket(zmq.REP)
game1.bind("tcp://127.0.0.1:9001")
game2 = context.socket(zmq.REP)
game2.bind("tcp://127.0.0.1:9002")

seconds = 10

while True:
    print "Time left: %ss" % seconds
    print game1.recv()
    print game2.recv()
    game1.send("%s" % (int(math.ceil(seconds))))
    game2.send("%s" % (int(math.ceil(seconds))))
    seconds -= 0.2
    time.sleep(0.2)
    if seconds < 0.1:
        print game1.recv()
        print game2.recv()
        game1.send("0")
        game2.send("0")
        p1 = game1.recv()
        p2 = game2.recv()
        if "option:" in p1 and "option:" in p2:
            p1 = int(p1.split(':')[1])
            p2 = int(p2.split(':')[1])
            game1.send("win")
            game2.send("loss")
        seconds = 10
        time.sleep(2)
