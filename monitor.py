import redis
import sys

if __name__ == "__main__":
    r = redis.Redis(host='localhost', port=6379, db=0)
    ps = r.pubsub()
    ps.execute_command("monitor")
    while True:
        resp = ps.parse_response()
        parts = resp.split(" ")
        if len(parts) >= 4 and parts[1] == "\"SET\"":
            r.publish(parts[2], "")
            print "publishing:", parts[2]
