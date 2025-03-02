# prints list of players to kick for poor GE participation
# must add the full path name of the .csv file which contains participation info
# started 08/09/2024

import csv

# some kind of enum thing would be good to define rules
MIN_ENCOUNTERS = 32

# returns number of encounters by a given player for a certain week
# returns -1 if member was not in guild for that week
def encounters(week, player_name, player_data):
    for player in player_data[1:]:
        player = player.strip().split(";")
        if player[0] == week and player[2] == player_name:
            return player[4]
    return "-1"


# return 0 if no rules broken
# return 1 if two consecutive weeks of 0 GE
# return 2 if four out of five weeks under minimum (< MIN_ENCOUNTERS GE)
# return 3 if < MIN_ENCOUNTERS encounters - needs to be messaged
# feed this members from member_log
def rules_flouted(player):
    if int(player[-1]) == 0 and int(player[-2]) == 0:
        return "1"
    elif int(player[-1]) < MIN_ENCOUNTERS and int(player[-1]) >= 0:
        under_min = 0
        for week in player[2:]:
            if int(week) < MIN_ENCOUNTERS and int(week) >= 0:
                under_min += 1
        if under_min >= 4:
            return "2"
        else:
            return "3"
    else:
        return "0"

input_csv = input("Please enter the full file path of the .csv containing participation information: ")
input_csv.strip()

# change csv file as required
with open(f"{input_csv}", "r") as data_set:
    player_data = data_set.readlines()

weeks = []

for player in player_data[1:]:
    player = player.strip().split(";")
    if weeks == []:
        weeks.append(player[0])
    elif player[0] != weeks[-1]:
        weeks.append(player[0])

headers = ["player"] + weeks + ["rules_broken"]

# get a list of current players
current_players = []
for player in player_data[1:]:
    player = player.strip().split(";")
    if player[0] == weeks[-1]:
        current_players.append(player[2])

member_log = []
# now find encounters for each current player and attach to the list
for player_name in current_players:
    player_history = [f"{player_name}"]
    for week in weeks:
        player_history.append(encounters(week, player_name, player_data))

    member_log.append(player_history)


for player in member_log:
    player.append(rules_flouted(player))
# now print the list of miscreants
# first print consecutive zeros
print("Two consecutive weeks of zero GE")
for player in member_log:
    if int(player[-1]) == 1:
        print(f"{player[0]} - ({player[1]}) ({player[2]}) ({player[3]}) ({player[4]}) ({player[5]})")

print(f"\nFour consecutive weeks of <{MIN_ENCOUNTERS} GE")
for player in member_log:
    if int(player[-1]) == 2:
        print(f"{player[0]} - ({player[1]}) ({player[2]}) ({player[3]}) ({player[4]}) ({player[5]})")

print("\nUnder minimum this week - needs messaging")
for player in member_log:
    if int(player[-1]) == 3:
        print(f"{player[0]} - ({player[1]}) ({player[2]}) ({player[3]}) ({player[4]}) ({player[5]})")

# creates CSV file which can be used in Excel
with open("temp_data.csv", "w") as temp_data:
    temp_data.write(",".join(headers))
    for player in member_log:
        temp_data.write("\n" + ",".join(player))

