# e2mc
e2mc is a tool that will allow you to sync Elexio Community groups to a single MailChimp list as segments.

Currently the Elexio Community sync to MailChimp service can only sync any number of groups to a single list. It is possible to setup a sync to a list, then remove it and add a sync to another list, but this will allow duplicates in lists to cause you to need to pay for more users than you really have.

The solution is then to sync all or a certain set of groups that encompass all of your current church members and then use this intermediate program to sync Elexio groups to MailChimp segments. This allows for one list in MailChimp and emails can be in multiple segments.

This application is new and has only been tested in a limited environment. Please send any feedback to jeremy.lyon@thorncreek.church.

## Prerequisites
### MailChimp
You must have an account in MailChimp with an API key. The key can be created under the Account area under the Extras menu. Protect your API key to avoid any unauthorized changes to your lists and subscibers.

You will need your List ID. This can be found under the List -> Settings menu.

### Elexio Community
You will need an Elexio Community API Session ID. You can obtain the Session ID from the API documention site.  The URL is usually `https://YOUR_SHORT_NAME.elexiochms.com/api_documentation#!/user/userLogin_post_0`. Contact Elexio support if you need help identifying your API URL.

You will need a username and password that will have access to the groups that you want to sync as segments. I recommend you create an "API User" that is only used for this purpose.

I recommend that you first create a permission role called "API Access". It needs "view members" access to the groups you want to sync. This is a good way to make sure you only create segments that you actually need in MailChimp. Finally, add the API User to this role.

### System to run the program
#### Operating System
I have tested and run this sync program on a Linux system (Fedora 24), however it should run on any system that can run Python applications. As I get more feedback on successful tests, I will add the OS to the list below.

Tested Operating Systems:
- Fedora 24

#### Python
This application is written in Python. It has been tested successfully with using Python 2.7.13 and 3.5.3.

This application requires the [python-mailchimp-api](https://github.com/charlesthk/python-mailchimp) (`mailchimp3`) library.

#### Install mailchimp3
***There is a known issue with the latest version of `mailchiimp3`. Use version 2.0.11***

`pip install mailchimp3==2.0.11`

## Install e2mc
1. Download or clone the repository.
2. Edit `elexio.py` and update the `elexio_session_id` variable at the top of the file.
3. Edit `mailchimp.py` and update the `client` and `list_id` variables at the top of the file.

## Run e2mc
To manually run the application:

`python main.py`

A log file, `e2mc.log` will be created and appended to with each run showing details about emails that were found and whether they were added or removed to the segment in MailChimp.

Once you have successfully run the application manually and are happy with it, I would recommend you setup a scheduled run of the application via cron. I run it every 2 minutes to keep MailChimp up to date as much as possible.

## Known Issues
- The default configuration of the application is to create a segment in MailChimp if a group is found in Elexio. The application will not remove segments found in MailChimp but not in Elexio. This will allow you to create and use auto segments in MailChimp. If you would prefer to have the segments automatically removed, edit `main.py` and search for `Uncomment`. You will find the section that you can enable to do the removes.
- There is an issue with email addresses that are not all lowercase when trying to add them to a segment. You will see these logged as "not in Mailchimp" in the `e2mc.log` file. At this point, the fix is to change the email to all lowercase in Elexio.

## Licence
`e2mc` is licensed under GPLv3. Copyright (c) 2017 ThornCreek Church
