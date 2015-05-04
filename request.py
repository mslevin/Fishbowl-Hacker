#! /usr/bin/python

import requests
import curses
from BeautifulSoup import BeautifulSoup
from collections import defaultdict
from threading import Thread

# print "What do you want to do?"
# print "1) Manually select up to 3 hours"
# print "2) Reserve as many fishbowls as possible in one day"
# action = raw_input()

def get_param(prompt_string):
     scr.clear()
     scr.border(0)
     scr.addstr(2, 2, prompt_string)
     scr.refresh()
     input = scr.getstr(2, len(prompt_string) + 3, 60)
     return input

scr = curses.initscr()
scr.clear()
scr.border(0)
scr.addstr(2, 4, "Welcome to Michael's Fishbowl Service")
scr.refresh()

scr.addstr(4, 4, "Your name:")
scr.refresh()
name = scr.getstr(4, 15, 60)

scr.addstr(5, 4, "Cal Poly username:")
scr.refresh()
email = scr.getstr(5, 23, 60)

scr.addstr(6, 4, "Group name:")
scr.refresh()
group = scr.getstr(6, 16, 60)

scr.clear()
scr.border(0)

scr.addstr(1, 4, "Name: " + name) 
scr.addstr(2, 4, "Username: " + email) 
scr.addstr(3, 4, "Group: " + group) 

scr.addstr(5, 4, "Enter a date (format MM-DD):")
scr.refresh()
date = scr.getstr(5, 33, 60)

date = '2015-' + date

scr.clear()
scr.border(0)

scr.addstr(1, 4, "Name: " + name) 
scr.addstr(2, 4, "Username: " + email) 
scr.addstr(3, 4, "Group: " + group) 
scr.addstr(5, 4, "Available fishbowl times for: " + date)

scr.addstr(10, 4, "Loading...")

r = requests.get('http://schedule.lib.calpoly.edu/process_roombookings.php?m=calscroll&gid=2015&date=' + date)

scr.clear()
scr.border(0)
scr.addstr(1, 4, "Name: " + name) 
scr.addstr(2, 4, "Username: " + email) 
scr.addstr(3, 4, "Group: " + group) 
scr.addstr(5, 4, "Available fishbowl times for: " + date)


html = r.text
parsed = BeautifulSoup(r.text)

rooms = defaultdict(list)
id = {}

for a in parsed.findAll('a', href=True):
    room = a['onclick'] .split("'")[1]
    time = a['onclick'] .split("'")[3].split(" - ")[0]
    id[room, time] = a['id']
    rooms[room].append(time);

count = 1
space = 0
for room in rooms:
	space = count * 7
	scr.addstr(7, space, room)
	count += 1


times = ["8:00am", "9:00am", "10:00am", "11:00am", \
         "12:00am", "1:00pm", "2:00pm", "3:00pm", \
         "4:00pm", "5:00pm" , "6:00pm", "7:00pm", \
         "8:00pm", "9:00pm", "10:00pm", "11:00pm"]

count = 1
space = 0
for i in range(0, 16):
    for room in rooms:
        if times[i] in rooms[room]:
            space = count * 7
            scr.addstr(8 + i, space, times[i]) 
            #print times[i] + "\t",
        else:
            #print "------\t"
		    scr.addstr(8 + i, space, "------") 
        count += 1
    count = 0
    #print "\n"

scr.getch()
curses.endwin()

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
