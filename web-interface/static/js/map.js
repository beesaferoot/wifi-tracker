(function ($) {
    Map = {
        drawMap: () => {
            var $canvas = $('#Map').get(0);
            var ctx = $canvas.getContext('2d');
            // ctx.fillStyle = 'rgb(200, 0, 0)';
            // ctx.fillRect(10, 10, 50, 50);
    
            // ctx.fillStyle = 'rgba(0, 0, 200, 0.5)';
            // ctx.fillRect(30, 30, 50, 50);
            Map.placeDevices(ctx, Map.devices);
        },
        placePoints: (ctx, xcord, ycord) => {
            ctx.beginPath();
            ctx.arc(xcord, ycord, 5, 0, 2 * Math.PI);
            ctx.stroke();
        },
        placeDevices: (ctx, devices) => {
            for (device in devices) {
                Map.placePoints(ctx, devices[device].coordinate.xcord, devices[device].coordinate.ycord);
                ctx.fillStyle = Map.genRandomColor();
                ctx.fill();
                ctx.font = "15px Arial";
                ctx.fillText(devices[device].id, devices[device].coordinate.xcord, devices[device].coordinate.ycord + 25); 
            }
        },
        placeRouters: (ctx, xcord, ycord, width = 30, height = 30) => {
            ctx.fillStyle = Map.genRandomColor();
            ctx.fillRect(xcord, ycord, width, height);
        },
        setRouterLocations: (ctx, routers) => {
            routers.forEach(router => {
                var pos = router.coordinate;
                placeRouters(ctx, pos.xcord, pos.ycord);
            });
        },
        fetchRouters: () => {

        },
        fetchDevices: () => {
            return $.ajax({
                url: `/devices`,
            });
        },
        genRandomColor: () => {
            var randomColor = '#'+Math.floor(Math.random()*16777215).toString(16);
            return randomColor;
        },
        update: () => {
            //update Map devices 
            Map.fetchDevices().done(result => {
                Map.devices = JSON.parse(result);
            });
        }
    }
    // credit to Frank's Youtube Game series (How To Write A JavaScript PlatFormer) :)  
    var MapRenderer = function (time_step, Map) {
        this.updated = false;
        this.accumulated_time = undefined;
        this.animation_frame_request = undefined;
        this.time_step = time_step;
        this.time = undefined;
        this.run = (timestamp) => {
            this.accumulated_time += timestamp - this.time;
            this.time = timestamp;
            if (this.accumulated_time >= this.time_step * 3) {
                this.accumulated_time = this.time_step;
            }
            while (this.accumulated_time >= this.time_step) {
                this.accumulated_time -= this.time_step;
                Map.update();
                this.update = true;
            }

            if (this.update) {
                this.update = false;
                Map.drawMap();
            }
            this.animation_frame_request = window.requestAnimationFrame(this.handleRun);
        };
        this.handleRun = (time_step) => {
            this.run(time_step);
        }
    }
    MapRenderer.prototype = {
        start: function(){
            this.accumulated_time = this.time_step;
            this.time = window.performance.now();
            this.animation_frame_request = window.requestAnimationFrame(this.handleRun);
        },
        stop: function () {
            window.cancelAnimationFrame(this.animation_frame_request);
        }
    }
    $(document).ready(() => {
        //update Map every 2 seconds
        var mapEngine = new MapRenderer(2000, Map);
        mapEngine.start();
        
    });


})(jQuery);