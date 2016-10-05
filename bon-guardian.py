import urllib.request
import re
import datetime
import calendar


def get_number_of_meals(cookie):
    pattern = re.compile('subsidiesNumber">\d+')
    request = urllib.request.Request("https://www.studentska-prehrana.si/Pages/Overview.aspx", headers={'Cookie': cookie})
    raw_html = urllib.request.urlopen(request).read()
    target_string = re.findall(pattern, str(raw_html))
    number_of_meals = re.findall(r'\d+', target_string[0])
    return number_of_meals[0]


def get_remaining_workdays_in_month():
    now = datetime.datetime.now()
    today = datetime.date(now.year, now.month, now.day)
    number_of_days_in_month = calendar.monthrange(now.year, now.month)[1]
    end = datetime.date(now.year, now.month, number_of_days_in_month)
    daydiff = end.weekday() - today.weekday()

    return ((end-today).days - daydiff) / 7 * 5 + min(daydiff, 5) - (max(end.weekday() - 4, 0) % 5)


def get_warning_type(number_of_meals, workdays_left):
    if number_of_meals < workdays_left:
        return "You have less bon's than workdays left."
    elif number_of_meals < 2*workdays_left:
        return "You should not eat twice a day anymore."
    elif number_of_meals > 60:
        return "You should eat more because your bon's will go to waste."
    else:
        return 0


with open('cookie.txt', 'r') as myfile:
    cookie = myfile.read()
number_of_meals = float(get_number_of_meals(cookie))
workdays_left = get_remaining_workdays_in_month()
print(number_of_meals)
print(get_warning_type(number_of_meals, workdays_left))




