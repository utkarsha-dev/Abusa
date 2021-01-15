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


function words() {
  var $fl = document.getElementById('flag');
  var $dl = document.getElementById('delete');

  if($fl.checked){
      chrome.tabs.executeScript({file: 'scripts/main/flagscript.js'});
    }
  else if($dl.checked){
    chrome.tabs.executeScript({file: 'scripts/main/deletescript.js'});
  }
}
 
document.getElementById('act').addEventListener('click', words);