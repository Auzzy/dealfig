import pytz

from dealfig.app import app

_DATE_FORMAT = "%b %d"
_TIME_FORMAT = "%I:%M %p"
_DATETIME_FORMAT = _DATE_FORMAT + _TIME_FORMAT

def _datetimefilter(value, format):
    localized_datetime = pytz.utc.localize(value)
    return localized_datetime.astimezone(pytz.timezone("US/Eastern")).strftime(format)

@app.template_filter()
def datetimefilter(value, format=_DATETIME_FORMAT):
    return _datetimefilter(value, format)

@app.template_filter()
def datefilter(value, format=_DATE_FORMAT):
    return _datetimefilter(value, format)

@app.template_filter()
def timefilter(value, format=_TIME_FORMAT):
    return _datetimefilter(value, format)

app.jinja_env.filters['datetime'] = datetimefilter
app.jinja_env.filters['date'] = datefilter
app.jinja_env.filters['time'] = timefilter
