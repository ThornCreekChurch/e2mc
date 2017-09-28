from datetime import datetime

file = None

def open_log():
    global file
    file = open("e2mc.log", "w")

def close_log():
    global file
    file.close()

def e2mclog(message):
    file.write("%s: %s\n" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), message))
