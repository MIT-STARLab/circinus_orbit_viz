import jdcal
import math
from datetime import datetime

def iso_string_to_dt(iso_string):
    return datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S.%fZ")

def mjd2datetime(mjd):
    '''  convert modified Julian date to Python daytime
    
    Uses jdcal package for dealing with modified julian dates 
        See https://oneau.wordpress.com/2011/08/30/jdcal/
        jdcal.jd2gcal(jdcal.MJD_0,57827.5774306)
        (have to pass both base date of MJD and the MJD to this function)

    :param mjd: time as modified julian date
    :return: equivalent datetime object
    '''

    jdcal_time = jdcal.jd2gcal(jdcal.MJD_0, mjd)
    jdcal_time_hours = math.floor(jdcal_time[3] * 24)
    jdcal_time_minutes = math.floor((jdcal_time[3] * 24 - jdcal_time_hours) * 60)
    jdcal_time_seconds = math.floor(((jdcal_time[3] * 24 - jdcal_time_hours) * 60 - jdcal_time_minutes) * 60)
    datetime_time = datetime(jdcal_time[0], jdcal_time[1], jdcal_time[2], int(jdcal_time_hours),
                                            int(jdcal_time_minutes), int(jdcal_time_seconds))
    return datetime_time

def datetime2mjd(time):
    '''
    :param time: datetime object
    :return: time as modified julian date
    '''

    dummy, mjd_midnight = jdcal.gcal2jd(time.year , time.month, time.day)

    # add in fraction of day
    mjd = mjd_midnight+ time.hour/24.0 + time.minute/24.0/60 + time.second/24.0/60/60

    return mjd
