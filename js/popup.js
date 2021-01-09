$(document).ready(function () {
  $('#switch').click(function () {
    $('#flag').prop("disabled", !$("#switch").prop("checked"));
    $('#delete').prop("disabled", !$("#switch").prop("checked"));
    $('#Check').prop("disabled", !$("#switch").prop("checked")); 
    $('#act').prop("disabled", !$("#switch").prop("checked"));

    if (!this.checked) {
      $("#generate").prop("disabled",true);
      $('#Check').prop("checked",false);
      $('#flag').prop("checked",false);
      $('#delete').prop("checked",false);
    }

  })
});

$(document).ready(function () {
  $('#Check').click(function () {
    $('#generate').prop("disabled", !$("#Check").prop("checked")); 
  })
});

$(function(){
  $('#generate').click(function(){
    alert('Contact Admin!');
  });
});