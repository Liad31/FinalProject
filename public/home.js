$(document).ready(function(){
    let user
    let videoId
    $('submitButton').click(submitAnswer);
})
function nextVideo(){
    
}
function submitAnswer(){
    const id=this.id
    $.ajax({
        url: 'submitTag',
        type: 'post',
        data: JSON.stringify({
            'userId': user
            'videoId': 
            'tag': id
            'features': 
        }),
        success:function(){
            console.log("hi")
        }
    });
}