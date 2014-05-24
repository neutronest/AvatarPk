env.engine = (function(){

  
  // require : load the js actively
  var require = function(url) {

    var s=document.createElement("script");
    s.setAttribute('type','text/javascript');
    s.src=env.config.base_url +url;	
    //document.write('<script type="text/javascript" src="'+sol.config.base_url+url+'" > <\/script>');
    document.getElementsByTagName("head")[0].appendChild(s);
    return 1;
  };

  // load data by ajax
  var ajax = function(data, url, async){
    var r;
    $.ajax({

      type: "POST",
      cache: false,
      url: env.config.base_url + url,
      async: false,
      data: data,
      success: function(data){
        r = JSON.parse(data);
      },
      error: function(data) {
        console.log("Error:" + data);
      }
    });
  };

  return {

    require : require,
    ajax : ajax
  };

})();

console.log("engine.js is loaded successful!!!");
