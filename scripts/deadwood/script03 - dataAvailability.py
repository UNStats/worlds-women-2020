import os
import utils
import time
import csv
import statistics

# -----------------------------------
# Add details for reference areas
# -----------------------------------

series_cat = []

for file in os.listdir('data/clean/series/'):

    if file != 'NV__IND_0550__S_0720.csv':
        continue

    list_ids = file.split('__')
    theme_id = list_ids.pop(0)
    indicator_id = list_ids.pop(0)
    list_ids = list_ids[0].split('.')
    series_id = list_ids.pop(0)

    print(f"Theme: {theme_id}")
    print(f"Indicator: {indicator_id}")
    print(f"Series: {series_id}")

    x = []
    with open('data/clean/series/' + file, mode="r", encoding="utf-8-sig") as f:
        for line in csv.DictReader(f):
            x.append(dict(line))

    print(f"cols = {x[0].keys()}")

    x_series = utils.subdict_list(
        x, ['THEME_ID', 'NARRATIVE_ID', 'NARRATIVE_DESC', 'SERIES', 'SERIES_DESC'])[0]

    print(f'x_series: {x_series}')

    # -------------------

    x_regions = utils.select_dict(x, {'GEOLEVEL': '0'})
    x_regions.extend(utils.select_dict(x, {'GEOLEVEL': '1'}))
    x_regions.extend(utils.select_dict(x, {'GEOLEVEL': '2'}))
    x_regions.extend(utils.select_dict(x, {'GEOLEVEL': '3'}))

    # Number of regions:
    regions = utils.dictItem2List(x_regions, 'REF_AREA', unique=True)
    n_regions = len(regions)
    print(f'regions: {regions}')

    # Years for which data is available at the region level:
    years_regions = utils.dictItem2List(
        x_regions, 'TIME_PERIOD', unique=True, sort_list=True)
    n_years_regions = len(years_regions)
    print(f'years_regions: {years_regions}')

    # --------------------------------------------------------

    x_countries = utils.select_dict(x, {'GEOLEVEL': '4'})

    # Number of countries:
    countries = utils.dictItem2List(x_countries, 'REF_AREA', unique=True)
    n_countries = len(countries)
    print(f'countries: {countries}')

    # Years for which data is available at the region level:
    years_countries = utils.dictItem2List(
        x_countries, 'TIME_PERIOD', unique=True, sort_list=True)
    n_years_countries = len(years_countries)
    print(f'years_countries: {years_countries}')

    # --------------------------------------------------------

    x_subnational = utils.select_dict(x, {'GEOLEVEL': '5'})

    # Number of subnational areas:
    subnational_areas = utils.dictItem2List(
        x_subnational, 'REF_AREA', unique=True)
    n_subnational = len(subnational_areas)
    print(f'subnational_areas: {subnational_areas}')

    # Years for which data is available at the region level:
    years_subnational = utils.dictItem2List(
        x_subnational, 'TIME_PERIOD', unique=True, sort_list=True)
    n_years_subnational = len(years_subnational)
    print(f'years_subnational: {years_subnational}')

    # utils.dictList2tsv(data, 'data/processed/' + theme_id +
    #                    '__' + indicator_id + '__' + series_id + '.txt')
