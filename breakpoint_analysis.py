import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import ruptures as rpt
import pymannkendall as mk
import datetime

def fill_null_and_interpolate(df):
    #df["site"].fillna(np.NaN, inplace=True)
    df = df.interpolate(method ='linear')
    return df

def run_mankendal(mark, data):
    algo = rpt.KernelCPD(kernel="linear", min_size=14).fit(data.values)
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

        emp_li.append(mk.yue_wang_modification_test(temp, 0.10)[0])

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
    labels[9] = "Increasing"
    ax[x, y].set_yticklabels(labels)
    ax[x, y].tick_params(left=False)

def fmt_gen(x, y, fmt_month, fmt_year):
    ax[x, y].xaxis.set_minor_locator(fmt_month)
    ax[x, y].xaxis.set_minor_formatter(mdates.DateFormatter('%b'))
    ax[x, y].xaxis.set_major_locator(fmt_year)
    ax[x, y].xaxis.set_major_formatter(mdates.DateFormatter('%b/%y'))


data = pd.read_csv('/Users/sayevikram/PycharmProjects/pythonProject/new_dat.csv')
df_co = fill_null_and_interpolate(pd.read_csv("/Users/sayevikram/PycharmProjects/pythonProject/CO_DATA.csv"))
df_no2 = fill_null_and_interpolate(pd.read_csv("/Users/sayevikram/PycharmProjects/pythonProject/NO2.csv"))
df_so2 = fill_null_and_interpolate(pd.read_csv("/Users/sayevikram/PycharmProjects/pythonProject/SO2.csv"))
df_pm10 = fill_null_and_interpolate(pd.read_csv("/Users/sayevikram/PycharmProjects/pythonProject/PM10.csv"))
data = data.assign(co=df_co["site"])
data = data.assign(so2=df_so2["site"])
data = data.assign(pm10=df_pm10["site"])
data = data.assign(no2=df_no2["site"])



a = pd.to_datetime(data['date'], format="%m/%d/%y")
models = ["l1", "rbf", "l2"]
x = 0
marker = models[x]






while True:

  try:

    cut_pm, temp_pm = run_mankendal(marker, data["pm"])
    cut_ozon, temp_ozon = run_mankendal(marker, data["ozone"])
    cut_no2, temp_no2 = run_mankendal(marker, data["no2"])
    cut_so2, temp_so2 = run_mankendal(marker, data["so2"])
    cut_pm10, temp_pm10 = run_mankendal(marker, data["pm10"])
    cut_co, temp_co = run_mankendal(marker, data["co"])

#decrease by one

    temp_ozon = decr(temp_ozon)
    temp_pm = decr(temp_pm)
    temp_so2 = decr(temp_so2)
    temp_no2 = decr(temp_no2)
    temp_pm10= decr(temp_pm10)
    temp_co= decr(temp_co)

# USE temp = data["pm"].iloc[0:5].values

#res = mk.original_test(temp)
#print(res)


#for i, val in enumerate()

#print(temp_pm)

    mankendal_ozon = []
    mankendal_pm = []
    mankendal_so2= []
    mankendal_no2= []
    mankendal_co= []
    mankendal_pm10= []

    mankendal_ozon = trend_analysis(mankendal_ozon, temp_ozon, 'ozone')
    mankendal_pm = trend_analysis(mankendal_pm, temp_pm, 'pm')
    mankendal_co = trend_analysis(mankendal_co, temp_co, 'co')
    mankendal_pm10 = trend_analysis(mankendal_pm10, temp_pm10, 'pm10')
    mankendal_no2 = trend_analysis(mankendal_no2, temp_no2, 'no2')
    mankendal_so2 = trend_analysis(mankendal_so2, temp_so2, 'so2')



  except:
    x = x+1
    if x == 3:
        x = 0
    marker = models[x]
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


test_three = pd.DataFrame(data={"date": data["date"]})
test_three = test_three.set_index("date")
test_three = assign_trends_ini(test_three, mankendal_co)
test_three = change_trend(test_three, mankendal_co, temp_co)
test_three['trend'] = pd.Categorical(test_three['trend'], categories=['decreasing', 'no trend', 'increasing'], ordered=True).codes

test_four = pd.DataFrame(data={"date": data["date"]})
test_four = test_four.set_index("date")
test_four = assign_trends_ini(test_four, mankendal_so2)
test_four = change_trend(test_four, mankendal_so2, temp_so2)
test_four['trend'] = pd.Categorical(test_four['trend'], categories=['decreasing', 'no trend', 'increasing'], ordered=True).codes

test_five = pd.DataFrame(data={"date": data["date"]})
test_five = test_five.set_index("date")
test_five = assign_trends_ini(test_five, mankendal_pm10)
test_five = change_trend(test_five, mankendal_pm10, temp_pm10)
test_five['trend'] = pd.Categorical(test_five['trend'], categories=['decreasing', 'no trend', 'increasing'], ordered=True).codes

test_six = pd.DataFrame(data={"date": data["date"]})
test_six = test_six.set_index("date")
test_six = assign_trends_ini(test_six, mankendal_no2)
test_six = change_trend(test_six, mankendal_no2, temp_no2)
test_six['trend'] = pd.Categorical(test_six['trend'], categories=['decreasing', 'no trend', 'increasing'], ordered=True).codes




#Plotting now

fig, ax = plt.subplots(nrows=6, ncols=3, figsize=(80, 30))


ax[0, 0].plot(a, data["pm"], 'b', lw =0.8, label="PM2.5 AQI")
ax[0, 0].set_title('AQI VALUE OF PM2.5')
fmt_month = mdates.MonthLocator(interval=3)
fmt_year = mdates.YearLocator()
fmt_gen(0, 0, fmt_month, fmt_year)
#
#
ax[0, 1].plot(a, data["pm"], 'b', lw =0.8, label="PM2.5 AQI")
ax[1, 0].set_title('AQI VALUE OF PM2.5')
plot_xline(0,1 , cut_pm)
fmt_month = mdates.MonthLocator(interval=3)
fmt_year = mdates.YearLocator()
fmt_gen(0,1, fmt_month, fmt_year)
#
ax[0, 2].plot(a, test[['trend']])
fmt_gen(0, 2, fmt_month, fmt_year)
plot_xline(0, 2, cut_ozon)
relabel(0,2)
#
ax[1, 0].plot(a, data["ozone"], 'b', lw =0.8, label="OZONE AQI")
ax[1, 0].set_title('AQI VALUE OF OZONE')
fmt_month = mdates.MonthLocator(interval=3)
fmt_year = mdates.YearLocator()
fmt_gen(1, 0, fmt_month, fmt_year)
#
ax[1, 1].plot(a, data["ozone"], 'b', lw =0.8, label="OZONE AQI")
ax[1, 1].set_title('AQI VALUE OF OZONE')
plot_xline(1, 1, cut_ozon)
fmt_month = mdates.MonthLocator(interval=3)
fmt_year = mdates.YearLocator()
fmt_gen(1, 1, fmt_month, fmt_year)
#
#
ax[1, 2].plot(a, test_two[['trend']])
fmt_gen(1, 2, fmt_month, fmt_year)
plot_xline(1, 2, cut_pm)
relabel(1, 2)
#
ax[2, 0].plot(a, data["so2"], 'b', lw =0.8, label="SO2 AQI")
ax[2, 0].set_title('AQI VALUE OF SO2')
fmt_month = mdates.MonthLocator(interval=3)
fmt_year = mdates.YearLocator()
fmt_gen(2, 0, fmt_month, fmt_year)
#
ax[2, 1].plot(a, data["so2"], 'b', lw =0.8, label="SO2 AQI")
ax[2, 1].set_title('AQI VALUE OF SO2')
fmt_month = mdates.MonthLocator(interval=3)
fmt_year = mdates.YearLocator()
fmt_gen(2, 1, fmt_month, fmt_year)
plot_xline(2, 1, cut_so2)
#
ax[2, 2].plot(a, test_four["trend"])
fmt_gen(2, 2, fmt_month, fmt_year)
plot_xline(2, 2, cut_so2)
relabel(2, 2)
#
ax[3, 0].plot(a, data["co"], 'b', lw =0.8, label="CO AQI")
ax[3, 0].set_title('AQI VALUE OF CO')
fmt_month = mdates.MonthLocator(interval=3)
fmt_year = mdates.YearLocator()
fmt_gen(3, 0, fmt_month, fmt_year)
#
ax[3, 1].plot(a, data["co"], 'b', lw =0.8, label="CO AQI")
ax[3, 1].set_title('AQI VALUE OF CO')
fmt_month = mdates.MonthLocator(interval=3)
fmt_year = mdates.YearLocator()
fmt_gen(3,1, fmt_month, fmt_year)
plot_xline(3, 1, cut_co)
#
ax[3, 2].plot(a, test_three["trend"])
fmt_gen(3, 2, fmt_month, fmt_year)
plot_xline(3, 2, cut_co)
relabel(3, 2)
#
ax[4, 0].plot(a, data["pm10"], 'b', lw =0.8, label="PM10 AQI")
ax[4, 0].set_title('AQI VALUE OF PM10')
fmt_month = mdates.MonthLocator(interval=3)
fmt_year = mdates.YearLocator()
fmt_gen(4, 0, fmt_month, fmt_year)
#
ax[4, 1].plot(a, data["pm10"], 'b', lw =0.8, label="PM10 AQI")
ax[4, 1].set_title('AQI VALUE OF PM10')
fmt_month = mdates.MonthLocator(interval=3)
fmt_year = mdates.YearLocator()
fmt_gen(4,1, fmt_month, fmt_year)
plot_xline(4, 1, cut_pm10)
#
ax[4, 2].plot(a, test_five["trend"])
fmt_gen(4, 2, fmt_month, fmt_year)
plot_xline(4, 2, cut_pm10)
relabel(4, 2)
#
#
ax[5, 0].plot(a, data["no2"], 'b', lw =0.8, label="NO2 AQI")
ax[5, 0].set_title('AQI VALUE OF NO2')
fmt_month = mdates.MonthLocator(interval=3)
fmt_year = mdates.YearLocator()
fmt_gen(5, 0, fmt_month, fmt_year)
#
ax[5, 1].plot(a, data["no2"], 'b', lw =0.8, label="NO2 AQI")
ax[5, 1].set_title('AQI VALUE OF NO2')
fmt_month = mdates.MonthLocator(interval=3)
fmt_year = mdates.YearLocator()
fmt_gen(5,1, fmt_month, fmt_year)
plot_xline(5, 1, cut_no2)
#
ax[5, 2].plot(a, test_six["trend"])
fmt_gen(5, 2, fmt_month, fmt_year)
plot_xline(5, 2, cut_no2)
relabel(5, 2)




#test[['trend']].plot()

plt.show()

