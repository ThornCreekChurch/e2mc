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


import elexio
import mailchimp
import log
import sys

debug = False
adds = []
deletes = []

def sync():
    global adds
    global deletes

    egroups = elexio.get_groups()
    mcgroups = mailchimp.get_groups()
    # Iterate through all groups found in elexio.  If any groups are missing
    #   from MailChimp, add it in.  Iterate through each group's membership as
    #   well.  If they are missing from the Mailchimp group, add them to an
    #   array that will be passed for a bulk update for addition.
    for egroup in egroups:
        if not mailchimp.group_exists(egroup['name']):
            if(debug):
                log.e2mclog("%s NOT found in MailChimp Groups" % egroup['name'])
            group_id = mailchimp.create_group(egroup['name'])
            if group_id > 0:
                log.e2mclog("%s created in MailChimp Groups: id #%d" % (egroup['name'], group_id))
            elif debug:
                log.e2mclog("%s found in mcgroups" % egroup['name'])
        else:
            if(debug):
                log.e2mclog("%s found in mcgroups" % egroup['name'])
            group_id = mailchimp.get_group_id(egroup['name'])

        eemails = elexio.get_group_email_list(egroup)
        for eemail in eemails:
            if not eemail == "":
                if not mailchimp.email_exists(egroup['name'], eemail):
                    if(debug):
                        log.e2mclog("\t%s NOT found in group %s" % (eemail, egroup['name']))
                    if(mailchimp.check_user(eemail) == "subscribed"):
                        adds.append(eemail)
                else:
                    if(debug):
                        log.e2mclog("\t%s found in group %s" % (eemail, egroup['name']))

        # Now iterate through MailChimp e-mail addresses to see if any have
        #   been removed from Elexio.
        memails = mailchimp.get_group_email_list(egroup['name'])
        for memail in memails:
            if not elexio.email_exists(egroup['name'], memail):
                if(debug):
                    log.e2mclog("\t%s NOT found in Elexio group %s" % (memail, egroup['name']))
                deletes.append(memail)
            
        if(len(adds) > 0 or len(deletes) > 0):
            log.e2mclog("Adds: %s" % adds)
            log.e2mclog("Deletes: %s" % deletes)
            response = mailchimp.update(group_id, adds, deletes)
            log.e2mclog("Updates for Group %s" % egroup['name'])
            log.e2mclog("Members Added:")
            for ma in response['members_added']:
                log.e2mclog("\t%s" % ma['email_address'])
            log.e2mclog("Total Added: %d" % response['total_added'])
            log.e2mclog("Members Deleted:")
            for md in response['members_removed']:
                log.e2mclog("\t%s" % md['email_address'])
            log.e2mclog("Total Deleted: %d" % response['total_removed'])
            log.e2mclog("Errors:")
            for error in response['errors']:
                log.e2mclog("%s:" % error['error'])
                for ea in error['email_addresses']:
                    log.e2mclog("\t%s" % ea)
            log.e2mclog("Total Errors: %d" % response['error_count'])
        else:
            log.e2mclog("No Adds or Deletes for Group %s" % egroup['name'])
        
        adds = []
        deletes = []



    # Iterate through all groups found in MailChimp.  If any groups are missing
    #   from Elexio, then the group will be deleted out of MailChimp.  Iterate
    #   through each group's membership as well.  If any are found in MailChimp
    #   that are not in Elexio, then add them to an array that will be passed
    #   for a bulk update for deletion.

    # Uncomment this section to have Segments removed from MailChimp that are
    #   not an Elexio Group.
    #for mcgroup in mcgroups:
    #   if not elexio.group_exists(mcgroup):
    #       if debug:
    #           log.e2mclog("MailChimp group %s NOT found in Elexio." % mcgroup['name'])
    #       log.e2mclog("MailChimp %s deleted.  E-mails that were in %s:" % (mcgroup['name'], mcgroup['name']))
    #       for email in mailchimp.get_group_email_list(mcgroup['name']):
    #           log.e2mclog("\t%s" % email)
    #       mailchimp.delete_group(mcgroup)
    #   else:
    #       if debug:
    #           log.e2mclog("MailChimp group %s found in Elexio." % mcgroup['name'])
    
    

log.open_log()
if len(sys.argv) > 1:
    for arg in sys.argv:
        if arg == '--debug':
            debug = True

if(debug):
    log.e2mclog("Debug mode enabled.")

elexio.init()
mailchimp.init()
egroups = elexio.get_groups()
if(debug):
    log.e2mclog("Elexio Group(s) identified...")
    if(len(egroups) == 0):
        log.e2mclog("None.")
    else:
        log.e2mclog(egroups)
mcgroups = mailchimp.get_groups()
if(debug):
    log.e2mclog("MailChimp Group(s) identified...")
    if(len(mcgroups)==0):
        log.e2mclog("None.")
    else:
        log.e2mclog(mcgroups)
if(debug):
    log.e2mclog("Syncing...")
sync()
if(debug):
    log.e2mclog("Synchronization complete.")
log.close_log()

