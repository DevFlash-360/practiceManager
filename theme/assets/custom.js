$(document).on('click','#pm-appbar-sidebar-toggle',function() {
  console.log('test');
  if ($("#pm-sidebar").hasClass("e-close")) {
    console.log("close class");
  } else {
    console.log("open class");
  }
});