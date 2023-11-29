# Mean-Reversion Simulation for Gas, Coal, and CO₂
For modeling the prices of gas, coal, and carbon dioxide (CO$_2$), a stochastic mean-reverting process is employed, specifically a variant of the Ornstein-Uhlenbeck process adapted for discrete time series data. This method is grounded in the principle that these commodity prices, though subject to random fluctuations, tend to revert to their historical mean values over time.

The mean reversion rate for each commodity is estimated through linear regression, analyzing the logarithmic differences between the actual prices and their rolling mean values. This rate quantifies the speed at which prices revert to the mean, capturing the essential dynamics of the market's historical behavior.

$$Z_t = \ln{X_t} - \ln{y_t} = \alpha Z_{t-1} + \epsilon_t$$

In this equation, $X_t$ is the historical spot price of the commodity at time $t$, and $y_t$ is a rolling mean with a window of 28 days. The term $\alpha$ represents the mean reversion rate, and $\epsilon_t$ encapsulates the random shocks or fluctuations in price.

To simulate future price paths, we employ a stochastic differential equation that integrates the estimated mean reversion rate with randomly sampled residuals from our regression model. These residuals represent the random shocks or fluctuations in price, ensuring that each simulated path reflects potential real-world variability.

$$ P_t = \exp({\ln{F_t} + Z_t})$$

Where $P_t$ is the future spot prices, and $F_t$ is the future curve or the mean-level to which the natural logarithm of the spot price reverts. $F_t$ is derived from the future data set, representing the expected price level for the future period.

This stochastic modeling approach allows for the creation of multiple simulated future price paths, providing a range of scenarios for gas, coal, and CO$_2$ prices. This methodology is particularly useful for risk assessment and financial planning in markets where commodity prices are a critical factor.


# Simulated Energy Data Visualizations

Below are links to the simulated energy data visualizations for gas, coal, and carbon. Click on the links to view the respective PDFs.

- [Simulated Gas Data](./graphs/simulated_gas.pdf) - Visualization of simulated gas data.
- [Simulated Coal Data](./graphs/simulated_coal.pdf) - Visualization of simulated coal data.
- [Simulated Carbon Data](./graphs/simulated_carbon.pdf) - Visualization of simulated carbon data.
