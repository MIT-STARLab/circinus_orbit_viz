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
from circinus_tools  import time_tools as tt
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
        viz_sat_history = data['viz_sat_history']

        sat_name_prefix = "sat"

        cz = CzmlWrapper()

        satellite_callbacks = None
        renderers_list =  None
        renderer_mapping =  None
        if viz_params['version'] == "0.1":
            orbit_time_precision = viz_params['orbit_time_precision_s']
            satellite_callbacks = viz_params['satellite_callbacks']
            renderers_list =  [rndr for rndr in viz_params['available_renderers'].values()]
            renderer_mapping =  viz_params['selected_renderer_mapping']
        else:
            raise NotImplementedError


        # initializing these here so they will be in scope for use down below
        num_sats = None
        num_gs = None
        num_targets = None
        gs_names= None
        start_utc_dt = None
        end_utc_dt = None
        sat_ids = None
        gs_ids = None

        if orbit_prop_inputs['version'] == "0.3":
            scenario_params = orbit_prop_inputs['scenario_params']

            start_utc_dt =tt.iso_string_to_dt (scenario_params['start_utc'] ) 
            end_utc_dt = tt.iso_string_to_dt (scenario_params['end_utc'] ) 
            num_sats = orbit_prop_inputs['sat_params']['num_satellites']
            num_gs = orbit_prop_inputs['gs_params']['num_stations']
            num_targets = orbit_prop_inputs['obs_params']['num_targets']

            # add ground stations to czml file
            gs_params = orbit_prop_inputs['gs_params']
            gs_names = [gs['name'] for gs in gs_params['stations']]

            # todo: should really verify that sat_id_order is correctly formatted
            sat_ids = orbit_prop_inputs ['sat_params']['sat_id_order']
            gs_ids = [station ['id'] for station in gs_params['stations']]

            for station in gs_params['stations']:

                cz.make_gs(
                    gs_id=station ['id'],
                    name=station['name'],
                    name_pretty=station['name_pretty'],
                    start_utc=scenario_params['start_utc'],
                    end_utc=scenario_params['end_utc'],
                    lat_deg=station['latitude_deg'],
                    lon_deg=station['longitude_deg'],
                    h_m=station['height_m']
                )

            # add observation targets to czml file
            obs_params = orbit_prop_inputs['obs_params']

            for targ in obs_params['targets']:
                cz.make_obs_target(
                    targ_id=targ ['id'],
                    name=targ['name'],
                    name_pretty=targ['name_pretty'],
                    start_utc=scenario_params['start_utc'],
                    end_utc=scenario_params['end_utc'],
                    lat_deg=targ['latitude_deg'],
                    lon_deg=targ['longitude_deg'],
                    h_m=targ['height_m']
                )
        else:
            raise NotImplementedError


        if orbit_prop_data['version'] == "0.2":

            scenario_params = orbit_prop_data['scenario_params']
            sat_orbit_data = orbit_prop_data['sat_orbit_data']

            # add czml file document header
            name = "sats_file_"+datetime.utcnow().isoformat()
            cz.make_doc_header(name,scenario_params['start_utc'],scenario_params['end_utc'])

            # add satellites to czml file
            for sat_indx,elem in enumerate ( sat_orbit_data):
                cz.make_sat(
                    sat_id = elem['sat_id'],
                    name=sat_name_prefix+str(elem['sat_id']),
                    name_pretty='sat'+str(elem['sat_id']),
                    start_utc=scenario_params['start_utc'],
                    end_utc=scenario_params['end_utc'],
                    orbit_t_r= elem['time_s_pos_km'],
                    orbit_epoch= scenario_params['start_utc'],
                    orbit_time_precision=orbit_time_precision,
                    orbit_pos_units_mult = 1000,
                    callbacks =satellite_callbacks
                )
        else:
            raise NotImplementedError

        renderer_description= None
        if viz_sat_history['version'] == "0.1":
            viz_data = viz_sat_history['viz_data']

            cz.make_downlinks(
                viz_data['dlnk_times_flat'],
                viz_data['dlnk_partners'],
                num_sats,
                num_gs,
                gs_names,
                sat_ids,
                gs_ids,
                start_utc_dt,
                end_utc_dt
            )

            cz.make_crosslinks(
                viz_data['xlnk_times_flat'],
                viz_data['xlnk_partners'],
                num_sats,
                sat_ids,
                start_utc_dt,
                end_utc_dt
            )

            cz.make_observations(
                viz_data['obs_times_flat'],
                num_sats,
                sat_ids,
                start_utc_dt,
                end_utc_dt
            )

            dlnk_rate_history_epoch_dt= tt.iso_string_to_dt (viz_data['dlnk_rate_history_epoch'])
            cz.make_downlink_rates(
                viz_data['dlnk_rate_history'],
                dlnk_rate_history_epoch_dt,
                num_sats,
                num_gs,
                sat_ids,
                gs_ids,
                end_utc_dt
            )

            xlnk_rate_history_epoch_dt= tt.iso_string_to_dt (viz_data['xlnk_rate_history_epoch'])
            cz.make_crosslink_rates(
                viz_data['xlnk_rate_history'],
                xlnk_rate_history_epoch_dt,
                num_sats,
                sat_ids,
                end_utc_dt
            )

            renderer_description = cz.get_renderer_description(
                renderers_list,
                renderer_mapping,
                num_sats,
                num_gs,
                sat_ids,
                gs_ids,
                viz_data['dlnk_rate_history'],
                viz_data['xlnk_rate_history']
            )

        else:
            raise NotImplementedError



        return cz.get_czml(), cz.get_viz_objects (), renderer_description


if __name__ == "__main__":

    pr = PipelineRunner()

    # with open(os.path.join(REPO_BASE,'crux/config/examples/orbit_prop_inputs_ex.json'),'r') as f:
    with open(os.path.join(REPO_BASE,'crux/config/examples/orbit_prop_inputs.json'),'r') as f:
        orbit_prop_inputs = json.load(f)

    with open(os.path.join(REPO_BASE,'crux/config/examples/orbit_prop_data.json'),'r') as f:
    # with open(os.path.join(REPO_BASE,'crux/config/examples/orbit_prop_data_ex.json'),'r') as f:
        orbit_prop_data = json.load(f)

    with open(os.path.join(REPO_BASE,'crux/config/examples/viz_params_ex.json'),'r') as f:
        viz_params = json.load(f)

    with open(os.path.join(REPO_BASE,'crux/config/examples/sat_link_history.json'),'r') as f:
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
        json.dump(output [0],f)
    with open('../app_data_files/viz_objects.json','w') as f:
        json.dump(output [1],f)
    with open('../renderers/description.json','w') as f:
        json.dump(output [2],f)

    print('run time: %f'%(b-a))
