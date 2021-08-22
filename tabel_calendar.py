#!/usr/bin/env python
# -*- coding: utf-8 -*-

#pip install ipython-beautifulsoup

import json
import requests
import re
from bs4 import BeautifulSoup

month_days = {
    0: 31,
    1: 28,
    2: 31,
    3: 30,
    4: 31,
    5: 30,
    6: 31,
    7: 31,
    8: 30,
    9: 31,
    10: 30,
    11: 31
}


def if_leap_year(ayear):
    if (ayear % 4) == 0:
        if (year % 100) == 0 and (ayear % 400) != 0:
            month_days[1] = 28
            return 0
        month_days[1] = 29
        return 1

    month_days[1] = 28
    return 0


# Получение исходного кода производственного календаря
calendar_url = "https://www.consultant.ru/law/ref/calendar/proizvodstvennye/"
page = requests.get(calendar_url)
soup = BeautifulSoup(page.text, "html.parser")

# получить год календаря
title_text = soup.find("title").text
year = int(re.findall(r'\d+', title_text)[0])

# Получение только необходимого куска кода
code_content = soup.find('div', {'id': 'content'})

# Получение всех тегов таблиц
code_table = code_content.findAll('table', {'class': 'cal'})

arr = {}  # словарь хранения месяцев
table_num = 0  # номер таблицы

for table in code_table:

    arr[table_num] = {}
    table_days_content = table.findAll('tbody')
    days_content = table.findAll('td')

    for day in days_content:
        tday = day.text
        iday = int(tday.replace("*", ""))

        if 'workday' not in arr[table_num].keys():
            arr[table_num]['workday'] = []

        if 'weekend' not in arr[table_num].keys():
            arr[table_num]['weekend'] = []

        if 'shortday' not in arr[table_num].keys():
            arr[table_num]['shortday'] = []

        if 'holiday' not in arr[table_num].keys():
            arr[table_num]['holiday'] = []

        if 'noworkday' not in arr[table_num].keys():
            arr[table_num]['noworkday'] = []

        if "inactively" not in day['class']:
            if '**' in tday:
                arr[table_num]['noworkday'].append(iday)
            elif '*' in tday:
                arr[table_num]['shortday'].append(iday)
            elif 'holiday' in day['class']:
                arr[table_num]['holiday'].append(iday)
            else:
                if 'weekend' in day['class']:
                    arr[table_num]['weekend'].append(iday)
                else:
                    arr[table_num]['workday'].append(iday)

    arr[table_num]['workday'].sort()
    arr[table_num]['weekend'].sort()
    arr[table_num]['shortday'].sort()
    arr[table_num]['holiday'].sort()
    arr[table_num]['noworkday'].sort()

    arr[table_num]['calendar_days'] = month_days[table_num]
    arr[table_num]['workin_days'] = len(arr[table_num]['workday']) + len(arr[table_num]['noworkday']) + len(
        arr[table_num]['shortday'])
    arr[table_num]['weekend_days'] = arr[table_num]['calendar_days'] - arr[table_num]['workin_days']
    arr[table_num]['work_40'] = round(
        len(arr[table_num]['workday']) * 8 + len(arr[table_num]['noworkday']) * 8 + len(arr[table_num]['shortday']) * 7,
        1)
    arr[table_num]['work_39'] = round(
        len(arr[table_num]['workday']) * 7.8 + len(arr[table_num]['noworkday']) * 7.8 + len(
            arr[table_num]['shortday']) * 6.8, 1)
    arr[table_num]['work_36'] = round(
        len(arr[table_num]['workday']) * 7.2 + len(arr[table_num]['noworkday']) * 7.2 + len(
            arr[table_num]['shortday']) * 6.2, 1)
    arr[table_num]['work_24'] = round(
        len(arr[table_num]['workday']) * 4.8 + len(arr[table_num]['noworkday']) * 4.8 + len(
            arr[table_num]['shortday']) * 3.8, 1)

    table_num += 1

allarr = {}
allarr['year'] = year
allarr['leap_year'] = if_leap_year(year)
allarr['months'] = arr

with open("tabel_calendar_" + str(year) + ".json", 'w', encoding='utf-8') as f:
    json.dump(allarr, f, ensure_ascii=False, indent=4)

f.close()
