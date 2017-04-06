/**
 *  Auxillary renderer for satellite data volume
 *
 * RGB chart: http://www.rapidtables.com/web/color/RGB_Color.htm
 */
class BatteryAuxRenderer {
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

        if ('battery' in ent && ent.battery !== undefined) {
            // console.log('yo')

            var battery = ent.battery.getValue(viewer.clock.currentTime)

            if (battery !== undefined) {

                var start_x = pos.x + 30;
                var start_y = pos.y + 7;
                var gauge_height = 7;

                var max_batt = 50;
                var min_desired_DOD = 35;

                var gauge_len = 70;
                var battery_fill_len = gauge_len*battery/max_batt;
                // console.log(battery)

                // put a gold border around data gauge
                ctx.fillStyle = 'rgba(255,215,0,0.7)'; // gold
                ctx.fillRect( start_x, start_y, gauge_len+4, gauge_height+4);

                // ctx.fillStyle = 'rgb(255,215,255)'; // white
                ctx.clearRect(start_x+2, start_y + 2 , gauge_len, gauge_height);

                if (battery > 45) {
                    ctx.fillStyle = 'rgba(0, 255, 0, 0.5)';
                }
                else if (battery > 40) {
                    ctx.fillStyle = 'rgba(173,255,47, 0.5)';
                }
                else if (battery > min_desired_DOD) {
                    ctx.fillStyle = 'rgba(255,255,0, 0.5)';
                }
                else {
                    ctx.fillStyle = 'rgba(255,0,0, 0.5)';
                }

                ctx.fillRect(start_x+2, start_y +2 , battery_fill_len, gauge_height);

                // label for battery
                ctx.font = '12px monospace';
                ctx.fillStyle = 'white';
                ctx.fillText(Math.round(battery).toString(), start_x+gauge_len+10, start_y + 10);

            }

        }
	}

}

// register with the auxrenderers
AuxRenderers.Battery = BatteryAuxRenderer
