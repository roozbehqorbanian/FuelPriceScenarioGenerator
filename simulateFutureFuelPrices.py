import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from calculateMeanRevertingRate import calculate_rolling_log_diff

def simulateFutureFuelPrices(param_historical_fuels, param_fuel_future, simulation_config):
    """
    Simulates future fuel prices based on historical data and mean reverting models.

    :param param_historical_fuels: DataFrame with historical fuel prices.
    :param param_fuel_future: DataFrame with forward curve fuel prices.
    :param simulation_config: Dictionary containing simulation configurations.
    :return: Tuple containing dictionaries for mrr_values, future_fuel_prices, and residuals_dict.
    """
    mrr_values = {}
    future_fuel_prices = {}  # Dictionary to store future fuel prices
    residuals_dict = {}  # Dictionary to store residuals for each commodity
    numScenarios = simulation_config['numScenarios']

    for commodity in param_historical_fuels.columns[:3]:
        window_size = simulation_config['windowSizes'].get(commodity, 28)
        mrr, residuals = calculate_rolling_log_diff(simulation_config['dataConfig'], commodity, window=window_size)
        mrr_values[commodity] = mrr
        residuals_dict[commodity] = residuals  # Store the residuals

        plt.figure(figsize=(10, 5))
        n_steps = param_fuel_future.shape[0]
        X = np.zeros((numScenarios, n_steps))
        Z = np.zeros((numScenarios, n_steps))
        X[:, 0] = param_fuel_future[commodity].iloc[0]

        for n in range(numScenarios):
            epsilon = np.random.choice(residuals_dict[commodity], size=n_steps)
            F_0_t = param_fuel_future[commodity].to_numpy()
            for t in range(1, n_steps):
                Z[n, t] = mrr * Z[n, t - 1] + epsilon[t]
                lnX = np.log(F_0_t[t]) + Z[n, t]
                X[n, t] = np.exp(lnX)

            plt.plot(param_fuel_future.index, X[n], label='Simulated Price Path' if n == 0 else "", alpha=0.1, color='blue')

        plt.plot(param_fuel_future.index, param_fuel_future[commodity].to_numpy(), color='black', label='Forward Curve')
        plt.title(f'Simulated Future Price Paths for {commodity} (numScenarios={numScenarios} simulations)')
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.legend()
        plt.show()

        sim_columns = [f'Sim_{n}' for n in range(numScenarios)]
        future_fuel_prices[commodity] = pd.DataFrame(X.T, index=param_fuel_future.index, columns=sim_columns)

    return mrr_values, future_fuel_prices, residuals_dict
