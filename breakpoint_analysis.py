import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import ruptures as rpt
import pymannkendall as mk
import datetime


data = pd.read_csv('/Users/sayevikram/PycharmProjects/pythonProject/new_dat.csv')

a = pd.to_datetime(data['date'], format="%m/%d/%y")
models = ["l1", "l2", "rbf"]
x = 0
marker = models[x]


def run_mankendal(mark, data):
    algo = rpt.Pelt(model=mark, min_size=14).fit(data.values)
    result = algo.predict(pen=1)

    times = a.values
    cut_times = []

    for i in result:
        cut_times.append(times[(i-1)])

    return cut_times, result

def decr(li):
    return [x-1 for x in li]

def trend_analysis(emp_li, temp_li, air_param):
    for i, val in enumerate(temp_li):
        if val == temp_li[-1]:
            break
        else:
            first_mark = temp_li[i]
            second_mark = temp_li[i+1]
        temp = data[air_param].iloc[first_mark: second_mark].values

        emp_li.append(mk.original_test(temp)[0])

    return emp_li

# trends is mankendal_ozon
# breaks is temp_ozon pm
# empty df too

def assign_trends_ini(df, trends):
    df['trend'] = trends[0]
    return df

def change_trend(df, trends, breaks):
    for i, trend in enumerate(trends):
        if i != 0:
            start, end = breaks[i - 1], breaks[i]
            start_index, end_index = df.index[start], df.index[end]
            # print(start_index, end_index)
            df.loc[start_index:end_index, 'trend'] = trend
    return df
#    for i, trend in enumerate(trends):
#        if i != 0:
#            start, end = breaks[i-1], breaks[i]
#            start_index, end_index = df.index[start], df.index[end]
#            df.loc[start_index, end_index, 'trend_ozon'] = trend
#    return df


def plot_xline(x, y, li):
    for i in li:
        ax[x, y].axvline(x = i, color = 'r', label = 'dashed', linestyle = "dashed")


def relabel(x, y):
    labels = [item.get_text() for item in ax[x, y].get_yticklabels()]

    for idx, val in enumerate(labels):
        labels[idx] = " "

    labels[1] = "Decreasing"
    labels[5] = "No trend"
    labels[9] = "Increasing"
    ax[x, y].set_yticklabels(labels)
    ax[x, y].tick_params(left=False)



while True:

  try:

    cut_pm, temp_pm = run_mankendal(marker, data["pm"])
    cut_ozon, temp_ozon = run_mankendal(marker, data["ozone"])

#decrease by one

    temp_ozon = decr(temp_ozon)
    temp_pm = decr(temp_pm)


# USE temp = data["pm"].iloc[0:5].values

#res = mk.original_test(temp)
#print(res)


#for i, val in enumerate()

#print(temp_pm)

    mankendal_ozon = []
    mankendal_pm = []

    mankendal_ozon = trend_analysis(mankendal_ozon, temp_ozon, 'ozone')
    mankendal_pm = trend_analysis(mankendal_pm, temp_pm, 'pm')

  except:
    x = x+1
    if x == 3:
      x == 0
    models[x]
    continue

  else:
    break

test = pd.DataFrame(data={"date": data["date"]})
test = test.set_index("date")
test = assign_trends_ini(test, mankendal_ozon)

test = change_trend(test, mankendal_ozon, temp_ozon)
test['trend'] = pd.Categorical(test['trend'], categories=['decreasing', 'no trend', 'increasing'], ordered=True).codes


test_two = pd.DataFrame(data={"date": data["date"]})
test_two = test_two.set_index("date")
test_two = assign_trends_ini(test_two, mankendal_pm)

test_two = change_trend(test_two, mankendal_pm, temp_pm)
test_two['trend'] = pd.Categorical(test_two['trend'], categories=['decreasing', 'no trend', 'increasing'], ordered=True).codes



#Plotting now

fig, ax = plt.subplots(nrows=3, ncols=2, figsize=(30, 15))


ax[0, 0].plot(a, data["pm"], 'b', lw =0.8, label="PM2.5 AQI")
ax[0, 0].set_title('AQI VALUE OF PM2.5')
fmt_month = mdates.MonthLocator(interval=3)
fmt_year = mdates.YearLocator()
ax[0, 0].xaxis.set_minor_locator(fmt_month)
ax[0, 0].xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
ax[0, 0].xaxis.set_major_locator(fmt_year)
ax[0, 0].xaxis.set_major_formatter(mdates.DateFormatter('%b/%y'))

ax[1, 0].plot(a, data["pm"], 'b', lw =0.8, label="PM2.5 AQI")
ax[1, 0].set_title('AQI VALUE OF PM2.5')
plot_xline(1, 0, cut_pm)
fmt_month = mdates.MonthLocator(interval=3)
fmt_year = mdates.YearLocator()
ax[1, 0].xaxis.set_minor_locator(fmt_month)
ax[1, 0].xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
ax[1, 0].xaxis.set_major_locator(fmt_year)
ax[1, 0].xaxis.set_major_formatter(mdates.DateFormatter('%b/%y'))


ax[0, 1].plot(a, data["ozone"], 'b', lw =0.8, label="OZONE AQI")
ax[0, 1].set_title('AQI VALUE OF OZONE')
fmt_month = mdates.MonthLocator(interval=3)
fmt_year = mdates.YearLocator()
ax[0, 1].xaxis.set_minor_locator(fmt_month)
ax[0, 1].xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
ax[0, 1].xaxis.set_major_locator(fmt_year)
ax[0, 1].xaxis.set_major_formatter(mdates.DateFormatter('%b/%y'))

ax[1, 1].plot(a, data["ozone"], 'b', lw =0.8, label="OZONE AQI")
ax[1, 1].set_title('AQI VALUE OF OZONE')
plot_xline(1, 1, cut_ozon)
fmt_month = mdates.MonthLocator(interval=3)
fmt_year = mdates.YearLocator()
ax[1, 1].xaxis.set_minor_locator(fmt_month)
ax[1, 1].xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
ax[1, 1].xaxis.set_major_locator(fmt_year)
ax[1, 1].xaxis.set_major_formatter(mdates.DateFormatter('%b/%y'))



ax[2, 1].plot(a, test[['trend']])
ax[2, 1].xaxis.set_minor_locator(fmt_month)
ax[2, 1].xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
ax[2, 1].xaxis.set_major_locator(fmt_year)
ax[2, 1].xaxis.set_major_formatter(mdates.DateFormatter('%b/%y'))
plot_xline(2, 1, cut_ozon)
relabel(2, 1)



ax[2, 0].plot(a, test_two[['trend']])
ax[2, 0].xaxis.set_minor_locator(fmt_month)
ax[2, 0].xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
ax[2, 0].xaxis.set_major_locator(fmt_year)
ax[2, 0].xaxis.set_major_formatter(mdates.DateFormatter('%b/%y'))
plot_xline(2, 0, cut_pm)
relabel(2, 0)


#test[['trend']].plot()
plt.show()