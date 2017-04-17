/**
 *  Auxillary renderer for satellite data volume
 *
 * RGB chart: http://www.rapidtables.com/web/color/RGB_Color.htm
 */
class DataRateAuxRenderer {
	/**
	 * No arg constructor
	 */
	constructor() {
		this.randomID = Math.floor(Math.random() * 100);
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

        if ('polyline' in ent && ent.polyline !== undefined) {

            ent.polyline.width = 15;

            console.log('rate change')

            // var gs_availability = ent.gs_availability.getValue(viewer.clock.currentTime);

            // if (gs_availability !== undefined) {



            // }
        }
	}

}

// register with the auxrenderers
AuxRenderers.DataRate = DataRateAuxRenderer
