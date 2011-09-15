import redis
import sys

if __name__ == "__main__":
  r = redis.Redis(host='localhost', port=6379, db=0)
  ps = r.pubsub()
  ps.execute_command("monitor")
  while True:
    print ps.parse_response()

