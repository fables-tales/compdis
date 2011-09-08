import redis
import sys

if __name__ == "__main__":
  r = redis.Redis(host='localhost', port=6379, db=0)
  ps = r.pubsub()
  ps.psubscribe("org.srobo*")
  last_time = 0
  last_offset = 0
  last_start = 0
  lg = ps.listen()
  for x in lg:
    print x["channel"], r.get(x["channel"])
