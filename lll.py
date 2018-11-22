import sqlite3
import datetime
from time import time

import csv

# with sqlite3.connect("elite.db") as connection:
#      try:
#          c = connection.cursor()
#          c.execute('CREATE TABLE System ( `id` INTEGER, `edsm_id` INTEGER, `name` TEXT, `x` INTEGER, `y` INTEGER, `z` INTEGER,'
#                        ' `population` INTEGER, `is_populated` TEXT, `government_id` INTEGER, `government` TEXT, `allegiance_id` INTEGER,'
#                        ' `allegiance` TEXT, `state_id` INTEGER, `state` TEXT, `security_id` INTEGER, `security` TEXT, `primary_id` INTEGER,'
#                        ' `primary_economy` TEXT, `power` TEXT,  `power_state` TEXT, `power_state_id` INTEGER, `needs_permit` TEXT, `updated_at` INTEGER, `simbad_ref` TEXT,'
#                        ' `controlling_minor_faction_id` INTEGER, `controlling_minor_faction` TEXT, `reserve_type_id` INTEGER, `reserve_type` TEXT,'
#                        ' PRIMARY KEY(`id`))')
#          code = "INSERTION OK IN TABLE FACTION"
#      except sqlite3.Error as er:
#          print("PROBLEM WHEN INSERTING FACTION TABLE", er, )
# with sqlite3.connect("elite.db") as connection:
#     try:
#         c = connection.cursor()
#         c.execute('select count(System_Populated.controlling_minor_faction) from System_Populated where System_Populated.controlling_minor_faction_id = 363')
#         code = "INSERTION OK IN TABLE FACTION"
#         rows = c.fetchone()
#         print('number of system under DoM control : {}'.format(rows))
#     except sqlite3.Error as er:
#         print("PROBLEM WHEN INSERTING FACTION TABLE", er, )
#
# with sqlite3.connect("elite.db") as connection:
#     try:
#         c = connection.cursor()
#         c.execute('select count(System_Populated.controlling_minor_faction) from System_Populated where System_Populated.allegiance = "Alliance"')
#         code = "INSERTION OK IN TABLE FACTION"
#         rows2 = c.fetchone()
#         print('number of systems under Alliance control : {}'.format(rows2))
#     except sqlite3.Error as er:
#         print("PROBLEM WHEN INSERTING FACTION TABLE", er, )
#pragma optimize( "", on )
with sqlite3.connect("elite.db") as connection:
     try:
         c = connection.cursor()
         c.execute('pragma journal_mode=wal')
         c.execute('PRAGMA synchronous = normal')
         c.execute('PRAGMA main.page_size = 4096')
         c.execute('PRAGMA main.cache_size = 10000')

         c.execute(' EXPLAIN QUERY plan select * '
                    'from system_populated as s, station as t, commodities as c, prices as p ')

         #
         rows = c.fetchall()
         for d in rows:
              print(d)


     except sqlite3.Error as er:
         print("PROBLEM WHEN INSERTING FACTION TABLE", er, )
#
# with sqlite3.connect("elite.db") as connection:
#      try:
#          c = connection.cursor()
#          c.execute('DELETE FROM faction')
#          code = "INSERTION OK IN TABLE FACTION"
#
#
#      except sqlite3.Error as er:
#          print("PROBLEM WHEN INSERTING FACTION TABLE", er, )
# #
