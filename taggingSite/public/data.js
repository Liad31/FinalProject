
 $.ajax({
    url: 'api/tiktok/userIds',
    type: 'get',
    success: function (users) {
        console.log(users)
        ids = users;
    }
});


$.ajax({
    url: 'api/tiktok/userStats',
    type: 'get',
    data: { userId: "61770c2c3840138c7225f572" },
    success: function (stats) {
        console.log(stats)
    }
});


// $.ajax({
//     url: 'api/tiktok/stats',
//     type: 'get',
//     success: function (stats) {
//         console.log(stats)
//     }
// });

$.ajax({
    url: 'api/tiktok/weeklyUserStats',
    type: 'get',
    data: { userId: "61770c2c3840138c7225f572" },
    success: function (stats) {
        console.log(stats)
    }
});


// $.ajax({
//     url: 'api/tiktok/weeklyStats',
//     type: 'get',
//     success: function (stats) {
//         console.log(stats)
//     }
// });