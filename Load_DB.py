import json
import sqlite3
import csv
import time
from datetime import timedelta
import datetime
import odict

from ast import literal_eval


def chunks(data, rows=5000000):
    """

    :param data:
    :param rows:
    :return:
    """

    for i in range(0, len(data), rows):
        yield data[i:i + rows]


def fill_in_the_blanks(self, length):
    """

    :param self:
    :param length:
    :return:
    """
    for i in range(length, 10):
        self.append(None)
        self.append(None)
        self.append(None)
        self.append(None)
    return self

def fill_in_the_blanks2(self, length):
    """

    :param self:
    :param length:
    :return:
    """
    for i in range(length, 10):
        self.append(None)
    return self

#
# #
# open file in read mode
#
start_time = time.monotonic()
with open("commodities.json", 'r') as json_data:
    # Reading each line as a valid JSON and put it in list of lists
    for line in json_data:
        d = json.loads(line, strict=False)
        tuple_general_commodities = []
        line_count = 0
        for v in d:
            commodities_reference = []
            for k, g in v.items():

                if not isinstance(g, dict):
                    commodities_reference.append(g)
                if isinstance(g, dict):
                    dict1 = g
                    commodities_reference.append(dict1.get("id"))
                    commodities_reference.append(dict1.get("name"))
            line_count += 1
            tuple_general_commodities += commodities_reference,


with sqlite3.connect("elite.db") as connection:
    try:
        c = connection.cursor()
        c.execute('PRAGMA synchronous = normal')
        c.execute('PRAGMA main.page_size = 4096')
        c.execute('PRAGMA main.cache_size = 10000')

        c.executemany('INSERT OR REPLACE INTO Commodities VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                      tuple_general_commodities)
        code = "INSERTION OK IN TABLE COMMODITIES"
    except sqlite3.Error as er:
        print("PROBLEM WHEN INSERTING COMMODITIES TABLE", er, tuple_general_commodities)

end_time = time.monotonic()
print('duration for commodities :', timedelta(seconds=end_time - start_time),
      'for {} commodities registered'.format(line_count))
#
#
start_time = time.monotonic()
with open("factions.json", 'r') as json_data:
    # Reading each line as a valid JSON and put it in list of lists
    for line in json_data:
        d = json.loads(line, strict=False)

        line_count = 0
        tuple_general_faction = []
        for v in d:
            faction_reference = []

            for k, g in v.items():
                faction_reference.append(g)
            tuple_general_faction += faction_reference,
            line_count += 1

    with sqlite3.connect("elite.db") as connection:
        try:
            c = connection.cursor()
            c.execute('PRAGMA synchronous = normal')
            c.execute('PRAGMA main.page_size = 4096')
            c.execute('PRAGMA main.cache_size = 10000')
            c.executemany('INSERT OR REPLACE INTO faction VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                          tuple_general_faction)
        except sqlite3.Error as er:
            print("PROBLEM WHEN INSERTING FACTION TABLE", er, tuple_general_faction)

end_time = time.monotonic()
print('duration for factions :', timedelta(seconds=end_time - start_time),
      'for {} factions registered'.format(line_count))
#
start_time = time.monotonic()
with open("systems_populated.json", 'r') as json_data:
    # Reading each line as a valid JSON and put it in list of lists
    for line in json_data:
        d = json.loads(line, strict=False)
        k = len(d)
        tuple_general_populated = []

        line_count = 0
        for v in d:
            system_populated = []
            faction = []

            for k, g in v.items():
                if not isinstance(g, list):
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

                # Filled with none the list need for having 10 faction list before inserting in DB
                    row = faction
                    new_row = fill_in_the_blanks(row, l)
                    t = datetime.datetime.now()
                    day = t.day
                    year = t.year
                    month = t.month
                    week_number = datetime.date(year, month, day).strftime("%V")
                    faction.append(week_number)
                    faction.append(year)
                tuple_general_populated += faction,
            line_count += 1

    with sqlite3.connect("elite.db") as connection:
        try:
            c = connection.cursor()
            c.execute('PRAGMA synchronous = normal')
            c.execute('PRAGMA main.page_size = 4096')
            c.execute('PRAGMA main.cache_size = 10000')
            c.executemany(
                'INSERT OR REPLACE INTO System_Populated VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,'
                ' ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,'
                ' ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?)', tuple_general_populated)
        except sqlite3.Error as er:
            print("PROBLEM WHEN INSERTING SYSTEM POPULATED", er, tuple_general_populated)

end_time = time.monotonic()
print('duration for systems populated :', timedelta(seconds=end_time - start_time),
      'for {} populated systems registered'.format(line_count))
#

start_time = time.monotonic()
with open('system2.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    tuple_general_systems = []
    line_count = 0
    for row in csv_reader:
        systems = []
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
        line_count += 1
        for k, v in row.items():
            systems.append(v)
        tuple_general_systems += systems,
        #print(line_count)

divData = chunks(tuple_general_systems)
with sqlite3.connect("elite.db") as connection:
    c = connection.cursor()
    c.execute('PRAGMA synchronous = normal')
    c.execute('PRAGMA main.page_size = 4096')
    c.execute('PRAGMA main.cache_size = 10000')
for chunk in divData:
   c.execute('BEGIN TRANSACTION')
   try:
       c.executemany('INSERT OR REPLACE INTO System VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,'
                      ' ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)', chunk)
   except sqlite3.Error as er:
        print("PROBLEM WHEN INSERTING SYSTEMS TABLE", er)
   c.execute('commit')
end_time = time.monotonic()
print('duration for systems :', timedelta(seconds=end_time - start_time),
      'for {} systems registered'.format(line_count))

start_time = time.monotonic()
# update of prices in mass
with open('listings.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    tuple_general_prices = []
    tuple_general_prices2 = []
    tuple_prices = ()
    line_count = 0
    for row in csv_reader:
        price = []
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
        line_count += 1
        for k, v in row.items():
            price.append(v)
        tuple_general_prices += price,

with sqlite3.connect("elite.db") as connection:
    try:
        c = connection.cursor()
        c.execute('PRAGMA synchronous = normal')
        c.execute('PRAGMA main.page_size = 4096')
        c.execute('PRAGMA main.cache_size = 10000')
        c.executemany('INSERT OR REPLACE INTO Prices VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', tuple_general_prices)
        code = "INSERTION OK IN TABLE PRICES"
    except sqlite3.Error as er:
        print("PROBLEM WHEN INSERTING PRICES TABLE", er, tuple_general_prices)

end_time = time.monotonic()
print('duration for prices updates :', timedelta(seconds=end_time - start_time),
      'for {} prices registered'.format(line_count))

# Update stations in mass
start_time = time.monotonic()
with open("stations.json", 'r') as json_data:
    # Reading each line as a valid JSON and put it in list of lists
    for line in json_data:
        d = json.loads(line, strict=False)
        k = len(d)
        tuple_general_station = []
        tuple_station = []

        line_count = 0
        for v in d:
            station = []
            try:
                del v["selling_ships"]
            except KeyError:
                print("Key selling_ships not found")
            try:
                del v["selling_modules"]
            except KeyError:
                print("Key selling_modules not found")

            for k, g in v.items():

                if 'prohibited_commodities' in str(k):
                    s = len(g)
                    row = g
                    new_row = fill_in_the_blanks2(row, s)
                    for i in range(10):
                        station.append(new_row[i])

                if 'import_commodities' in str(k):
                    t = len(g)
                    row = g
                    for f in range(t, 5):
                        row.append(None)
                    station.append(row[0])
                    station.append(row[1])
                    station.append(row[2])
                    station.append(row[3])
                    station.append(row[4])

                if 'export_commodities' in str(k):
                    t = len(g)
                    row = g
                    for f in range(t, 5):
                        row.append(None)
                    station.append(row[0])
                    station.append(row[1])
                    station.append(row[2])
                    station.append(row[3])
                    station.append(row[4])

                if 'economies' in str(k):
                    s = len(g)
                    row = g
                    if s == 0:
                        station.append(None)
                        station.append(None)
                    if s == 1:
                        row.append(None)
                        station.append(row[0])
                        station.append(row[1])
                    elif s >= 2:
                        station.append(row[0])
                        station.append(row[1])

                if not isinstance(g, list):
                    station.append(g)

            tuple_general_station += station,
            line_count += 1
        # print(line_count)

    with sqlite3.connect("elite.db") as connection:
        try:
            c = connection.cursor()
            c.execute('PRAGMA synchronous = normal')
            c.execute('PRAGMA main.page_size = 4096')
            c.execute('PRAGMA main.cache_size = 10000')
            c.executemany(
                'INSERT OR REPLACE INTO station VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,'
                ' ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                tuple_general_station)
        except sqlite3.Error as er:
            print("PROBLEM WHEN INSERTING SYSTEM POPULATED", er, tuple_general_station)

end_time = time.monotonic()
print('duration for stations :', timedelta(seconds=end_time - start_time),
      'for {}  stations registered'.format(line_count))
