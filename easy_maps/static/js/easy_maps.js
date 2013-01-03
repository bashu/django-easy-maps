// will contain the boundary of the map.
var g_lat_long_bound = new google.maps.LatLngBounds();

function easy_map_add_listener(id, marker) {
    // update the coordinate on marker dragging
    google.maps.event.addListener(marker, 'dragend', function(evt) {
        var ll = marker.getPosition();
        // FIXME: fix id names
        document.getElementById(id + 'latitude').value = ll.lat();
        document.getElementById(id + 'longitude').value = ll.lng();
    });
}

function easy_maps_add_marker(map, marker) {
    var latlng = new google.maps.LatLng(marker.latitude, marker.longitude);
    var marker = new google.maps.Marker({
        position: latlng,
        map: map,
        draggable: true,
        title: marker.address
    });

    // add marker's coordinate to the boundary
    g_lat_long_bound.extend(latlng);

    return marker;
}
