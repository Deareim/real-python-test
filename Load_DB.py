import json
import sqlite3
import datetime
import sys, os
import camelcase
from pprint import pprint

wantedEvents = [
    'Docked',
    'FSDJump',
    'Location',
    'MissionAccepted',
    'MissionAbandoned',
    'MarketSell',
    'MissionCompleted',
    'CommitCrime',
    'RedeemVoucher',
    'SellExplorationData',
    'SearchAndRescue',
    'DatalinkVoucher',
    'PowerplayCollect',
    'PowerplayDeliver',
    'PowerplayVote'
]


global_variable = ""

class DateWeek():

    def date_conversion_to_week(self, time2):

        self.time2 = time2
        week_split_hour = self.time2.split('T')
        week_split_date = week_split_hour[0].split('-')
        year = week_split_date[0]
        month = week_split_date[1]
        day = week_split_date[2]
        timestamp = week_split_hour[0]
        week_number = datetime.date(int(year), int(month), int(day)).strftime("%V")
        return [timestamp, week_number]

class Powerplay:

    def vote(self):


        code = ""

        with sqlite3.connect("elite.db") as connection:
            try:
                c = connection.cursor()
                c.execute('INSERT OR REPLACE INTO vote(week_vote, power_name, vote_strength, type_vote, cmdr_name)'
                          ' VALUES (?,?, ?, ?, ?)', self)
                code = "INSERT/UPDATE OK IN TABLE VOTE"
            except sqlite3.Error as er:
                print("PROBLEM WHEN INSERTING/UPDATING POWER TABLE", er, self)

        return code

    def power_table_init(self, power_name):

        self.power_name = power_name
        code = ""

        with sqlite3.connect("elite.db") as connection:
            try:
                c = connection.cursor()
                c.execute('INSERT OR REPLACE INTO power(power_name) VALUES (?)', [self.power_name])
                code = "INSERT/UPDATE OK IN TABLE POWER"
            except sqlite3.Error as er:
                print("PROBLEM WHEN INSERTING/UPDATING POWER TABLE", er, [self.power_name])

        return code

    def power_commodities_table_init(self, power_commodities_name):

        self.power_commodities_name = power_commodities_name
        code = ""

        with sqlite3.connect("elite.db") as connection:
            try:
                c = connection.cursor()
                c.execute('INSERT OR REPLACE INTO power_commodities(commodities_name, power_name) VALUES (?,?)',
                          self.power_commodities_name)
                code = "INSERT/UPDATE OK IN TABLE POWER_COMMODITIES"
            except sqlite3.Error as er:
                print("PROBLEM WHEN INSERTING/UPDATING POWER_COMMODITIES TABLE", er, self.power_commodities_name)

        return code


    def power_action_table(self):

        if self[-1] == "Collect":
            code = ""
            with sqlite3.connect("elite.db") as connection:
                try:
                    c = connection.cursor()
                    c.execute('INSERT OR REPLACE INTO powerplay_Action(Id, week, timestamp, cmdr_name, system_name, '
                              'power_name, commodities_name, count, action_name) VALUES (NULL,?,?,?,?,?,?,?,?)', self)
                    code = "INSERT/UPDATE OK IN TABLE POWERPLAY_ACTION FOR COLLECT ITEMS"
                except sqlite3.Error as er:
                    print("PROBLEM WHEN INSERTING/UPDATING POWERPLAY_ACTION FOR COLLECT ITEMS", er, self)
            return code

        if self[-1] == "Deliver":
            code = ""
            with sqlite3.connect("elite.db") as connection:
                try:
                    c = connection.cursor()
                    c.execute('INSERT OR REPLACE INTO powerplay_Action(Id, week, timestamp, cmdr_name, system_name, power_name,'
                              'commodities_name, count, action_name) VALUES (NULL,?,?,?,?,?,?,?,?)', self)
                    code = "INSERT/UPDATE OK IN TABLE POWERPLAY_ACTION FOR DELIVER ITEMS"
                except sqlite3.Error as er:
                    print("PROBLEM WHEN INSERTING/UPDATING POWERPLAY_ACTION FOR DELIVER ITEMS", er, self)
        return code





class Player:

    def player_init(self, cmdr_name):

        self.cmdr_name = cmdr_name
        code = ""
        with sqlite3.connect("elite.db") as connection:
            try:
                c = connection.cursor()
                c.execute('INSERT OR REPLACE INTO player(cmdr_name) VALUES (?)', [self.cmdr_name])
                code = "INSERT/UPDATE OK IN TABLE PLAYER"
            except sqlite3.Error as er:
                print("PROBLEM WHEN INSERTING/UPDATING PLAYER TABLE", er, self.cmdr_name)

        return code


class Faction:

    def faction_number(self):
        """

        :return:
        """
        num = len(self)
        return num


class UpdateFactionDB:

    def system_table(self, sys_info):
        """

        :param sys_info:
        :return:
        """
        self.system_info = sys_info
        code = ""

        with sqlite3.connect("elite.db") as connection:
            try:
                c = connection.cursor()
                c.execute('SELECT * FROM system WHERE system_name = ?', (self.system_info[0],))
                rows = c.fetchone()
                code = "READ OK IN TABLE SYSTEM"
            except sqlite3.Error as er:
                print("PROBLEM WHEN READING SYSTEM TABLE", er, self.system_info)
            if not rows:
                try:
                    c.execute('INSERT OR REPLACE INTO system VALUES (?, ?, ?, ?, ? , ?, ?, ?, ?, ?)', self.system_info)
                    code = "INSERTION OK IN TABLE SYSTEM"
                except sqlite3.Error as er:
                    print("PROBLEM WHEN INSERTING SYSTEM TABLE", er, self.system_info)
        return code

    def faction_table(self, faction_info):

        self.faction_info = faction_info
        code = ""

        with sqlite3.connect("elite.db") as connection:
            try:
                c = connection.cursor()
                c.execute('SELECT * FROM faction WHERE faction_name = ?', (self.faction_info[0],))
                rows = c.fetchone()
                code = "READ OK IN TABLE FACTION"
            except sqlite3.Error as er:
                print("PROBLEM WHEN READING FACTION TABLE", er, self.faction_info)
            if not rows:
                try:
                    c.execute('INSERT OR REPLACE INTO faction VALUES (?, ?, ?)', self.faction_info)
                    code = "INSERTION OK IN TABLE FACTION"
                except sqlite3.Error as er:
                    print("PROBLEM WHEN INSERTING FACTION TABLE", er, self.faction_info)
            # else:
            #    if rows(-1) and not self.faction_info(-1):
            #       sql = ('UPDATE faction SET faction_name = ?, system_government = ?,'
            #          'faction_allegiance = ?)
            # c.execute(sql, self.faction_info)
            # code = "UPDATE OK IN TABLE FACTION"
        return code

    def status_table(self, status_info):

        self.status_info = status_info
        code = ""
        test1 = self.status_info[0]
        test2 = self.status_info[1]
        list = []
        list.append(test1)
        list.append(test2)
        with sqlite3.connect("elite.db") as connection:
            try:
                c = connection.cursor()
                c.execute('SELECT * FROM status WHERE system_name = ? and faction_name = ?', list)
                rows = c.fetchone()
                code = "READ OK IN TABLE STATUS"
            except sqlite3.Error as er:
                print(er, self.status_info)
            # if not rows:
            try:
                c.execute('INSERT OR REPLACE INTO status VALUES (?, ?, ?, ?, ? , ?, ?, ?)', self.status_info)
                code = "INSERTION OK IN TABLE STATUS"
            except sqlite3.Error as er:
                print("UPDATE on table status :", er, self.status_info)

        return code


# open file in read mode
with open('journal5.log', 'r') as json_data:
    # Reading each line as a valid JSON and put it in list of lists
    for line in json_data:
        d = json.loads(line, strict=False)
        if d['event'] in ["Commander", "Load Game", "New Game"]:
            s = d.get("Name")
            s4 = ''.join((s))
            s2 = Player()
            s3 = s2.player_init(s4)
        # time = DateWeek()
        #time2 = d.get("timestamp")
        #time3 = time.date_conversion_to_week(time2)



        # t = datetime.date(2010, 6, 16).strftime("%V")
        if d['event'] in wantedEvents:

            if d['event'] in "FSDJump":
                system_info = []
                system_info.append(d.get("StarSystem"))
                system_info.append(d.get("SystemAllegiance"))
                system_info.append(d.get("SystemEconomy_Localised"))
                system_info.append(d.get("SystemSecondEconomy_Localised"))
                system_info.append(d.get("SystemGovernment_Localised"))
                system_info.append(d.get("SystemSecurity_Localised"))
                system_info.append(d.get("Population"))
                pp = d.get("Powers")
                my_var = ""
                if pp:
                    my_var = ''.join(str(x) for x in pp)

                system_info.append(my_var)
                system_info.append(d.get("Exploited"))

                system_info.append(d.get("TimeStamp"))
                k = UpdateFactionDB()
                db_update_system = k.system_table(system_info)
                print(db_update_system)
                week = d.get("timestamp").split('-')
                time = DateWeek()
                time2 = d.get("timestamp")
                time3 = time.date_conversion_to_week(time2)
                faction_time = time3[0]
                y = d.get("Factions")
                xyz = Faction
                if y:
                    k = xyz.faction_number(y)
                    i = 0
                    while i <= k:
                        for v in y:
                            faction_info = []
                            status_info = []
                            r = UpdateFactionDB()
                            faction_info.append(v.get("Name"))
                            faction_info.append(v.get("Government"))
                            faction_info.append(v.get("Allegiance"))
                            db_update_faction = r.faction_table(faction_info)
                            print(db_update_faction)
                            status_info.append(d.get("StarSystem"))
                            status_info.append(v.get("Name"))
                            status_info.append(v.get("FactionState"))
                            status_info.append('none')
                            status_info.append('none')
                            status_info.append('none')
                            status_info.append(v.get("Influence") * 100)
                            time = DateWeek()
                            time2 = d.get("timestamp")
                            time3 = time.date_conversion_to_week(time2)
                            status_info.append(time3[0])
                            j = UpdateFactionDB()
                            db_update_influence = j.status_table(status_info)
                            print(db_update_influence)

                            i += 1
            if d['event'] in "Docked":
                global_variable = d.get("StarSystem")
                print(global_variable)

            if d['event'] in ["PowerplayCollect", "PowerplayDeliver"]:

                #init table power and/or power_commodities if new items.

                p = Powerplay()
                power_commodities_name = []
                power_name = d.get('Power')

                pu = p.power_table_init(power_name)
                power_commodities_name.append(d.get('Type_Localised'))
                power_commodities_name.append(d.get('Power'))
                f = Powerplay()
                pc = f.power_commodities_table_init(power_commodities_name)

            if d['event'] in "PowerplayVote":

                time = DateWeek()
                time2 = d.get("timestamp")
                time3 = time.date_conversion_to_week(time2)
                powerplay_vote = []

                powerplay_vote.append(time3[1])
                powerplay_vote.append(d.get('Power'))
                powerplay_vote.append(str(d.get('Votes')))

                if "VoteToConsolidate":
                    powerplay_vote.append("Consolidation")
                else:
                    powerplay_vote.append("Preparation")
                powerplay_vote.append(s4)
                act3 = Powerplay
                action_send = act3.vote(powerplay_vote)

                print(powerplay_vote)

            if d['event'] in "PowerplayCollect":

                time = DateWeek()
                time2 = d.get("timestamp")
                time3 = time.date_conversion_to_week(time2)
                powerplay_action = []

                powerplay_action.append(time3[1])
                powerplay_action.append(time3[0])
                powerplay_action.append(s4)
                powerplay_action.append(global_variable)
                powerplay_action.append(d.get('Power'))
                powerplay_action.append(d.get('Type_Localised'))
                powerplay_action.append(d.get('Count'))
                powerplay_action.append("Collect")
                act = Powerplay
                action_send = act.power_action_table(powerplay_action)
                print(powerplay_action)

            if d['event'] in "PowerplayDeliver":

                powerplay_action = []
                time = DateWeek()
                time2 = d.get("timestamp")
                time3 = time.date_conversion_to_week(time2)
                powerplay_action.append(time3[1])
                powerplay_action.append(time3[0])
                powerplay_action.append(s4)
                powerplay_action.append(global_variable)
                powerplay_action.append(d.get('Power'))
                powerplay_action.append(d.get('Type_Localised'))
                powerplay_action.append(d.get('Count'))
                powerplay_action.append("Deliver")
                act2 = Powerplay
                action_send = act2.power_action_table(powerplay_action)
                print(powerplay_action)







    else:
        print("FILE LOADED")  # if "PendingStates" in v:
