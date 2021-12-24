let user_tag = -1
let videosIDs
let userID
let numOfVideos = 0
let currentVideoPos = 0
$(document).ready(function () {
  $("#expert").hide();
  // $("#error").hide();
  $("div.buttons-top").hide();
  //TODO: remove these
  $.ajax({
    url: 'api/tagLocation/getUser',
    type: 'get',
    data: { expert: false },
    success: function (user) {
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

      $("#headline").text(`Tag the video ${currentVideoPos + 1}/${numOfVideos}`);

      $.ajax({
        url: 'api/tiktokTag/getVideosLoc',
        type: 'get',
        data: { userId: user['userId'] },
        success: function (videosJson) {
          videoIds = videosJson['videoIds']
          videoIds = String(videoIds)
          videoIds = videoIds.split(',');
          $("#iframe").prop("src", "api/tiktokTag/video?id=" + videoIds[currentVideoPos])
        }
      });
    }
  });
});

function tag(tag) {
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


function submitTag() {

  if (currentVideoPos == numOfVideos && user_tag < 0) {
    alert("you havent taged the user")
    return
  }

  currentVideoPos++
  $("#rel").prop("class", "btn-off");
  $("#sec").prop("class", "btn-off");

  if (currentVideoPos < numOfVideos) {
    $("#iframe").prop("src", "api/tiktokTag/video?id=" + videoIds[currentVideoPos])
    $("#headline").text(`Tag the video ${currentVideoPos + 1}/${numOfVideos}`);
  }
  else if (currentVideoPos == numOfVideos) {
    $("div.iframe").hide();
    $("#iframe").prop("src", "api/tiktokTag/video?id=0")
    $("div.tag-panel").css("left", `${$(window).width() * 45 / 100}px`);
    $("div.buttons-top").show(); //TODO: remove this
    $("#headline").html(`Tag the <a href='https://www.tiktok.com/@${userName}?' target="_blank">user</a>`);
  }
  else {
    $.ajax({
      url: 'api/tagLocation/tag',
      type: 'post',
      data: { id: userID, user_tag: user_tag },
      success: function (videosJson) {
        window.location.href = "/location";
      }
    });
  }
}

function passToExpert() {
  $.ajax({
    url: 'api/tagLocation/expert',
    type: 'post',
    data: { id: userID, message: $('textarea#message').val() },
    success: function (videosJson) {
      window.location.href = "/location";
    }
  });
}

function markError() {
  $.ajax({
    url: 'api/tagLocation/markError',
    type: 'post',
    data: { id: userID },
    success: function (videosJson) {
      window.location.href = "/location";
    }
  });
}

function refresh() {
  currentVideoPos -= 1;
  return submitTag();
}