import datetime

now = datetime.datetime.now()
date = now.strftime('%Y%m%d')
date = date[2:]
print(date)
