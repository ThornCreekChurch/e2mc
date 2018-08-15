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


from mailchimp3 import MailChimp
import json
import log
import hashlib

client = MailChimp(mc_api='YOUR_MC_API_KEY', mc_user='YOUR_MC_USER')
list_id = 'YOUR_MC_LIST_ID'

# Using the term "groups" in this module to keep the API between the elexio &
#   mailchimp modules.  In this module, groups actually refers to segments
#   within the list within MailChimp.

# This automation is a quick utility and therefore does not assume any changes
#   will be made while it's running.  To speed up the process even further, it
#   reduces the number of queries to the site by storing the previously queried
#   information in json arrays/objects. The likelihood of values being changed
#   while this is running is very low, and even if such a change does occur, it
#   will be picked up next time it runs.

groups = {}
group_members = {}

# Currently no initialization needed for mailchimp.  Don't do anything.
def init():
    return True


def get_groups():
    global groups
    if groups == {}:
        mc_group_response = client.lists.segments.all(list_id, get_all=True)
        groups = mc_group_response['segments']
    return groups


def create_group(group_name):
    mc_response = client.lists.segments.create(list_id, { 'name' : group_name, 'static_segment': [] })
    if mc_response['type'] == "static":
        groups.append(mc_response)
        return mc_response['id']
    else:
       log.e2mclog("Error creating new group in Mailchimp: %s : %s" % (mc_response['title'], mc_response['detail'])) 
       return 0


def delete_group(group):
    mc_response = client.lists.segments.delete(list_id, group['id'])
    log.e2mclog(mc_response)
    if not (mc_response == None):
        log.e2mclog("\t%s: %s" % (mc_response['status'], mc_response['detail']))


def group_exists(group_name):
    groups = get_groups()
    for group in groups:
        if (group_name == group['name']):
            return True
    return False


def get_group_id(group_name):
    global groups
    for group in groups:
        if(group_name == group['name']):
            return group['id']
    return 0


def load_emails(group_name):
    global group_members
    session_id = get_group_id(group_name)
    group_members[group_name] =  client.lists.segments.members.all(list_id, session_id, get_all=True)['members']


def get_group_email_list(group_name):
    global group_members
    emails = []

    if group_name not in group_members:
        load_emails(group_name)
    for member in group_members[group_name]:
        emails.append(member['email_address'])
    return emails


def email_exists(group_name, email):
    global group_members
    if group_name not in group_members:
        load_emails(group_name)

    for member in group_members[group_name]:
        if(email == member['email_address']):
            return True
    return False


def delete_email(group_name, email):
    log.e2mclog("Delete email requested:  Group: %s, E-mail: %s" % (group_name, email))


def update(group_id, adds, deletes):
    return client.lists.segments.update_members(list_id, group_id, data={ 'members_to_add': adds, 'members_to_remove': deletes })

def check_user(email):
    ehash = hashlib.md5(email.encode('utf-8')).hexdigest()
    try:
        user = client.lists.members.get(list_id, ehash)
    except:
        log.e2mclog("%s is not in MailChimp list. Can't add to segment" % email)
        return "failed"
    log.e2mclog("%s is status of %s" % (email, user['status']))
    return user['status']
