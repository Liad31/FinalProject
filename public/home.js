$(document).ready(function(){
        $('#tagForm').submit(function(e){
        e.preventDefault();
        $.ajax({
            url: 'submitTag',
            type: 'post',
            data:$('#tagForm').serialize(),
            success:function(){
                console.log("hi")
            }
        });
    });
})
