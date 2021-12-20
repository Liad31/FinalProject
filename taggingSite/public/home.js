let times
let user_tag = -1
let tags_array
let videosIDs
let userID
let numOfVideos = 0
let currentVideoPos = 0
let userName
let features = []
$( document ).ready(function() {
  // $("#expert").hide();
  // $("#error").hide();
  // $("div.buttons-top").hide();
  $.ajax({
      url: 'api/tiktok/getUser',
      type: 'get',
      data : {expert: false},
      success:function(user){
        if (user == null) {
          $("div.iframe").hide();
          $("div.tag-panel").css("left", `${$(window).width() * 40 / 100}px`);
          $("#headline").text("There are no users to tag");
          $("div.features").hide();
          $("div.buttons-top").hide();
          $("div.buttons-bottom").hide();
          return
        }
        if (user.message != null) {
          $("#expert-message").show();
          $("p").text(user.message);
        }
        
        numOfVideos = user['numOfVideos']
        userID = user['userId']
        userName = user.userName;
        tags_array = new Array(numOfVideos)
        for (let i = 0; i < numOfVideos; i++) {
          tags_array[i] = -1
        }
        $("#headline").text(`Tag the video ${currentVideoPos + 1}/${numOfVideos}`);
        times = new Array(numOfVideos)
        $.ajax({
          url: 'api/tiktok/getVideos',
          type: 'get',
          data: { userId: user['userId'] },
          success:function(videosJson){
            videoIds = videosJson['videoIds']
            videoIds = String(videoIds)
            videoIds = videoIds.split(',');
            $("#iframe").prop("src", "api/tiktok/video?id=" + videoIds[currentVideoPos])
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
      $("#sec").prop("class", "btn-on");
      $("#rel").prop("class", "btn-off");

    } else {
      tags_array[currentVideoPos] = 1
      $("#rel").prop("class", "btn-on");
      $("#sec").prop("class", "btn-off");

    }
  } else {
    if (tag == 0) {
      user_tag = 0
      $("#sec").prop("class", "btn-on");
      $("#rel").prop("class", "btn-off");

    } else {
      user_tag = 1
      $("#rel").prop("class", "btn-on");
      $("#sec").prop("class", "btn-off");
    }
  }
}


function submitTag(calc_seconds){

  if (currentVideoPos < numOfVideos && tags_array[currentVideoPos] < 0) {
    alert("you havent taged the video")
    return
  }
  if (currentVideoPos == numOfVideos && user_tag < 0) {
    alert("you havent taged the user")
    return
  }
  if (currentVideoPos < numOfVideos) {
    if (calcSeconds){
      times[currentVideoPos] = calcSeconds(new Date(), time);
    }
    time = new Date();
    let this_features = {}
    $(':checkbox').each(function(i){
      console.log($(this), "checkbox")
      console.log($(this).prop('checked'), "is checked")
      this_features[$(this).prop('name')] = $(this).prop('checked')
    });
    features.push(this_features)
    console.log(features, "this_features")
  }
  
  currentVideoPos++
  $("#rel").prop("class", "btn-off");
  $("#sec").prop("class", "btn-off");

  if (currentVideoPos < numOfVideos){
    $("#iframe").prop("src", "api/tiktok/video?id=" + videoIds[currentVideoPos])
    $("#headline").text(`Tag the video ${currentVideoPos + 1}/${numOfVideos}`);
  }
  else if(currentVideoPos == numOfVideos){
    $("div.iframe").hide();
    $("div.tag-panel").css("left", `${$(window).width() * 45 / 100}px`);
    $("#headline").html(`Tag the <a href='https://www.tiktok.com/@${userName}?' target="_blank">user</a>`);
    // $("div.buttons-top").show();
  }
  else {
    console.log(features, "this_features")
    $.ajax({
    url: 'api/tiktok/tag',
    type: 'post',
    data: { id: userID, user_tag: user_tag, features:features, videos_tag: tags_array, times_array: times },
    success:function(videosJson){
      window.location.href = "/";
    }
  });    }
}

function passToExpert(){
  $.ajax({
    url: 'api/tiktok/expert',
    type: 'post',
    data: { id: userID, message: $('textarea#message').val() },
    success:function(videosJson){
      window.location.href = "/";
    }
  });
}

function markError() {
  $.ajax({
    url: 'api/tiktok/markError',
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

function refresh(){
  currentVideoPos-=1;
  return submitTag(false);
}
