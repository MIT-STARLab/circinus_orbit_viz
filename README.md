# MATLAB_sat_viz
For quick and easy visualization of constellation simulation output from MATLAB

## Setup Instruction

### 1. Setting Up CesiumJS

MATLAB_sat_viz has been tested with [CesiumJS 1.27](https://cesiumjs.org/downloads.html), and I'd recommend you use that version for your visualization needs.

Unzip this folder into a convenient working directory - you'll be running code from directly within the Cesium-1.27 folder.

As a first step, you'll need to install NodeJS. This is helpful for running a server that provides the Cesium files to your web browser. [Here](https://nodejs.org/en/)'s a link

After that, follow the rest of the Quick Start Guide on the Cesium downloads page (same link from above). To actually run the server, you'll want to first cd to the Cesium-1.27 folder, e.g.

```
$ cd /path_on_your_machine/Cesium-1.27
$ node server.js
```

Once your server is up and running, you're ready to get the




### 2. Cloning MATLAB_sat_viz

For clonging the repo, you'll first want to be in the Apps directory within the Cesium-1.27 directory:

```
$ cd /path_on_your_machine/Cesium-1.27/Apps
```

Now we can actually clone THIS repo.

To clone the repo correctly, use recursive option on git clone (to grab all the CSTAR library files immediately):

```
$ git clone --recursive https://github.com/apollokit/MATLAB_sat_viz.git
```

You should now be set up to run the visualization code!

### 3. Look at all the pretty visualizationzzz

The Cesium files are provided by a webserver (hence the "node server.js" command), but the actual rendering is done in a web browser. So open a web browser! I strongly recommend you use Google Chrome. I won't give any guarantees of functionality in other browsers.

So open the browser and navigate to: [http://localhost:8080/Apps/MATLAB_sat_viz/runner.html](http://localhost:8080/Apps/MATLAB_sat_viz/runner.html)

The visualization should start running immediately. It should look something like the below.

![Viz image](viz_shot.png)


## Updating Visualization with Simulation Output

### 1. Clone the Comm_constellation_MDO repo

Currently our workflow is to run constellation simulations in the Comm_constellation_MDO code, and then use the output from that to update the visualization. It's not the *best* workflow, and I (Kit) envision many improvements over the course of my thesis work. For now though, that's the way we do it. [Here](https://github.com/ebclements/Comm_constellation_MDO)'s a link.

### 2. Clone the OrbitPropagation repo

[This](https://github.mit.edu/star-lab/OrbitPropagation) is yet another repo, in this case containing all kinds of nifty tools for orbit propagation and czml file creation.

Clone this to a convenient location. It doesn't have to be in any particular place relative to the other repos. Here's the line:

```
$ git clone https://github.mit.edu/star-lab/OrbitPropagation.git
```

### 3. Run a sim

So you'll need to first run a sim in Comm_constellation_MDO. That produces an output file, Comm_constellation_MDO/landing_pad/timing_output.mat that has all the necessary data for populating an input .czml file to the visualization.

### 4. Update sats_file.czml

This is the input file with all the relevant viz data. It's here: Cesium-1.27/Apps/MATLAB_sat_viz/app_data_files.

I've made a python script for doing an automated update of this file from the sim output, update_sats_file.py.

First you should open the file and update the necessary inputs:

```python
simulation_input_file_path = '/Users/ktikennedy/Dropbox (MIT)/MIT/Research/MDO Paper Work/Comm_constellation_MDO/landing_pad/timing_output.mat'
czml_tools_path = '/Users/ktikennedy/Dropbox (MIT)/MIT/Research/MDO Paper Work/OrbitPropagation/czml/Tools'

czml_header_file = './czml_headers/sats_file_single_sfn_0_0_1.czml'
output_file = './sats_file.czml'
```

The first two lines are pretty self explanatory: modify the paths listed based on where the *Comm_constellation_MDO* and *OrbitPropagation* repos are on your machine.

The czml_header_file line specifies the *first half* of the czml file that will be input to the visualization. It's all the ground station, observation target, and satellite orbit data - all the stuff that **doesn't** change when running a sim. The generation of these files is still a little clumsy - I have to do it by "hand" (i.e. with some tools in *OrbitPropagation*). I'll improve that workflow at some point.

For the time being, stick to the provided hearder files in MATLAB_sat_viz/app_data_files/czml_headers. The names are meant to be sufficiently descriptive.

Though as an alternative, I generally set czml_header_file just to './sats_file.czml', which allows me to use the header that is currently already being used for the visualization.

The output file is just the full czml file that will be created after appending things together. This should be sats_file.czml, because that's what the app's main runner.html page is expecting.

Those inputs being set, now you can run the tool and generate the input file:

```
$ cd MATLAB_sat_viz/app_data_files
$ python update_sats_file.py
```

### 5. Refresh visualization

Now go back to the browser and hard reload the visualization page - this clears any cached data files and reloads with the newly updated czml file.

On chrome on Mac, the shortcut I use is Command + Shift + r .

You should see the updated visualization running! If you don't see any changes from before, it may be that you didn't actually hard reload.

Also if you have a scenario mismatch between the czml header file and the sim you're running in *Comm_constellation_MDO*, you'll likely get an error on this page. Make sure you're using the right header file!


