def get_default_chicago_map_config():
    """Returns the configuration for a map centered on Chicago."""
    # Chicago coordinates
    center = {"lat": 41.8781, "lng": -87.6298}
    # No markers, just center on Chicago
    return {"center": center, "zoom": 10, "markers": []}


def render_map(api_key, center, zoom=14, markers=None):
    """
    Renders a Google Map with specified center, zoom, and markers.

    :param api_key: str - Google Maps API key.
    :param center: dict - Center coordinates of the map, e.g., {"lat": 41.8781, "lng": -87.6298}.
    :param zoom: int - Zoom level of the map.
    :param markers: list - A list of markers to plot, each with "lat", "lng", "title", and "info".
    :return: str - HTML string for embedding the map in Streamlit.
    """
    html = f"""
    <!DOCTYPE html>
    <html>
        <head>
            <script src="https://maps.googleapis.com/maps/api/js?key={api_key}&libraries=places" async defer></script>
            <script>
                function initMap() {{
                    var mapCenter = {{ lat: {center['lat']}, lng: {center['lng']} }};
                    var map = new google.maps.Map(document.getElementById('map'), {{
                        center: mapCenter,
                        zoom: {zoom}
                    }});

                    var infowindow = new google.maps.InfoWindow();
    """
    
    if markers:
        for i, marker in enumerate(markers):
            html += f"""
                    (function() {{
                        var marker = new google.maps.Marker({{
                            position: {{ lat: {marker['lat']}, lng: {marker['lng']} }},
                            map: map,
                            title: "{marker['title']}"
                        }});
                        var infoContent = `
                            <h3>{marker['title']}</h3>
                            <p>{marker['info']}</p>
                        `;
                        google.maps.event.addListener(marker, 'click', function() {{
                            infowindow.setContent(infoContent);
                            infowindow.open(map, marker);
                        }});
                    }})();
            """
    
    html += """
                }
            </script>
        </head>
        <body onload="initMap()">
            <div id="map" style="height: 500px; width: 100%;"></div>
        </body>
    </html>
    """
    return html


def create_property_map(api_key, top_properties):
    """
    Creates a map for the given properties, including an image banner in each marker.

    :param api_key: str - Google Maps API key.
    :param top_properties: list - A list of property dictionaries containing latitude, longitude, and other details.
    :return: str - HTML string for embedding the map in Streamlit.
    """
    if not top_properties:
        print("No properties match your search.")
        return render_map(
            api_key,
            center={"lat": 41.8781, "lng": -87.6298},
            zoom=12,
            markers=[]
        )

    # Extract markers from property data
    markers = []
    for prop in top_properties:
        # Fallback image if no images are available
        image_url = prop.get("imgSrc") or "https://via.placeholder.com/200"

        # Create marker info with image as a banner
        info = f"""
            <div style="text-align:center;">
                <img src="{image_url}" alt="Property Image" style="width:200px;height:auto;border-radius:10px;"><br>
                Price: {prop.get('price', 'N/A')}<br>
                Bedrooms: {prop.get('bedrooms', 'N/A')}<br>
                Bathrooms: {prop.get('bathrooms', 'N/A')}<br>
                <a href="{prop['detailUrl']}" target="_blank">View Details</a>
            </div>
        """

        markers.append(
            {
                "lat": prop["latitude"],
                "lng": prop["longitude"],
                "title": prop["address"],
                "info": info,
            }
        )

    # Center the map on the first property
    center = {
        "lat": top_properties[0]["latitude"],
        "lng": top_properties[0]["longitude"]
    }

    return render_map(api_key, center=center, zoom=14, markers=markers)


def create_local_advisor_map(api_key, places):
    """
    Creates an interactive map for the Local Advisor feature.

    :param api_key: str - Google Maps API key.
    :param places: list - List of places returned by the Places API.
    :return: str - HTML string for embedding the map in Streamlit.
    """
    markers = []

    for place in places[:5]:
        # Extract required fields
        lat = place["geometry"]["location"]["lat"]
        lng = place["geometry"]["location"]["lng"]
        title = place["name"]
        address = place.get("formatted_address", "No address available")
        price_level = place.get("price_level", "Not available")
        rating = place.get("rating", "Not rated")
        user_ratings = place.get("user_ratings_total", "No ratings")
        open_now = (
            "Yes" if place.get("opening_hours", {}).get("open_now") else "No information"
        )
        icon_url = place.get("icon")  # Icon URL
        google_maps_link = place.get("google_maps_link")
        photo_reference = None

        # Check for a photo in the place details
        if "photos" in place and len(place["photos"]) > 0:
            photo_reference = place["photos"][0].get("photo_reference")
        
        # Construct photo URL (if available)
        if photo_reference:
            photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={api_key}"
        else:
            photo_url = icon_url  # Fallback to icon if no photo available

        # Create an HTML info string for the marker
        info = (
            f"<div style='text-align:center;'>"
            f"<img src='{photo_url}' alt='Image' style='width:100px;height:auto;'><br>"
            f"<b>{title}</b><br>"
            f"</div>"
            f"Address: {address}<br>"
            f"Price Level: {price_level}<br>"
            f"Rating: {rating} ({user_ratings} reviews)<br>"
            f"Open Now: {open_now}"
        )
        if google_maps_link:
            info += f"<br><a href='{google_maps_link}' target='_blank'>View on Google Maps</a>"

        # Append the marker information
        markers.append(
            {
                "lat": lat,
                "lng": lng,
                "title": title,
                "info": info,
            }
        )

    # Center the map on the first place if available, otherwise use Chicago coordinates
    if places:
        center = {
            "lat": places[0]["geometry"]["location"]["lat"],
            "lng": places[0]["geometry"]["location"]["lng"],
        }
    else:
        center = {"lat": 41.8781, "lng": -87.6298}

    return render_map(api_key, center=center, markers=markers, zoom=12)


