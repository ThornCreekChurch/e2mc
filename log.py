##  Copyright (C) 2017  ThornCreek Church
##
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
##
##  You should have received a copy of the GNU General Public License
##  along with this program.  If not, see <http://www.gnu.org/licenses/>
##
##  Contact:
##          Jeremy Lyon <jeremy.lyon@thorncreek.church>
##          ThornCreek Church
##          PO Box 1282, Eastlake, CO 80614


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
