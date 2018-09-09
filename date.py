#!/usr/bin/python3

import datetime

filename = "testname"
today = datetime.datetime.now().strftime("%Y-%m-%d")
filename += today + ".csv"

f = open(filename,'w',encoding='utf-8')

print(datetime.datetime.now(), file=f)
print(datetime.datetime.now().strftime("%Y-%m-%d"), file=f)

f.close()

