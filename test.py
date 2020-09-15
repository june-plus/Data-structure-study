#!/usr/bin/python

import sqlite3, random, string, datetime
from tabulate import tabulate

a = [[1,2,3], [2,3,4],[44,4,4]]
print(tabulate(a, ["first", "second", "third"]))