from datetime import datetime, date, timedelta


def change_dateformat_as_fullmonth(Date):
    date_obj = datetime.strptime(str(Date), "%B %d, %Y")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date

def change_dateformat_as_shortmonth(Date):
    date_obj = datetime.strptime(str(Date), "%b. %d, %Y")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date

def ChangeDateFormat(Date):
    # Date format Change(dd-mm-yyyy => yyyy-mm-dd)
    date_object = datetime.strptime(Date, "%Y-%m-%d")
    Date = date_object.strftime("%b. %d, %Y")
    date_object = datetime.strptime(Date, "%b. %d, %Y").date()
    return date_object