let times
let user_tag = -1
let tags_array
let videosIDs
let userID
let numOfVideos = 0
let currentVideoPos = 0
$( document ).ready(function() {
  $.ajax({
      url: 'api/tiktok/getUser',
      type: 'get',
      data : {expert: false},
      success:function(user){
        numOfVideos = user['numOfVideos']
        userID = user['userId']
        tags_array = new Array(numOfVideos)
        for (let i = 0; i < numOfVideos; i++) {
          tags_array[i] = -1
        }
        times = new Array(numOfVideos)
        $.ajax({
          url: 'api/tiktok/getVideos',
          type: 'get',
          data: { userId: user['userId'] },
          success:function(videosJson){
            videoIds = videosJson['videoIds']
            videoIds = String(videoIds)
            videoIds = videoIds.split(',');
            document.getElementsByClassName("iframe")[0].setAttribute("src", "api/tiktok/video?id=" + videoIds[currentVideoPos])
            time = new Date();
          }
        });
      }
  });
});

function tag(tag) {
  if (currentVideoPos < numOfVideos){
    if (tag == 0) {
      tags_array[currentVideoPos] = 0
      document.getElementById("sec").style.background = 'cyan'
      document.getElementById("rel").style.background = 'gray'

    } else {
      tags_array[currentVideoPos] = 1
      document.getElementById("rel").style.background = 'cyan'
      document.getElementById("sec").style.background = 'gray'

    }
  } else {
    if (tag == 0) {
      user_tag = 0
      document.getElementById("sec").style.background = 'cyan'
      document.getElementById("rel").style.background = 'gray'

    } else {
      user_tag = 1
      document.getElementById("rel").style.background = 'cyan'
      document.getElementById("sec").style.background = 'gray'

    }
  }
}


function submitTag(){

  if (currentVideoPos < numOfVideos && tags_array[currentVideoPos] < 0) {
    alert("you havent taged the video")
    return
  }
  if (currentVideoPos == numOfVideos && user_tag < 0) {
    alert("you havent taged the user")
    return
  }
  if (currentVideoPos < numOfVideos) {
    times[currentVideoPos] = calcSeconds(new Date(), time);
    time = new Date();
  }
  
  currentVideoPos++
  btns = document.getElementsByClassName("btn");
  for (let i = 0; i < 2; i++) {
    btns[i].style.background = 'gray'
  }

  if (currentVideoPos < numOfVideos){
    document.getElementsByClassName("iframe")[0].setAttribute("src", "api/tiktok/video?id=" + videoIds[currentVideoPos])
  }
  else if(currentVideoPos == numOfVideos){
    document.getElementsByClassName("iframe")[0].style.display = 'none'; //change something
  }
  else {
    $.ajax({
    url: 'api/tiktok/tag',
    type: 'post',
    data: { id: userID, user_tag: user_tag, videos_tag: tags_array, times_array: times },
    success:function(videosJson){
      window.location.href = "/";
    }
  });    }
}

function passToExpert(){
  $.ajax({
    url: 'api/tiktok/expert',
    type: 'post',
    data: { id: userID },
    success:function(videosJson){
      window.location.href = "/";
    }
  });
}

function calcSeconds(time2, time1){
  var dif = time2 - time1;
  return dif / 1000;
}
