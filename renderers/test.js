/**
 * Example auxillary renderer
 *
 * RGB chart: http://www.rapidtables.com/web/color/RGB_Color.htm
 */
class TestAuxRenderer {
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



        // console.log(ent.name)

        if ('datavol' in ent && ent.datavol !== undefined) {
            // console.log('hey')
            // console.log(ent.datavol.getValue(viewer.clock.currentTime))
            var datavol = ent.datavol.getValue(viewer.clock.currentTime)

    		// ctx.font = '16px monospace';
    		// ctx.fillStyle = 'red';
    		// ctx.fillText(this.randomID + ':' + viewer.clock.currentTime.toString().split('.')[0], pos.x + 10, pos.y + 15);

            var total_horizontal_len = datavol;
            var start_x = pos.x + 30;
            var start_y = pos.y + 10;
            var gauge_height = 20;

            // put a gold border around data gauge
            ctx.fillStyle = 'rgba(255,215,0,0.7)'; // gold
            ctx.fillRect( start_x, start_y, total_horizontal_len+4, gauge_height+4);

            // ctx.fillStyle = 'rgb(255,215,255)'; // white
            ctx.clearRect(start_x+2, start_y + 2 , datavol, gauge_height);

            ctx.fillStyle = 'rgba(0, 255, 255, 0.5)';
            ctx.fillRect(start_x+2, start_y +2 , datavol, gauge_height);

            // ctx.beginPath();
            // ctx.arc(pos.x + 60, pos.y + 30, customProperty+11, 0, Math.PI*2, true);
            // ctx.closePath();
            // ctx.fill();


            // ctx.fillStyle = 'rgb(250,128,114)';  //salmon
            // // ctx.fillRect(pos.x + 10, pos.y + 10, 100, 100);

            // ctx.beginPath();
            // ctx.arc(pos.x + 60, pos.y + 30, customProperty+10, 0, Math.PI*2, true);
            // ctx.closePath();
            // ctx.fill();

            // ctx.fillStyle = 'rgb(100,149,237)';  //corn flower blue
            // // ctx.fillRect(pos.x + 10, pos.y + 10, 100, 100);

            // ctx.beginPath();
            // ctx.arc(pos.x + 60, pos.y + 30, customProperty, 0, Math.PI*2, true);
            // ctx.closePath();
            // ctx.fill();
        }
	}

}

// register with the auxrenderers
AuxRenderers.Test = TestAuxRenderer
