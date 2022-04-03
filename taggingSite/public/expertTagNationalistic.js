let decision = -1;
let id;
let vidId;
$(document).ready(function () {
    $.ajax({
        url: 'api/expertTagNationalistic/getVid',
        type: 'get',
        data: { expert: false },
        success: function (vid) {
            if (vid == null) {
                $("div.iframe").hide();
                $("div.tag-panel").css("left", `${$(window).width() * 40 / 100}px`);
                $("#headline").text("There are no users to tag");
                $("div.buttons-top").hide();
                $("div.buttons-bottom").hide();
                return
            }
            $("#iframe").prop("src", "api/tiktokTag/video?id=" + vid.vidId);
            id = vid.objId;
            vidId = vid.vidId;
        }
    });
});


function tag(tag) {
    if (tag == 0) {
        decision = 0
        $("#sec").prop("class", "btn-on");
        $("#rel").prop("class", "btn-off");

    } else {
        decision = 1
        $("#rel").prop("class", "btn-on");
        $("#sec").prop("class", "btn-off");

    }
}


function submitTag() {
    if (decision < 0) {
        alert("you havent taged the video")
        return
    }
    $.ajax({
        url: 'api/expertTagNationalistic/tag',
        type: 'post',
        data: { id: id, tag: decision},
        success: function (videosJson) {
            window.location.href = "/expert-nationalistic";
        }
    });
}


function markError() {
    decision = 2
    submitTag()
}

function refresh() {
    $("#iframe").prop("src", "api/tiktokTag/video?id=" + vidId)
}

