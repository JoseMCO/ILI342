import time
import zmq
import math
import sys

# 0 -> tie, 1 -> p1, 2 -> p2
winners = [
    # Fire Grass Light Fight Water   P1/P2
    [  0,     2,   1,    2,    1  ], # Fire
    [  1,     0,   2,    1,    2  ], # Grass
    [  2,     1,   0,    1,    2  ], # Light
    [  1,     2,   2,    0,    1  ], # Fight
    [  2,     1,   1,    2,    0  ], # Water
]
ip = "127.0.0.1"
if len(sys.argv) > 1:
	ip = sys.argv[1]

# ZeroMQ Context
context = zmq.Context()

# Define the socket using the "Context"
game1 = context.socket(zmq.REP)
game1.bind("tcp://%s:9001" % ip)
game2 = context.socket(zmq.REP)
game2.bind("tcp://%s:9002" % ip)

seconds = 10

while True:
    print "Time left: %ss" % seconds
    print "9001: %s" % game1.recv()
    print "9002: %s" % game2.recv()
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
            win = winners[p2][p1]
            if win==1:
                game1.send("win")
                game2.send("loss")
            elif win==2:
                game1.send("loss")
                game2.send("win")
            else:
                game1.send("tie")
                game2.send("tie")
        seconds = 10
        time.sleep(2)
