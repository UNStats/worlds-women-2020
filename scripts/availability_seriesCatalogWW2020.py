import utils
import utils2
import json 
from os import listdir
from os.path import isfile, join

# List of series files
datafiles = [f for f in listdir('data/processed/series_csv')]
#print(datafiles)

# Read geographic areas catalog
geo = utils.xlsx2dict('data/external/CL_AREA.xlsx',0)
print(geo[0:3])

# What is the latest year that has passed
current_year = 2020

series_source = []
availability_by_series_and_country = []

for fdx, f in enumerate(datafiles):

    # if fdx != 2:
    #     continue

    if f != 'S_0330.csv':
        continue

    print(f)

    x = utils.tsv2dictlist('data/processed/series_csv/'+ f)

    #-----------------------------------------

    # Replace 'nan' string with None value

    for record in x:
        for k,v in record.items():
            if v == 'nan':
                record[k] = None

    #-----------------------------------------
    

    
    # Ensure column names are uppercase
    x = utils2.col_names_to_uppercase(x)


    print(x[0])

    

    #-----------------------------------
    # Trasformations on individual series
    #-----------------------------------

    # Get list of columns for the current series dataset:
    all_columns = list(x[0].keys())

    #print(f"{all_columns=}")


    # Get the list of "dimension columns" except time (used to identify time series)



    non_TSK_columns = [ 'TIME_PERIOD',
                        'COMMENT_OBS',
                        'LOWER_BOUND',
                        'LOWER_BOUND_MODIFIER',
                        'NATURE',
                        'NATURE_DESC',
                        'OBS_VALUE',
                        'SDG_REGION',
                        'SOURCE_DETAIL',
                        'SOURCE_DETAIL_URL',
                        'SOURCE_YEAR',
                        'TIME_DETAIL',
                        'UNIT_MEASURE',
                        'UNIT_MEASURE_DESC',
                        'UNIT_MULT', 
                        'UNIT_MULT_DESC',
                        'UPPER_BOUND',
                        'UPPER_BOUND_MODIFIER',
                        'VALUE_CATEGORY',
                        'VALUE_CATEGORY_DESC',
                        'REPORTING_TYPE', 
                        'REPORTING_TYPE_DESC',
                        'X',
                        'Y']

    #------
    
    print(f"\n{non_TSK_columns=}")
    
    TSK_columns = [x for x in all_columns if x not in non_TSK_columns]

    print(f"\n{TSK_columns=}")

    #------

    TSK_sub = [x for x in TSK_columns 
                    if x not in ['SERIES', 'SERIES_DESC', 'GEOLEVEL', 'GEOLEVEL_DESC', 'REF_AREA', 'REF_AREA_DESC','STD_ERROR', 'VAR_COEF'] and 
                    not x.endswith('_DESC')]

    print(f"\n{TSK_sub=}")

    #------

    # Obtain the list of Time-series identifiers (composed by TSK dimensions)
    unique_TSK_values = utils.unique_dicts(utils.subdict_list(x, non_TSK_columns, exclude=True))
    print(f"this dataset has {len(unique_TSK_values)} time series.")

    print(f"{unique_TSK_values=}")
    #------

    for u in unique_TSK_values:
    
        TSK_sub_values = []
        TSK_sub_descriptions = []
        for tsk in TSK_sub:
            TSK_sub_values.append(u[tsk])
            TSK_sub_descriptions.append(u[tsk+'_DESC'])
            
        u["TSK_sub_dims"] ='__'.join(TSK_sub)
        u["TSK_sub_id"] ='__'.join(TSK_sub_values)
        u["TSK_sub_desc"] = ', '.join(TSK_sub_descriptions).capitalize()

        

        

    with open('tests/ts_keys.json', 'w') as fp:
        json.dump(unique_TSK_values, fp, indent=2)

        
    # Add empty column in data, which will hold the "isLatestYear" boolean
    new_data = []

    has_duplicates = []

    availability = []

    for idx, ts in enumerate(unique_TSK_values):

        # if idx!=0:
        #     continue

        # print(ts)

        TSK_sub_dims = ts['TSK_sub_dims']
        TSK_sub_id = ts['TSK_sub_id']
        TSK_sub_desc = ts['TSK_sub_desc']

        ts_1 = {k: ts[k] for k in ts.keys() if k not in ['TSK_sub_dims','TSK_sub_id','TSK_sub_desc']}


        # Number of records in time series group:
        x_ts = utils.select_dict(x, ts_1)

        

        print(x_ts)
        N = len(x_ts)
        print(N)


        # Number of unique years in time series group:
        unique_years = []
        for record in utils.unique_dicts(utils.subdict_list(x_ts, ['TIME_PERIOD'])):
            unique_years.append(int(float(record['TIME_PERIOD'])))

        unique_years.sort()

        n = len(unique_years)

        if (N != n):
            has_duplicates.append(ts)

        if(len(has_duplicates)>0):
            print(f"file {f} has_duplicates")

        # Latest year available:
        y_max = max(unique_years)

        # Latest year value:

        keys = x_ts[0].keys()
        # print(f'{keys=}')

        value_y_max = utils.select_dict(x_ts, {'TIME_PERIOD': str(y_max)})[0]['OBS_VALUE']



        # Add ts keys and "isLatestYear"value
        for r in x_ts:
            r['TSK_sub_dims'] = TSK_sub_dims
            r['TSK_sub_id'] = TSK_sub_id
            r['TSK_sub_desc'] = TSK_sub_desc
            if r['TIME_PERIOD'] == str(y_max):
                r['isLatestValue'] = True
            else:
                r['isLatestValue'] = False

        new_data.extend(x_ts)


        #------------------------------------
        # AVAILABILITY CALCULATIONS
        #------------------------------------

        ts_availability = dict(ts)  # or orig.copy()

        ref_area = ts['REF_AREA']
        #print(ref_area)

        geo_info = utils.select_dict(geo, {'REF_AREA': ref_area}, keep=True)
        #print(geo_info[0])

        ts_availability['ISO3'] = geo_info[0]['ISO3']
        ts_availability['X'] = geo_info[0]['X']
        ts_availability['Y'] = geo_info[0]['Y']
        ts_availability['GEOLEVEL_Desc'] = geo_info[0]['GEOLEVEL_Desc']
        ts_availability['GEOLEVEL'] = geo_info[0]['GEOLEVEL']

        ts_availability['UNmember'] = geo_info[0]['UNmember']
        ts_availability['SDG_REGION'] = geo_info[0]['SDG_REGION']

        ts_availability['years'] = unique_years
        ts_availability['min_year'] = min(unique_years)
        ts_availability['max_year'] = max(unique_years)
        ts_availability['N_years'] = len(unique_years)
        ts_availability['N_years_lag5'] = len([y for y in unique_years if y >= current_year - 5])
        ts_availability['N_years_lag10'] = len([y for y in unique_years if y >= current_year - 10])
        
        # Get availability stats: min(years), max (years), Number of years, Number of years after 2015
        availability.append(ts_availability)

    utils.dictList2tsv(new_data, 'tests/' + 'test.csv')

    #------------------------------------------------------
    # Within current series, obtain availability summary for each country
    #------------------------------------------------------

    # Obtain the list of all countries that have data for this series
    countries =  utils.unique_dicts(utils.subdict_list(availability, ['REF_AREA']) )
    countries =  [ c['REF_AREA'] for c in countries]

    #For each country, obtain series availability (with detail for disaggregation)
    for c in countries:
    
        d = dict()

        # if c not in ['8','32']:
        #         continue
        
        # Select TS availability for this country
        data = utils.select_dict(availability, {'REF_AREA': c})

        
        d['SERIES'] = data[0]['SERIES']
        d['SERIES_DESC'] = data[0]['SERIES_DESC']
        d['REF_AREA'] = data[0]['REF_AREA']
        d['REF_AREA_DESC'] = data[0]['REF_AREA_DESC']
        d['ISO3'] = data[0]['ISO3']
        d['X'] = data[0]['X']
        d['Y'] = data[0]['Y']
        d['SDG_REGION'] = data[0]['SDG_REGION']
        d['UNmember'] = data[0]['UNmember']
        d['GEOLEVEL_Desc'] = data[0]['GEOLEVEL_Desc']
        d['GEOLEVEL'] = data[0]['GEOLEVEL']
        if data[0]['UNmember'] or  data[0]['REF_AREA'] in ['275','336']:
            d['Select195'] = True
        else:
            d['Select195'] = False
        d['years'] = [] 
        for ts in data:
            d['years'].extend(ts['years'])
        d['years'] = list(set(d['years']))

        d['max_year'] = max([ ts['max_year'] for ts in data ])
        d['min_year'] = min([ ts['min_year'] for ts in data ])
        d['data_points'] = sum([ ts['N_years'] for ts in data ])
        d['data_points_lag5'] = sum([ ts['N_years_lag5'] for ts in data ])
        d['data_points_lag10'] = sum([ ts['N_years_lag10'] for ts in data ])

        #--------

    
        availability_by_series_and_country.append(d)
    
    utils.dictList2tsv(availability, 'tests/availability_ts_'+ f)