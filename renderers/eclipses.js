/**
 *  Auxillary renderer for satellite eclipse times
 *
 * RGB chart: http://www.rapidtables.com/web/color/RGB_Color.htm
 */
class EclipsesAuxRenderer {
	/**
	 * No arg constructor
	 */
	constructor() {
		this.randomID = Math.floor(Math.random() * 100);

        var img1 = new Image();
        img1.src = 'renderers/sun.png';
        this.sunImg = img1;

        var img2 = new Image();
        img2.src = 'renderers/eclipse.png';
        this.eclipseImg = img2;
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

        if ('eclipse' in ent && ent.eclipse !== undefined) {

            var eclipse = ent.eclipse.getValue(viewer.clock.currentTime);

            if (eclipse !== undefined) {


                if (eclipse == true) {
                    ctx.drawImage(this.eclipseImg, pos.x + 10, pos.y - 50, 25 ,25);
                }
                else {
                    ctx.drawImage(this.sunImg, pos.x + 10, pos.y - 50, 25,25);
                }
            }
        }
	}

}

// register with the auxrenderers
AuxRenderers.Eclipses = EclipsesAuxRenderer
