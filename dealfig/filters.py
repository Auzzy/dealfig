import pytz

from dealfig.app import app

def _datetimefilter(value, format='%b %d %I:%M %p'):
    localized_datetime = pytz.utc.localize(value)
    return localized_datetime.astimezone(pytz.timezone("US/Eastern")).strftime(format)

@app.template_filter()
def datetimefilter(value, format='%b %d %I:%M %p'):
    return _datetimefilter(value, format)

@app.template_filter()
def datefilter(value, format='%b %d'):
    return _datetimefilter(value, format)

@app.template_filter()
def timefilter(value, format='%I:%M %p'):
    return _datetimefilter(value, format)

app.jinja_env.filters['datetime'] = datetimefilter
app.jinja_env.filters['date'] = datefilter
app.jinja_env.filters['time'] = timefilter
