import json
import sqlite3
from ast import literal_eval

# # open file in read mode
#
# with open("commodities.json", 'r') as json_data:
#     # Reading each line as a valid JSON and put it in list of lists
#     for line in json_data:
#         d = json.loads(line, strict=False)
#
#         i = 0
#         k = len(d)
#
#         for v in d:
#             commodities_reference = []
#             for k, g in v.items():
#                 if isinstance(g, dict):
#                     dict1 = g
#                     my_value1 = dict1.get("id")
#                     my_value2 = dict1.get("name")
#
#             for s, i in v.items():
#                 if not isinstance(i, dict):
#                     commodities_reference.append(i)
#             commodities_reference.append(my_value1)
#             commodities_reference.append(my_value2)
#             # print(commodities_reference)
#
#             with sqlite3.connect("elite.db") as connection:
#                 try:
#
#                     c = connection.cursor()
#                     # c.execute('INSERT OR REPLACE INTO Commodities VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
#                     #          '', commodities_reference)
#                     code = "INSERTION OK IN TABLE FACTION"
#                     print(commodities_reference)
#
#                 except sqlite3.Error as er:
#                     print("PROBLEM WHEN INSERTING FACTION TABLE", er, commodities_reference)
# #
#
#
# # open file in read mode
# # with open('', 'r') as json_data:
# with open("factions.json", 'r') as json_data:
#     # Reading each line as a valid JSON and put it in list of lists
#     for line in json_data:
#         d = json.loads(line, strict=False)
#
#         #  k = len(d)
#         # tuple_general_faction = ()
#         tuple_general_faction = ()
#         tuple_faction = ()
#         for v in d:
#             faction_reference = []
#
#             counter = 0
#             for k, g in v.items():
#                 counter = counter + 1
#                 faction_reference.append(g)
#             tuple_faction = tuple(faction_reference)
#             tuple_general_faction += tuple_faction,
#         print([tuple_general_faction])
#
#     with sqlite3.connect("elite.db") as connection:
#        try:
#         c = connection.cursor()
#         c.executemany('INSERT INTO faction VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', tuple_general_faction)
#         code = "INSERTION OK IN TABLE FACTION"
#        except sqlite3.Error as er:
#          print("PROBLEM WHEN INSERTING FACTION TABLE", er, tuple_general_faction)

with open("systems_populated2.json", 'r') as json_data:
     # Reading each line as a valid JSON and put it in list of lists
     for line in json_data:
         d = json.loads(line, strict=False)
#
#         #  k = len(d)
#         # tuple_general_faction = ()
#         tuple_general_faction = ()
#         tuple_faction = ()
         for v in d:
             system_populated = []
             faction = []
             counter = 0
             for k, g in v.items():
                 faction.append(g)
                 if isinstance(g, list):
                     l = len(g)

                     dict1 = g
                     i = 0

                     while i < l:
                         for y in dict1:

                                  faction.append(y.get("minor_faction_id"))
                                  faction.append(y.get("state_id"))
                                  faction.append(y.get("influence"))
                                  faction.append(y.get("state"))
                                  i = i + 1
                     print(faction)
             for s, i in v.items():
                 if not isinstance(i, dict):
                     system_populated.append(i)
             system_populated.append(my_value1)
             system_populated.append(my_value2)
             system_populated.append(my_value3)
             system_populated.append(my_value4)
             print(system_populated)
#
#     with sqlite3.connect("elite.db") as connection:
#        try:
#         c = connection.cursor()
#         c.executemany('INSERT INTO faction VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', tuple_general_faction)
#         code = "INSERTION OK IN TABLE FACTION"
#        except sqlite3.Error as er:
#          print("PROBLEM WHEN INSERTING FACTION TABLE", er, tuple_general_faction)