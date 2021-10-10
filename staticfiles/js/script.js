if (document.getElementById('main_canvas')) {

  // context
  let main_canvas = document.getElementById("main_canvas");

  main_canvas.width = window.innerWidth;

  let setting = {
    move:true,
    canvas:main_canvas,
    offset:{
      grid:{
        x:0,
        y:0,
      },
      price:{
        x:0,
        y:main_canvas.offsetHeight,
      },
    },
    zoom: {
      x:1,
      y:1,
    },
    style:{
      grid:{
        linecolor:"#151414",
        linewidth:2,
        spacing:{
          x:50,
          y:50,
        },
      },
      price:{
        linecolor:{
          high:"lime",
          low:'red'
        },
        linewidth:1,
        linebackground:{
          high:"green",
          low:"darkred",
          transition:"#000000",
        }
      },
      axis:{
        linecolor:"#151414",
        linewidth:5
      }
    }
  }

  raw = {
    close:[]
  };

  for (balance in chart) {
    raw.close.push(chart[balance].balance);
  }

  let client = {
    x:0, y:0,
    old:{
      x:0, y:0
    }
  }

  get_in_view_data({
    client:client,
    setting:setting,
    raw:raw,
  });

  window.onresize = (event) => {

    // change canvas width to fit window
    main_canvas.width = window.innerWidth;

    // update settings on window resize
    setting.canvas = main_canvas,
    setting.offset.price = {
        x:0,
        y:main_canvas.offsetHeight,
      }

    clear_canvas({
      setting:setting,
    });

    get_in_view_data({
      client:client,
      setting:setting,
      raw:raw,
    });
  }

  key_events = function(event) {

    event = event || window.event;

    if(setting.move) {

      setting.move =  false;

      if (event.keyCode == '37') {
          clear_canvas({
            setting:setting,
          });

          // assigning x to old x before updating x locations
          client.old.x = client.x;
          client.x+=50;

          // left arrow
          get_in_view_data({
            client:client,
            setting:setting,
            raw:raw,
          });

      }
      else if (event.keyCode == '39') {  

        clear_canvas({
          setting:setting,
        });

        // assigning x to old x before updating x locations
        client.old.x = client.x;
        client.x-=50;

        // right arrow
        get_in_view_data({
          client:client,
          setting:setting,
          raw:raw,
        });
      }

      setting.move =  true;

    }

  }

  document.onkeydown = key_events;

}

