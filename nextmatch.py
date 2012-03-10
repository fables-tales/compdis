import redis

match_length = 180

r = redis.Redis(host='localhost', port=6379, db=0)

def get_next_match():
    global r;
    len = r.llen("org.srobo.matches") 
    comptime = float(r.get("org.srobo.time.competition"))
    for i in xrange(0, len):
        v = r.lindex("org.srobo.matches", i)
        match = match_from_ms(v)
        if match["time"] > comptime+match_length:
            return match

    return match_from_ms(r.lindex("org.srobo.matches", index))

def get_current_match():
    global r;
    len = r.llen("org.srobo.matches") 
    comptime = float(r.get("org.srobo.time.competition"))
    for i in xrange(0, len):
        v = r.lindex("org.srobo.matches", i)
        match = match_from_ms(v)
        upper = match["time"] + match_length
        lower = match["time"]
        if comptime > lower and comptime < upper:
            return match

def match_from_ms(ms):
    match = ms.split(",")
    match_dict = {"time": float(match[0]),
                  "teams": [ int(x) for x in match[1:-1]]}
    match_dict["number"] = match[-1]
    return match_dict

if __name__ == "__main__":
    time = r.get("org.srobo.time.competition")
    print time
    print get_current_match()
    print get_next_match()
