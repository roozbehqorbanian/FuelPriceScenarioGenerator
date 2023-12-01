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
    residuals_2_dict = {}  # Dictionary to store residuals_2 for each commodity
    numScenarios = simulation_config['numScenarios']
    window_sizes = simulation_config['windowSizes']

    n_steps = param_fuel_future.shape[0]
    indices_dict = {
        n: np.random.randint(0, param_historical_fuels.shape[0] - window_sizes[max(window_sizes, key=window_sizes.get)],
                             size=n_steps) for n in range(numScenarios)}

    for commodity in param_historical_fuels.columns[:3]:
        window_size = simulation_config['windowSizes'].get(commodity, 28)
        mrr, residuals, residuals_2 = calculate_rolling_log_diff(simulation_config['dataConfig'], commodity, window=window_size)
        mrr_values[commodity] = mrr
        residuals_dict[commodity] = residuals  # Store the residuals
        residuals_2_dict[commodity] = residuals_2  # Store the residuals_2 or ln(mean/shifted_mean)

        plt.figure(figsize=(10, 5))
        n_steps = param_fuel_future.shape[0]
        X = np.zeros((numScenarios, n_steps))
        Z = np.zeros((numScenarios, n_steps))
        U = np.zeros((numScenarios, n_steps))
        X[:, 0] = param_fuel_future[commodity].iloc[0]
        Z[:, 0] = 0.01
        U[:, 0] = 0.01

        for n in range(numScenarios):
            indices = indices_dict[n]
            epsilon = residuals_dict[commodity][indices]
            mean = residuals_2_dict[commodity].mean()
            std_dev = residuals_2_dict[commodity].std()
            normal_samples = np.random.normal(0, std_dev, n_steps)
            epsilon_2 = normal_samples
            F_0_t = param_fuel_future[commodity].to_numpy()
            for t in range(1, n_steps):
                Z[n, t] = mrr * Z[n, t - 1] + epsilon[t]
                U[n, t] = U[n, t - 1] + epsilon_2[t - 1] - (0.5 * std_dev ** 2)
                lnX = (np.log(F_0_t[t]) + Z[n, t]) + (U[n, t])
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
