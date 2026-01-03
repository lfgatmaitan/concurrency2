# Concurrency counter
# by: Leif Gatmaitan
# created on: 01/03/2025

from datetime import datetime,timedelta
import csv

filepath = "test.csv"
entry_list = []
entry_dict = {}
users = []
dates = []
unique_ids = []
time_list = []

time_entry_dict = {}

start_time = datetime.strptime("00:00:00", "%H:%M:%S")
for i in range(60*24):
	x = start_time + timedelta(minutes=i)
	time_list.append(x.strftime("%H:%M:%S"))


# create a list of lists. each inner list contains the ff:
# unique chat ID, chat ID, agent ID, date, start time, end time
# end time has been subtracted by 1 min to avoid concurency inflation

with open(filepath) as raw:
	file = raw
	for line in file:
		entry_list.append(line.rstrip().split(","))

del entry_list[0]
# entry_list is finished here

# converting times and dates from text to timedate objects
for line in entry_list:
	date_text = line[3]
	time_text = line[4]
	date_obj = datetime.strptime(date_text, "%m/%d/%Y").date()
	time_obj = datetime.strptime(time_text, "%H:%M:%S").time()
# converting time and date formats end here

# creating list of users and list of dates
for line in entry_list:
	if line[2] not in users:
		users.append(line[2])
	if line[3] not in dates:
		dates.append(line[3])
	if line[0] not in unique_ids:
		unique_ids.append(line[0])

unique_id_dict = {}
for entry in unique_ids:
	unique_id_dict[entry] = []

# identifying concurrency for a given user, date, time combo

for user in users:
	time_entry_dict[user] = {}

for user in users:
	for date in dates:
		time_entry_dict[user][date] = {}

for user in users:
	for date in dates:
		for time in time_list:
			time_entry_dict[user][date][time] = []

for entry in entry_list:
	for time in time_list:
		if time >= entry[4] and time <= entry[5]:
			if entry[0] not in time_entry_dict[entry[2]][entry[3]][time]:
				time_entry_dict[entry[2]][entry[3]][time].append(entry[0])

for key1 in time_entry_dict.keys():
	for key2 in time_entry_dict[key1].keys():
		for key3 in time_entry_dict[key1][key2].keys():
			for chat_id in time_entry_dict[key1][key2][key3]:
				xlist = time_entry_dict[key1][key2][key3]
				unique_id_dict[chat_id].append(len(xlist))

concurrency = {}

for key, value in unique_id_dict.items():
	if value:
		concurrency[key] = max(value)
	else:
		concurrency[key] = 1


with open("output.csv", "w", newline="") as file:
	writer = csv.writer(file)
	writer.writerow(["ChatID", "Concurrency"])
	for key, value in concurrency.items():
		writer.writerow([key, value])
