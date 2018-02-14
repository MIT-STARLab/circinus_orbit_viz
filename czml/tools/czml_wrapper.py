import os
import pkg_resources
import json
from collections import OrderedDict
import copy

# should be 'czml', the package name
package_name = __name__.split('.')[0] 

class CzmlWrapper:
    FLATTEN_NEG_INFINITY_SEC = -3153600000.0  # 100 years in the past, in seconds.
    
    # DOC_HEADER_PROTO = os.path.join( "..","prototypes","doc_header_proto.json")
    DOC_HEADER_PROTO = pkg_resources.resource_filename(package_name, '/'.join(('prototypes','doc_header_proto.json')))
    GS_PROTO = pkg_resources.resource_filename(package_name, '/'.join(('prototypes','gs_proto.json')))
    OBS_PROTO = pkg_resources.resource_filename(package_name, '/'.join(('prototypes','obs_proto.json')))
    SAT_PROTO = pkg_resources.resource_filename(package_name, '/'.join(('prototypes','satellite_proto.json')))

    def __init__(self):
        with open(self.DOC_HEADER_PROTO,'r') as f:
            self.DOC_HEADER_PROTO_JSON = json.load(f,object_pairs_hook=OrderedDict)
        with open(self.GS_PROTO,'r') as f:
            self.GS_PROTO_JSON = json.load(f,object_pairs_hook=OrderedDict)
        with open(self.OBS_PROTO,'r') as f:
            self.OBS_PROTO_JSON = json.load(f,object_pairs_hook=OrderedDict)
        with open(self.SAT_PROTO,'r') as f:
            self.SAT_PROTO_JSON = json.load(f,object_pairs_hook=OrderedDict)

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
            return the_json

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
            return the_json

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
            return the_json

        else:
            raise NotImplementedError

    def make_obs(self,
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
            return the_json

        else:
            raise NotImplementedError