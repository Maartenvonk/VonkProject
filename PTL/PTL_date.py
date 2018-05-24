import datetime


def date_Today_String():
    """
    :return: the date of today in a string: yyy-mm-dd
    """
    date_In_String = datetime.now().strftime("%Y-%m-%d")
    return date_In_String


def date_today_datetime():
    """

    :return: the date of today in a datetime form
    """
    return datetime.datetime.now().strftime("%Y-%m-%d")


def from_Date_To_String(dateDate):
    """
    :param dateDate: take a date of the type datetime
    :return: string in the form. yyyy-mm-dd
    """
    y = datetime.strptime(dateDate, "%d-%m-%Y")
    return y.strftime("%Y-%m-%d")


def week_start_date(year, week):
    """
    Returns date of the monday of a weeknumber
    :param year: int year
    :param week: int weeknumber
    :return: string, date (exm: 2016-01-04)
    """
    d = datetime.date(year, 1, 1)
    delta_days = d.isoweekday() - 1
    delta_weeks = week
    if year == d.isocalendar()[0]:
        delta_weeks -= 1
    delta = datetime.timedelta(days=-delta_days, weeks=delta_weeks)
    return d + delta


def end_date_of_a_month(date):
    start_date_of_this_month = date.replace(day=1)

    month = start_date_of_this_month.month
    year = start_date_of_this_month.year
    if month == 12:
        month = 1
        year += 1
    else:
        month += 1
    next_month_start_date = start_date_of_this_month.replace(month=month, year=year)

    this_month_end_date = next_month_start_date - datetime.timedelta(days=1)
    return this_month_end_date


def date_in_period(date, start_date_period, end_date_period):
    """
    :param date: required date to check
    :param start_date_period: start date in period
    :param end_date_period: end date in period
    :return: True when date is between (and including) start and from date
    """
    if start_date_period <= date <= end_date_period:
        return True
    else:
        return False
