"""
Embodied energy and related grey emissions model algorithm

J. Fonseca  script development          26.08.15
D. Thomas   formatting and cleaning
D. Thomas   integration in toolbox
J. Fonseca  new development             13.04.16
M. Mosteiro fixed calculation errors    07.11.16
"""
from __future__ import division

import numpy as np
import pandas as pd
from cea.utilities.dbfreader import dbf2df
from geopandas import GeoDataFrame as Gdf
import cea.globalvar
import cea.inputlocator

__author__ = "Jimeno A. Fonseca"
__copyright__ = "Copyright 2015, Architecture and Building Systems - ETH Zurich"
__credits__ = ["Jimeno A. Fonseca"]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Daren Thomas"
__email__ = "cea@arch.ethz.ch"
__status__ = "Production"


def lca_embodied(year_to_calculate, locator, gv):
    """
    Algorithm to calculate the embodied emissions and non-renewable primary energy of buildings according to the method
    of [Fonseca et al., 2015] and [Thoma et al., 2014]. The calculation method assumes a 60 year payoff for the embodied
    energy and emissions of a building, after which both values become zero.

    The results are provided in total as well as per square meter:

    - embodied non-renewable primary energy: E_nre_pen_GJ and E_nre_pen_MJm2
    - embodied greenhouse gas emissions: E_ghg_ton and E_ghg_kgm2

    As part of the algorithm, the following files are read from InputLocator:

    - architecture.shp: shapefile with the architecture of each building
        locator.get_building_architecture()
    - occupancy.shp: shapefile with the occupancy types of each building
        locator.get_building_occupancy()
    - age.shp: shapefile with the age and retrofit date of each building
        locator.get_building_age()
    - zone.shp: shapefile with the geometry of each building in the zone of study
        locator.get_building_geometry()
    - Archetypes_properties: csv file with the database of archetypes including embodied energy and emissions
        locator.get_archetypes_properties()

    As a result, the following file is created:

    - Total_LCA_embodied: .csv
        csv file of yearly primary energy and grey emissions per building stored in locator.get_lca_embodied()

    :param year_to_calculate:  year between 1900 and 2100 indicating when embodied energy is evaluated
        to account for emissions already offset from building construction and retrofits more than 60 years ago.
    :type year_to_calculate: int
    :param locator: an instance of InputLocator set to the scenario
    :type locator: InputLocator
    :returns: This function does not return anything
    :rtype: NoneType

    .. [Fonseca et al., 2015] Fonseca et al. (2015) "Assessing the environmental impact of future urban developments at
        neighborhood scale." CISBAT 2015.
    .. [Thoma et al., 2014] Thoma et al. (2014). "Estimation of base-values for grey energy, primary energy, global
        warming potential (GWP 100A) and Umweltbelastungspunkte (UBP 2006) for Swiss constructions from before 1920
        until today." CUI 2014.


    Files read / written from InputLocator:

    get_building_architecture
    get_building_occupancy
    get_building_age
    get_building_geometry
    get_archetypes_embodied_energy
    get_archetypes_embodied_emissions

    path_LCA_embodied_energy:
        path to database of archetypes embodied energy file
        Archetypes_embodied_energy.csv
    path_LCA_embodied_emissions:
        path to database of archetypes grey emissions file
        Archetypes_embodied_emissions.csv
    path_age_shp: string
        path to building_age.shp
    path_occupancy_shp:
        path to building_occupancyshp
    path_geometry_shp:
        path to building_geometrys.hp
    path_architecture_shp:
        path to building_architecture.shp
    path_results : string
        path to demand results folder emissions
    """

    # local variables
    architecture_df = dbf2df(locator.get_building_architecture())
    prop_occupancy_df = dbf2df(locator.get_building_occupancy())
    occupancy_df = pd.DataFrame(prop_occupancy_df.loc[:, (prop_occupancy_df != 0).any(axis=0)])
    age_df = dbf2df(locator.get_building_age())
    geometry_df = Gdf.from_file(locator.get_building_geometry())
    geometry_df['footprint'] = geometry_df.area
    geometry_df['perimeter'] = geometry_df.length
    geometry_df = geometry_df.drop('geometry', axis=1)

    # get list of uses
    list_uses = list(occupancy_df.drop({'PFloor', 'Name'}, axis=1).columns)

    # define main use:
    occupancy_df['mainuse'] = calc_mainuse(occupancy_df, list_uses)

    # DataFrame with joined data for all categories
    cat_df = occupancy_df.merge(age_df, on='Name').merge(geometry_df, on='Name').merge(architecture_df, on='Name')

    # calculate building geometry
    ## total window area
    cat_df['windows_ag'] = cat_df['win_wall'] * cat_df['perimeter'] * (cat_df['height_ag'] * cat_df['PFloor'])
    ## wall area above ground
    cat_df['area_walls_ext_ag'] = cat_df['perimeter'] * (cat_df['height_ag'] * cat_df['PFloor']) - cat_df['windows_ag']
    ## wall area below ground
    cat_df['area_walls_ext_bg'] = cat_df['perimeter'] * cat_df['height_bg']
    ## floor area above ground
    cat_df['floor_area_ag'] = cat_df['footprint'] * cat_df['floors_ag']
    ## floor area below ground
    cat_df['floor_area_bg'] = cat_df['footprint'] * cat_df['floors_bg']
    ## total floor area
    cat_df['total_area'] = cat_df['floor_area_ag'] + cat_df['floor_area_bg']

    # get categories for each year of construction/retrofit
    ## each building component gets categorized according to its occupancy type, construction year and retrofit year
    ## e.g., for an office building built in 1975, cat_df['cat_built'] = 'OFFICE3'
    ## e.g., for an office building with windows renovated in 1975, cat_df['cat_windows'] = 'OFFICE9'
    cat_df['cat_built'] = cat_df.apply(lambda x: calc_category_construction(x['mainuse'], x['built']), axis=1)
    retro_cat = ['envelope', 'roof', 'windows', 'partitions', 'basement', 'HVAC']
    for cat in retro_cat:
        cat_df['cat_' + cat] = cat_df.apply(lambda x: calc_category_retrofit(x['mainuse'], x[cat]), axis=1)

    # calculate contributions to embodied energy and emissions
    ## calculated by multiplying the area of the given component by the energy and emissions per square meter for the
    ## given category according to the data in the archetype database
    result_energy = calculate_contributions('EMBODIED_ENERGY', cat_df, gv, locator, year_to_calculate,
                                            total_column='GEN_GJ', specific_column='GEN_MJm2')
    result_emissions = calculate_contributions('EMBODIED_EMISSIONS', cat_df, gv, locator, year_to_calculate,
                                               total_column='CO2_ton', specific_column='CO2_kgm2')

    # export the results for embodied emissions (E_ghg_) and non-renewable primary energy (E_nre_pen_) for each
    # building, both total (in t CO2-eq. and GJ) and per square meter (in kg CO2-eq./m2 and MJ/m2)
    fields_to_plot = ['Name', 'GFA_m2', 'E_nre_pen_GJ', 'E_nre_pen_MJm2', 'E_ghg_ton', 'E_ghg_kgm2']
    pd.DataFrame(
        {'Name': result_energy.Name, 'E_nre_pen_GJ': result_energy.GEN_GJ, 'E_nre_pen_MJm2': result_energy.GEN_MJm2,
         'E_ghg_ton': result_emissions.CO2_ton, 'E_ghg_kgm2': result_emissions.CO2_kgm2,
         'GFA_m2': result_energy.total_area}).to_csv(locator.get_lca_embodied(),
                                                     columns=fields_to_plot, index=False, float_format='%.2f')
    print('done!')


def calculate_contributions(archetype, cat_df, gv, locator, year_to_calculate, total_column, specific_column):
    """
    Calculate the embodied energy/emissions for each building based on their construction year, and the area and 
    renovation year of each building component.

    :param archetype: String that defines whether the 'EMBODIED_ENERGY' or 'EMBODIED_EMISSIONS' are being calculated.
    :type archetype: str
    :param cat_df: DataFrame with joined data of all categories for each building, that is: occupancy, age, geometry,
        architecture, building component area, construction category and renovation category for each building component
    :type cat_df: DataFrame
    :param gv: an instance of GlobalVariables with the constants to be used (like `list_uses` etc.)
    :type gv: GlobalVariables
    :param locator: an InputLocator instance set to the scenario to work on
    :type locator: InputLocator
    :param year_to_calculate: year in which the calculation is done; since the embodied energy and emissions are
        calculated over 60 years, if the year of calculation is more than 60 years after construction, the results
        will be 0
    :type year_to_calculate: int
    :param total_column: label for the column with the total results (e.g., 'GEN_GJ')
    :type total_column: str
    :param specific_column: label for the column with the results per square meter (e.g., 'GEN_MJm2')
    :type specific_column: str

    :return result: DataFrame with the calculation results (i.e., the total and specific embodied energy or emisisons
        for each building)
    :rtype result: DataFrame
    """

    # get archetype properties from the database
    database_df = pd.read_excel(locator.get_archetypes_properties(), archetype)
    
    # merge databases according to category
    built_df = cat_df.merge(database_df, left_on='cat_built', right_on='Code')
    envelope_df = cat_df.merge(database_df, left_on='cat_envelope', right_on='Code')
    roof_df = cat_df.merge(database_df, left_on='cat_roof', right_on='Code')
    windows_df = cat_df.merge(database_df, left_on='cat_windows', right_on='Code')
    partitions_df = cat_df.merge(database_df, left_on='cat_partitions', right_on='Code')
    basement_df = cat_df.merge(database_df, left_on='cat_basement', right_on='Code')
    HVAC_df = cat_df.merge(database_df, left_on='cat_HVAC', right_on='Code')
    
    # calculate the embodied energy/emissions due to construction
    # these include: external walls, roof, windows, interior floors, partitions, HVAC systems, and excavation
    ## calculate how many years before the calculation year the building was built in
    built_df['delta_year'] = year_to_calculate - built_df['built']
    ## if it was built more than 60 years before, the embodied energy/emissions have been "paid off" and are set to 0
    built_df['confirm'] = built_df.apply(lambda x: calc_if_existing(x['delta_year'], gv.sl_materials), axis=1)
    ## if it was built less than 60 years before, the contribution from each building component is calculated
    built_df['contrib'] = (((built_df['Wall_ext_ag'] * built_df['area_walls_ext_ag']) +
                            (built_df['Roof'] * built_df['footprint']) +
                            (built_df['windows_ag'] * built_df['Win_ext']) +
                            (built_df['floor_area_ag'] * built_df['Floor_int'] +
                             built_df['floor_area_ag'] * built_df['Wall_int_sup'] * gv.fwratio +
                             built_df['footprint'] * built_df['Wall_int_nosup'] * gv.fwratio) +
                            (basement_df['footprint'] * basement_df['Floor_g'] +
                             basement_df['Wall_ext_bg'] * basement_df['area_walls_ext_bg']) +
                            (built_df['footprint'] * built_df['Excavation'])) / gv.sl_materials + \
                           ((HVAC_df['floor_area_ag'] + HVAC_df['footprint']) * HVAC_df[
                               'Services']) / gv.sl_services) * built_df['confirm']
    
    # calculate the embodied energy/emissions due to retrofits
    # if a component was retrofitted more than 60 years before, its contribution has been "paid off" and is set to 0
    ## contributions due to envelope retrofit
    envelope_df['delta_year'] = year_to_calculate - envelope_df['envelope']
    envelope_df['confirm'] = envelope_df.apply(lambda x: calc_if_existing(x['delta_year'], gv.sl_materials), axis=1)
    envelope_df['contrib'] = (envelope_df['Wall_ext_ag'] * envelope_df['area_walls_ext_ag']) * envelope_df[
        'confirm'] / (gv.sl_materials)
    ## contributions due to roof retrofit
    roof_df['delta_year'] = year_to_calculate - roof_df['roof']
    roof_df['confirm'] = roof_df.apply(lambda x: calc_if_existing(x['delta_year'], gv.sl_materials), axis=1)
    roof_df['contrib'] = roof_df['Roof'] * roof_df['footprint'] * roof_df['confirm'] / gv.sl_materials
    ## contributions due to windows retrofit
    windows_df['delta_year'] = year_to_calculate - windows_df['windows']
    windows_df['confirm'] = windows_df.apply(lambda x: calc_if_existing(x['delta_year'], gv.sl_materials), axis=1)
    windows_df['contrib'] = windows_df['windows_ag'] * windows_df['Win_ext'] * windows_df[
        'confirm'] / gv.sl_materials
    ## contributions due to partitions retrofit
    partitions_df['delta_year'] = year_to_calculate - partitions_df['partitions']
    partitions_df['confirm'] = partitions_df.apply(lambda x: calc_if_existing(x['delta_year'], gv.sl_materials),
                                                   axis=1)
    partitions_df['contrib'] = (partitions_df['floor_area_ag'] * partitions_df['Floor_int'] +
                                partitions_df['floor_area_ag'] * partitions_df['Wall_int_sup'] * gv.fwratio +
                                partitions_df['footprint'] * partitions_df['Wall_int_nosup'] * gv.fwratio) * \
                               partitions_df['confirm'] / gv.sl_materials
    ## contributions due to basement_df
    basement_df['delta_year'] = year_to_calculate - basement_df['basement']
    basement_df['confirm'] = basement_df.apply(lambda x: calc_if_existing(x['delta_year'], gv.sl_materials), axis=1)
    basement_df['contrib'] = ((basement_df['footprint'] * basement_df['Floor_g'] +
                               basement_df['Wall_ext_bg'] * basement_df['area_walls_ext_bg'])
                              * basement_df['confirm'] / gv.sl_materials)
    ## contributions due to HVAC_df
    HVAC_df['delta_year'] = year_to_calculate - HVAC_df['HVAC']
    HVAC_df['confirm'] = HVAC_df.apply(lambda x: calc_if_existing(x['delta_year'], gv.sl_services), axis=1)
    HVAC_df['contrib'] = ((HVAC_df['floor_area_ag'] + HVAC_df['footprint']) * HVAC_df['Services']) * HVAC_df[
        'confirm'] / gv.sl_services

    # the total embodied energy/emissions are calculated as a sum of the contributions from construction and retrofits
    built_df[total_column] = (HVAC_df['contrib'] + basement_df['contrib'] + partitions_df['contrib']
                              + built_df['contrib'] + roof_df['contrib'] + envelope_df['contrib']
                              + windows_df['contrib']) / 1000
    built_df[specific_column] = built_df[total_column] * 1000 / built_df['total_area']

    # the total and specific embodied energy/emissions are returned 
    result = built_df[['Name', total_column, specific_column, 'total_area']]

    return result

def calc_if_existing(x, y):
    """
    Function to verify if one value is greater than or equal to another (then return 1) or not (return 0). This is used
    to verify whether a building's construction or retrofits happened more than 60 years before the year to calculate.
    Since the embodied energy and emissions are calculated over 60 years, if the year of calculation is more than 60 
    years after construction, the results will be 0.
    
    :param x: Number of years since construction/retrofit
    :type x: long
    :param y: Number of years over which the embodied energy/emissions calculation is carried out (i.e., 60)
    :type y: int

    :return value: 1 if x <= y; 0 otherwise
    :rtype value: int

    """

    if x <= y:
        return 1
    else:
        return 0

def calc_category_construction(a, x):
    """
    Function to assign a building its construction category based on its occupancy type and year of construction.
    e.g., an office building built in 1975 will be assigned the category 'OFFICE3'.
    These categories are then used to look up the reference values in the archetypes database.

    :param a: Main use of the building being categorized (e.g., 'OFFICE')
    :type a: str
    :param x: Year of construction of the building
    :type x: long

    :return category: string with the building's construction category (e.g., 'OFFICE3')
    :rtype category: str

    """

    # for each range of construction years, the building's occupancy + a value of 1 to 6 is assigned
    if 0 <= x <= 1920:
        result = '1'
    elif 1920 < x <= 1970:
        result = '2'
    elif 1970 < x <= 1980:
        result = '3'
    elif 1980 < x <= 2000:
        result = '4'
    elif 2000 < x <= 2020:
        result = '5'
    else:
        result = '6'

    category = a + result

    return category

def calc_category_retrofit(a, y):
    """
    Function to assign a building component its retrofit category based on its occupancy type and year of renovation.
    e.g., a window in an office building renovated in 1975 will be assigned the category 'OFFICE9'.
    These categories are then used to look up the reference values in the archetypes database.

    :param a: Main use of the building being categorized (e.g., 'OFFICE')
    :type a: str
    :param y: Year of renovation of the building component
    :type y: long

    :return category: string with the building component's renovation category (e.g., 'OFFICE9')
    :rtype category: str

    """

    # for each range of construction years, the building's occupancy + a value of 1 to 6 is assigned
    if 0 <= y <= 1920:
        result = '7'
    elif 1920 < y <= 1970:
        result = '8'
    elif 1970 < y <= 1980:
        result = '9'
    elif 1980 < y <= 2000:
        result = '10'
    elif 2000 < y <= 2020:
        result = '11'
    else:
        result = '12'

    category = a + result

    return category

def calc_mainuse(uses_df, uses):
    """
    Calculate a building's main use
    :param uses_df: DataFrame containing the share of each building that corresponds to each occupancy type
    :type uses_df: DataFrame
    :param uses: list of building uses actually available in the area
    :type uses: list

    :return mainuse: array containing each building's main occupancy
    :rtype mainuse: ndarray

    """

    databaseclean = uses_df[uses].transpose()
    array_min = np.array(databaseclean[databaseclean[:] > 0].idxmin(skipna=True), dtype='S10')
    array_max = np.array(databaseclean[databaseclean[:] > 0].idxmax(skipna=True), dtype='S10')
    mainuse = np.array(map(calc_comparison, array_min, array_max))

    return mainuse

def calc_comparison(array_min, array_max):
    """
    This function reads the least and most common occupancy types in each building and, if the most common occupancy
    type is 'PARKING', reassigns this building's occupancy type to its least common.

    :param array_min: array containing the occupancy type that takes up the least space (>0) for each building
    :type array_min: ndarray
    :param array_max: array containing each building's predominant occupancy type
    :type array_max: ndarray

    :return array_max: array containing the predominant occupancy type in each building after clean up of any 'DEPO' values
    :rtype array_max: ndarray

    """

    if array_max == 'PARKING':
        if array_min != 'PARKING':
            array_max = array_min
    return array_max


def run_as_script(scenario_path=None, year_to_calculate=2050):
    gv = cea.globalvar.GlobalVariables()
    if not scenario_path:
        scenario_path = gv.scenario_reference
    locator = cea.inputlocator.InputLocator(scenario_path=scenario_path)
    lca_embodied(locator=locator, year_to_calculate=year_to_calculate, gv=gv)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--scenario', help='Path to the scenario folder')
    parser.add_argument('-y', '--year', default=2020, help='Year to calculate')
    args = parser.parse_args()
    run_as_script(scenario_path=args.scenario, year_to_calculate=args.year)
