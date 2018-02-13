#! /usr/bin/env python

##
# Python runner for orbit visualization pipeline
# @author Kit Kennedy
# 

import time
import os.path
import json
import copy
from datetime import datetime
from collections import OrderedDict

REPO_BASE = os.path.abspath(os.pardir)  # os.pardir aka '..'

OUTPUT_JSON_VER = '0.1'

FLATTEN_NEG_INFINITY_SEC = -3153600000.0  # 100 years in the past, in seconds.

class CzmlWrapper:
	DOC_HEADER_PROTO = os.path.join(REPO_BASE,"czml","prototypes","doc_header_proto.json")
	GS_PROTO = os.path.join(REPO_BASE,"czml","prototypes","gs_proto.json")
	OBS_PROTO = os.path.join(REPO_BASE,"czml","prototypes","obs_proto.json")
	SAT_PROTO = os.path.join(REPO_BASE,"czml","prototypes","satellite_proto.json")

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

		last_time = FLATTEN_NEG_INFINITY_SEC
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


class PipelineRunner:

	def run(self, data):
		"""
		Run orbit propagation pipeline element using the inputs supplied per input.json schema. Formats the high level output json and calls various subcomponents for processing

		:param orbit_prop_data: input json per input.json schema
		:return: output json per output.json schema
		"""

		orbit_prop_data = data['orbit_prop_data']
		orbit_prop_inputs = data['orbit_prop_inputs']
		viz_params = data['viz_params']

		the_czml = []
		cz = CzmlWrapper()

		if viz_params['version'] == "0.1":
			orbit_time_precision = viz_params['orbit_time_precision_s']

		if orbit_prop_data['version'] == "0.1":

			scenario_params = orbit_prop_data['scenario_params']
			sat_orbit_data = orbit_prop_data['sat_orbit_data']

			# add czml file document header
			name = "sats_file_"+datetime.utcnow().isoformat()
			the_czml.append(
				cz.make_doc_header(name,scenario_params['start_utc'],scenario_params['end_utc'])
			)

			# add satellites to czml file
			for elem in sat_orbit_data:
				the_czml.append(
					cz.make_sat(
						name='sat'+str(elem['sat_indx']),
						name_pretty='sat'+str(elem['sat_indx']),
						start_utc=scenario_params['start_utc'],
						end_utc=scenario_params['end_utc'],
						orbit_t_r= elem['time_s_pos_km'],
						orbit_epoch= scenario_params['start_utc'],
						orbit_time_precision=orbit_time_precision,
						orbit_pos_units_mult = 1000
				))
		else:
			raise NotImplementedError

		if orbit_prop_inputs['version'] == "0.2":
			scenario_params = orbit_prop_inputs['scenario_params']

			# add ground stations to czml file
			gs_params = orbit_prop_inputs['gs_params']

			for station in gs_params['stations']:

				the_czml.append(
					cz.make_gs(
						name=station['name'],
						name_pretty=station['name_pretty'],
						start_utc=scenario_params['start_utc'],
						end_utc=scenario_params['end_utc'],
						lat_deg=station['latitude_deg'],
						lon_deg=station['longitude_deg'],
						h_m=station['height_m']
				))

			# add observation targets to czml file
			obs_params = orbit_prop_inputs['obs_params']

			for targ in obs_params['targets']:
				the_czml.append(
					cz.make_obs(
						name=targ['name'],
						name_pretty=targ['name_pretty'],
						start_utc=scenario_params['start_utc'],
						end_utc=scenario_params['end_utc'],
						lat_deg=targ['latitude_deg'],
						lon_deg=targ['longitude_deg'],
						h_m=targ['height_m']
					))
		else:
			raise NotImplementedError

		return the_czml


if __name__ == "__main__":

	pr = PipelineRunner()

	# with open(os.path.join(REPO_BASE,'crux/config/examples/orbit_prop_inputs_ex.json'),'r') as f:
	with open(os.path.join(REPO_BASE,'crux/config/examples/orbit_prop_inputs_ex_small.json'),'r') as f:
		orbit_prop_inputs = json.load(f)

	with open(os.path.join(REPO_BASE,'crux/config/examples/orbit_prop_data_ex_small.json'),'r') as f:
	# with open(os.path.join(REPO_BASE,'crux/config/examples/orbit_prop_data_ex.json'),'r') as f:
		orbit_prop_data = json.load(f)

	with open(os.path.join(REPO_BASE,'crux/config/examples/viz_params_ex.json'),'r') as f:
		viz_params = json.load(f)

	data = {
		"orbit_prop_data": orbit_prop_data,
		"orbit_prop_inputs": orbit_prop_inputs,
		"viz_params": viz_params
	}

	a = time.time()
	output = pr.run(data)
	b = time.time()

	with open('../app_data_files/sats_file.czml','w') as f:
		json.dump(output,f)

	print('run time: %f'%(b-a))
