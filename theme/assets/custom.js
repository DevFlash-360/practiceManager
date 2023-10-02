$(document).ready(function() {
  console.log('hello');
$(document).on('click','#pm-appbar-sidebar-toggle',function() {
  if ($("#pm-sidebar").hasClass("e-close")) {
    $("#pm-content").css("margin-left", "95px");
    $("#pm-content").removeClass("pm-custom-margin");
  } 
  if ($("#pm-sidebar").hasClass("e-open")) {
    $("#pm-content").css("margin-left", "280px");
    $("#pm-content").addClass("pm-custom-margin");
  }
});
$(document).on('click','.e-list-item',function() {
  if ($("#pm-sidebar").hasClass("e-close")) {
    $("#pm-content").removeClass("pm-custom-margin");
  } 
  if ($("#pm-sidebar").hasClass("e-open")) {
    $("#pm-content").addClass("pm-custom-margin");
  }
});
