$(document).ready(function(){
  $("audio").each(index => {
    $("#soundButton"+(index+1).toString()).click(function(){
      console.log($('#'+(index+1).toString()))
      document.getElementById((index+1).toString()).play()
    })
  });

});