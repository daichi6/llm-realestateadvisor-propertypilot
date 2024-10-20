import pandas as pd
import geopandas as gpd


def load_neighborhood_info(neighborhood_info_path):
    """
    Loads neighborhood information from a CSV file.

    :param neighborhood_info_path: str - Path to the CSV file containing neighborhood information.
    :return: DataFrame - The loaded neighborhood information.
    """
    neighborhood_info = pd.read_csv(neighborhood_info_path)       
    return neighborhood_info


def load_neighborhood_boundaries(neighborhood_boundaries_path):
    """
    This function loads the neighborhood boundaries using geopandas from a shapefile or geojson.

    :param neighborhood_boundaries_path: The path to the file containing neighborhood boundaries.
    :return: A GeoDataFrame containing the neighborhood boundaries.
    """
    neighborhoods = gpd.read_file(neighborhood_boundaries_path)
    return neighborhoods


def get_neighborhood_details(top_properties, neighborhoods_info, neighborhoods_boundaries):
    """
    This function fetches neighborhood information and boundaries for the top properties.

    :param top_properties: DataFrame containing top property details.
    :param neighborhoods_info: DataFrame containing neighborhood information.
    :param neighborhoods_boundaries: GeoDataFrame containing neighborhood boundaries.
    :return: A DataFrame with the neighborhood information and boundaries merged for the top properties.
    """
    top_properties = fetch_neighborhood_info(top_properties, neighborhoods_info)
    top_properties = fetch_neighborhood(top_properties, neighborhoods_boundaries)
    return top_properties