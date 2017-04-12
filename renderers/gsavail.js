/**
 *  Auxillary renderer for satellite data volume
 *
 * RGB chart: http://www.rapidtables.com/web/color/RGB_Color.htm
 */
class GSavailAuxRenderer {
	/**
	 * No arg constructor
	 */
	constructor() {
		this.randomID = Math.floor(Math.random() * 100);

        var img1 = new Image();
        img1.src = 'renderers/sun.png';
        this.sunImg = img1;

        var img2 = new Image();
        img2.src = 'renderers/cloud.png';
        this.cloudImg = img2;

        var img3 = new Image();
        img3.src = 'renderers/moon.png';
        this.moonImg = img3;
	}

	/**
	 * Render method
	 * @param ctx canvas 2d render context
	 * @param ent the entity to bind to
	 * @param pos the position of that entity (window-space coordinates)
	 * @param visible boolean, true if visible (not occluded)
	 */
	render(ctx, ent, pos, visible) {
        // console.log('yo')

		if (!visible) return;

        if ('gs_availability' in ent && ent.gs_availability !== undefined) {

            var gs_availability = ent.gs_availability.getValue(viewer.clock.currentTime);

            if (gs_availability !== undefined) {


                if (gs_availability == true) {
                    // Need to figure out whether to draw sun or moon.

                    // center of the earth
                    var earthCenter = new Cesium.Cartesian3(0, 0, 0);

                    var sunPos_eci = Cesium.Simon1994PlanetaryPositions.computeSunPositionInEarthInertialFrame(viewer.clock.currentTime, new Cesium.Cartesian3());

                    // vec from center of earth to GS
                    var earthCenterToGS_ecef = Cesium.Cartesian3.subtract(ent.position.getValue(viewer.clock.currentTime), earthCenter, new Cesium.Cartesian3())

                    // TEME is an earth centered inertial frame, and though the cesium documentation is not very explicit, this seems to be the same inertial frame as that used for Simon1994PlanetaryPositions.computeSunPositionInEarthInertialFrame above
                    var inertialToFixed = Cesium.Transforms.computeTemeToPseudoFixedMatrix(viewer.clock.currentTime);

                    var sunPos_ecef = Cesium.Matrix3.multiplyByVector(inertialToFixed, sunPos_eci, new Cesium.Cartesian3());

                    // find angle between vector to sun and vector to sat. If greater than 90deg, it's night for the GS
                    var angle = Cesium.Cartesian3.angleBetween(sunPos_ecef, earthCenterToGS_ecef);

                    // console.log(ent.id.toString())
                    // // var String str1 = ent.id.toString();
                    // if ( ent.id.toString() === "Facility/Dadaab 3") {
                    //     console.log('Dadaabb 3')
                    //     console.log('current time: '+viewer.clock.currentTime.toString())

                    //     console.log('entpos: '+ent.position.getValue(viewer.clock.currentTime).toString())
                    //     console.log('sunPos_ecef: '+sunPos_ecef.toString())
                    //     console.log('earthCenterToGS_ecef: '+earthCenterToGS_ecef.toString())
                    //     // console.log('earthCenterToGS: '+earthCenterToGS.toString())
                    //     console.log((angle * 180 / Math.PI).toString())
                    // }


                    if (angle > Math.PI/2) {
                        ctx.drawImage(this.moonImg, pos.x + 10, pos.y - 50, 40 ,40);
                    }
                    else {
                        ctx.drawImage(this.sunImg, pos.x + 10, pos.y - 50, 50 ,50);
                    }

                }
                else {
                    ctx.drawImage(this.cloudImg, pos.x + 10, pos.y - 50, 50,50);
                }
            }
        }
	}

}

// register with the auxrenderers
AuxRenderers.GSavail = GSavailAuxRenderer
