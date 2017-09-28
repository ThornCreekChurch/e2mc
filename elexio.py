import json
import requests
import log

elexio_url    = "YOUR_ELEXIO_API_URL"
elexio_userid = "YOUR_ELEXIO_API_USER"
elexio_passwd = "YOUR_ELEXIO_API_PASSWORD"

# This automation is a quick utility and therefore does not assume any changes
#   will be made while it's running.  To speed up the process even further, it
#   reduces the # of queries to the site by storing the previously queried
#   information in json arrays/objects. The likelihood of values being changed
#   while this is running is very low, and even if such a change does occur, it
#   will be picked up next time it runs.

session_id = None
groups = []
group_members = {}

def init():
    global session_id
    session_params = { "username": elexio_userid, "password": elexio_passwd }
    session = requests.get((elexio_url + "/user/login"), params=session_params)
    session_id = session.json()['data']['session_id']
    return True


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

    if not group['name'] in group_members:
        groups_params = { "session_id": session_id }
        people = requests.get(elexio_url + "/groups/" + str(group['gid']) + "/people", params=groups_params).json()['data']
        e = []
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
