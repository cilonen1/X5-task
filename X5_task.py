import pandas as pd
import numpy as np
import datetime
from random import randint,uniform

def generalize(std,num,days):
    """"
    Генерирует датафрейм с трафиком за каждый день(на протяжении всего периода days) так, чтобы значения
    для каждого магазина  были одного порядка
    :param std : предел отклонения от значения трафика, полученного  случайным образом в 1-й итерации
    :param num : число магазинов
    :param days : кол-во дней для всего рассматриваемого периода
    :return final: датафрейм, в котором для каждого магазина и для каждого дня (за период days) указано кол-во посетителей
     """"
    shops = [i + 1 for i in range(num) for j in range(days)]
    date = [datetime.date(2019,1,1) + datetime.timedelta(j) for i in range(num) for j in range(days)]
    traffic = []
    elem = {}
    for i in range(days*num):
        if shops[i] in elem:
            traffic.append(int(elem[shops[i]] + elem[shops[i]]*uniform(-std,std)))
        else:
            elem[shops[i]] = randint(100,10000)
            traffic.append(elem[shops[i]])
    dat = {'ID':shops,'date':date,'traffic':traffic}
    final = pd.DataFrame(dat)
    return final

def linearize(final,year,month,day):
    """"
    1.Считаем среднее значение траффика для каждого магазина в предпилотный период
    2.Создаем датафрейм, в который вносим данные из датафрейма final, но только за пилотный период, причем
    в качестве траффика вносим отклонение от среднего значения для обсчитываемого магазина
    :param final : датафрейм, в котором для каждого магазина и для каждого дня (за период days) указано кол-во посетителей
    :param year : год окончания предпилотного периода
    :param month : месяц окончания предпилотного периода
    :param day : день окончания предпилотного периода
    :return pilot: датафрейм, в котором для каждого магазина и для каждого дня (за пилотный период) 
    указано кол-во посетителей, но не в абсолютном значении,а отклонение от среднего значения для этого магазина в предпилотный период 
    """"
    avg = final[final['date'] <= datetime.date(year,month,day)].groupby('ID')['traffic'].mean()
    pilot = pd.DataFrame()
    for row in final[final['date'] > datetime.date(year,month,day)].itertuples(index = False):
        pilot = pilot.append({'ID':row[0],'traffic':(row[2]-avg[row[0]]),'date':row[1]},ignore_index=True)
    return pilot


final = generalize(-0.15,10,181)
pilot = linearize(final,2019,3,31)
final.to_csv("gen.csv")
pilot.to_csv("pilot.csv")




