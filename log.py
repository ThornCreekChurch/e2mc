from datetime import datetime

file = None
timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')

def open_log():
    global file
    file = open("e2mc.log", "a+")
    # Comment the above line and uncomment the line below if you want a log file
    #   for each run of the sync
    #file = open("e2mc.log.%s" % timestamp, "w")

def close_log():
    global file
    file.close()

def e2mclog(message):
    file.write("%s: %s\n" % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), message))
