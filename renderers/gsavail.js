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
                    var earthCenter = new Cesium.Cartesian3(0, -6371, 0);

                    var sunPos = Cesium.Simon1994PlanetaryPositions.computeSunPositionInEarthInertialFrame(viewer.clock.currentTime, new Cesium.Cartesian3());

                    // vec from center of earth to sat
                    var earthCenterToSat = Cesium.Cartesian3.subtract(ent.position.getValue(viewer.clock.currentTime), earthCenter, new Cesium.Cartesian3())

                    // find angle between vector to sun and vector to sat. If greater than 90deg, it's night for the GS
                    var angle = Cesium.Cartesian3.angleBetween(sunPos, earthCenterToSat)

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
