from django.shortcuts import render
from . functions import UPorDOWN,  AbrDay,  Date_Today, DateRecieveX,  fetch, recieve_data, value_recieve, recieve_urls_to_fetch, task_threading
from .models import FastProd_DATA, NewApp_DATA


def showhowmany(request):
    date_d, date_pd, date_m, date_pm = DateRecieveX()
    try:
        DayValue = FastProd_DATA.objects.order_by('-id')[0]
        daval=DayValue.date
    except IndexError:
        daval='No'
    if daval ==str(date_d):
        DAU = DayValue.DAU
        MAU = DayValue.MAU
        prevDAU = DayValue.prevDAU
        prevMAU = DayValue.prevMAU

    else:
        data = recieve_data()
        urls = recieve_urls_to_fetch(data, date_d, date_pd, date_m, date_pm, "fast prod")
        results = task_threading(urls)
        DAUX, prevDAUX, MAUX, prevMAUX = value_recieve(results, data)
        DAU = DAUX["fast prod"]
        prevDAU = prevDAUX["fast prod"]
        MAU = MAUX["fast prod"]
        prevMAU = prevMAUX["fast prod"]
        f = FastProd_DATA(date=date_d, prevDAU=prevDAU, prevMAU=prevMAU, DAU=DAU, MAU=MAU)
        f.save()
    date_day = AbrDay(date_d)
    date_month = AbrDay(date_m) + " - " + AbrDay(date_d)
    tria_DAU, DAUgrowth, colD = UPorDOWN(DAU, prevDAU)#изменения за прошлый день
    tria_MAU, MAUgrowth, colM = UPorDOWN(MAU, prevMAU)#изменения за прошлый месяц
    MAU = str(MAU)[:-3] + ' ' + str(MAU)[-3:]
    DAU = str(DAU)[:-3] + ' ' + str(DAU)[-3:]
    date_today = Date_Today()
    date_today_year = date_today.year
    date_today = AbrDay(date_today) + ", " + str(date_today_year)

    context = {"DAU": DAU, "MAU": MAU , "date_day": date_day, "date_month": date_month, "MAUgrowth": MAUgrowth, "DAUgrowth":DAUgrowth, "trMAU":tria_MAU, "trDAU":tria_DAU, "CD": colD, "CM":colM,"date_today":date_today}

    return render(request, 'showusers/howmanyusers.html', context)

def show_app1(request):
    date_d, date_pd, date_m, date_pm = DateRecieveX()

    data = recieve_data()
    urls = recieve_urls_to_fetch(data, date_d, date_pd, date_m, date_pm, "new_app1")
    results = task_threading(urls)
    DAUX, prevDAUX, MAUX, prevMAUX = value_recieve(results, data)
    DAU = DAUX["new_app1"]
    prevDAU = prevDAUX["new_app1"]
    MAU = MAUX["new_app1"]
    prevMAU = prevMAUX["new_app1"]
    f = FastProd_DATA(date=date_d, prevDAU=prevDAU, prevMAU=prevMAU, DAU=DAU, MAU=MAU)
    f.save()
    date_day = AbrDay(date_d)
    date_month = AbrDay(date_m) + " - " + AbrDay(date_d)
    tria_DAU, DAUgrowth, colD = UPorDOWN(DAU, prevDAU)#изменения за прошлый день
    tria_MAU, MAUgrowth, colM = UPorDOWN(MAU, prevMAU)#изменения за прошлый месяц
    MAU = str(MAU)[:-3] + ' ' + str(MAU)[-3:]
    DAU = str(DAU)[:-3] + ' ' + str(DAU)[-3:]
    date_today = Date_Today()
    date_today_year = date_today.year
    date_today = AbrDay(date_today) + ", " + str(date_today_year)

    context = {"DAU": DAU, "MAU": MAU , "date_day": date_day, "date_month": date_month, "MAUgrowth": MAUgrowth, "DAUgrowth":DAUgrowth, "trMAU":tria_MAU, "trDAU":tria_DAU, "CD": colD, "CM":colM,"date_today":date_today}
    return render(request, 'showusers/app1.html', context)

def allapps(request):
    date_d, date_pd, date_m, date_pm = DateRecieveX()
    data = recieve_data()
    app_list = []
    DAU, prevDAU, MAU, prevMAU = {}, {}, {}, {}
    for i in range(len(data["aplications"])):
        app_list.append(data["aplications"][i]["name"])
    try:
        DayValue= FastProd_DATA.objects.order_by('-id')[0]
        daval=DayValue.date
    except IndexError:
        daval= ''
    if daval==str(date_d):
        DAU["fast prod"] =DayValue.DAU
        MAU["fast prod"] =DayValue.MAU
        prevDAU["fast prod"] = DayValue.prevDAU
        prevMAU["fast prod"] = DayValue.prevMAU
    else:
        data = recieve_data()
        urls = recieve_urls_to_fetch(data, date_d, date_pd, date_m, date_pm, "fast prod")
        results=task_threading(urls)
        DAUX, prevDAUX, MAUX, prevMAUX = value_recieve(results, data)
        DAU["fast prod"] = DAUX["fast prod"]
        prevDAU["fast prod"] = prevDAUX["fast prod"]
        MAU["fast prod"] = MAUX["fast prod"]
        prevMAU["fast prod"] = prevMAUX["fast prod"]
        f = FastProd_DATA(date=date_d, prevDAU=prevDAU["fast prod"], prevMAU=prevMAU["fast prod"], DAU=DAU["fast prod"],
                   MAU=MAU["fast prod"])
        f.save()
        app_list.pop("fast prod")
    DAU_all, MAU_all, prevDAU_all, prevMAU_all = 0, 0, 0, 0


    for key in DAU:
        DAU_all += DAU[key]
        MAU_all += MAU[key]
        prevDAU_all += prevDAU[key]
        prevMAU_all += prevMAU[key]

    tria_DAU, DAUgrowth, colD = UPorDOWN(DAU_all, prevDAU_all)  # изменения за прошлый день
    tria_MAU, MAUgrowth, colM = UPorDOWN(MAU_all, prevMAU_all)  # изменения за прошлый месяц
    MAU_all = str(MAU_all)[:-3] + ' ' + str(MAU_all)[-3:]
    DAU_all = str(DAU_all)[:-3] + ' ' + str(DAU_all)[-3:]
    date_today = Date_Today()
    date_today_year = date_today.year
    date_today = AbrDay(date_today) + ", " + str(date_today_year)
    date_day = AbrDay(date_d)
    date_month = AbrDay(date_m) + " - " + AbrDay(date_d)

    #context = {"DAU": DAU, "MAU": MAU , "date_day": date_day, "date_month": date_month, "MAUgrowth": MAUgrowth, "DAUgrowth":DAUgrowth, "trMAU":tria_MAU, "trDAU":tria_DAU, "CD": colD, "CM":colM,"date_today":date_today}

    #return render(request, 'showusers/howmanyusers.html', context)