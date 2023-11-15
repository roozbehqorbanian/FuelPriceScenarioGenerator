import pandas as pd

def load_data(data_config):
    """
    Loads historical and future fuel data from specified Excel files and sheets.

    :param data_config: Dictionary containing data file paths, sheet names, and date range.
    :return: Tuple of DataFrames (historical_fuels, future_fuels)
    """
    try:
        # Extracting configuration
        HISTORICAL_DATA_PATH = data_config['HISTORICAL_DATA_PATH']
        FUTURE_DATA_PATH = data_config['FUTURE_DATA_PATH']
        HISTORICAL_SHEET = data_config['HISTORICAL_SHEET']
        FUTURE_SHEET = data_config['FUTURE_SHEET']
        START_DATE_FUTURE = data_config['START_DATE_FUTURE']
        END_DATE_FUTURE = data_config['END_DATE_FUTURE']

        # Loading historical data
        fuels = pd.read_excel(HISTORICAL_DATA_PATH, sheet_name=HISTORICAL_SHEET, header=0)
        fuels = fuels.resample('D', on='Delivery Date').first().interpolate().fillna(method="bfill")

        # Loading future data
        param_fuel_future = pd.read_excel(FUTURE_DATA_PATH, header=0, sheet_name=FUTURE_SHEET)
        param_fuel_future = param_fuel_future.set_index('year').interpolate().loc[START_DATE_FUTURE:END_DATE_FUTURE]

        return fuels, param_fuel_future

    except Exception as e:
        # Handle exceptions like FileNotFoundError, KeyError, etc.
        print(f"An error occurred: {e}")
        return None, None