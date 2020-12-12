import requests
import pandas as pd

# Pulls data from website and saves json file for reference.
def get_data():
    html = requests.get("https://www.gtabase.com/media/com_jamegafilter/en_gb/1.json?1605369289")
    return html


# json file is loaded into dataframe and transposed.
json = get_data()
vehicle_df_initial = pd.read_json(json.content)

vehicle_df_initial = vehicle_df_initial.transpose()

# Hits and ID fields made numeric
vehicle_df_initial['id'] = pd.to_numeric(vehicle_df_initial['id'])
vehicle_df_initial['hits'] = pd.to_numeric(vehicle_df_initial['hits'])


# New DF initialised to hold iterated results (this is to expand the 'attributes' nested fields)
attributes_expanded = pd.DataFrame()

vehicle_df_initial.reset_index(inplace=True, drop=True)

# Iterates over rows and expands nested json. Then appends to new dataframe car_data_all
for i in range(0, vehicle_df_initial.shape[0]):
    car_data = pd.json_normalize(data=vehicle_df_initial['attr'].iloc[i], meta=['id'])
    attributes_expanded = attributes_expanded.append(car_data)

# Reset car_data_all index to match original df
attributes_expanded.reset_index(inplace=True, drop=True)

# Concatanates original df with new fields
vehicles = pd.concat([vehicle_df_initial, attributes_expanded], axis=1)
print(vehicles.head(10))

# Selects relevant fields from total datasource and removes irrelevant fields
vehicles = vehicles[['hits', 'name', 'thumbnail', 'ct1.frontend_value', 'ct2.frontend_value',
                     'ct13.frontend_value', 'ct15.frontend_value',
                     'ct72.frontend_value',
                     'ct32.frontend_value', 'ct11.frontend_value', 'ct33.frontend_value', 'ct34.value',
                     'ct6.frontend_value',
                     'ct7.frontend_value', 'ct8.frontend_value', 'ct9.frontend_value', 'ct10.frontend_value']]

# Renames Columns to be more understandable
vehicles.rename(columns=
    {
        'hits': 'Hits',
        'name': 'Name',
        'thumbnail': 'Thumbnail',
        'ct1.frontend_value': 'Vehicle Type',
        'ct2.frontend_value': 'Manufacturer',
        'ct13.frontend_value': 'Purchase Price',
        'ct15.frontend_value': 'Sell Price',
        'ct72.frontend_value': 'Based On',
        'ct32.frontend_value': 'Top Speed',
        'ct11.frontend_value': 'No. of seats',
        'ct33.frontend_value': 'Weight',
        'ct34.value': 'Drivetrain',
        'ct6.frontend_value': 'Speed(stat)',
        'ct7.frontend_value': 'Acceleration',
        'ct8.frontend_value': 'Braking',
        'ct9.frontend_value': ' Acceleration',
        'ct10.frontend_value': 'Overall rating'
    }, inplace=True)

# Fill any null values with 0
vehicles.fillna(0)


# Functions created to remove redundant square brackets from some fields. Parameterised with no. of chars for other uses if needed later.
def strip_columns(dataframe, columns, chars):

    def strip_brackets(val, chars):
        return str(val)[chars:(chars*-1)]

    for i in columns:
        dataframe[i] = dataframe[i].apply(strip_brackets, args=[chars])


strip_columns(vehicles, ['Drivetrain', 'No. of seats', 'Manufacturer'], 2)

vehicles.fillna(0, inplace=True)
vehicles['Manufacturer'] = vehicles['Manufacturer'].replace('', 'Unknown')

# Converts fields to ints and floats
convert_dict = {
    'Hits': int,
    'Purchase Price': int,
    'Sell Price': int,
    'Top Speed': float,
    'Weight': float,
    'Speed(stat)': float,
    'Acceleration': float,
    'Braking': float,
    'Overall rating': float
}
vehicles = vehicles.astype(convert_dict)

# Vehicle types are exploded and added to separate sheet due to some vehicles having a one-to-many relationship.
vehicle_types = vehicles['Vehicle Type'].explode()

# Exports datasets to Car Data Sheet.
with pd.ExcelWriter('Vehicles.xlsx') as writer:
    vehicles.to_excel(writer, sheet_name='Vehicle information')
    vehicle_types.to_excel(writer, sheet_name='Vehicle category')


