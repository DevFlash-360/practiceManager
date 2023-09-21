$(document).on('click','#pm-appbar-sidebar-toggle',function() {
  if ($("#pm-sidebar").hasClass("e-close")) {
    $("#pm-content").css("margin-left", "80px");
  } 
  if ($("#pm-sidebar").hasClass("e-open")) {
    $("#pm-content").css("margin-left", "280px");
  }
});
$(document).on('click','.e-list-item',function() {
  console.log('testing');
  if ($("#pm-sidebar").hasClass("e-close")) {
    $("#pm-content").removeClass("pm-custom-margin");
  } 
  if ($("#pm-sidebar").hasClass("e-open")) {
    $("#pm-content").addClass("pm-custom-margin");
  }
});