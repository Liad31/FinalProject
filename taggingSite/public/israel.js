tag = undefined
imageID = 0
$(document).ready(function () {

    imageID = document.getElementById('image').getAttribute('src').slice(7, -4);
    //TODO: remove these
    // $.ajax({
    //   url: 'api/tagIsrael/getImage',
    //   type: 'get',
    //   success: function (image) {

    //     if (image == null) {
    //       return
    //     }
  
    //     imageID = image['imageID']
    //     $("#headline").text('Tag the image please');
    //     document["image"].src = "images/" + imageID + ".png"
        
    //   }
    // });
});

  
function tag_img(user_tag) {
    if (user_tag == 0) {
    tag = false
    $("#sec").prop("class", "btn-on");
    $("#rel").prop("class", "btn-off");

    } else {
    tag = true
    $("#rel").prop("class", "btn-on");
    $("#sec").prop("class", "btn-off");
    }
}

  
  function submitTag() {

    if (tag == undefined) {
      alert("you havent taged the image")
      return
    }
  
    $.ajax({
    url: 'api/tagIsrael/tag',
    type: 'post',
    data: { id: imageID, tag: tag },
    success: function (res) {
        window.location.href = "/israel";
    }
    });
    
}