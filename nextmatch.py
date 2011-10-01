import redis

r = redis.Redis(host='localhost', port=6379, db=0)

def get_next_match():
    global r;
    match = r.lindex("org.srobo.matches", 0).split(",")
    match_dict = {"time": float(match[0]),
                  "teams": [ int(x) for x in match[1:]]}
    return match_dict

if __name__ == "__main__":
    print get_next_match()
    
