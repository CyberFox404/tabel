# pip install ipython-beautifulsoup

import requests
import re
from bs4 import BeautifulSoup

from lib.cycle_stepper import cycle_stepper


cs = cycle_stepper(1, 3)



month_days = {
    1: 31,
    2: 28,
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31
}


def if_leap_year(ayear):
    if (ayear % 4) == 0:
        if (year % 100) == 0 and (ayear % 400) != 0:
            month_days[2] = 28
            return 0
        month_days[2] = 29
        return 1

    month_days[2] = 28
    return 0


# Получение исходного кода производственного календаря
calendar_url = "http://www.garant.ru/calendar/buhpravo/"
page = requests.get(calendar_url)
soup = BeautifulSoup(page.text, "html.parser")

# получить год календаря
meta_title = soup.find("meta", {"property": "og:title"})
year = int(re.findall(r'\d+', meta_title["content"])[0])
print("год %d\n" % year)

# проверка года на високосность
print("проверка года на високосность %d\n" % (if_leap_year(year)))

# Получение только необходимого куска кода
code_content = soup.find('div', {'class': 'page-content'})

# Получение всех тегов таблиц
code_table = code_content.findAll('table', {'class': 'tabCalendar'})
num_table = 0
num_tr = 0
num_td = 0
last_date = 0
arr = {}
#month_num = 1
#month_min = 1
#month_num_count = 3
day_arr = 0

for table in code_table:

    if (num_table + 2) % 2 == 0:

        print("таблица %d\n" % num_table)
        code_tr = table.findAll('tr')

        for tr in code_tr:

            print("строка %d\n" % num_tr)

            if num_tr == 0:
                print("пропуск строки %d\n" % num_tr)
                num_tr += 1
                continue
            code_td = tr.findAll('td')

            for td in code_td:

                if_holiday = False

                td_text = td.text.strip()
                td_clean_text = td_text.replace("*", "").replace("'", "")

                if td_text != "":

                    day_arr = 0

                    if num_td == 0:
                        print("пропуск столбца %d / %s" % (num_td, td_text))
                        num_td += 1
                        continue

                    if "/" in td_clean_text:
                        day_arr = 1
                        daya = list(map(int, td_clean_text.split('/')))
                        day = daya[0]
                    else:
                        day = int(td_clean_text)

                    if day < last_date:
                        #month_num += 1
                        #if month_num > month_num_count:
                        #    month_num = month_min
                        cs.step()
                        #cs.nextgroup()
                        print()

                    print("month_num %d" % cs.check())
                    print("td.text.strip() %s" % td_text)

                    if len(arr) < cs.check():
                        arr[cs.check()] = {}

                    if 'workday' not in arr[cs.check()].keys():
                        print("not workday in %d" % cs.check())
                        arr[cs.check()]['workday'] = []

                    if 'deworkday' not in arr[cs.check()].keys():
                        print("not deworkday in %d" % cs.check())
                        arr[cs.check()]['deworkday'] = []

                    if 'shortday' not in arr[cs.check()].keys():
                        print("not shortday in %d" % cs.check())
                        arr[cs.check()]['shortday'] = []

                    if 'holiday' not in arr[cs.check()].keys():
                        print("not holiday in %d" % cs.check())
                        arr[cs.check()]['holiday'] = []

                    # проверка даты на выходной день
                    if_holiday = td.find('span')

                    if td.has_attr('style'):
                        if "color: rgb(255, 0, 0)" in td['style']:
                            if_holiday = True

                    # Сортируем дни на выходные, праздничные, сокращенные и рабочие
                    if "'" in td_text:
                        print("deworkday %d" % day)

                        if day_arr == 1:
                            for t in range(len(daya)):
                                arr[cs.check()]['deworkday'].append(t)
                        else:
                            arr[cs.check()]['deworkday'].append(day)

                        arr[cs.check()]['deworkday'].sort()

                    elif "*" in td_text:
                        # print("is_short")
                        print("shortday %d" % day)
                        if day_arr == 1:
                            for t in range(len(daya)):
                                arr[cs.check()]['shortday'].append(t)
                        else:
                            arr[cs.check()]['shortday'].append(day)

                        arr[cs.check()]['shortday'].sort()

                    elif if_holiday:
                        # print("is_holiday")
                        # print(arr)
                        print("holiday %d" % day)
                        if day_arr == 1:
                            for t in range(len(daya)):
                                arr[cs.check()]['holiday'].append(t)
                        else:
                            arr[cs.check()]['holiday'].append(day)

                        arr[cs.check()]['holiday'].sort()

                    elif tr.has_attr('class'):
                        if tr['class'][0] == 'redDay':  # Notice that I put [0], as para['class'] is a list.
                            # print("is_holiday")
                            print("holiday %d" % day)
                            if day_arr == 1:
                                for t in range(len(daya)):
                                    arr[cs.check()]['holiday'].append(t)
                            else:
                                arr[cs.check()]['holiday'].append(day)

                            arr[cs.check()]['holiday'].sort()

                    else:
                        print("work day %d" % day)
                        if day_arr == 1:
                            for t in range(len(daya)):
                                arr[cs.check()]['workday'].append(t)
                        else:
                            arr[cs.check()]['workday'].append(day)

                        arr[cs.check()]['workday'].sort()

                    print(arr)

                    last_date = day
                    num_td += 1

            num_tr += 1
            num_td = 0

            # Здесь считать часы

            # quarter

            print("--- коней строки ---")
            print()

        num_tr = 0
        # break

        #month_min = month_min + month_num_count
        #month_num = month_min
        cs.nextgroup()
        # month_min = 1
        # month_num_count = 3

    num_table += 1

for u in range(1, len(arr) + 1):
    print(u)
    arr[u]['calendar_days'] = month_days[u]
    arr[u]['work_40'] = round(len(arr[u]['workday']) * 8 + len(arr[u]['shortday']) * 7, 1)
    arr[u]['work_39'] = round(len(arr[u]['workday']) * 7.8 + len(arr[u]['shortday']) * 6.8, 1)
    arr[u]['work_36'] = round(len(arr[u]['workday']) * 7.2 + len(arr[u]['shortday']) * 6.2, 1)
    arr[u]['work_24'] = round(len(arr[u]['workday']) * 4.8 + len(arr[u]['shortday']) * 3.8, 1)

print(arr)
