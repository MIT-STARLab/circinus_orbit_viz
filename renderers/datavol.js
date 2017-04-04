/**
 *  Auxillary renderer for satellite data volume
 *
 * RGB chart: http://www.rapidtables.com/web/color/RGB_Color.htm
 */
class DataVolAuxRenderer {
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

        if ('datavol' in ent && ent.datavol !== undefined) {
            // console.log('yo')

            var datavol = ent.datavol.getValue(viewer.clock.currentTime)

            if (datavol !== undefined) {

                datavol_urgent = undefined

                if ('datavol_urgent' in ent && ent.datavol_urgent !== undefined) {
                    var datavol_urgent = ent.datavol_urgent.getValue(viewer.clock.currentTime)
                }

                if (datavol_urgent !== undefined) {
                    var total_horizontal_len = datavol + datavol_urgent;
                }
                else {
                    var total_horizontal_len = datavol;
                }
                var start_x = pos.x + 30;
                var start_y = pos.y + 10;
                var gauge_height = 20;

                // put a gold border around data gauge
                ctx.fillStyle = 'rgba(255,215,0,0.7)'; // gold
                ctx.fillRect( start_x, start_y, total_horizontal_len+4, gauge_height+4);

                // ctx.fillStyle = 'rgb(255,215,255)'; // white
                ctx.clearRect(start_x+2, start_y + 2 , total_horizontal_len, gauge_height);

                ctx.fillStyle = 'rgba(0, 255, 255, 0.5)';
                ctx.fillRect(start_x+2, start_y +2 , datavol, gauge_height);

                if (datavol_urgent !== undefined) {
                    ctx.fillStyle = 'rgba(255,69,0, 0.5)';
                    ctx.fillRect(start_x+2 + datavol, start_y +2 , datavol_urgent, gauge_height);
                }

                // label for data vol
                // ctx.font = '16px monospace';
                // ctx.fillStyle = 'white';
                // ctx.fillText(datavol.toString(), start_x+4, start_y + 17);
            }

        }
	}

}

// register with the auxrenderers
AuxRenderers.DataVol = DataVolAuxRenderer
