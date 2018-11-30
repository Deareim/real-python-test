import json
import sqlite3
import csv
import time
from datetime import timedelta
import datetime
import odict

from ast import literal_eval


def fill_in_the_blanks(self, length):
    """

    :param self:
    :param length:
    :return:
    """

    self = [None for i in range(length,10) for k in range(0,4)]

    return self

list = []
ff = fill_in_the_blanks(list, 5)
print(ff)