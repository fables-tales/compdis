import nextmatch
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def main():

    r.set("org.srobo.matches.currmatch", 0)
    next_match = nextmatch.get_next_match()
    print next_match
    ps = r.pubsub()
    ps.psubscribe("org.srobo.time*") 
    lg = ps.listen()
    for x in lg:
        if x["channel"] == "org.srobo.time":
            now = float(r.get(x["channel"]))
            if now > next_match["time"]:
                index = int(r.get("org.srobo.matches.currmatch"))
                index += 1
                r.set("org.srobo.matches.currmatch", index)
                next_match = nextmatch.get_next_match()

if __name__ == "__main__":
    main()
