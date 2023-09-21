$(document).on('click','#pm-appbar-sidebar-toggle',function() {
  if ($("#pm-sidebar").hasClass("e-close")) {
    $("#pm-content").css("margin-left", "80px");
  } 
});