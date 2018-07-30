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

import json
import requests
import log

elexio_url    = "YOUR_ELEXIO_API_URL"

# Reomved the use of the userID and password to get a new session ID every run.
#   Instead, visit your api section and get your session ID. Go to:
#   https://YOURCHURCH.elexiochms.com/api_documentation#!/user/userLogin_post_0
#   Login with our ID for the API and get the session ID. Then put it in the
#   Variable below.
#
#   I have left the old code in case you want to use it for some reason.

#elexio_userid = "YOUR_ELEXIO_API_USER"
#elexio_passwd = "YOUR_ELEXIO_API_PASSWORD"
elexio_session_id = "YOUR_ELEXIO_API_SESSION_ID"

# This automation is a quick utility and therefore does not assume any changes
#   will be made while it's running.  To speed up the process even further, it
#   reduces the # of queries to the site by storing the previously queried
#   information in json arrays/objects. The likelihood of values being changed
#   while this is running is very low, and even if such a change does occur, it
#   will be picked up next time it runs.

session_id = elexio_session_id
groups = []
group_members = {}

#def init():
    #global session_id
    #session_params = { "username": elexio_userid, "password": elexio_passwd }
    #session = requests.get((elexio_url + "/user/login"), params=session_params)
    #session_id = session.json()['data']['session_id']
    #return True


def get_groups():
    global groups
    global session_id
    if groups == []:
        groups_params = { "session_id": session_id }
        groups_response = requests.get(elexio_url + "/groups/sync", params=groups_params)
        groups = groups_response.json()['data']
    return groups


def group_exists(group):
    global group_members

    egroups = get_groups
    for g in groups:
        if group['name'] == g['name']:
            return True
    return False


def get_group_email_list(group):
    global group_members
    global session_id

    e = []
    if not group['name'] in group_members:
        groups_params = { "session_id": session_id }
        people = requests.get(elexio_url + "/groups/" + str(group['gid']) + "/people", params=groups_params).json()['data']
        for letter in people:
            for entry in people[letter]:
                if(not entry['mail'] == ""):
                    e.append(entry['mail'])
        group_members[group['name']] = e
    return e


def email_exists(group_name, email):
    global group_members

    if group_name in group_members:
        for g in group_members[group_name]:
            if email == g:
                log.e2mclog("email %s found in group_members[%s]" % (email, group_name))
                return True
        log.e2mclog("email %s NOT found in group_members[%s]" % (email, group_name))
        return False
    log.e2mclog("group %s NOT found in elexio.group_members" % group_name)
    return False

    if segment_id not in group_members:
        group_members[segment_id] =  client.lists.segments.members.all(tc_list_id, segment_id, get_all=True)['members']
    for member in group_members[segment_id]:
        if(email == member['email_address']):
            return True
    return False
