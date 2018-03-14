/**
 *  Auxillary renderer for for link data rates
 *
 * RGB chart: http://www.rapidtables.com/web/color/RGB_Color.htm
 *
 * note: also have to set up the datarate property in setupczml.js
 */
class DataRateAuxRenderer {
	/**
	 * No arg constructor
	 */
	constructor() {
		this.randomID = Math.floor(Math.random() * 100);

        var img1 = new Image();
        img1.src = 'renderers/x.png';
        this.xImg = img1;
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

            if (show !== undefined) {

                if ('datarate' in ent && ent.datarate !== undefined) {

                    var datarate = ent.datarate.getValue(viewer.clock.currentTime);

                    if (datarate !== undefined) {

                        if ( show ===  true) {
                            // write the data rate
                            let link_char = undefined;
                            if (ent.id.includes('Xlnk')) {
                                link_char = 'x';
                            }
                            if (ent.id.includes('Dlnk')) {
                                link_char = 'd';
                            }
                            ctx.font = '12px monospace';
                            ctx.fillStyle = 'white';
                            // ctx.fillText(link_char + ' ' + datarate.toPrecision(3).toString() + ' Mbps', pos.x + 60, pos.y - 20);
                        }

                        // do things with polyline - including displaying errors if necessary

                        // normal case
                        if (show === true &&  datarate > 0) {

                            var show_rate_change = true
                            if (show_rate_change) {
                                ent.polyline.width =  Math.max (datarate/10,1);
                            }
                            else {
                                ent.polyline.width = 6;
                            }

                            // console.log('rate change')

                            // figure out identifier character to add in front of datarate number
                            if (ent.id.includes('Xlnk')) {
                                ent.polyline.material.color._value.alpha = 1;
                                ent.polyline.material.color._value.blue = 0;
                                ent.polyline.material.color._value.red = 1;
                                ent.polyline.material.color._value.green = 0;
                            }
                            if (ent.id.includes('Dlnk')) {
                                ent.polyline.material.color._value.alpha = 1;
                                ent.polyline.material.color._value.blue = 1;
                                ent.polyline.material.color._value.red = 0;
                                ent.polyline.material.color._value.green = 0;
                            }

                        }
                        // // data rate shouldn't be zero with polyline displayed
                        // else if (show === true &&  datarate <= 0) {
                        //     ent.polyline.width = 100;
                        //     ent.polyline.material.color._value.alpha = 1;
                        //     ent.polyline.material.color._value.blue = 0;
                        //     ent.polyline.material.color._value.red = 1;
                        //     ent.polyline.material.color._value.green = 1;
                        //     ctx.drawImage(this.xImg, pos.x + 70, pos.y - 20, 40 ,40);
                        // }
                        // // data rate shouldn't be greater than zero if this isn't a link time
                        // else if (show === false &&  datarate > 0) {
                        //     ctx.drawImage(this.xImg, pos.x + 70, pos.y - 20, 40 ,40);
                        // }
                    }
                }
            }
            // else {
            //    ent.polyline.show = true;
            //    ent.polyline.material.color._value.alpha = 1;
            //    ent.polyline.material.color._value.blue = 0;
            //    ent.polyline.material.color._value.red = 1;
            //    ent.polyline.material.color._value.green = 1;
            // }
        }
	}

}

// register with the auxrenderers
AuxRenderers.DataRate = DataRateAuxRenderer
