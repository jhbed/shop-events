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
        console.log('response is' + data)
    }

    function showPosition(position) {
        console.log('made it in showPosition')
        var lat = position.coords.latitude;
        var lon = position.coords.longitude;
        console.log(lat + ', ' + lon)
        var url = "/events/compare_latlon/";
        var data = {latitude:lat, longitude:lon, csrfmiddlewaretoken: csrf, event_pk:event_pk};
        //console.log(data)
        //$.post(url, data, handleData);
        
        $.ajax({
            url: url,
            type: 'post', // This is the default though, you don't actually need to always mention it
            data: data,
            success: handleData,
            failure: function(data) { 
                console.log('Got an error dude');
            }
        });
    }

    function initMap() {
        // The location of Uluru
        var uluru = {lat: -25.344, lng: 131.036};
        // The map, centered at Uluru
        var map = new google.maps.Map(
            document.getElementById('map'), {zoom: 4, center: uluru});
        // The marker, positioned at Uluru
        var marker = new google.maps.Marker({position: uluru, map: map});
    }

    $('#map-button').on('click', getLocation);

    console.log('test')
    

});