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