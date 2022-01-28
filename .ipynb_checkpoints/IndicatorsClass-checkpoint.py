# Import libraries and dependencies
import numpy as np
import pandas as pd
import hvplot.pandas
from sklearn.preprocessing import StandardScaler
from sklearn import svm
from sklearn.metrics import classification_report

class ClassificationSimulation:
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
    
    def __init__(self, X, y, split_fact = 0.7):
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
        if not isinstance(X, pd.DataFrame):
            raise TypeError("X data must be a Pandas DataFrame")
            
        # Check to make sure that all attributes are set
        if not isinstance(y, pd.DataFrame):
            raise TypeError("y data must be a Pandas DataFrame")
            
        # Set initial class attributes
        self.X = X
        self.y = y
        self.split_fact = split_fact
        
        # Set class attributes generated in functions
        self.training_predictions = ""
        self.training_report = ""
        self.testing_predictions = ""
        self.testing_report = ""
        
        self.X_train_scaled = ""
        self.X_test_scaled = ""
        self.y_train = ""
        self.y_test = ""
        
    def data_prep(self):   
        split = int(self.split_fact * len(self.X))

        # Shift values
        #self.X.drop(index= self.X.index.max(), inplace=True)
        # Split training and testing set
        X_train = np.array(self.X[: split])
        X_test =  np.array(self.X[split:])

        # Create a StandardScaler instance
        scaler = StandardScaler()

        # Apply the scaler model to fit the X-train data
        X_scaler = scaler.fit(X_train)
        # Transform the X_train and X_test DataFrames using the X_scaler
        self.X_train_scaled = X_scaler.transform(X_train)
        self.X_test_scaled = X_scaler.transform(X_test)
        
        """
        Prepare y.

        """
        # Shift values
        #self.y.drop(index= self.y.index.max(), inplace=True)

        # Split training and testing set
        self.y_train = self.y.iloc[: split]["signal"]
        self.y_test = self.y.iloc[split :]["signal"]
        
        
        return self.X_train_scaled, self.X_test_scaled, self.y_train, self.y_test
        
        
        
    def svc_model_generator(self):

        """
        Build model.

        """
        # Create the classifier model
        svm_model = svm.SVC()

        # Fit the model to the data using X_train_scaled and y_train
        svm_model = svm_model.fit(self.X_train_scaled, self.y_train)
        
        self.training_predictions = svm_model.predict(self.X_train_scaled)
        self.training_report = classification_report(self.y_train, self.training_predictions)
        self.testing_predictions = svm_model.predict(self.X_test_scaled)
        self.testing_report = classification_report(self.y_test, self.testing_predictions)
        
        
        return  svm_model, self.testing_predictions, self.training_report, self.testing_report
    
    
    
    def logisticRegression_model_generator(self):
        
        """
        Build model.

        """    
        # Create an instance of the LogisticRegression model
        logistic_regression_model = LogisticRegression()

        # Fit the LogisticRegression model
        logistic_regression_model.fit(self.X_train_scaled, self.y_train)
        
        
        self.training_predictions = logistic_regression_model.predict(self.X_train_scaled)
        self.training_report = classification_report(self.y_train, self.training_predictions)
        self.testing_predictions = logistic_regression_model.predict(self.X_test_scaled)
        self.testing_report = classification_report(self.y_test, self.testing_predictions)
        
        
        return  logistic_regression_model, self.testing_predictions