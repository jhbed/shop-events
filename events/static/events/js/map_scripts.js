$(document).ready(function(){

    var x = $('.demo');

    function getLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(showPosition);
            console.log('made it in getLocation')
        } else { 
            x.html("Geolocation is not supported by this browser.");
        }
    }

    function handleData(data) {
        console.log('response is ' + data)
        if (data == 'Successfully checked you in') {
            var tag = '#ajax-success'
        } else {
            var tag = '#ajax-error'
        }



        $(tag).html(data)
        $(tag).show()
    }

    function showPosition(position) {
        console.log('made it in showPosition')
        var lat = position.coords.latitude;
        var lon = position.coords.longitude;
        console.log(lat + ', ' + lon)
        var url = "/events/compare_latlon/";
        
        var data = {
                latitude:lat, 
                longitude:lon, 
                csrfmiddlewaretoken: csrf, 
                event_pk:event_pk
            };
        //console.log(data)
        //$.post(url, data, handleData);
        
        $.ajax({
            url: url,
            type: 'post', // This is the default though, you don't actually need to always mention it
            data: data,
            success: handleData,
            failure: function(data) { 
                console.log('There was an ajax error. This msg is sent from js code in the POST Ajax call');
            }
        });
    }

    $('#map-button').on('click', getLocation);
    var today = new Date();
    //console.log(today)
    //console.log(event_month == today.getMonth + 1)
    var event_date = new Date(event_year, event_month-1, event_day)
    if(event_day == today.getDate() && event_month == today.getMonth() + 1 && event_year == today.getFullYear()) {
        $('#today-button').show();
    } else if (event_date < today) {
        $('#day-passed').show();
    } else {
        $('#not-today-button').show();
    }

});