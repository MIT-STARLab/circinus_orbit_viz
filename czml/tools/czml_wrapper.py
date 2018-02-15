import os
import pkg_resources
import json
from collections import OrderedDict
import copy
import math
import datetime

import jdcal

from  .activity_window import ActivityWindow
from . import czml_text_tools as cztl

# should be 'czml', the package name
package_name = __name__.split('.')[0] 

class CzmlWrapper:
    FLATTEN_NEG_INFINITY_SEC = -3153600000.0  # 100 years in the past, in seconds.
    
    DOC_HEADER_PROTO = pkg_resources.resource_filename(package_name, '/'.join(('prototypes','doc_header_proto.json')))
    GS_PROTO = pkg_resources.resource_filename(package_name, '/'.join(('prototypes','gs_proto.json')))
    OBS_PROTO = pkg_resources.resource_filename(package_name, '/'.join(('prototypes','obs_proto.json')))
    SAT_PROTO = pkg_resources.resource_filename(package_name, '/'.join(('prototypes','satellite_proto.json')))
    PROTO_DEFS = pkg_resources.resource_filename(package_name, '/'.join(('prototypes','definitions.json')))

    czml_dict_keys = ['header','ground stations','observations','satellites','downlinks']

    def __init__(self):
        with open(self.DOC_HEADER_PROTO,'r') as f:
            self.DOC_HEADER_PROTO_JSON = json.load(f,object_pairs_hook=OrderedDict)
        with open(self.GS_PROTO,'r') as f:
            self.GS_PROTO_JSON = json.load(f,object_pairs_hook=OrderedDict)
        with open(self.OBS_PROTO,'r') as f:
            self.OBS_PROTO_JSON = json.load(f,object_pairs_hook=OrderedDict)
        with open(self.SAT_PROTO,'r') as f:
            self.SAT_PROTO_JSON = json.load(f,object_pairs_hook=OrderedDict)
        with open(self.PROTO_DEFS,'r') as f:
            self.PROTO_DEFS = json.load(f)

        self.czml_dict = {key: None for key in  self.czml_dict_keys}

    def make_doc_header(self,
                 name,
                 start_utc="2017-03-15T10:00:00Z",
                 end_utc="2017-03-16T10:00:00Z"):

        if self.DOC_HEADER_PROTO_JSON['PROTO_VERSION'] == '0.1':
            the_json = copy.deepcopy(self.DOC_HEADER_PROTO_JSON)
            del the_json['PROTO_VERSION']
            the_json['name'] = name
            the_json['clock']['interval'] = start_utc + '/' + end_utc
            the_json['clock']['currentTime'] = start_utc
            self.czml_dict['header'] =  [the_json] 

        else:
            raise NotImplementedError

    def flatten_orbit_t_r(self,orbit_t_r,orbit_time_precision,orbit_pos_units_mult):

        orbit_t_r_flat = []

        last_time = self.FLATTEN_NEG_INFINITY_SEC
        mult = orbit_pos_units_mult

        # grab every sub array from orbit_t_r and add to flat array.
        # throw out points if they're less than the desired time diff from the last time
        for t_elem in orbit_t_r:
            curr_time = t_elem[0]
            if last_time + orbit_time_precision <= curr_time:
                to_add = [t_elem[0],t_elem[1]*mult,t_elem[2]*mult,t_elem[3]*mult]
                orbit_t_r_flat = orbit_t_r_flat+to_add

                last_time = curr_time

        return orbit_t_r_flat

    def make_sat(self,
                 name,
                 name_pretty,
                 start_utc="2017-03-15T10:00:00Z",
                 end_utc="2017-03-16T10:00:00Z",
                 description="My very first cubesat!",
                 img_file="CubeSat1.png",
                 orbit_t_r=[],
                 orbit_epoch="2017-03-15T10:00:00Z",
                 orbit_time_precision=1.0,
                 orbit_pos_units_mult=1):

        if self.SAT_PROTO_JSON['PROTO_VERSION'] == '0.1':
            the_json = copy.deepcopy(self.SAT_PROTO_JSON)
            del the_json['PROTO_VERSION']
            the_json['id'] = "Satellite/"+name
            the_json['name'] = name
            the_json['label']['text'] = name_pretty
            the_json['availability'] = start_utc+'/'+end_utc
            the_json['description'] = "<!--HTML-->\\r\\n<p>"+ description +"</p>"
            the_json['billboard']['image']['uri'] = img_file
            the_json['path']['show']['interval'] = start_utc+'/'+end_utc
            the_json['position']['epoch'] =orbit_epoch
            the_json['position']['cartesian'] = self.flatten_orbit_t_r(orbit_t_r,orbit_time_precision,orbit_pos_units_mult)
            
            if self.czml_dict['satellites'] is None:
                self.czml_dict['satellites'] = []
            self.czml_dict['satellites'].append(the_json)

        else:
            raise NotImplementedError

    def make_gs(self,
                 name,
                 name_pretty,
                 start_utc="2017-03-15T10:00:00Z",
                 end_utc="2017-03-16T10:00:00Z",
                 description="A nice ground station",
                 lat_deg=0,
                 lon_deg=0,
                 h_m=0):

        if self.GS_PROTO_JSON['PROTO_VERSION'] == '0.1':
            the_json = copy.deepcopy(self.GS_PROTO_JSON)
            del the_json['PROTO_VERSION']
            the_json['id'] = "Facility/"+name
            the_json['name'] = name
            the_json['label']['text'] = name_pretty
            the_json['availability'] = start_utc+'/'+end_utc
            the_json['description'] = "<!--HTML-->\\r\\n<p>"+ description +"</p>"
            the_json['position']['cartographicDegrees'] = [lon_deg,lat_deg,h_m]
            
            if self.czml_dict['ground stations'] is None:
                self.czml_dict['ground stations'] = []
            self.czml_dict['ground stations'].append(the_json)

        else:
            raise NotImplementedError

    def make_obs_target(self,
             name,
             name_pretty,
             start_utc="2017-03-15T10:00:00Z",
             end_utc="2017-03-16T10:00:00Z",
             description="A nice observation target",
             lat_deg=0,
             lon_deg=0,
             h_m=0):

        if self.OBS_PROTO_JSON['PROTO_VERSION'] == '0.1':
            the_json = copy.deepcopy(self.OBS_PROTO_JSON)
            del the_json['PROTO_VERSION']
            the_json['id'] = "Target/"+name
            the_json['name'] = name
            the_json['label']['text'] = name_pretty
            the_json['availability'] = start_utc+'/'+end_utc
            the_json['description'] = "<!--HTML-->\\r\\n<p>"+ description +"</p>"
            the_json['position']['cartographicDegrees'] = [lon_deg,lat_deg,h_m]

            if self.czml_dict['observations'] is None:
                self.czml_dict['observations'] = []
            self.czml_dict['observations'].append(the_json)

        else:
            raise NotImplementedError

    def convert_flat_times_to_windows(self, times_mat, mat_num_rows, activity_partners_mat= None, mat_num_cols=None):
        """Converts an imported time history matrix to activity windows
        
        [description]

        Uses jdcal package for dealing with modified julian dates from MATLAB code. 
        See https://oneau.wordpress.com/2011/08/30/jdcal/
        jdcal.jd2gcal(jdcal.MJD_0,57827.5774306)
        (have to pass both base date of MJD and the MJD to this function)

        :param times_mat: [description]
        :type times_mat: [type]
        :param mat_num_rows: [description]
        :type mat_num_rows: [type]
        :param activity_partners_mat: [description], defaults to None
        :type activity_partners_mat: [type], optional
        :param mat_num_cols: [description], defaults to None
        :type mat_num_cols: [type], optional
        :returns: [description]
        :rtype: {[type]}
        """

        if activity_partners_mat:
            times_winds = [[[]  for j in range(mat_num_cols)] for k in range(mat_num_rows)]
        else:
            times_winds = [[] for k in range(mat_num_rows)]

        for row_indx in range(0,mat_num_rows):
            if not len(times_mat) > 0:
                break

            times_list = times_mat[row_indx]

            for times_indx, times in enumerate(times_list):

                # if it's not empty
                if len (times)  > 0:

                    # do a bunch of crap to convert to datetime. Note that jd2gcal returns year,month,day, FRACTION OF DAY (GOD WHY!?) so we have to convert.
                    start_time = jdcal.jd2gcal(jdcal.MJD_0,times[0])
                    end_time = jdcal.jd2gcal(jdcal.MJD_0,times[1])
                    start_time_hours = math.floor(start_time[3]*24)
                    start_time_minutes = math.floor((start_time[3]*24-start_time_hours) * 60)
                    start_time_seconds = math.floor(((start_time[3]*24-start_time_hours) * 60 - start_time_minutes) * 60)
                    end_time_hours = math.floor(end_time[3]*24)
                    end_time_minutes = math.floor((end_time[3]*24-end_time_hours) * 60)
                    end_time_seconds = math.floor(((end_time[3]*24-end_time_hours) * 60 - end_time_minutes) * 60)
                    start_time_datetime = datetime.datetime(start_time[0],start_time[1],start_time[2],int(start_time_hours),int(start_time_minutes),int(start_time_seconds))
                    end_time_datetime = datetime.datetime(end_time[0],end_time[1],end_time[2],int(end_time_hours),int(end_time_minutes),int(end_time_seconds))

                    if activity_partners_mat:
                        activity_partner_number = int (activity_partners_mat[row_indx][times_indx]) 
                        times_winds[row_indx][activity_partner_number-1].append(ActivityWindow(start_time_datetime,end_time_datetime))
                    else:
                        times_winds[row_indx].append(ActivityWindow(start_time_datetime,end_time_datetime))

        return times_winds


    def make_downlinks(self,
            dlnk_times_flat,
            dlnk_partners,
            num_sats,
            num_gs,
            gs_names,
            sat_name_prefix,
            start_utc,
            end_utc):

        dlink_winds =  self.convert_flat_times_to_windows(dlnk_times_flat, num_sats, dlnk_partners, num_gs)

         # create downlinks
        if len(dlink_winds) > 0:
            czml_content = []

            dlnk_color = [0,0,255,255]
            i = 0
            for sat_indx in range(num_sats):
                for gs_indx in range(num_gs):
                    name = 'downlink '+str(i)

                    dlnk_winds_sat = dlink_winds[sat_indx][gs_indx]

                    # print dlnks_winds
                    ID = 'Dlnk/Sat'+str(sat_indx+1)+'-GS'+str(gs_indx+1)

                    ref1 =  self.PROTO_DEFS['sat_pos_ref_pre']+ sat_name_prefix +str(sat_indx)+self.PROTO_DEFS['pos_ref_post']
                    gs_name = gs_names[gs_indx]
                    ref2 = self.PROTO_DEFS['gs_pos_ref_pre']+gs_name+self.PROTO_DEFS['pos_ref_post']
                    czml_content.append(cztl.createLinkPacket(ID,name,start_utc,end_utc, polyline_show_times = dlnk_winds_sat, color=dlnk_color,reference1=ref1,reference2=ref2))

                    i+=1

            self.czml_dict['downlinks'] = czml_content


    def get_czml( self,key_list=None):

        if key_list is None:
            key_list = self.czml_dict_keys


        the_czml = []
        for key in key_list:
            if not self.czml_dict.get(key,None) is None:
                the_czml +=self.czml_dict[key]
            else:
                raise RuntimeError ('key %s either is not a valid key or has not been initialized')

        return the_czml
        