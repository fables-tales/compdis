import redis
import time
import threading

r = redis.Redis(host='localhost', port=6379, db=0)
started = False
start_time = None
offset = float(r.get("org.srobo.time.offset"))
paused = False
quit = False

def interaction_thread():
  global quit
  global started
  global start_timoe
  global offset
  global paused
  global r
   
  try:
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
  except:
    quit = True
    
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
    r.publish("org.srobo.time", "")
    r.publish("org.srobo.time.offset", "")
    last = time.time()
    time.sleep(1)


def main():
  interaction_thread()
if __name__ == "__main__":
  main()
