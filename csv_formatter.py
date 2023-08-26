import pandas as pd
import datetime as dt
from pathlib import Path


x=0
check_li = ["CO_DATA.csv", "NO2.csv", "PM10.csv", "SO2.csv"]


df = pd.read_csv('')

use = []

use = df["date"]


check = pd.DataFrame(data={"date": use})
a = pd.to_datetime(check["date"])


missing_vals = pd.date_range(start = '2020-01-01', end = '2022-12-30' ).difference(a).values
print(missing_vals)


