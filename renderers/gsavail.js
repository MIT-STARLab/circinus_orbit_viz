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
	}

	/**
	 * Render method
	 * @param ctx canvas 2d render context
	 * @param ent the entity to bind to
	 * @param pos the position of that entity (window-space coordinates)
	 * @param visible boolean, true if visible (not occluded)
	 */
	render(ctx, ent, pos, visible) {
		if (!visible) return;

        if ('gs_availability' in ent && ent.gs_availability !== undefined) {
            // console.log('yo')

            var gs_availability = ent.gs_availability.getValue(viewer.clock.currentTime)

            if (gs_availability !== undefined) {
                var img = new Image();   // Create new img element

                if (gs_availability == true) {

                    img.src = 'renderers/sun.png'; // Set source path
                    ctx.drawImage(img, pos.x + 10, pos.y - 50, 50 ,50)
                }
                else {
                    img.src = 'renderers/cloud.png'; // Set source path
                    ctx.drawImage(img, pos.x + 10, pos.y - 50, 50,50)
                }

                // var start_x = pos.x + 30;
                // var start_y = pos.y + 10;
                // var gauge_height = 20;

                // // put a gold border around data gauge
                // ctx.fillStyle = 'rgba(255,215,0,0.7)'; // gold
                // ctx.fillRect( start_x, start_y, 15+4, gauge_height+4);

            }

        }
	}

}

// register with the auxrenderers
AuxRenderers.GSavail = GSavailAuxRenderer
