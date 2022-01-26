# Import libraries and dependencies
import numpy as np
import pandas as pd
import pytz
import hvplot.pandas

class BacktestingSimulation:
    """
    A Python class for runnning a simulation on portfolio price data. 
    
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

    simulated_returns : pandas.DataFrame
        Simulated investement strategy over historical data

        
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
        self.simulated_return = ""
        
        
        
        
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
            label = self.Signal
        )
        
        # Overlay the plots
        portfolio_entry_exit_plot = total_portfolio_value * entry * exit
        portfolio_entry_exit_plot.opts(
            title="Total Portfolio Value",
            yformatter='%.0f'
        )
        
        return portfolio_entry_exit_plot




    def investement_ratios (self):
        """
        Define a function that return a dataframe with all the investement ratio's for a strategy.

        """
        # Check to make sure that simulation has run previously. 
        if not isinstance(self.simulated_returns,pd.DataFrame):
            self.portfolio_returns()

        # Create a list for the column name
        columns = [f"Backtest {self.Signal}"]

        # Create a list holding the names of the new evaluation metrics
        metrics = [
            "Annualized Return",
            "Cumulative Returns",
            "Annual Volatility",
            "Sharpe Ratio",
            "Sortino Ratio"]

        # Initialize the DataFrame with index set to the evaluation metrics and the column
        portfolio_evaluation_df = pd.DataFrame(index=metrics, columns=columns)

        # Calculate annualized return
        portfolio_evaluation_df.loc["Annualized Return"] = (
            self.simulated_returns["Portfolio Daily Returns"].mean() * 365
        )

        # Calculate cumulative return
        portfolio_evaluation_df.loc["Cumulative Returns"] = self.simulated_returns["Portfolio Cumulative Returns"][-1]

        # Calculate annual volatility
        portfolio_evaluation_df.loc["Annual Volatility"] = (
            self.simulated_returns["Portfolio Daily Returns"].std() * np.sqrt(365)
        )

        # Calculate Sharpe ratio
        portfolio_evaluation_df.loc["Sharpe Ratio"] = (
            self.simulated_returns["Portfolio Daily Returns"].mean() * 365) / (
            self.simulated_returns["Portfolio Daily Returns"].std() * np.sqrt(365)
        )

        
        # Calculate Sharpe ratio Sortino ratio:
        #First create a DataFrame that contains the Portfolio Daily Returns column and the downside return values
        sortino_ratio_df = self.simulated_returns[["Portfolio Daily Returns"]].copy()
        sortino_ratio_df.loc[:,"Downside Returns"] = 0

        # Second Find Portfolio Daily Returns values less than 0,
        # square those values, and add them to the Downside Returns column
        sortino_ratio_df.loc[sortino_ratio_df["Portfolio Daily Returns"] < 0,
                            "Downside Returns"] = sortino_ratio_df["Portfolio Daily Returns"]**2

        # Then Calculate the annualized return value and the annualized downside standard deviation value
        annualized_return = (
            sortino_ratio_df["Portfolio Daily Returns"].mean() * 365)

        downside_standard_deviation = (
            np.sqrt(sortino_ratio_df["Downside Returns"].mean()) * np.sqrt(365))

        # Finally do the last calculation for the sortino_ratio
        sortino_ratio = annualized_return/downside_standard_deviation

        # Add the Sortino ratio to the evaluation DataFrame
        portfolio_evaluation_df.loc["Sortino Ratio"] = sortino_ratio
        
        return portfolio_evaluation_df



        # Initialize trade evaluation DataFrame with columns
    def trade_evaluation(self):
        """
        Define a function that summarizes all the trasaction history.

        """
        # Check to make sure that simulation has run previously. 
        if not isinstance(self.simulated_returns,pd.DataFrame):
            self.portfolio_returns()

        # Initialize a DataFrame to contain the summary
        trade_evaluation_df = pd.DataFrame(
                    columns=[
                        "CURRENCY",
                        "Entry Date",
                        "Exit Date",
                        "Shares",
                        "Entry Share Price",
                        "Exit Share Price",
                        "Entry Portfolio Holding",
                        "Exit Portfolio Holding",
                        "Profit/Loss"]
                )

            # Loop through signal DataFrame
            # If `Entry/Exit` is 1, set entry trade metrics
            # Else if `Entry/Exit` is -1, set exit trade metrics and calculate profit
            # Then append the record to the trade evaluation DataFrame
        for index, row in self.simulated_returns.iterrows():
            if row["Entry/Exit Position"] == 500:
                entry_date = index
                entry_portfolio_holding = row["Portfolio Holdings"]
                share_size = row["Entry/Exit Position"]
                entry_share_price = row["Real_Closing"]

            elif row["Entry/Exit Position"] == -500:
                exit_date = index
                exit_portfolio_holding = abs(row["Real_Closing"] * row["Entry/Exit Position"])
                exit_share_price = row["Real_Closing"]
                profit_loss = exit_portfolio_holding - entry_portfolio_holding
                trade_evaluation_df = trade_evaluation_df.append(
                            {
                                "CURRENCY": self.ticker,
                                "Entry Date": entry_date,
                                "Exit Date": exit_date,
                                "Shares": share_size,
                                "Entry Share Price": entry_share_price,
                                "Exit Share Price": exit_share_price,
                                "Entry Portfolio Holding": entry_portfolio_holding,
                                "Exit Portfolio Holding": exit_portfolio_holding,
                                "Profit/Loss": profit_loss
                            },
                            ignore_index=True)

                # Print the DataFrame
        return trade_evaluation_df