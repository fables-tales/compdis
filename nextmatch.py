import redis

match_length = 60*7 
STATE_ENTER = 0x01
STATE_BOOT  = 0x02
STATE_LIVE  = 0x04
STATE_SCORE = 0x08
import time


r = redis.Redis(host='localhost', port=6379, db=0)

def get_next_match():
    global r;
    len = r.llen("org.srobo.matches") 
    comptime = float(r.get("org.srobo.time.competition"))
    for i in xrange(0, len):
        v = r.lindex("org.srobo.matches", i)
        match = match_from_ms(v)
        if match["time"] > comptime and match["time"] < comptime + match_length:
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

def get_current_state():
    global r
    current_match = get_current_match()
    comptime = float(r.get("org.srobo.time.competition"))
    into_match = comptime-current_match["time"]
    minute = into_match/60
    if minute <= 1:
        return STATE_ENTER
    elif minute > 1 and minute <= 2:
        return STATE_BOOT
    elif minute > 2 and minute <= 5:
        return STATE_LIVE
    elif minute > 5 and minute <= 7:
        return STATE_SCORE

    
def match_from_ms(ms):
    match = ms.split(",")
    match_dict = {"time": float(match[0]),
                  "teams": [ int(x) for x in match[1:-1]]}
    match_dict["number"] = match[-1]
    return match_dict

def match_to_ms(match):
    str_teams = []
    teams = match["teams"]
    for x in teams:
        str_teams.append(str(x))
    return str(match["time"]) + "," + ",".join(str_teams) + "," + str(match["number"])

if __name__ == "__main__":
    ps = r.pubsub()
    ps.psubscribe("org.srobo.time.competition") 
    lg = ps.listen()
    for message in lg:
        ctime = r.get("org.srobo.time.competition")
        print ctime
        print get_current_match()
        print get_next_match()
        print get_current_state()
        r.set("org.srobo.matches.current", match_to_ms(get_current_match()))
        r.set("org.srobo.matches.next", match_to_ms(get_next_match()))
        r.set("org.srobo.matches.state", get_current_state())
