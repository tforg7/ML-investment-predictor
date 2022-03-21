# Import libraries and dependencies
import numpy as np
import pandas as pd
import hvplot.pandas
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

class LSTMmultiSimunation:
    """
    A Python class for runnning a simulation on portfolio price data. 
    
    ...
    
    Attributes
    ----------
    df : pandas.DataFrame
        portfolio dataframe with a feature 'Closing' and the index 'Date'
    parameters: dict
        Dictionnary of the parameters that are used in this LSTM
    ticker: str
        Name of ticker used in this simulation

        
    """
    
    def __init__(self, X_df, y_df, parameters, ticker):
        """
        Constructs all the necessary attributes for the BacktestingSimulation object.

        Parameters
        ----------
        df: pandas.DataFrame
            DataFrame containing stock price information from  API
        parameters: dict( floats)
            A dict containing the parameters we would like to use for this model
        ticker: str
            Name of the ticker we would like tu use
        """
        
        # # Check to make sure that all attributes are set
        # if not isinstance(X_df, pd.DataFrame):
        #     raise TypeError("DataFrame X_df data must be a Pandas DataFrame")
            
        # # Check to make sure that all attributes are set
        # if not isinstance(y_df, np.array):
        #     raise TypeError("DataFrame y_df data must be a Pandas DataFrame")
            
         # Set initial class attributes
        self.X = X_df
        self.y = y_df
        self.ticker = ticker
        
         # Set initial attributes for the elements in the dict
        self.window_size = parameters["window_size"]
        self.horizon = parameters["horizon"]
        self.split_train = parameters["split_train"]
        self.dropout_fraction = parameters["dropout_fraction"]
        self.epoch = parameters["epoch"]
        self.batch = parameters["batch"]
        self.split_val = parameters["split_val"]  
        
        # Set class attributes generated in functions
        self.training_predictions = ""
        self.training_report = ""
        self.testing_predictions = ""
        self.testing_report = ""
        
        self.X_scaler =""
        self.Y_scaler =""
        
        self.X_train = []
        self.X_test = []
        self.y_train = []
        self.y_test = []
        
    """
     Define a function for the window
    """   
    def get_window(self):
        
        self.X_scaler = MinMaxScaler()
        X_data = self.X_scaler.fit_transform(self.X)
        self.Y_scaler = MinMaxScaler()
        y_data = self.Y_scaler.fit_transform(self.y)

        # Size splitting
        split = int(self.split_train * len(self.X))
        start = self.window_size
        end = len(self.X) - self.horizon +1
        
        # Make training set
        for i in range(start, split):
             indices = range(i-self.window_size, i)
             self.X_train.append(X_data[indices])
             indicey = range(i, i+self.horizon)
             self.y_train.append(y_data[indicey])
            
            
          # Make testing set
        for i in range(split, end) :
             indices = range(i-self.window_size, i)
             self.X_test.append(X_data[indices])
             indicey = range(i, i+self.horizon)
             self.y_test.append(y_data[indicey])
    
            
        return np.array(self.X_train), np.array(self.X_test), np.array(self.y_train), np.array(self.y_test)
    
    """
     Define a function for the scaler
    """

    def data_scaler(self):
        split = int(self.split_train * len(self.X))
        X_train = self.X[: split]
        X_test = self.X[split:]
        y_train = self.y[: split]
        y_test = self.y[split:]

        self.X_scaler = StandardScaler()
        self.Y_scaler = StandardScaler()

        self.X_scaler.fit(self.X_train)
        X_train = self.X_scaler.transform(self.X_train)
        X_test = self.X_scaler.transform(self.X_test)

        self.Y_scaler.fit(self.y_train)
        y_train = self.Y_scaler.transform(self.y_train)
        y_test = self.Y_scaler.transform(self.y_test)

        self.X = np.concatenate((X_train, X_test))
        self.y = np.concatenate((y_train, y_test))

        return self.X, self.y
        
          
    """
     Define a function to get the scalers
    """     
    def get_Xscaler(self):
        return self.X_scaler
    
                               
    def get_Yscaler(self):
        return self.Y_scaler
    

    
    

        