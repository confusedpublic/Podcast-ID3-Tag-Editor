#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Dave Race on 2013-03-30.
Copyright (c) 2013 confusedpublic. All rights reserved.
"""

import os
import sys
import id3reader
import string
from mutagen.id3 import ID3, TIT2, TDRL, TDES, WFED, TGID, TPUB

"""
Functions
"""

# Function to change a date in the form Day, d Mon YY into YYYY-MM-DD
def fixdate(date_str):
	# We split the date string by spaces, and keep the three bits we need (d Mon YY)
	# So we get:
	#	date_data[0] = Day name abbreviation
	#	date_data[1] = Date (single digit)
	#	date_data[2] = Month abreviation
	#	date_data[3] = Year, double digits
	date_data = date_str.split(' ')

	# Now pass that info through the date function to format it.	
	# First, make a dictionary that allows for quick swapping from month abbreviation to number:
	month_d = {
		"Jan" : "01", "Feb" : "02", "Mar" : "03", "Apr" : "04", "May" : "05", "Jun" : "06",
		"Jul" : "07", "Aug" : "08", "Sep" : "09", "Oct" : "10", "Nov" : "11", "Dec" : "12"
	}
	# And now change the date to a digits
	date_data[2] = month_d[date_data[2]]
	
	# Now make sure the day has a preceeding zero
	# First have to fudge the day into an int (it's a unicode, rather than string for some reason)
	date_data[1] = int(float(str(date_data[1])))
	if date_data[1] < 10:
		date_data[1] = "0" + str(date_data[1])

	# And now make sure the the year is four digits, with a big fudge on what year we add the 99 for.
	if date_data[3] > "12":
		date_data[3] = "19" + date_data[3]
	else:
		date_data[3] = "20" + date_data[3]

	# Now make a string with the info... YYYY-MM-DD
	ep_date = "%s-%s-%s" % (date_data[3], date_data[2], date_data[1])

	return ep_date
	
"""
Code
"""

# Set up the variables...

# General podcast directory...
gen_podcasts_dir = "/Users/DAVE/Music/Podcasts/In Our Time Archive_ "

# First, decide which archive I'm going to edit; others are commented out.
# Science:
#iot = "iots"
#podcast_dir = gen_podcasts_dir + "Science/"
#podcast_ident = "In Our Time Archive: Science"
# Culture:
#iot = "iotc"
#podcast_dir = gen_podcasts_dir + "Culture/"
#podcast_ident = "In Our Time Archive: Culutre"
# History:
iot = "ioth"
podcast_dir = gen_podcasts_dir + "History/"
podcast_ident = "In Our Time Archive: History"
# Philosophy:
#iot = "iotp"
#podcast_dir = gen_podcasts_dir + "Philosophy/"
#podcast_ident = "In Our Time Archive: Philosophy"
# Religion:
#iot = "iotr"
#podcast_dir = gen_podcasts_dir + "Religion/"
#podcast_ident = "In Our Time Archive: Religion"

info_f_path = iot + ".txt"

ep_file = open(info_f_path, "r")
	
ep_block = ep_file.readlines()

ep_file.close()

for i in range(len(ep_block)):
	ep_block[i] = ep_block[i].decode('utf-8').strip()

episodes = [] # This will contain the all the episode info in embedded lists
ep_info = [] # This will contain the processed information for each ep
 
j = 0 # This just counts
# Get number of episodes
for i in range(len(ep_block)):
	if ep_block[i] == "</li>":
		j += 1

# Make the list with each eliment for an episode
for i in range(j):
	episodes.append(i)
	ep_info.append(i)
	episodes[i] = [] # Make the embedded list for each ep
	ep_info[i] = {} # Make the embedded dictionary for each ep

j = 0
for i in range(len(ep_block)):
	episodes[j].append(ep_block[i])
	if ep_block[i] == "</li>":
		j += 1

for i in range(len(episodes)):
	for j in range(len(episodes[i])):
		if j == 2:
			ep_info[i]["title"] = iot.upper() + ": " + episodes[i][j]
			ep_info[i]["filename"] = iot.upper() + "_ " + episodes[i][j] + ".mp3"
		if j == 5:
			ep_info[i]["date"] = fixdate(episodes[i][j])
		if j == 12:
			ep_info[i]["description"] = episodes[i][j]

trans_table = {
	ord(u"’") : u"'",
	ord(u"‘") : u"'",
	ord(u"–") : u"-",
	ord(u"é") : u"e",
	ord(u"“") : u"\"",
	ord(u"”") : u"\""
}

fix_fnames_punc = ["'", ":"]

# All this translation stuff fails on an episode with é in the filename.

# Lets see if I can access the files' info & ID3 tags:

for i in range(len(ep_info)):
	# Try first where : and ' are replaced with _
	f_name = ep_info[i]["filename"].translate(trans_table)
	for j in range(len(fix_fnames_punc)):
		if fix_fnames_punc[j] in f_name:
			f_name = f_name.replace(fix_fnames_punc[j], "_")
		
	if "IOT_ " in f_name: #This is a fudge for eps which're named in general, rather than specific archives
		f_name = f_name.replace("IOT_ ", "")
	
	podcast_path = podcast_dir + f_name
	try:
		# Use mutagen to open the file info
		pod_info = ID3(podcast_path)
		
		# Update the description; have to translate any unicode away
		descript = ep_info[i]["description"].translate(trans_table)
		pod_info.add(TDES(encoding=0, text=descript))
		
		# Update the release time
		pod_info.add(TDRL(encoding=0, text=ep_info[i]["date"]))
		
		# Update the podcast identifier
		pod_info.add(TGID(encoding=0, text=podcast_ident))
		
		# Might want to update the comment if it's not there...
		passed = True
		
	# Small worry; the file name might actually include a ' (cause it's not a unicode one for some reason)
	# So just check if the file exists with the ' in it
	except:	
		try:
			f_name = ep_info[i]["filename"].translate(trans_table)
			# Assuming ' is in the file name; only need to replace :
			if ":" in f_name:
				f_name = f_name.replace(":", "_")

			if "IOT_ " in f_name: #This is a fudge for eps which're named in general, rather than specific archives
				f_name = f_name.replace("IOT_ ", "")

			podcast_path = podcast_dir + f_name
		
			# Use mutagen to open the file info
			pod_info = ID3(podcast_path)

			# Update the description; have to translate any unicode away
			descript = ep_info[i]["description"].translate(trans_table)
			pod_info.add(TDES(encoding=0, text=descript))

			# Update the release time
			pod_info.add(TDRL(encoding=0, text=ep_info[i]["date"]))

			# Update the podcast identifier
			pod_info.add(TGID(encoding=0, text=podcast_ident))

			# Might want to update the comment if it's not there...
			passed = True
			
		# Give up; blame it on not finding the file
		except:
			print "WARNING!:\nCouldn't find the file for podcast " + ep_info[i]["title"] + "\n\
			Used filename: " + ep_info[i]["filename"] + "\n Index: " + str(i) + "\n WARNING!"
			passed = False
	pod_info.save()
	# Show that I've at least updated *something*
	if passed == True:
		print "Updated " + ep_info[i]["title"] + " with the following info:\n\
		Description: " + str(pod_info["TDES"]) + "\n\
		Released Date: " + str(pod_info["TDRL"]) + "\n\
		Podcast Identity: " + podcast_ident