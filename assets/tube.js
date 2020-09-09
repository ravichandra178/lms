console.log('Script called');
// 2. This code loads the IFrame Player API code asynchronously.
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// 3. This function creates an <iframe> (and YouTube player)
//    after the API code downloads.
var playerDivs = document.querySelectorAll(".player"); // get .player nodes
var playerDivsArr = [].slice.call(playerDivs); // nodelist to array to use forEach();
var players = new Array(playerDivsArr.length);

// when youtube stuff is ready
function onYouTubeIframeAPIReady() {

  // create yt players
  playerDivsArr.forEach(function (e, i) { // forEach ...
    var iframe_id = e.id;
    //alert(iframe_id)
    players[i] = new YT.Player(iframe_id, {
      videoId: iframe_id,
      width: "100%",
      height: "562",
      events: {
        //'onReady': onPlayerReady,
        'onStateChange': function (event) {
          onPlayerStateChange(event, iframe_id);
        }
      }
    })
  })


}
//function onPlayerReady(event) {
//
// }
function onEnded(playerStatus, iframe_id) {
  var color;
  if (playerStatus == -1) {
    color = "#37474F"; // unstarted = gray
  } else if (playerStatus == 0) {
    color = "#FFFF00"; // ended = yellow
    //alert(iframe_id)
    console.log("Video ended");
    $.ajax({
      url: "/ajax/onended/",
      data: { 'iframe_id': iframe_id },
      success: function (data) {
        var status = 'status_' + data.module;
        document.getElementById(status).innerHTML = data.count;
        // alert('#videoContent'+data.lesson);
        $(`#videoContent${data.lesson}`).attr("checked", "checked");
        $(`#playBtn${data.lesson}`).css("color", "#04a83b");
      }
    })
  } else if (playerStatus == 1) {
    color = "#33691E"; // playing = green
  } else if (playerStatus == 2) {
    color = "#DD2C00"; // paused = red
    //alert('im paused')
  } else if (playerStatus == 3) {
    color = "#AA00FF"; // buffering = purple
  } else if (playerStatus == 5) {
    color = "#FF6DOO"; // video cued = orange
  }
}
function onPlayerStateChange(event, iframe_id) {
  //alert(iframe_id)
  onEnded(event.data, iframe_id);
}

// Video deferring
$(document).ready(function () {
  $(function () {
    $('iframe').attr('data-src', function () { return $(this).attr('src'); })
      .removeAttr('src');
  });

})