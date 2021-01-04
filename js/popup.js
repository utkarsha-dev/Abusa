$(document).ready(function () {
  $('#switch').click(function () {
    $('#flag').prop("disabled", !$("#switch").prop("checked"));
    $('#delete').prop("disabled", !$("#switch").prop("checked"));
    $('#Check').prop("disabled", !$("#switch").prop("checked")); 
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