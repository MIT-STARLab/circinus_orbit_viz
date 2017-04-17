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

            var show = ent.polyline.show.getValue(viewer.clock.currentTime);

            if (show !== undefined && show === true) {

                if ('datarate' in ent && ent.datarate !== undefined) {

                    var datarate = ent.datarate.getValue(viewer.clock.currentTime);

                    if (datarate !== undefined) {

                        var show_rate_change = true
                        if (show_rate_change) {
                            ent.polyline.width = datarate;
                        }

                        // console.log('rate change')

                        // figure out identifier character to add in front of datarate number
                        let link_char = undefined;
                        if (ent.id.includes('Xlnk')) {
                            link_char = 'x'
                        }
                        if (ent.id.includes('Dlnk')) {
                            link_char = 'd'
                        }

                        // label for battery
                        ctx.font = '12px monospace';
                        ctx.fillStyle = 'white';
                        ctx.fillText(link_char + ' ' + datarate.toPrecision(3).toString() + ' Mbps', pos.x + 50, pos.y - 20);

                    }
                }
            }
        }
	}

}

// register with the auxrenderers
AuxRenderers.DataRate = DataRateAuxRenderer
