import matplotlib.pyplot as plt

def plot_residuals(residuals_dict):
    """
    Plots the residuals for each commodity in the residuals_dict.

    :param residuals_dict: Dictionary with commodities as keys and their residuals as values.
    """
    for commodity in residuals_dict:
        residuals = residuals_dict[commodity]

        # Plotting the residuals
        plt.figure(figsize=(10, 5))
        plt.plot(residuals, label=f'Residuals for {commodity}')
        plt.title(f'Residuals for {commodity}')
        plt.xlabel('Observation')
        plt.ylabel('Residual Value')
        plt.legend()
        plt.show()