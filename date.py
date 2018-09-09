#!/usr/bin/python3

import datetime

today = datetime.datetime.now().strftime("%Y-%m-%d")
f = open(.join('asdf', '-', filename),'w',encoding='utf-8')

print(datetime.datetime.now(), file=f)
print(datetime.datetime.now().strftime("%Y-%m-%d"), file=f)

f.close()

