import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def get_next_match():
    global r;
    index = int(r.get("org.srobo.matches.currmatch"))+1
    return match_from_ms(r.lindex("org.srobo.matches", index))


def get_current_match():
    global r;
    index = int(r.get("org.srobo.matches.currmatch"))
    return match_from_ms(r.lindex("org.srobo.matches", index))

def match_from_ms(ms):
    match = ms.split(",")
    match_dict = {"time": float(match[0]),
                  "teams": [ int(x) for x in match[1:]]}
    return match_dict

if __name__ == "__main__":
    print get_next_match()
    
