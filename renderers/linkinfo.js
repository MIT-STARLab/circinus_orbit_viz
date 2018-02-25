/**
 *  Auxillary renderer for satellite data volume
 *
 * RGB chart: http://www.rapidtables.com/web/color/RGB_Color.htm
 */
class LinkInfoAuxRenderer {
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

                if ('link_info' in ent && ent.link_info !== undefined) {

                    var link_info = ent.link_info.getValue(viewer.clock.currentTime);

                    if (link_info !== undefined) {

                        if ( show ===  true) {
                            ctx.font = '12px monospace';
                            ctx.fillStyle = 'white';
                            ctx.fillText(link_info.toString(), pos.x + 60, pos.y - 5);
                        }

                    }
                }
            }
        }
	}

}

// register with the auxrenderers
AuxRenderers.LinkInfo = LinkInfoAuxRenderer
