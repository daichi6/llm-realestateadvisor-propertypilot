import folium
import geopandas as gpd

def create_property_map(properties):
    """
    Creates a Folium map with markers for each property in the list.

    :param properties: list - A list of dictionaries, each containing property details such as latitude, longitude, and address.
    :return: folium.Map - A Folium map object with markers for each property.
    """
    # Attribution for custom tileset
    attr = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    
    # Initialize the map centered around Chicago
    property_map = folium.Map(location=[41.881832, -87.623177], zoom_start=11, tiles='OpenStreetMap_Mapnik', attr=attr)

    # Loop through each property in the list
    for prop in properties:
        # Extract latitude and longitude
        latitude = prop['latitude']
        longitude = prop['longitude']
        detail_url = prop['detailUrl']
        address = prop['address']

        # Add markers to the map
        folium.Marker(
            location=[latitude, longitude],
            popup=folium.Popup(f'<a href="{detail_url}" target="_blank">{address}</a>', max_width=250),
            tooltip="Click for Zillow Listing",
            icon=folium.Icon(icon = 'home', color="blue")
        ).add_to(property_map)
    return property_map


def create_property_restaurant_map(properties):
    """
    Creates a Folium map with markers for each property and associated restaurants.

    :param properties: list - A list of dictionaries, each containing property details and two associated restaurants.
    :return: folium.Map - A Folium map object with markers for each property and associated restaurants.
    """
    # Attribution for custom tileset
    attr = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    
    # Initialize the map centered around Chicago
    property_map = folium.Map(location=[41.881832, -87.623177], zoom_start=11, tiles='OpenStreetMap', attr=attr)

    # Loop through each property location in the list
    for prop in properties:
        # Extract property details
        latitude = prop['latitude']
        longitude = prop['longitude']
        detail_url = prop['detailUrl']
        address = prop['address']

        # Add a marker to the map for the property
        folium.Marker(
            location=[latitude, longitude],
            popup=folium.Popup(f'<a href="{detail_url}" target="_blank">{address}</a>', max_width=250),
            tooltip="Click for property details",
            icon=folium.Icon(icon='home', color="blue")
        ).add_to(property_map)

        # Loop through the associated restaurants
        for key in ['restaurant_1', 'restaurant_2']:
            if key in prop:
                restaurant = prop[key]
                # Extract relevant restaurant data
                name = restaurant['business_name']
                categories = ', '.join(restaurant['categories_titles'])
                rating = restaurant['rating']
                res_latitude = restaurant['latitude']
                res_longitude = restaurant['longitude']
                res_address = restaurant['display_address']
                url = restaurant['url']

                # Add a marker to the map for the restaurant
                folium.Marker(
                    location=[res_latitude, res_longitude],
                    popup=folium.Popup(f'<a href="{url}" target="_blank">{name}</a><br/>{categories}<br/>Rating: {rating}', max_width=250),
                    tooltip=f"Click for details on {name}",
                    icon=folium.Icon(icon='cutlery', color="red")
                ).add_to(property_map)
    return property_map


def create_yelp_restaurant_map(yelp_advisor_results):
    """
    Creates a map with markers for each restaurant from Yelp API results, using Folium for visualization.

    :param yelp_advisor_results: dict - A dictionary of Yelp API results containing business information.
    :return: folium.Map - A Folium map object with restaurant markers added to it.
    """
    # Attribution for custom tileset
    attr = '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    
    # Initialize the map centered around Chicago
    restaurant_map = folium.Map(location=[41.881832, -87.623177], zoom_start=11, tiles='OpenStreetMap', attr=attr)

    # Loop through each business in the Yelp results
    for business in yelp_advisor_results['businesses']:
        # Extract restaurant details
        name = business['name']
        categories = ', '.join([category['title'] for category in business['categories']])
        rating = business['rating']
        latitude = business['coordinates']['latitude']
        longitude = business['coordinates']['longitude']
        address = ', '.join(business['location']['display_address'])
        url = business['url']
        
        # Add a marker to the map for the restaurant
        folium.Marker(
            location=[latitude, longitude],
            popup=folium.Popup(f'<a href="{url}" target="_blank">{name}</a><br/>{categories}<br/>Rating: {rating}<br/>{address}', max_width=250),
            tooltip=f"Click for details on {name}",
            icon=folium.Icon(icon='cutlery', color="red")
        ).add_to(restaurant_map)

    # Return the map
    return restaurant_map


def load_neighborhood_boundaries(neighborhood_boundaries_path):
    """
    Loads neighborhood boundaries from a file using Geopandas.

    :param neighborhood_boundaries_path: str - Path to the file containing neighborhood boundaries.
    :return: GeoDataFrame - The loaded neighborhood boundaries.
    """
    neighborhoods = gpd.read_file(neighborhood_boundaries_path)
    return neighborhoods