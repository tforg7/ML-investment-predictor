# Import libraries and dependencies
import numpy as np
import pandas as pd
import pytz

class BacktestingSimulation:
    """
    A Python class for runnning Monte Carlo simulation on portfolio price data. 
    
    ...
    
    Attributes
    ----------
    signal_df : pandas.DataFrame
        portfolio dataframe
    Signal: str
        Name of feature that contains the signal  we want to similate
    ticker: str
        Name of ticker used in this simulation
    share_size: int
        number of share for every transaction in simulation
    initial_capital: int
        amount of initial capital to simulate

    simulated_return : pandas.DataFrame
        Simulated data from Monte Carlo
    confidence_interval : pandas.Series
        the 95% confidence intervals for simulated final cumulative returns
        
    """
    
    def __init__(self, signal_df , Signal="", ticker = "", initial_capital=100000, share_size= 500):
        """
        Constructs all the necessary attributes for the BacktestingSimulation object.

        Parameters
        ----------
        signal_df: pandas.DataFrame
            DataFrame containing stock price information from Alpaca API
        weights: list(float)
            A list fractions representing percentage of total investment per stock. DEFAULT: Equal distribution
        num_simulation: int
            Number of simulation samples. DEFAULT: 1000 simulation samples
        num_trading_days: int
            Number of trading days to simulate. DEFAULT: 252 days (1 year of business days)
        """
        
        # Check to make sure that all attributes are set
        if not isinstance(signal_df, pd.DataFrame):
            raise TypeError("portfolio_data must be a Pandas DataFrame")
            
        # Set class attributes
        self.signal_df = signal_df
        self.Signal = Signal
        self.ticker = ticker
        self.initial_capital = initial_capital
        self.share_size = share_size
        
        
        
        
    def portfolio_returns(self):
        """
        Calculates the cumulative return of a stock over time using a choosen strategy.

        """
        # Create a New Dataframe to hold the the return information
        portfolio_returns = pd.DataFrame(self.signal_df['Real_Closing'])
        
        # Buy a 500 share position when the dual moving average crossover Signal equals 1
        # Otherwise, `Position` should be zero (sell)
        portfolio_returns['Position'] = self.share_size * self.signal_df[self.Signal]

        # Determine the points in time where a 500 share position is bought or sold
        portfolio_returns['Entry/Exit Position'] = portfolio_returns['Position'].diff()

        # Multiply the close price by the number of shares held, or the Position
        portfolio_returns['Portfolio Holdings'] = self.signal_df['Real_Closing'] * portfolio_returns['Position']

        # Subtract the amount of either the cost or proceeds of the trade from the initial capital invested
        portfolio_returns['Portfolio Cash'] = self.initial_capital - (self.signal_df['Real_Closing'] * portfolio_returns['Entry/Exit Position']).cumsum() 

        # Calculate the total portfolio value by adding the portfolio cash to the portfolio holdings (or investments)
        portfolio_returns['Portfolio Total'] = portfolio_returns['Portfolio Cash'] + portfolio_returns['Portfolio Holdings']

        # Calculate the portfolio daily returns
        portfolio_returns['Portfolio Daily Returns'] = portfolio_returns['Portfolio Total'].pct_change()

        # Calculate the portfolio cumulative returns
        portfolio_returns['Portfolio Cumulative Returns'] = (1 + portfolio_returns['Portfolio Daily Returns']).cumprod() - 1
        
        self.simulated_returns = portfolio_returns.dropna()

        return portfolio_returns.dropna()
    
    
    
    
    def visual_portfolio(self):
        """
        Define a function that make a time dependant vizualisation of the potfolio using the return of function 'portfolio_returns'

        """
        # Check to make sure that simulation has run previously. 
        if not isinstance(self.simulated_returns,pd.DataFrame):
            self.portfolio_returns()


        # Visualize exit position relative to total portfolio value
        exit = self.simulated_returns[self.simulated_returns['Entry/Exit Position'] == -1.0]['Portfolio Total'].hvplot.scatter(
            color='yellow',
            marker='v',
            legend=False,
            ylabel='Total Portfolio Value',
            width=1000,
            height=400
        )

        # Visualize entry position relative to total portfolio value
        entry = self.simulated_returns[self.simulated_returns['Entry/Exit Position'] == 1.0]['Portfolio Total'].hvplot.scatter(
            color='purple',
            marker='^',
            ylabel='Total Portfolio Value',
            width=1000,
            height=400
        )

        # Visualize the value of the total portfolio
        total_portfolio_value = self.simulated_returns[['Portfolio Total']].hvplot(
            ylabel='Total Portfolio Value',
            xlabel='Date',
            width=1000,
            height=400,
            label = name_signal
        )
        
        # Overlay the plots
        portfolio_entry_exit_plot = total_portfolio_value * entry * exit
        portfolio_entry_exit_plot.opts(
            title="Total Portfolio Value",
            yformatter='%.0f'
        )
        

        return portfolio_entry_exit_plot