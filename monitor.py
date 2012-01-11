import redis
import sys


write_messages = ['"SET"', '"RPUSH"', '"LPUSH"']

if __name__ == "__main__":
    r = redis.Redis(host='localhost', port=6379, db=0)
    ps = r.pubsub()
    ps.execute_command("monitor")
    while True:
        resp = ps.parse_response()
        parts = resp.split(" ")
        if len(parts) >= 4 and (parts[1] in write_messages):
            r.publish(parts[2].replace("\"",""), "")
            print "publishing:", parts[2]
