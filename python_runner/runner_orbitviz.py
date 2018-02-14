#! /usr/bin/env python

##
# Python runner for orbit visualization pipeline
# @author Kit Kennedy
# 

import time
import os.path
import json
from datetime import datetime



import sys
sys.path.append ('..')
from czml import CzmlWrapper

REPO_BASE = os.path.abspath(os.pardir)  # os.pardir aka '..'

OUTPUT_JSON_VER = '0.1'


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

    with open(os.path.join(REPO_BASE,'crux/config/examples/viz_sat_history_ex_small.json'),'r') as f:
        viz_sat_history = json.load(f)

    data = {
        "orbit_prop_data": orbit_prop_data,
        "orbit_prop_inputs": orbit_prop_inputs,
        "viz_params": viz_params,
        "viz_sat_history": viz_sat_history
    }

    a = time.time()
    output = pr.run(data)
    b = time.time()

    with open('../app_data_files/sats_file.czml','w') as f:
        json.dump(output,f)

    print('run time: %f'%(b-a))
