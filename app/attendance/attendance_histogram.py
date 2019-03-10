import datetime
from pprint import pprint
import matplotlib.pyplot as plt
import pandas as pd

from attendance.bosscontrol import load_attendance_time, load_employees


def send_attendance_histogram(time_frame: int, date=datetime.datetime):
    collection = load_employees()
    load_attendance_time(collection, date)

    data = {'attendance_time': [], 'people': []}
    for item in collection.get_collection().values():
        attendance = item.get_attendance()
        if attendance.is_absent(date):
            continue
        attendance.sort()
        data['attendance_time'].append(attendance.get_first(date))
        data['attendance_time'].append(attendance.get_last(date))
        data['people'].append(1)
        data['people'].append(1)

    if len(data['attendance_time']) == 0:
        return

    data['attendance_time'].insert(0, date.replace(hour=6, minute=0, second=0))
    data['attendance_time'].append(date.replace(hour=23, minute=59, second=59))
    data['people'].insert(0, 0)
    data['people'].append(0)
    data['attendance_time'].sort()
    df = pd.DataFrame.from_dict(data)
    df.index = df['attendance_time']
    del df['attendance_time']

    df_resample = df.resample("%iT" % time_frame)
    df_resample = df_resample.sum()

    df_resample.plot()
    plt.title('When you come to office')
    plt.xlabel('Time')
    plt.ylabel('People Amount')
    plt.grid(axis='x')
    pic = plt.savefig('figure1.pdf')
    t = 1

