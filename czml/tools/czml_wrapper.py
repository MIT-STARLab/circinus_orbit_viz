import os
import pkg_resources
import json
from collections import OrderedDict
import copy
import math
from datetime import datetime

import jdcal

from circinus_tools.activity_window import ActivityWindow
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


    czml_dict_keys = ['header','ground stations','targets','satellites','downlinks','crosslinks','observations', 'downlink_rates','crosslink_rates']

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

        self.viz_objects_callbacks=  {}

        self.json_metadata = {
            "simulation_output_updated": None,
            "visualization_output_updated": str (datetime.utcnow ())
        }

        # self.renderers = renderers

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
                 sat_id,
                 name,
                 name_pretty,
                 start_utc="2017-03-15T10:00:00Z",
                 end_utc="2017-03-16T10:00:00Z",
                 description="My very first cubesat!",
                 img_file="CubeSat1.png",
                 orbit_t_r=[],
                 orbit_epoch="2017-03-15T10:00:00Z",
                 orbit_time_precision=1.0,
                 orbit_pos_units_mult=1,
                 callbacks= ['orientation','drawNadirRF']):

        sat_name =self.PROTO_DEFS['sat_ref_pre']+str(sat_id)
        if self.SAT_PROTO_JSON['PROTO_VERSION'] == '0.1':
            the_json = copy.deepcopy(self.SAT_PROTO_JSON)
            del the_json['PROTO_VERSION']
            the_json['id'] = sat_name
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

        for callback  in callbacks:
            if not callback  in self.viz_objects_callbacks.keys ():
                self.viz_objects_callbacks[callback] = []
            self.viz_objects_callbacks[callback].append (sat_name)


    def make_gs(self,
                 gs_id,
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
            the_json['id'] = self.PROTO_DEFS['gs_ref_pre']+str (gs_id)
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
             targ_id,
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
            the_json['id'] = self.PROTO_DEFS['obs_target_ref_pre']+str (targ_id)
            the_json['name'] = name
            the_json['label']['text'] = name_pretty
            the_json['availability'] = start_utc+'/'+end_utc
            the_json['description'] = "<!--HTML-->\\r\\n<p>"+ description +"</p>"
            the_json['position']['cartographicDegrees'] = [lon_deg,lat_deg,h_m]

            if self.czml_dict['targets'] is None:
                self.czml_dict['targets'] = []
            self.czml_dict['targets'].append(the_json)

        else:
            raise NotImplementedError

    def convert_flat_times_to_windows(self, times_mat, mat_num_rows, activity_partners_mat= None, mat_num_cols=None):
        """Converts an imported time history matrix to activity windows
        
        [description]

        Uses jdcal package for dealing with modified julian dates from MATLAB code. 
        See https://oneau.wordpress.com/2011/08/30/jdcal/
        jdcal.jd2gcal(jdcal.MJD_0,57827.5774306)
        (have to pass both base date of MJD and the MJD to this function)

        times_mat should look like:
            "xlnk_times_flat": [
            [
                [
                    58136.48652222222,
                    58136.48767962963
                ],
                [
                    58136.487968981484,
                    58136.489126388886
                ],
                ...
            ]

        activity_partners_mat should look like:
            "xlnk_partners": [
            [
                2,
                2,
                ...
            ]

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
                    start_time_datetime = datetime(start_time[0],start_time[1],start_time[2],int(start_time_hours),int(start_time_minutes),int(start_time_seconds))
                    end_time_datetime = datetime(end_time[0],end_time[1],end_time[2],int(end_time_hours),int(end_time_minutes),int(end_time_seconds))

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
            sat_ids,
            gs_ids,
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

                    # aux renderer datarate.js depends on "Dlnk"
                    # todo:  make this not hardcoded
                    ID = 'Dlnk/Sat'+str(sat_ids[sat_indx])+'-GS'+str(gs_ids[gs_indx])

                    ref1 =  self.PROTO_DEFS['sat_ref_pre'] +str(sat_ids[sat_indx])+self.PROTO_DEFS['pos_ref_post']
                    ref2 = self.PROTO_DEFS['gs_ref_pre']+str(gs_ids[gs_indx])+self.PROTO_DEFS['pos_ref_post']
                    czml_content.append(cztl.createLinkPacket(ID,name,start_utc,end_utc, polyline_show_times = dlnk_winds_sat, color=dlnk_color,reference1=ref1,reference2=ref2))

                    i+=1

            self.czml_dict['downlinks'] = czml_content

    def make_crosslinks(self,
            xlnk_times_flat,
            xlnk_partners,
            num_sats,
            sat_ids,
            start_utc,
            end_utc):

        xlnk_winds =  self.convert_flat_times_to_windows(xlnk_times_flat, num_sats, xlnk_partners, num_sats)

        if len(xlnk_winds) > 0:
            czml_content = []

            xlnk_color = [255,0,0,255]
            i = 0
            for sat_indx in range(num_sats):
                for other_sat_indx in range(sat_indx+1,num_sats):
                    name = 'crosslink '+str(i)

                    xlnk_winds_sat = xlnk_winds[sat_indx][other_sat_indx]

                    # aux renderer datarate.js depends on "Dlnk"
                    # todo:  make this not hardcoded
                    ID = 'Xlnk/Sat'+str(sat_ids[sat_indx])+'-Sat'+str(sat_ids[other_sat_indx])

                    ref1 =  self.PROTO_DEFS['sat_ref_pre'] +str(sat_ids[sat_indx])+self.PROTO_DEFS['pos_ref_post']
                    ref2 = self.PROTO_DEFS['sat_ref_pre']+str(sat_ids[other_sat_indx])+self.PROTO_DEFS['pos_ref_post']

                    czml_content.append(cztl.createLinkPacket(ID,name, start_utc, end_utc, polyline_show_times = xlnk_winds_sat, color=xlnk_color,reference1=ref1,reference2=ref2))

                    i+=1


            self.czml_dict['crosslinks'] = czml_content

    def make_observations(self,
            obs_times_flat,
            num_sats,
            sat_ids,
            start_utc,
            end_utc):

        obs_winds =  self.convert_flat_times_to_windows(obs_times_flat, num_sats)

        if len(obs_winds) > 0:
            czml_content = []

            for sat_indx in range(num_sats):
                name = 'observation sensor 1 for satellite '+str(sat_ids[sat_indx])

                obs_winds_sat = obs_winds[sat_indx]

                ID = self.PROTO_DEFS['sat_ref_pre']+str(sat_ids[sat_indx])+'/Sensor/Sensor1'
                parent = self.PROTO_DEFS['sat_ref_pre']+str(sat_ids[sat_indx])

                ref1 =  self.PROTO_DEFS['sat_ref_pre'] +str(sat_ids[sat_indx])+self.PROTO_DEFS['pos_ref_post']
                ref2 =  self.PROTO_DEFS['sat_ref_pre'] +str(sat_ids[sat_indx])+self.PROTO_DEFS['orient_ref_post']

                czml_content.append(cztl.createObsPacket(ID,name,parent,start_utc,end_utc, sensor_show_times = obs_winds_sat, lateral_color=[0,255,0,51],intersection_color=[0,255,0,255],position_ref=ref1,orientation_ref=ref2))


            self.czml_dict['observations'] = czml_content

    def make_downlink_rates(self,
            dlnk_rate_history,
            history_epoch,
            num_sats,
            num_gs,
            sat_ids,
            gs_ids,
            end_utc):

        
        if len(dlnk_rate_history) > 0:
            czml_content = []

            filter_seconds_beg=0
            filter_seconds_end= (end_utc- history_epoch).total_seconds ()

            i = 0
            for sat_indx in range(num_sats):
                for gs_indx in range(num_gs):

                    name = 'dlnk_rate_history for downlink '+str(i)+', satellite '+str(sat_ids[sat_indx])+' and GS '+str(gs_ids[gs_indx])

                    # needs to have same ID as original downlink to work
                    ID = 'Dlnk/Sat'+str(sat_ids[sat_indx])+'-GS'+str(gs_ids[gs_indx])

                    if len (dlnk_rate_history[sat_indx][gs_indx]) >0:
                        pkt = cztl.createSampledPropertyHistory(ID,name, 'datarate',history_epoch, dlnk_rate_history[sat_indx][gs_indx], filter_seconds_beg,filter_seconds_end)

                        # attach a proxy position for displaying data rate text
                        pkt['position_proxy'] = {"reference": self.PROTO_DEFS['gs_ref_pre']+str(gs_ids[gs_indx])+self.PROTO_DEFS['pos_ref_post']}

                        czml_content.append(pkt)

                    i+=1

            self.czml_dict['downlink_rates'] = czml_content

    def make_crosslink_rates(self,
            xlnk_rate_history,
            history_epoch,
            num_sats,
            sat_ids,
            end_utc):

        
        if len(xlnk_rate_history) > 0:
            czml_content = []

            filter_seconds_beg=0
            filter_seconds_end= (end_utc- history_epoch).total_seconds ()

            i = 0
            for sat_indx in range(num_sats):
                for  other_sat_indx in range(sat_indx+1,num_sats):

                    name = 'xlnk_rate_history for crosslink '+str(i)+', satellite '+str(sat_ids[sat_indx])+' and xsat '+str(sat_ids[sat_indx])

                    # needs to have same ID as original downlink to work
                    ID = 'Xlnk/Sat'+str(sat_ids[sat_indx])+'-Sat'+str(sat_ids[ other_sat_indx])

                    if len (xlnk_rate_history[sat_indx][other_sat_indx]) >0:
                        pkt = cztl.createSampledPropertyHistory(ID,name, 'datarate',history_epoch, xlnk_rate_history[sat_indx][other_sat_indx], filter_seconds_beg,filter_seconds_end)

                        # attach a proxy position for displaying data rate text
                        pkt['position_proxy'] = {"reference": self.PROTO_DEFS['sat_ref_pre'] +str(sat_ids[sat_indx])+self.PROTO_DEFS['pos_ref_post']}

                        czml_content.append(pkt)   

                    i+=1

            self.czml_dict['crosslink_rates'] = czml_content

    def get_czml( self,key_list=None):

        if key_list is None:
            key_list = self.czml_dict_keys


        the_czml = []
        for key in key_list:
            if not self.czml_dict.get(key,None) is None:
                the_czml +=self.czml_dict[key]
            else:
                raise RuntimeError ('key %s either is not a valid key or has not been initialized')

        #  Have to add the metadata after everything else because it must be placed after the document  prototype
        the_czml.append(self.json_metadata)

        return the_czml
        

    def get_viz_objects( self,):

        the_json = {}
        the_json ['metadata']=self.json_metadata
        the_json['callbacks']={}

        for callback in self.viz_objects_callbacks.keys ():
            the_json['callbacks'][callback] = self.viz_objects_callbacks[callback]

        return the_json

    def get_renderer_description(self,renderers_list,renderer_mapping,num_sats,num_gs,sat_ids,gs_ids,dlnk_rate_history,xlnk_rate_history):
        the_json = OrderedDict()

        the_json['renderers'] = renderers_list

        renderMapping = OrderedDict()

        if 'Satellite' in renderer_mapping.keys():
            for sat_indx in range(num_sats):
                renderMapping[self.PROTO_DEFS['sat_ref_pre']+str(sat_ids[sat_indx])] = renderer_mapping['Satellite']

        if 'Facility' in renderer_mapping.keys():
            for gs_indx in  range (num_gs):
                renderMapping[self.PROTO_DEFS['gs_ref_pre']+str (gs_ids[gs_indx])] = renderer_mapping['Facility']

        # aux renderer datarate.js depends on "Dlnk"  and  "Xlnk"
        # todo:  make this not hardcoded

        if 'Dlnk' in renderer_mapping.keys() and len(dlnk_rate_history)>0:
            for sat_indx in range(num_sats):
                for gs_indx in  range (num_gs):
                    if len (dlnk_rate_history[sat_indx][gs_indx]) >0:
                        renderMapping['Dlnk/Sat'+str(sat_ids[sat_indx])+'-GS'+str(gs_ids[gs_indx])] = renderer_mapping['Dlnk']

        if 'Xlnk' in renderer_mapping.keys() and len(xlnk_rate_history)>0:
            for sat_indx in range(num_sats):
                for  other_sat_indx in range(sat_indx+1,num_sats):
                    if len (xlnk_rate_history[sat_indx][other_sat_indx]) > 0:
                        renderMapping['Xlnk/Sat'+str(sat_ids[sat_indx])+'-Sat'+str(sat_ids[other_sat_indx])] = renderer_mapping['Xlnk']

        the_json['renderMapping'] = renderMapping

        return the_json
        