from datetime import datetime
from datetime import timedelta

str = '864180036437825,868683021584960,351608085310261'
print(str)

lst = str.split(',')
print(lst)

curr_time_str = '2020-07-14 11:25:30'
print(curr_time_str)
curr_time = datetime.strptime(curr_time_str, '%Y-%m-%d %H:%M:%S')
print(curr_time)
updated_curr_time = curr_time + timedelta(minutes=330)
print(updated_curr_time)
updated_curr_time_str = updated_curr_time.strftime('%Y-%m-%d %H:%M:%S')
print(updated_curr_time_str)