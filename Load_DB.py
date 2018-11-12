import json
import sqlite3
import datetime
import os
from pathlib import Path
import webbrowser
import csv

# open file in read mode
#with open('', 'r') as json_data:
with open("commodities.json", 'r') as json_data:
    # Reading each line as a valid JSON and put it in list of lists
    for line in json_data:
        d = json.loads(line, strict=False)
        i = 0
        k = len(d)
        while i <= k:
            for v in d:

                commodities_reference = []

                commodities_reference.append(v.get("id"))
                commodities_reference.append(v.get("name"))
                commodities_reference.append(v.get("category_id"))
                commodities_reference.append(v.get("average_price"))
                commodities_reference.append(v.get("is_rare"))
                commodities_reference.append(v.get("max_buy_price"))
                commodities_reference.append(v.get("max_sell_price"))
                commodities_reference.append(v.get("min_buy_price"))
                commodities_reference.append(v.get("min_sell_price"))
                commodities_reference.append(v.get("buy_price_lower_average"))
                commodities_reference.append(v.get("sell_price_upper_average"))
                commodities_reference.append(v.get("is_non_marketable"))
                commodities_reference.append(v.get("ed_id"))

                cat = v.get("category")

                commodities_reference.append(cat.get("id"))
                commodities_reference.append(cat.get("name"))

                with sqlite3.connect("elite.db") as connection:
                        try:
                            c = connection.cursor()
                            c.execute('INSERT OR REPLACE INTO Commodities VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
                                      '', commodities_reference)
                            code = "INSERTION OK IN TABLE FACTION"
                        except sqlite3.Error as er:
                            print("PROBLEM WHEN INSERTING FACTION TABLE", er, commodities_reference)
                i += 1
        print("FILE LOADED")  # if "PendingStates" in v:
