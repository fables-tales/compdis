import redis
import time
import threading

r = redis.Redis(host='localhost', port=6379, db=0)
started = False
start_time = None
pause_time = 0
paused = False
quit = False

def interaction_thread():
    global quit
    global started
    global start_time
    global paused
    global r

    quit = False
    while not quit:
        x = raw_input("timed> ");
        if x.lower() == "start":
            if started: print "already started the competition at:", start_time
            else:
                started = True
                start_competition()
        elif x.lower() == "pause":
            paused = True 
        elif x.lower() == "resume":
            paused = False
        elif x.lower() == "quit":
            quit = True
        elif x.lower() == "get":
            print r.get("org.srobo.time.real")
            print r.get("org.srobo.time.competition")
            print r.get("org.srobo.time.start")
        elif x.lower()[0:len("setstart")] == "setstart":
            #plus one because of the space
            diff = int(x.lower()[len("setstart") + 1:].strip())
            now = time.time()
            local_start_time = now + diff * 60
            r.set("org.srobo.time.start", local_start_time)
             
        elif x.lower() == "help":
            print "this is timed"
            print "the commands are"
            print "- start: start the timed clock, requires org.srobo.time.start to exist"
            print "- pause: pause the timed clock"
            print "- resume: resume the timed clock"
            print "- quit: quit timed"
            print "- setstart: sets the start time of the competition, offset in minutes"
    
time_thread = None

def start_competition():
    global time_thread
    global start_time
    time_thread = threading.Thread(target=clock_thread)
    start_time = float(r.get("org.srobo.time.start"))
    if start_time == None:
        print "the start time for the competiton has not been set" 
        print "to set it, create a key in redis \"org.srobo.time.start\""
        print "with a value equal to the unix time of the start of the competition"
        exit() 
    time_thread.start()

def clock_thread():
    global pause_time
    global start_time
    last = time.time()
    while not quit:
        r.set("org.srobo.time.real", time.time())
        if paused:
            pause_time += time.time() - last 
        r.set("org.srobo.time.competition", time.time() - pause_time - start_time)
        last = time.time()
        time.sleep(1)


def main():
    interaction_thread()
if __name__ == "__main__":
    main()
