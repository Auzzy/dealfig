import pytz

from dealfig.app import app

_DATE_FORMAT = "%m/%d/%Y"
_COMMENT_DATE_FORMAT = "%b %d"
_COMMENT_TIME_FORMAT = "%I:%M %p"

@app.template_filter("localize_datetime")
def localize_datetime_filter(value):
    return pytz.utc.localize(value).astimezone(pytz.timezone("US/Eastern"))

@app.template_filter("comment_datetime")
def comment_datetime_filter(value):
    comment_datetime = localize_datetime_filter(value)
    comment_date_str = comment_datetime.strftime(_COMMENT_DATE_FORMAT)
    comment_time_str = comment_datetime.strftime(_COMMENT_TIME_FORMAT)
    return "{} at {}".format(comment_date_str, comment_time_str)

@app.template_filter("date")
def date_filter(value):
    return value.strftime(_DATE_FORMAT)
