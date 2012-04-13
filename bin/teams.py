#!/usr/bin/env python
import sys
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

if __name__ == "__main__":
    teams = []
    teams.append({"real-name":"Lycee Argouges", "tla":"ARG", "number":1})
    teams.append({"real-name":"Bishop Wordsworth School", "tla":"BWS", "number":2})
    teams.append({"real-name":"Bishop Wordsworth School", "tla":"BWS2", "number":3})
    teams.append({"real-name":"Bristol Grammar School", "tla":"BGR", "number":4})
    teams.append({"real-name":"Brokenhurst College", "tla":"BRK", "number":5})
    teams.append({"real-name":"Bournemouth School for Girls", "tla":"BSG", "number":6})
    teams.append({"real-name":"Clifton High School", "tla":"CLF", "number":7})
    teams.append({"real-name":"Clifton High School", "tla":"CLF2", "number":8})
    teams.append({"real-name":"Lycee Emmanuel Mounier", "tla":"EMM", "number":9})
    teams.append({"real-name":"Gresham's", "tla":"GRS", "number":10})
    teams.append({"real-name":"Grey Matter Robotics", "tla":"GMR", "number":11})
    teams.append({"real-name":"Hills Road Sixth Form College", "tla":"HRS","number":12})
    teams.append({"real-name":"Hazelwick comprehensive School", "tla":"HZW","number":13})
    teams.append({"real-name":"Mirfield Free Grammar", "tla":"MFG", "number":14})
    teams.append({"real-name":"Munich", "tla":"MUC", "number":15})
    teams.append({"real-name":"Peter Symonds", "tla":"PSC","number":16})
    teams.append({"real-name":"Peter Symonds", "tla":"PSC2","number":17})
    teams.append({"real-name":"Queen Elizabeth's Hospital School", "tla":"QEH", "number":18})
    teams.append({"real-name":"Queen Mary's College", "tla":"QMC", "number":19})
    teams.append({"real-name":"Red maids bristol", "tla":"RMS", "number":20})
    teams.append({"real-name":"Southend School", "tla":"SEN", "number":21})
    teams.append({"real-name":"Southend School", "tla":"SEN2", "number":22})
    teams.append({"real-name":"St annes","tla":"STA","number":23})
    teams.append({"real-name":"Tauntons College", "tla":"TTN", "number":24})


    if len(sys.argv) == 2 and sys.argv[1] == "init":
        for x in teams:
            r.set("org.srobo.teams." + str(x["number"]) + ".tla", x["tla"])
            r.set("org.srobo.teams." + str(x["number"]) + ".org_name", x["real-name"])
            r.set("org.srobo.score.teams." + str(x["tla"]), 0)
        
    if len(sys.argv) == 4 and sys.argv[1] == "robotname":
        tla = sys.argv[2]
        description = sys.argv[3]
        found = False
        for i in xrange(0,25):
            check_tla = r.get("org.srobo.teams." + str(i) + ".tla")
            if check_tla != None and check_tla == tla:
                found = True
                print "found",tla,"updating their robot name"
                r.set("org.srobo.teams." + str(i) + ".robot_name", description)

        if not found:
            print "couldn't find team"


