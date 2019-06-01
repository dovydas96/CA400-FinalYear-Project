import arrow


def datetimeformat(date):
    date_time = arrow.get(date)
    return date_time.humanize()
