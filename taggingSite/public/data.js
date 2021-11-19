$.ajax({
    url: 'api/tiktok/getValue',
    type: 'get',
    data: { name: "videos_tagged" },
    success:function(value){
      console.log(value)
    }
  });