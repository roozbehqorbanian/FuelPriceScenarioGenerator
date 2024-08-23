# Fuel Price Scenario Generator
# This script loads historical fuel price data and uses mean reverting models to simulate and plot future fuel price scenarios. It calculates mean reverting rates, simulates future prices for different commodities, and plots the residuals for analysis.

from loadData import load_data
from plot_residuals import plot_residuals
from simulateFutureFuelPrices import simulateFutureFuelPrices

# Configuration for simulations and data paths
simulation_config = {
    'numScenarios': 1000,
    'windowSizes': {
        'gas': 28,   # window size for gas
        'coal': 28,  # window size for coal
        'carbon': 28 # window size for carbon
    },
    'dataConfig': {
        'HISTORICAL_DATA_PATH': 'HistoricalFuelPrices.xlsx',
        'FUTURE_DATA_PATH': 'ForwardCurveFuelPrices.xlsx',
        'HISTORICAL_SHEET': "Prices",
        'FUTURE_SHEET': 'Fuel price',
        'START_DATE_FUTURE': "2024-01-01 00:00",
        'END_DATE_FUTURE': "2030-12-31 23:00"
    }
}

# Load historical and future fuel price data
param_historical_fuels, param_fuel_future = load_data(simulation_config['dataConfig'])

# Perform simulations and plot the results
mrr_values, future_fuel_prices, residuals_dict = simulateFutureFuelPrices(param_historical_fuels, param_fuel_future, simulation_config)
print("Mean reverting rates: ", mrr_values)

# Graph the residuals of the simulations
# plot_residuals(residuals_dict)

for fuel, df in future_fuel_prices.items():
    filename = f"{fuel}_prices.csv.gz"
    df.to_csv(filename, compression='gzip', index=True)