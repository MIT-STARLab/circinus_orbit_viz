# use the SublimePrettyJson package in to pretty print the output czml correctly (note that the json has to be valid for pretty print to work). Link: https://github.com/dzhibas/SublimePrettyJson/issues

import datetime
import collections

def get_value_intervals(show_times, start_avail, end_avail, value_functions=  (lambda wind: True,False), value_type='boolean'):
    '''
    This creates a list of intervals with values specified by the functions present in the value_functions tuple

    the default use for this is Boolean "show" intervals in standard czml packets
    '''

    intervals = []
    intervals_values = []

    if len(show_times) > 0:
        last_time = start_avail

        for i, window  in enumerate(show_times):
            start = window.start
            end = window.end

            # check case where window is before start_avail
            if start < last_time and end < last_time:
                continue
            elif start < last_time:
                start_time = last_time
            else:
                start_time = start

            # check case where window is after end_avail
            if start > end_avail and end > end_avail:
                continue
            elif end > end_avail:
                end_time = end_avail
            else:
                end_time = end

            # add an empty space between windows. value_functions[1] with no arguments, because  it's not a function
            if not last_time == start_time:
                intervals.append([last_time,start_time])
                intervals_values.append(value_functions[1])

            # add a value for the current window. we call value_functions[0]  with an argument because it should be a function
            if not start_time == end_time:
                intervals.append([start_time,end_time])
                intervals_values.append( value_functions[0](window))

            if end_time < start_time:
                print('error 1')
            if start_time < last_time:
                print(start_time)
                print(last_time)
                print('error 2')

            last_time = end_time

        # add very last  empty space 
        intervals.append([last_time,end_avail])
        intervals_values.append(value_functions[1])

        if end_avail < last_time:
            print('error 3')

    # Store intervals in jsonic object
    json_intervals = []

    if intervals:
        for i, intervals in enumerate(intervals):

            interval = intervals[0].strftime('%Y-%m-%dT%H:%M:%SZ')+'/'+intervals[1].strftime('%Y-%m-%dT%H:%M:%SZ')

            json_intervals.append({'interval':interval,value_type:intervals_values[i]})

    return json_intervals

def create_gs(name,start_avail=datetime.datetime(2017, 3, 15, 10, 0, 0),end_avail=datetime.datetime(2017, 3, 16, 10, 0, 0),latitude=0.0,longitude=0.0):

    gs = collections.OrderedDict()

    name_without_num = ' '.join(name.split(' ')[:-1])

    gs['id'] = 'Facility/'+name
    gs['name'] = name
    gs['availability'] = start_avail.strftime('%Y-%m-%dT%H:%M:%SZ')+'/'+end_avail.strftime('%Y-%m-%dT%H:%M:%SZ')

    description = 'no description'
    gs['description'] = '<!--HTML--><p>'+description+'</p>'


    eyeOffset = {'cartesian':[0,0,0]}
    pixelOffset = {'cartesian2':[0,0]}
    img_str = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAACvSURBVDhPrZDRDcMgDAU9GqN0lIzijw6SUbJJygUeNQgSqepJTyHG91LVVpwDdfxM3T9TSl1EXZvDwii471fivK73cBFFQNTT/d2KoGpfGOpSIkhUpgUMxq9DFEsWv4IXhlyCnhBFnZcFEEuYqbiUlNwWgMTdrZ3JbQFoEVG53rd8ztG9aPJMnBUQf/VFraBJeWnLS0RfjbKyLJA8FkT5seDYS1Qwyv8t0B/5C2ZmH2/eTGNNBgMmAAAAAElFTkSuQmCC'
    billboard = {'eyeOffset':eyeOffset, \
        'image':img_str,                \
        'pixelOffset':pixelOffset,      \
        'scale':2.0,                    \
        'show':True,                    \
        'verticalOrigin':'CENTER',      \
        'horizontalOrigin':'CENTER'}
    gs['billboard'] = billboard


    fillColor = {'rgba':[0, 255, 255, 255]}
    outlineColor = {'rgba':[0, 0, 0, 255]}
    pixelOffset = {'cartesian2':[12,0]}
    label = {'fillColor':fillColor,     \
        'font':'10pt Lucida Console',   \
        'outlineColor':outlineColor,    \
        'outlineWidth':2,               \
        'pixelOffset':pixelOffset,      \
        'show':True,                    \
        'style':'FILL_AND_OUTLINE',     \
        'text':name_without_num,        \
        'verticalOrigin':'CENTER',      \
        'horizontalOrigin':'LEFT'}
    gs['label'] = label

    gs['position'] = {'cartographicDegrees':[longitude,latitude,0]}

    return gs

def create_obs_target(name,start_avail=datetime.datetime(2017, 3, 15, 10, 0, 0),end_avail=datetime.datetime(2017, 3, 16, 10, 0, 0),latitude=0.0,longitude=0.0,include_billboard = True, name_with_num = False, target_pic = 'target.jpg'):

    obs_targ = collections.OrderedDict()

    if name_with_num:
        name_without_num = name
    else:
        name_without_num = ' '.join(name.split(' ')[:-1])

    obs_targ['id'] = 'Target/'+name
    obs_targ['name'] = name
    obs_targ['availability'] = start_avail.strftime('%Y-%m-%dT%H:%M:%SZ')+'/'+end_avail.strftime('%Y-%m-%dT%H:%M:%SZ')

    description = 'no description'
    obs_targ['description'] = '<!--HTML--><p>'+description+'</p>'

    if include_billboard:
        eyeOffset = {'cartesian':[0,0,0]}
        pixelOffset = {'cartesian2':[0,0]}
        image = {'uri':target_pic}
        billboard = {'eyeOffset':eyeOffset, \
            'image':image,                  \
            'pixelOffset':pixelOffset,      \
            'scale':0.1,                    \
            'show':True,                    \
            'verticalOrigin':'CENTER',      \
            'horizontalOrigin':'CENTER'}
        obs_targ['billboard'] = billboard

    fillColor = {'rgba':[0, 255, 255, 255]}
    outlineColor = {'rgba':[0, 0, 0, 255]}
    pixelOffset = {'cartesian2':[12,0]}
    label = {'fillColor':fillColor,     \
        'font':'10pt Lucida Console',   \
        'outlineColor':outlineColor,    \
        'outlineWidth':2,               \
        'pixelOffset':pixelOffset,      \
        'show':True,                    \
        'style':'FILL_AND_OUTLINE',     \
        'text':name_without_num,        \
        'verticalOrigin':'CENTER',      \
        'horizontalOrigin':'LEFT'}
    obs_targ['label'] = label

    obs_targ['position'] = {'cartographicDegrees':[longitude,latitude,0]}

    return obs_targ

def create_obs_rectangle(name,start_avail=datetime.datetime(2017, 3, 15, 10, 0, 0),end_avail=datetime.datetime(2017, 3, 16, 10, 0, 0),color=[0,0,255,255],lower_lat=0.0,upper_lat=10.0,left_long=5.0,right_long=10.0):

    obs_rect = collections.OrderedDict()

    name_without_num = ' '.join(name.split(' ')[:-1])

    obs_rect['id'] = 'Rectangle/'+name
    obs_rect['name'] = name
    obs_rect['availability'] = start_avail.strftime('%Y-%m-%dT%H:%M:%SZ')+'/'+end_avail.strftime('%Y-%m-%dT%H:%M:%SZ')

    description = 'no description'
    obs_rect['description'] = '<!--HTML--><p>'+description+'</p>'


    rec_string_1 = '"rectangle": {\n"show": true,\n"height": 0,\n"coordinates": {\n"wsenDegrees": ['+str(left_long)+','+str(lower_lat)+','+str(right_long)+','+str(upper_lat)+']\n},'

    coordinates = {'wsenDegrees':[left_long,lower_lat,right_long,upper_lat]}
    material = {'solidColor':{'color':{'rgba':color}}}
    rectangle = {'show':True,       \
        'height':0,                 \
        'coordinates':coordinates,  \
        'fill':True,                \
        'material':material}
    obs_rect['rectangle'] = rectangle

    return obs_rect


def create_link_packet(ID='Xlnk/SatN-to-SatM',name='a link',start_avail=datetime.datetime(2017, 3, 15, 10, 0, 0),end_avail=datetime.datetime(2017, 3, 16, 10, 0, 0), polyline_show_times = [[datetime.datetime(2017, 3, 15, 12, 0, 0),datetime.datetime(2017, 3, 16, 1, 0, 0)],[datetime.datetime(2017, 3, 16, 5, 0, 0),datetime.datetime(2017, 3, 16, 9, 0, 0)]], color=[0,0,255,255],reference1='Satellite/CubeSatN#position',reference2='Satellite/CubeSatM#position'):

    link = collections.OrderedDict()

    link['id'] = ID
    link['name'] = name
    link['availability'] = start_avail.strftime('%Y-%m-%dT%H:%M:%SZ')+'/'+end_avail.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Figure out intervals for showing and not showing
    show_intervals = get_value_intervals(polyline_show_times, start_avail, end_avail)
    show_intervals = show_intervals if show_intervals else False

    material = {'solidColor':{'color':{'rgba':color}}}
    positions = {'references':[reference1,reference2]}
    polyline = {'width':6,          \
        'followSurface':False,      \
        'positions':positions,      \
        'show': show_intervals,      \
        'material':material}
    link['polyline'] = polyline

    #  we need to add a position proxy here so that a basic link packet can be used with auxrenderer without throwing missing position errors
    link['position_proxy'] = {'reference':reference2}

    return link


def create_obs_packet(ID='Satellite/CubeSatN/Sensor/SensorM',name='observation sensor M for satellite N',parent='Satellite/CubeSatN',start_avail=datetime.datetime(2017, 3, 15, 10, 0, 0),end_avail=datetime.datetime(2017, 3, 16, 10, 0, 0), sensor_show_times = [[datetime.datetime(2017, 3, 15, 12, 0, 0),datetime.datetime(2017, 3, 16, 1, 0, 0)],[datetime.datetime(2017, 3, 16, 5, 0, 0),datetime.datetime(2017, 3, 16, 9, 0, 0)]], lateral_color=[0,255,0,51],intersection_color=[0,255,0,255],position_ref='Satellite/CubeSatN#position',orientation_ref='Satellite/CubeSatN#orientation'):

    obs_sensor = collections.OrderedDict()

    obs_sensor['id'] = ID
    obs_sensor['name'] = name
    obs_sensor['parent'] = parent
    obs_sensor['availability'] = start_avail.strftime('%Y-%m-%dT%H:%M:%SZ')+'/'+end_avail.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Figure out intervals for showing and not showing
    # print sensor_show_times
    show_intervals = get_value_intervals(sensor_show_times, start_avail, end_avail)
    show_intervals = show_intervals if show_intervals else False

    intersectionColor = {'rgba':intersection_color}
    lateralSurfaceMaterial = {'solidColor':{'color':{'rgba':lateral_color}}}
    conicSensor = {
        'showIntersection':True,
        'intersectionColor':intersectionColor,
        'intersectionWidth':2,
        'portionToDisplay':"COMPLETE",
        'lateralSurfaceMaterial':lateralSurfaceMaterial,
        'innerHalfAngle':0,
        'outerHalfAngle':0.5,
        'minimumClockAngle':0.0,
        'maximumClockAngle':6.283185307179586,
        'radius':5e7,
        'show': show_intervals}
    obs_sensor['agi_conicSensor'] = conicSensor

    obs_sensor['position'] = {'reference':position_ref}
    obs_sensor['orientation'] = {'reference':orientation_ref}

    return obs_sensor

def create_sampled_property_history(ID='Satellite/CubeSatN',name='q_o_sizes_history for satellite', custom_property_name ='datavol', epoch = datetime.datetime(2017, 3, 15, 10, 0, 0) , history = [[0,0],[86400,0]],filter_seconds_beg=0,filter_seconds_end=86400, sample_type='number'):
    '''
    This creates a czml packet for a custom Number property.

    history must be in format:
    [ t1 , val1
      t2 , val2
      t3 , val3
      tf , valf ]

      t values are measured since epoch
    '''

    history_pkt = collections.OrderedDict()
    history_pkt['id'] = ID
    history_pkt['name'] = name

    interleaved_time_value_list = []
    for i, sample in enumerate(history):
        if sample[0] < filter_seconds_beg or sample[0] > filter_seconds_end:
            continue

        interleaved_time_value_list.append(sample[0])
        interleaved_time_value_list.append(sample[1])

    history_stuff = {'interpolationAlgorithm':'LINEAR',   \
        'interpolationDegree':1,                        \
        'epoch':epoch.strftime('%Y-%m-%dT%H:%M:%SZ'),   \
        sample_type:interleaved_time_value_list}
    history_pkt[custom_property_name] = history_stuff

    return history_pkt

def create_show_intervals_packet(ID='Facility/GS Name',name='gs avail windows gs num N', custom_property_name ='gs_availability', start_avail=datetime.datetime(2017, 3, 15, 10, 0, 0), end_avail=datetime.datetime(2017, 3, 16, 10, 0, 0), show_times = [[datetime.datetime(2017, 3, 15, 12, 0, 0),datetime.datetime(2017, 3, 16, 1, 0, 0)],[datetime.datetime(2017, 3, 16, 5, 0, 0),datetime.datetime(2017, 3, 16, 9, 0, 0)]]):
    '''
    This creates a czml packet for a custom boolean property. We hijack the show intervals creation function to create the intervals
    '''

    show_pkt = collections.OrderedDict()

    show_pkt['id'] = ID
    show_pkt['name'] = name

    # Figure out intervals for showing and not showing
    show_intervals = get_value_intervals(show_times, start_avail, end_avail)
    show_intervals = show_intervals if show_intervals else False

    show_pkt[custom_property_name] = show_intervals

    return show_pkt