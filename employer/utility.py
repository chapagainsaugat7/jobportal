import datetime

def default_deadline():
    #by default, deadline of job is 7 days.
    return datetime.datetime.now() + datetime.timedelta(days=7)