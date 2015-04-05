#!/usr/bin/env python

import requests
from BeautifulSoup import BeautifulSoup
from collections import defaultdict

date = raw_input("Enter a date (format: YYYY-MM-DD):")
print "Available fishbowl times for: " + date

r = requests.get('http://schedule.lib.calpoly.edu/process_roombookings.php?m=calscroll&gid=2015&date=' + date)

html = r.text
parsed = BeautifulSoup(r.text)

rooms = defaultdict(list)

for a in parsed.findAll('a', href=True):
    room = a['onclick'] .split("'")[1]
    time = a['onclick'] .split("'")[3].split(" - ")[0]
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
