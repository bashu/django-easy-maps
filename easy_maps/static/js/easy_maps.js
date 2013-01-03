// will contain the boundary of the map.
var g_lat_long_bound = new google.maps.LatLngBounds();

function easy_maps_set_form_value(id_prefix) {
    return function (computed_address, lat, lng, error) {
        document.getElementById(id_prefix + 'computed_address').value = computed_address;
        document.getElementById(id_prefix + 'latitude').value         = lat
        document.getElementById(id_prefix + 'longitude').value        = lng;
        document.getElementById(id_prefix + 'geocode_error').value    = error;
    };
}

function easy_maps_bind_button (id_prefix) {
        django.jQuery.post(
            // FIXME: this is hardcoded
            '/admin/easy_maps/address/geo/', {
            //'{% url admin:address_json %}', {
                'address': document.getElementById(id_prefix + 'address').value
            },
            function(data) {
                easy_maps_set_form_value(id_prefix)(
                    data["computed_address"],
                    data["latitude"],
                    data["longitude"],
                    data["geocode_error"]
                );
                var center = new google.maps.LatLng(data["latitude"], data["longitude"]);
                marker.setPosition(center);
                map.setCenter(center);
            }
        );

        return false;
}

function easy_maps_add_listener(id_prefix, marker) {
    // update the coordinate on marker dragging
    google.maps.event.addListener(marker, 'dragend', function(evt) {
        var ll = marker.getPosition();
        // FIXME: fix id names
        document.getElementById(id_prefix + 'latitude').value = ll.lat();
        document.getElementById(id_prefix + 'longitude').value = ll.lng();
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
