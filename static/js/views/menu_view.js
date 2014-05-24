env.views.menu_view = (function(){

  var logo = function() {

    var content =  "<div id='logo'>"
          + "<img src='/static/img/logo.png'></img>"
          + "</div>";

    var display = function() {
      $("#container").html(content);
    };
  };

  var init = function() {

    env.views.menu_view.logo.display();
  };
  
  return {

    logo : logo,
    init : init
  };
})();

console.log("menu_view has loaded successfully!!!");




