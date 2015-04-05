#!/usr/bin/env python

import requests
from BeautifulSoup import BeautifulSoup
from collections import defaultdict

print "What do you want to do?"
print "1) Manually select up to 3 hours"
print "2) Reserve as many fishbowls as possible in one day"
action = raw_input()

name = raw_input("Your name: ")
email = raw_input("Cal Poly username: ")
group = raw_input("Group name: ")

date = raw_input("Enter a date (format: MM-DD): ")
date = '2015-' + date
print "\nAvailable fishbowl times for: " + date



r = requests.get('http://schedule.lib.calpoly.edu/process_roombookings.php?m=calscroll&gid=2015&date=' + date)

html = r.text
parsed = BeautifulSoup(r.text)

rooms = defaultdict(list)
id = {}

for a in parsed.findAll('a', href=True):
    room = a['onclick'] .split("'")[1]
    time = a['onclick'] .split("'")[3].split(" - ")[0]
    id[room, time] = a['id']
    rooms[room].append(time);

count = 0
for room in rooms:
    print room + "\t",

print "\n"

times = ["8:00am", "9:00am", "10:00am", "11:00am", \
         "12:00am", "1:00pm", "2:00pm", "3:00pm", \
         "4:00pm", "5:00pm" , "6:00pm", "7:00pm", \
         "8:00pm", "9:00pm", "10:00pm", "11:00pm"]

for i in range(0, 16):
    for room in rooms:
        if times[i] in rooms[room]:
            print times[i] + "\t",
        else:
            print "------\t",
    print "\n"

roomSel = raw_input("Enter a room number: ")
timeSel = raw_input("Enter times: ")

timeSel = timeSel.split(" ")
timeIDs = ""

timeIDs = "|".join(id[roomSel, time] for time in timeSel)

headers = {'Origin':'http://schedule.lib.calpoly.edu', 'Referer':'http://schedule.lib.calpoly.edu/rooms.php?i=2015'}
payload = {'sid':str(timeIDs), 'tc':'done', 'gid':'2015', 'name':name, 'email':email+'@calpoly.edu', 'nick':group, 'qcount':'0', 'fid':'0'}
url = 'http://schedule.lib.calpoly.edu/process_roombookings.php?m=booking_full'
res = requests.post(url, headers=headers, data=payload)

print res.text
print "Done. Check your email to confirm the reservations."
