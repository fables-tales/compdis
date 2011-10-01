import redis
import time
import threading

r = redis.Redis(host='localhost', port=6379, db=0)
started = False
start_time = None
offset = r.get("org.srobo.time.offset")
if offset is not None:
    offset = float(offset)
paused = False
quit = False

def interaction_thread():
    global quit
    global started
    global start_time
    global offset
    global paused
    global r
     
    if 1:
        quit = False
        while not quit:
            x = raw_input("timed> ");
            if x.lower() == "start":
                if started: print "already started the competition at:", start_time
                else:
                    start_competition()
            elif x.lower() == "pause":
                paused = True 
            elif x.lower() == "resume":
                paused = False
            elif x.lower() == "quit":
                quit = True
            elif x.lower() == "get":
                print r.get("org.srobo.time")
                print r.get("org.srobo.time.offset")
                print r.get("org.srobo.time.start")
            elif x.lower()[0:len("setstart")] == "setstart":
                #plus one because of the space
                offset = int(x.lower()[len("setstart") + 1:].strip())
                now = time.time()
                local_start_time = now + offset * 60
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
    global offset
    time_thread = threading.Thread(target=clock_thread)
    if r.get("org.srobo.time.offset") == None:
        start_time = r.get("org.srobo.time.start")
        offset = float(start_time)
    time_thread.start()

def clock_thread():
    global offset
    last = time.time()
    while not quit:
        r.set("org.srobo.time", time.time())
        if paused:
            offset += time.time() - last 
        r.set("org.srobo.time.offset", offset)
        last = time.time()
        time.sleep(1)


def main():
    interaction_thread()
if __name__ == "__main__":
    main()
