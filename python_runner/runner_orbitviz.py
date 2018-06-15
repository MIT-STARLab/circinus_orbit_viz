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
import argparse

sys.path.append ('..')
from circinus_tools import io_tools
from circinus_tools  import time_tools as tt
from czml import CzmlWrapper

from circinus_tools import debug_tools

REPO_BASE = os.path.abspath(os.pardir)  # os.pardir aka '..'

OUTPUT_JSON_VER = '0.1'


class PipelineRunner:

    def consolidate_viz_data( self,sat_link_history, gp_history, option ='gp_and_sat_link'):
        
        viz_data = {}
        if option ==  "gp_and_sat_link":
            if not ((gp_history['version'] ==  "0.2") and (sat_link_history['version'] ==  "0.1")):
                raise NotImplementedError

            gp_history_v=gp_history['viz_data']
            sat_link_history_v=sat_link_history['viz_data']
            viz_data['update_time'] = gp_history['update_wall_clock_utc']
            viz_data['obs_times_flat'] = gp_history_v['obs_times_flat']
            viz_data['obs_locations'] = gp_history_v['obs_locations']
            viz_data['dlnk_times_flat'] = gp_history_v['dlnk_times_flat']
            viz_data['dlnk_partners'] = gp_history_v['dlnk_partners']
            viz_data['dlnk_link_info_history_flat'] = gp_history_v['dlnk_link_info_history_flat']
            viz_data['xlnk_times_flat'] = gp_history_v['xlnk_times_flat']
            viz_data['xlnk_partners'] = gp_history_v['xlnk_partners']
            viz_data['xlnk_link_info_history_flat'] = gp_history_v['xlnk_link_info_history_flat']
            viz_data['xlnk_rate_history_epoch'] = sat_link_history_v['xlnk_rate_history_epoch']
            viz_data['xlnk_rate_history'] = sat_link_history_v['xlnk_rate_history']
            viz_data['dlnk_rate_history_epoch'] = sat_link_history_v['dlnk_rate_history_epoch']
            viz_data['dlnk_rate_history'] = sat_link_history_v['dlnk_rate_history']

        elif option == "sat_link_only":
            if not (sat_link_history['version'] ==  "0.1"):
                raise NotImplementedError
            
            sat_link_history_v=sat_link_history['viz_data']
            viz_data['obs_times_flat'] = sat_link_history_v['obs_times_flat']
            viz_data['obs_locations'] = sat_link_history_v['obs_locations']
            viz_data['dlnk_times_flat'] = sat_link_history_v['dlnk_times_flat']
            viz_data['dlnk_partners'] = sat_link_history_v['dlnk_partners']
            viz_data['xlnk_times_flat'] = sat_link_history_v['xlnk_times_flat']
            viz_data['xlnk_partners'] = sat_link_history_v['xlnk_partners']
            viz_data['xlnk_rate_history_epoch'] = sat_link_history_v['xlnk_rate_history_epoch']
            viz_data['xlnk_rate_history'] = sat_link_history_v['xlnk_rate_history']
            viz_data['dlnk_rate_history_epoch'] = sat_link_history_v['dlnk_rate_history_epoch']
            viz_data['dlnk_rate_history'] = sat_link_history_v['dlnk_rate_history']

        return viz_data


    def run(self, data, params):
        """
        Run orbit propagation pipeline element using the inputs supplied per input.json schema. Formats the high level output json and calls various subcomponents for processing

        :param orbit_prop_data: input json per input.json schema
        :return: output json per output.json schema
        """

        orbit_prop_data = data['orbit_prop_data']
        orbit_prop_inputs = data['orbit_prop_inputs']
        viz_params = data['viz_params']
        sat_link_history = data['sat_link_history']
        gp_history = data['gp_history']
        display_link_info = data['display_link_info']

        history_input_option = params['history_input_option']

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
        sat_id_order = None
        gs_id_order = None

        if orbit_prop_inputs['version'] == "0.8":
            scenario_params = orbit_prop_inputs['scenario_params']

            start_utc_dt =tt.iso_string_to_dt (scenario_params['start_utc'] ) 
            end_utc_dt = tt.iso_string_to_dt (scenario_params['end_utc'] ) 
            num_sats = orbit_prop_inputs['sat_params']['num_satellites']
            num_gs = orbit_prop_inputs['gs_params']['num_stations']
            num_targets = orbit_prop_inputs['obs_params']['num_targets']

            # add ground stations to czml file
            gs_params = orbit_prop_inputs['gs_params']
            gs_names = [gs['name'] for gs in gs_params['stations']]

            num_satellites = orbit_prop_inputs['sat_params']['num_satellites']
            sat_id_prefix = orbit_prop_inputs['sat_params']['sat_id_prefix']

            sat_id_order= orbit_prop_inputs['sat_params']['sat_id_order']
            # in the case that this is default, then we need to grab a list of all the satellite IDs. We'll take this from all of the satellite IDs found in the orbit parameters
            if sat_id_order == 'default':
                dummy, all_sat_ids = io_tools.unpack_sat_entry_list(  orbit_prop_inputs['orbit_params']['sat_orbital_elems'],force_duplicate =  True)
            #  make the satellite ID order. if the input ID order is default, then will assume that the order is the same as all of the IDs passed as argument
            sat_id_order = io_tools.make_and_validate_sat_id_order(sat_id_order,sat_id_prefix,num_satellites,all_sat_ids)
            io_tools.validate_ids(validator=sat_id_order,validatee=all_sat_ids)

            gs_id_order = io_tools.make_and_validate_gs_id_order(orbit_prop_inputs['gs_params'])

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


        if orbit_prop_data['version'] == "0.3":

            scenario_params = orbit_prop_data['scenario_params']
            sat_orbit_data = orbit_prop_data['sat_orbit_data']

            # add czml file document header
            name = "sats_file_"+datetime.utcnow().isoformat()
            cz.make_doc_header(name,scenario_params['start_utc'],scenario_params['end_utc'])

            # add satellites to czml file
            for sat_indx,elem in enumerate ( sat_orbit_data):
                cz.make_sat(
                    sat_id = elem['sat_id'],
                    name=elem['sat_id'],
                    name_pretty=elem['sat_id'],
                    start_utc=scenario_params['start_utc'],
                    end_utc=scenario_params['end_utc'],
                    orbit_t_r= elem['time_s_pos_eci_km'],
                    orbit_epoch= scenario_params['start_utc'],
                    orbit_time_precision=orbit_time_precision,
                    orbit_pos_units_mult = 1000,
                    callbacks =satellite_callbacks
                )
        else:
            raise NotImplementedError

        #  now make all the cesium outputs
        print (history_input_option)
        viz_data =self.consolidate_viz_data(sat_link_history, gp_history, option =history_input_option)
        
        cz.json_metadata['input_data_updated'] = viz_data.get('update_time', None)

        cz.make_downlinks(
            viz_data['dlnk_times_flat'],
            viz_data['dlnk_partners'],
            num_sats,
            num_gs,
            gs_names,
            sat_id_order,
            gs_id_order,
            start_utc_dt,
            end_utc_dt
        )

        cz.make_crosslinks(
            viz_data['xlnk_times_flat'],
            viz_data['xlnk_partners'],
            num_sats,
            sat_id_order,
            start_utc_dt,
            end_utc_dt
        )

        cz.make_observations(
            viz_data['obs_times_flat'],
            num_sats,
            sat_id_order,
            start_utc_dt,
            end_utc_dt
        )

        dlnk_rate_history_epoch_dt= tt.iso_string_to_dt (viz_data['dlnk_rate_history_epoch'])
        cz.make_downlink_rates(
            viz_data['dlnk_rate_history'],
            dlnk_rate_history_epoch_dt,
            num_sats,
            num_gs,
            sat_id_order,
            gs_id_order,
            end_utc_dt
        )

        if viz_data.get ('dlnk_link_info_history_flat') and display_link_info:
            cz.make_downlink_link_info(
                viz_data['dlnk_link_info_history_flat'],
                viz_data['dlnk_partners'],
                num_sats,
                num_gs,
                sat_id_order,
                gs_id_order,
                start_utc_dt,
                end_utc_dt
            )

        xlnk_rate_history_epoch_dt= tt.iso_string_to_dt (viz_data['xlnk_rate_history_epoch'])
        cz.make_crosslink_rates(
            viz_data['xlnk_rate_history'],
            xlnk_rate_history_epoch_dt,
            num_sats,
            sat_id_order,
            end_utc_dt
        )

        if viz_data.get ('xlnk_link_info_history_flat') and display_link_info:
            cz.make_crosslink_link_info(
                viz_data['xlnk_link_info_history_flat'],
                viz_data['xlnk_partners'],
                num_sats,
                sat_id_order,
                start_utc_dt,
                end_utc_dt
            )

        renderer_description = cz.get_renderer_description(
            renderers_list,
            renderer_mapping,
            num_sats,
            num_gs,
            sat_id_order,
            gs_id_order,
            viz_data['dlnk_rate_history'],
            viz_data['xlnk_rate_history'],
            viz_data.get ('dlnk_link_info_history_flat',[]),
            viz_data['dlnk_partners'],
            viz_data.get ('xlnk_link_info_history_flat',[]),
            viz_data['xlnk_partners'],
        )


        return cz.get_czml(), cz.get_viz_objects (), renderer_description


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description='orbit propagation')
    ap.add_argument('--prop_inputs_file',
                    type=str,
                    default='orbit_prop_inputs.json',
                    help='specify orbit propagation inputs file')

    ap.add_argument('--prop_data_file',
                    type=str,
                    default='orbit_prop_data.json',
                    help='specify orbit propagation data output file')

    ap.add_argument('--sat_link_file',
                    type=str,
                    default='sat_link_history.json',
                    help='specify sat link file')

    ap.add_argument('--history_input_option',
                    type=str,
                    default='sat_link_only',
                    help= "specify what link data to use for visualization. Options:['sat_link_only','gp_and_sat_link']")

    ap.add_argument('--display_link_info',
                    action='store_true',
                    help= "Whether or not to display link info text")

    args = ap.parse_args()

    pr = PipelineRunner()

    # with open(os.path.join(REPO_BASE,'crux/config/examples/orbit_prop_inputs_ex.json'),'r') as f:
    with open(os.path.join(REPO_BASE,args.prop_inputs_file),'r') as f:
        orbit_prop_inputs = json.load(f)

    with open(os.path.join(REPO_BASE,args.prop_data_file),'r') as f:
    # with open(os.path.join(REPO_BASE,'crux/config/examples/orbit_prop_data_ex.json'),'r') as f:
        orbit_prop_data = json.load(f)

    with open(os.path.join(REPO_BASE,'crux/config/examples/viz_params_ex.json'),'r') as f:
        viz_params = json.load(f)

    with open(os.path.join(REPO_BASE,args.sat_link_file),'r') as f:
        sat_link_history = json.load(f)
    
    try:
        with open(os.path.join(REPO_BASE,'crux/config/examples/gp_outputs.json'),'r') as f:
            gp_history = json.load(f)

        history_param = args.history_input_option
    except:
        gp_history = ""
        history_param = 'sat_link_only'

    data = {
        "orbit_prop_data": orbit_prop_data,
        "orbit_prop_inputs": orbit_prop_inputs,
        "viz_params": viz_params,
        "sat_link_history": sat_link_history,
        "gp_history": gp_history,
        "display_link_info": args.display_link_info
    }

    params =  {
        'history_input_option':history_param
    }

    a = time.time()
    output = pr.run(data,params)
    b = time.time()

    with open('../app_data_files/sats_file.czml','w') as f:
        json.dump(output [0],f)
    with open('../app_data_files/viz_objects.json','w') as f:
        json.dump(output [1],f)
    with open('../renderers/description.json','w') as f:
        json.dump(output [2],f)

    print('run time: %f'%(b-a))
 