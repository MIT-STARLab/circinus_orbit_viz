# OrbitViz
For quick and easy visualization of satellite orbits and constellation simulation results.

## Dependencies

1. CesiumJS 1.27
2. [cesium-sensor-volumes](https://github.com/jlouns/cesium-sensor-volumes)

## Setup

### 1. Setting Up CesiumJS

OrbitViz has been tested with [CesiumJS 1.27](https://cesiumjs.org/downloads.html), and I'd recommend you use that version for your visualization needs.

Unzip this folder into a convenient working directory - you'll be running code from directly within the Cesium-1.27 folder.

As a first step, you'll need to install NodeJS. This is helpful for running a server that provides the Cesium files to your web browser. [Here](https://nodejs.org/en/)'s a link

After that, follow the rest of the Quick Start Guide on the Cesium downloads page (same link from above). To actually run the server, you'll want to first cd to the Cesium-1.27 folder, e.g.

```
$ cd /path_on_your_machine/Cesium-1.27
$ node server.js
```

So that's how you run the server for visualization.

We also need to install another [package](https://github.com/jlouns/cesium-sensor-volumes) for sensor visualization.

To do this, in the Cesium-1.27 directory, use
```
$ npm install --save cesium-sensor-volumes
```

This uses the Node package manager to install the sensor viz code. You'll likely get an error about an unmet dependency - I needed "electron-prebuilt". If that happens, do the following:

```
$ npm install electron-prebuilt
$ npm install --save cesium-sensor-volumes
```

### 2. Python

This code has been tested with Python 3.5.  I recommend running this in a Python virtual environment.


### 3. Cloning OrbitViz

For cloning the repo, you'll first want to be in the Apps directory within the Cesium-1.27 directory:

```
$ cd /PATH_ON_YOUR_MACHINE/Cesium-1.27/Apps
```

Now we can actually clone the repo.

To clone the repo correctly, use recursive option on git clone with SSH (to grab all the CSTAR submodule immediately):

```
$ git clone --recursive git@github.mit.edu:star-lab/OrbitViz.git
```

Note that you can't use HTTPS with the MIT enterprise github. See [this page](https://github.mit.edu/star-lab/lab_wiki/wiki/Accessing-STAR-Lab-Git-Repos) for more info.

You should now be set up to run the visualization code!

FYI about the submodule:

#### CSTAR

[This](https://github.mit.edu/star-lab/CSTAR) repo has a bunch of custom code that we've written for Cesium for visualizing satellites and orbits as well as better camera movement. It's the general repo for all Cesium extensions we'll work on now and in the future.

#### Working with Git Submodules

Just a quick note on this because submodules are a little confusing.

When we originally cloned OrbitViz, i.e.
```
$ git clone --recursive https://github.mit.edu/star-lab/OrbitViz.git
```
we used the --recursive flag to grab the submodule files as well. (can also clone the repo normally, and use `$ git submodule init` to grab the submodule files)

In general though, the files in the submodule are versioned distinctly from the main repo (OrbitViz). If you make changes to the files in OrbitViz, then the submodules aren't affected.

OrbitViz has a reference to a particular commit of the submodules, the code snapshot that it works with. If another user on a different machine updates the submodule code and changes OrbitViz's recorded commit of that submodule, then when you pull the latest commits to OrbitViz to your machine, you won't actually get the latest submodule commits required. Generally, if you do a git status in the top directory for OrbitViz, you should see some indication that the CSTAR or OrbitPropagation commit reference has changed. To update the actual files on your machine, you'll use:
```
$ git submodule update
```

### 3. Look at all the pretty visualizationzzz

The Cesium files are provided by a webserver (hence the "node server.js" command), but the actual rendering is done in a web browser. So after you start up the server again (see section 1), open a web browser! I strongly recommend you use Google Chrome. I won't give any guarantees of functionality in other browsers.

So open the browser and navigate to: [http://localhost:8080/Apps/OrbitViz/runner.html](http://localhost:8080/Apps/OrbitViz/runner.html)

The visualization should start running immediately. It should look something like the below.

![Viz image](viz_shot.png)


## Execution

TODO: this needs an update when the crux pipeline is more fully baked

### 1. Open The Visualization In A Browser

Open [http://localhost:8080/Apps/OrbitViz/runner.html](http://localhost:8080/Apps/OrbitViz/runner.html) in a browser.  If you have not yet modified `sats_file.czml`, this should display a default visualization of two satellites over a few hour period.

<!-- ### 1. Clone the Comm_constellation_MDO repo

Currently our workflow is to run constellation simulations in the Comm_constellation_MDO code, and then use the output from that to update the visualization. It's not the *best* workflow, and I (Kit) envision many improvements over the course of my thesis work. For now though, that's the way we do it. [Here](https://github.com/ebclements/Comm_constellation_MDO)'s a link.

### 2. Run a sim

So you'll need to first run a sim in Comm_constellation_MDO. That produces an output file, Comm_constellation_MDO/landing_pad/timing_output.mat that has all the necessary data for populating an input .czml file to the visualization. -->

### 2. Run `runner_orbitviz.py`

This script ingests input files from orbit propagation as well as simulation output and uses them to construct the necessary visualization input files. Run it like so:

```
python runner_orbitviz.py
```

This updates the `sats_file.czml` input file in `app_data_files/`. 

### 3. Refresh visualization

Now go back to the browser and hard reload the visualization page - this clears any cached data files and reloads with the newly updated czml file.

On chrome on Mac, the shortcut I use is Cmd + Shift + r .

You should see the updated visualization running! If you don't see any changes from before, it may be that you didn't actually hard reload.

## Crux Component

This code is meant to be run as a component within a Crux pipeline. That means inputs and outputs are specified in the config files stored in `./crux/config/`, with input and output schemas defined in `./crux/config/schema`. The Crux backend uses the schemas to verify the correctness of input and output files. Input and output can be JSON, CSV, or some other file types.

## Directories

1. `app_data_files`

   Contains cesium-readable input files used for visualization.

   * `sats_file.czml`
      This is the input file containing all relevant data about geometry for the visualization. The full path relative to the cesium home directory should be: `Cesium-1.27/Apps/OrbitViz/app_data_files.`

   * `viz_objects.json`
      Contains configuration settings for some of the custom rendering code in CSTAR. Contain settings for callbacks used in the JavaScript code.

2. `renderers`

   Contains custom JavaScript renderers used on top of the Cesium engine. These are run by the CSTAR code.

   * `*.js`
      Renderer code.

   * `description.json`
      Contains a description of the renderers used, as well as a map to individual satellites in the visualization.

3. `python_runner`

   Entry point for Python code to run orbit  visualization. `runner_orbitviz.py` is what you should call from the command line for quick execution.

3. `crux`

   This contains the config files for using this repo as a Crux component.

   * `crux/config/schema`
      Directory containing the schema is used to validate inputs and outputs. Generally good to look here for explanations of the data found in the input and output files

   * `crux/config/examples/orbit_prop_inputs_ex.json`
      Example of a configuration file that contains all the inputs used for orbit propagation. This is also needed for visualization because it contains various important scenario parameters.

   * `crux/config/examples/orbit_prop_data_ex_small.json`
      Example of an output file with the data produced from orbit propagation. This is used in  visualization for constructing the geometric inputs used in the visualization (the .czml file)

   * `crux/config/examples/viz_params_ex.json`
      Example of an visualization parameters input file. Change `orbit_time_precision_s` to change the granularity of the time points used to describe the orbits in the visualization.

4. `czml`

   Contains prototypes for czml files, as well as other czml-related tools

5. `CSTAR`

   see above

6. `Storyboard`

   Contain storyboard files used for scripting time-related actions in a visualization ( use for example for making movies)

## Work In Progress

This is still a work in progress and is yet to be tested with the full Crux pipeline. More work to be done!
