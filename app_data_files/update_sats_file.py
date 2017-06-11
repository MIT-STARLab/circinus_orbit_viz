import json
from collections import OrderedDict
import argparse
from strip_sats_file import strip_file
import sys

#############################
# Inputs
#############################

# might have to also modify the slashes in here if you're in e.g. windows / -> \

simulation_input_file_path = '/Users/ktikennedy/Dropbox (MIT)/MIT/Research/MDO Paper Work/Comm_constellation_MDO/landing_pad/timing_output.mat'
czml_tools_path = '../OrbitPropagation/czml/Tools'
# czml_header_file = './sats_file.czml'
# czml_header_file = '/Users/ktikennedy/Dropbox (MIT)/MIT/Research/MDO Paper Work/Comm_constellation_MDO/orbit_inputs/sso_and_equatorial/czml/orbitprop_ssoequat_orb30-0-0_gs5_t259200-10.czml'

czml_header_file = '/Users/ktikennedy/Desktop/MDO_paper_sim_results/walker/czml/orbitprop_walker_orb3-30_gs1_t259200-10.czml'
# czml_header_file = '/Users/ktikennedy/Desktop/MDO_paper_sim_results/sso_and_equatorial/czml/orbitprop_ssoequat_orb10-10-10_gs2_t259200-10.czml'

output_file = './sats_file.czml'
renderer_description_file = '../renderers/description.json'
viz_objects_file = './viz_objects.json'


#############################
# Code
#############################

output_viz_czml_file = './viz_out.json'

print 'simulation_input_file_path: '+simulation_input_file_path
print 'czml_tools_path: '+czml_tools_path
print 'czml_header_file: '+czml_header_file
print 'output_file: '+ output_file

# strip all the extra stuff out of selected file - leave packets for document, satellite orbits, facilities, and observation locations
strip_file(czml_header_file)


# now create the extra czml content for visualization - obs cones, comm links, data volumes, battery indicator, GS availability, eclipse indicator...
sys.path.append(czml_tools_path)
from VizInputsGenerator import generateVizInputs, writeRendererDescription, writeVizObjectsFile

generateVizInputs(file_from_sim = simulation_input_file_path, output_viz_czml_file = output_viz_czml_file)


# now open both the header file and the czml content file, unserialize, and append
fd1 = open(czml_header_file, "r")
fd2 = open(output_viz_czml_file, "r")

czml1 = json.load(fd1,object_pairs_hook=OrderedDict)
czml2 = json.load(fd2,object_pairs_hook=OrderedDict)

final_czml = czml1 + czml2


# write out all the czml to file. Note that this will first nuke output_file!
fd1.close()
fd2.close()

fd3 = open(output_file, "w")

json.dump(final_czml,fd3,indent=4)

fd3.close()


# Also take care of renderer description file
renderers_list = [
        "/Apps/MATLAB_SatViz/renderers/test.js",
        "/Apps/MATLAB_SatViz/renderers/datavol.js",
        "/Apps/MATLAB_SatViz/renderers/gsavail.js",
        "/Apps/MATLAB_SatViz/renderers/battery.js",
        "/Apps/MATLAB_SatViz/renderers/eclipses.js",
        "/Apps/MATLAB_SatViz/renderers/datarate.js"
    ]

# renderer_mapping = {'Satellite':["DataVol","Battery","Eclipses"]}
renderer_mapping = {'Satellite':["DataVol","Battery","Eclipses"],'Facility':["GSavail"],'Dlnk':["DataRate"],'Xlnk':["DataRate"]}

writeRendererDescription(simulation_input_file_path,renderer_description_file,renderers_list, renderer_mapping)


# Also take care of visualization objects file
callbacks_mapping = {'Satellite':["orientation","drawNadirRF"]}

writeVizObjectsFile(simulation_input_file_path,viz_objects_file, callbacks_mapping)