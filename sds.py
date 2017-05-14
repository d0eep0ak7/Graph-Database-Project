import datetime
your_timestamp = float(-1455411600000)
date = datetime.datetime.fromtimestamp(your_timestamp)
print(date)
print(date.strftime("%Y-%m-%d"))