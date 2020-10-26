import json
import requests
import datetime
import monthdelta
import math
from concurrent.futures import ThreadPoolExecutor, as_completed


def UPorDOWN(first, second):
    index = str(math.fabs(round((first - second) / second * 100 , 1)))
    if first>second:
        index=index + '%'
        tria='▲'
        color='green'
    elif first<second:
        index=index + "%"
        tria='▼'
        color='red'
    else:
        index = index + "%"
        tria = ''
        color='grey'
    return tria ,index, color

def AbrDay(date):
    x = str(date)
    a = x.split('-')
    mdate = datetime.datetime.strptime(str(a[1]), "%m").strftime("%b")
    return (mdate+" " +a[2])

def Date_Today():
    date = datetime.date.today()
    return date

def DateRecieveX():
    date = datetime.date.today()-datetime.timedelta(days=1)
    if date.weekday() == 6:
        date = date-datetime.timedelta(days=2)
    elif date.weekday() == 5:
        date = date-datetime.timedelta(days=1)
    date_pday= date - datetime.timedelta(days=1)
    if date_pday.weekday() == 6:
        date_pday = date-datetime.timedelta(days=2)
    elif date_pday.weekday() == 5:
        date = date_pday-datetime.timedelta(days=1)
    date_month = date - monthdelta.monthdelta(months=1)
    date_pmonth = date - monthdelta.monthdelta(months=2)
    return date, date_pday, date_month, date_pmonth

def fetch(url, headers, params, app_name, time_interval):
    response = requests.get(url,
                            headers=headers, params=params)

    mydata = json.loads(response.text)
    value = mydata['tables'][-1]['rows'][-1][-1]

    return value, time_interval, app_name

def task_threading(urls):
    processes = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        for url in urls:
            processes.append(executor.submit(fetch, url[0], url[1], url[2], url[3], url[4]))

    results=[]
    for task in as_completed(processes):
        results.append(task.result())
    return results

def recieve_data():
    with open("showusers/properties.json", "r") as read_file:
        data = json.load(read_file)
    return data

def recieve_urls_to_fetch(data, date_day, date_pday, date_month, date_pmonth, *app_names):

    x=(data['params']['day'])
    x_1=(x.replace("start_date", str(date_day))).replace("end_date", str(date_day))
    x_2=(x.replace("start_date", str(date_pday))).replace("end_date", str(date_pday))
    y=(data['params']['month'])
    y_1=(y.replace("start_date", str(date_month))).replace("end_date", str(date_pday))
    y_2=(y.replace("start_date", str(date_pmonth))).replace("end_date", str(date_month))
    params = [(('query', x_1),), (('query', x_2),), (('query', y_1),), (('query', y_2),)]

    headers = []
    url = []
    app_name=[]
    for i in range(len(data["applications"])):
        if data["applications"][i]["name"] in app_names:
            headers.append({'x-api-key': data["applications"][i]["ap_key"], })
            url.append(data["applications"][i]["ap_url"])
            app_name.append(data["applications"][i]["name"])

    time_intervals=data['time_intervals'].split()

    urls=[]
    for i in range(len(url)):
        for j in range(len(params)):
            row = []
            row.extend([url[i], headers[i], params[j], app_name[i], time_intervals[j]])
            urls.append(row)
    return urls

def value_recieve(results, data):
    DAU, prevDAU, MAU, prevMAU = {}, {}, {}, {}
    for i in range(len(results)):
        time_intervals = data['time_intervals'].split()
        if results[i][1] == time_intervals[0]:
            DAU[results[i][2]]=results[i][0]
        elif results[i][1] == time_intervals[1]:
            prevDAU[results[i][2]]=results[i][0]
        elif results[i][1] == time_intervals[2]:
            MAU[results[i][2]]=results[i][0]
        else:
            prevMAU[results[i][2]]=results[i][0]
    return DAU, prevDAU, MAU, prevMAU