import os
import utils
import time
import json
import math
import string

# ----------------------------------------------
# This script reads the json file with the merged
# data ("02_AllData.json") and fixes coding issues
# identified during review of code lists
# -----------------------------------------------``


def fix_dimension(dimension, code_fix, description_fix):
    if dimension in record.keys():

        for k, v in code_fix.items():
            if record[dimension + '_DESC'] == v:
                record[dimension] = k

        for k, v in description_fix.items():
            if record[dimension] == k:
                record[dimension + '_DESC'] = v

# Read the data


data = utils.open_json('data/02_AllData.json')
print(data[0])

series_catalog = utils.tsv2dictlist('data/source/SeriesCatalog.txt')
print(series_catalog[0])

update_SeriesNames = utils.tsv2dictlist('data/source/update_SeriesNames.txt')

check = []

for record in data:

    series_desc = record['SERIES_DESC']

    # Fix 1: Fix series names:

    series_name_fix = utils.select_dict(
        update_SeriesNames, {'SERIES_DESC_OLD': series_desc})

    if len(series_name_fix) > 0:
        record['SERIES_DESC'] = update_SeriesNames[0]['SERIES_DESC_NEW']

    # Fix 2: Add series code:

    series_data = utils.select_dict(
        series_catalog, {'SERIES_DESC': series_desc})

    if len(series_data) > 1:
        print(
            f"The series {record['SERIES_DESC']} appears multiple times in the series catalog")
        break
    elif len(series_data) == 0:
        check.append(record['SERIES_DESC'])
        check = list(set(check))
    else:
        record['SERIES'] = series_data[0]['SERIES']

    # Fix 3: Fix AGE coding:

    code_fix = dict()

    description_fix = {
        '_T': 'All age ranges or no breakdown by age',
        'Y_GE15': '15 years old and over',
        'Y_GE65': '65 years old and over',
        'Y_GE80': '80 old and over',
        'Y15T25': '15 to 25 years',
        'Y50T54': '50 to 54 years old',
        'Y55T59': '55 to 59 years old',
        'Y60T64': '60 to 64 years old',
        'Y65T69': '65 to 69 years old',
        'Y70T74': '70 to 74 years old',
        'Y75T79': '75 to 79 years old',
        'Y80T84': '80 to 84 years old',
        'Y85T89': '85 to 89 years old'
    }

    fix_dimension('AGE', code_fix, description_fix)

    # Fix 4: Fix COD coding:

    code_fix = {
        '800': 'Diabetes',
    }

    description_fix = {
        '800': 'Diabetes mellitus'
    }

    fix_dimension('COD', code_fix, description_fix)

    # Fix 5: Fix EDUCATION_LEV coding:

    code_fix = dict()

    description_fix = {
        'ISCED11_1':	'Primary education',
        'ISCED11_2':	'Lower secondary education',
        'ISCED11_3':	'Upper secondary education',
        'ISCED11A_0_G23': 'Some primary education, grades 2 or 3'
    }

    fix_dimension('EDUCATION_LEV', code_fix, description_fix)

    # Fix 6: Fix ETHNICITY coding:

    code_fix = {
        'WH': 'White',
        'BL_BR': 'Black or brown'
    }

    description_fix = {
        '_T': 'Total or no breakdown by ethnicity'
    }

    fix_dimension('ETHNICITY', code_fix, description_fix)

    # Fix 7: Fix FREQ coding:

    if 'FREQ' in record.keys():

        if record['FREQ'] == 'S':
            record['FREQ'] = 'A'
            record['FREQ_DESC'] = 'Annual'

    # Fix 8: Fix GEOLEVEL coding:

    code_fix = {
        '4'	: 'National'
    }

    description_fix = {
        '4': 'Country or Area',
        '5': 'Sub-national'
    }

    fix_dimension('GEOLEVEL', code_fix, description_fix)

    # Fix 9: Fix HOUSEHOLD_TYPE coding:

    code_fix = {
        '_T': 'Total'
    }

    description_fix = {
        '2': 'Couples without children',
        '3': 'Couples with children',
        '4': 'Lone parents'
    }

    fix_dimension('HOUSEHOLD_TYPE', code_fix, description_fix)

    # Fix 10: Fix INCOME_WEALTH_QUANTILE coding:

    code_fix = dict()

    description_fix = {
        'Q1': 'Quintile 1 (poorest)',
        'Q2': 'Quintile 2 (second poorest)',
        'Q3': 'Quintile 3 (middle)',
        'Q4': 'Quintile 4 (second richest)',
        'Q5': 'Quintile 5 (richest)'
    }

    fix_dimension('INCOME_WEALTH_QUANTILE', code_fix, description_fix)

    # Fix 11: Fix MARITAL_STATUS coding:

    code_fix = {
        '_T': 'Total'
    }

    description_fix = dict()

    fix_dimension('MARITAL_STATUS', code_fix, description_fix)

    # Fix 12: Fix MINISTER_PORTFOLIO coding:

    code_fix = dict()

    description_fix = {
        '7': 'Housing and Urban Affairs',
        '20': 'Justice'
    }

    fix_dimension('MINISTER_PORTFOLIO', code_fix, description_fix)

    # Fix 13: Fix NATURE coding:

    code_fix = dict()

    description_fix = {
        'M': 'Modeled'
    }

    fix_dimension('NATURE', code_fix, description_fix)

    # Fix 14: Fix OCCUPATION coding:

    code_fix = {
        'ISCO08_101': 'Commissioned armed forces officers',
        'ISCO08_102': 'Non-commissioned armed forces officers',
        'ISCO08_103': 'Armed forces occupations, other ranks'
    }

    description_fix = dict()

    fix_dimension('OCCUPATION', code_fix, description_fix)

    # Fix 15: Fix REF_AREA coding:

    code_fix = dict()

    description_fix = {
        "1": "World",
        "2": "Africa",
        "4": "Afghanistan",
        "5": "South America",
        "8": "Albania",
        "9": "Oceania",
        "11": "Western Africa",
        "12": "Algeria",
        "13": "Central America",
        "14": "Eastern Africa",
        "15": "Northern Africa",
        "16": "American Samoa",
        "17": "Middle Africa",
        "18": "Southern Africa",
        "19": "Americas",
        "20": "Andorra",
        "21": "Northern America",
        "24": "Angola",
        "28": "Antigua and Barbuda",
        "29": "Caribbean",
        "30": "Eastern Asia",
        "31": "Azerbaijan",
        "32": "Argentina",
        "34": "Southern Asia",
        "35": "South-Eastern Asia",
        "36": "Australia",
        "39": "Southern Europe",
        "40": "Austria",
        "44": "Bahamas",
        "48": "Bahrain",
        "50": "Bangladesh",
        "51": "Armenia",
        "52": "Barbados",
        "53": "Australia and New Zealand",
        "54": "Melanesia",
        "56": "Belgium",
        "57": "Micronesia",
        "60": "Bermuda",
        "61": "Polynesia",
        "62": "Central and Southern Asia",
        "64": "Bhutan",
        "68": "Bolivia (Plurinational State of)",
        "70": "Bosnia and Herzegovina",
        "72": "Botswana",
        "76": "Brazil",
        "84": "Belize",
        "90": "Solomon Islands",
        "92": "British Virgin Islands",
        "96": "Brunei Darussalam",
        "100": "Bulgaria",
        "104": "Myanmar",
        "108": "Burundi",
        "112": "Belarus",
        "116": "Cambodia",
        "120": "Cameroon",
        "124": "Canada",
        "132": "Cabo Verde",
        "136": "Cayman Islands",
        "140": "Central African Republic",
        "142": "Asia",
        "143": "Central Asia",
        "144": "Sri Lanka",
        "145": "Western Asia",
        "148": "Chad",
        "150": "Europe",
        "151": "Eastern Europe",
        "152": "Chile",
        "154": "Northern Europe",
        "155": "Western Europe",
        "156": "China",
        "158": "China, Taiwan Province of China",
        "170": "Colombia",
        "174": "Comoros",
        "175": "Mayotte",
        "178": "Congo",
        "180": "Democratic Republic of the Congo",
        "184": "Cook Islands",
        "188": "Costa Rica",
        "191": "Croatia",
        "192": "Cuba",
        "196": "Cyprus",
        "199": "Least Developed Countries (LDCs)",
        "202": "Sub-Saharan Africa",
        "203": "Czechia",
        "204": "Benin",
        "208": "Denmark",
        "212": "Dominica",
        "214": "Dominican Republic",
        "218": "Ecuador",
        "222": "El Salvador",
        "226": "Equatorial Guinea",
        "231": "Ethiopia",
        "232": "Eritrea",
        "233": "Estonia",
        "234": "Faroe Islands",
        "238": "Falkland Islands (Malvinas)",
        "242": "Fiji",
        "246": "Finland",
        "250": "France",
        "254": "French Guiana",
        "258": "French Polynesia",
        "262": "Djibouti",
        "266": "Gabon",
        "268": "Georgia",
        "270": "Gambia",
        "275": "State of Palestine",
        "276": "Germany",
        "288": "Ghana",
        "292": "Gibraltar",
        "296": "Kiribati",
        "300": "Greece",
        "304": "Greenland",
        "308": "Grenada",
        "312": "Guadeloupe",
        "316": "Guam",
        "320": "Guatemala",
        "324": "Guinea",
        "328": "Guyana",
        "332": "Haiti",
        "336": "Holy See",
        "340": "Honduras",
        "344": "China, Hong Kong Special Administrative Region",
        "348": "Hungary",
        "352": "Iceland",
        "356": "India",
        "360": "Indonesia",
        "364": "Iran (Islamic Republic of)",
        "368": "Iraq",
        "372": "Ireland",
        "376": "Israel",
        "380": "Italy",
        "384": "Côte d'Ivoire",
        "388": "Jamaica",
        "392": "Japan",
        "398": "Kazakhstan",
        "400": "Jordan",
        "404": "Kenya",
        "408": "Democratic People's Republic of Korea",
        "410": "Republic of Korea",
        "414": "Kuwait",
        "417": "Kyrgyzstan",
        "418": "Lao People's Democratic Republic",
        "419": "Latin America and the Caribbean",
        "420": "Latin America",
        "422": "Lebanon",
        "426": "Lesotho",
        "428": "Latvia",
        "430": "Liberia",
        "432": "Landlocked developing countries (LLDCs)",
        "434": "Libya",
        "438": "Liechtenstein",
        "440": "Lithuania",
        "442": "Luxembourg",
        "446": "China, Macao Special Administrative Region",
        "450": "Madagascar",
        "454": "Malawi",
        "458": "Malaysia",
        "462": "Maldives",
        "466": "Mali",
        "470": "Malta",
        "474": "Martinique",
        "478": "Mauritania",
        "480": "Mauritius",
        "484": "Mexico",
        "492": "Monaco",
        "496": "Mongolia",
        "498": "Republic of Moldova",
        "499": "Montenegro",
        "500": "Montserrat",
        "504": "Morocco",
        "508": "Mozambique",
        "512": "Oman",
        "513": "Europe and Northern America",
        "514": "​Developed",
        "515": "​Developing",
        "516": "Namibia",
        "520": "Nauru",
        "524": "Nepal",
        "528": "Netherlands",
        "531": "Curaçao",
        "533": "Aruba",
        "534": "Sint Maarten (Dutch part)",
        "540": "New Caledonia",
        "543": "Oceania (exc. Australia and New Zealand)",
        "548": "Vanuatu",
        "554": "New Zealand",
        "558": "Nicaragua",
        "562": "Niger",
        "566": "Nigeria",
        "570": "Niue",
        "578": "Norway",
        "580": "Northern Mariana Islands",
        "583": "Micronesia (Federated States of)",
        "584": "Marshall Islands",
        "585": "Palau",
        "586": "Pakistan",
        "591": "Panama",
        "598": "Papua New Guinea",
        "600": "Paraguay",
        "604": "Peru",
        "608": "Philippines",
        "616": "Poland",
        "620": "Portugal",
        "624": "Guinea-Bissau",
        "626": "Timor-Leste",
        "630": "Puerto Rico",
        "634": "Qatar",
        "638": "Réunion",
        "642": "Romania",
        "643": "Russian Federation",
        "646": "Rwanda",
        "654": "Saint Helena",
        "659": "Saint Kitts and Nevis",
        "660": "Anguilla",
        "662": "Saint Lucia",
        "666": "Saint Pierre and Miquelon",
        "670": "Saint Vincent and the Grenadines",
        "674": "San Marino",
        "678": "Sao Tome and Principe",
        "682": "Saudi Arabia",
        "686": "Senegal",
        "688": "Serbia",
        "690": "Seychelles",
        "694": "Sierra Leone",
        "702": "Singapore",
        "703": "Slovakia",
        "704": "Viet Nam",
        "705": "Slovenia",
        "706": "Somalia",
        "710": "South Africa",
        "716": "Zimbabwe",
        "722": "Small island developing States (SIDS)",
        "724": "Spain",
        "728": "South Sudan",
        "729": "Sudan",
        "740": "Suriname",
        "747": "Northern Africa and Western Asia",
        "748": "Eswatini",
        "752": "Sweden",
        "753": "Eastern and South-Eastern Asia",
        "756": "Switzerland",
        "760": "Syrian Arab Republic",
        "762": "Tajikistan",
        "764": "Thailand",
        "768": "Togo",
        "772": "Tokelau",
        "776": "Tonga",
        "780": "Trinidad and Tobago",
        "784": "United Arab Emirates",
        "788": "Tunisia",
        "792": "Turkey",
        "795": "Turkmenistan",
        "796": "Turks and Caicos Islands",
        "798": "Tuvalu",
        "800": "Uganda",
        "804": "Ukraine",
        "807": "North Macedonia",
        "818": "Egypt",
        "826": "United Kingdom",
        "830": "Channel Islands",
        "833": "Isle of Man",
        "834": "United Republic of Tanzania",
        "840": "United States of America",
        "850": "United States Virgin Islands",
        "854": "Burkina Faso",
        "858": "Uruguay",
        "860": "Uzbekistan",
        "862": "Venezuela (Bolivarian Republic of)",
        "876": "Wallis and Futuna Islands",
        "882": "Samoa",
        "887": "Yemen",
        "894": "Zambia",
        "910": "High income economies (WB)",
        "911": "Low income economies (WB)",
        "912": "Lower middle economies (WB)",
        "914": "Upper middle economies (WB)"
    }

    fix_dimension('REF_AREA', code_fix, description_fix)

    # Fix 16: Fix SEX coding:

    code_fix = {
        'M': 'Male',
        'F': 'Female'
    }

    description_fix = {
        '_T': 'Both sexes or no breakdown by sex',
        'M': 'Male',
        'F': 'Female'
    }

    fix_dimension('SEX', code_fix, description_fix)

    # Fix 17: Fix UNIT_MULT coding:

    code_fix = {
        '0': 'Units'
    }

    description_fix = {
        '0': 'Units'
    }

    fix_dimension('UNIT_MULT', code_fix, description_fix)


with open("data/02_AllData.json", "w") as write_file:
    json.dump(data, write_file, indent=4)

print("The following series are not in the series catalog:")
print(check)
