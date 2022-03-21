# Import libraries and dependencies
import numpy as np
import pandas as pd
import hvplot.pandas
from sklearn import svm
from sklearn.metrics import classification_report
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

class LSTMClosingSimunation:
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
     Define a function for the window: Input X and output y should be np.array
    """   
    def get_window(self):

        # Size splitting
        split = int(self.split_train * len(self.X))
        start = self.window_size
        end = len(self.X) - self.horizon +1
        
        # Make training set
        for i in range(start, split):
             indices = range(i-self.window_size, i)
             self.X_train.append(self.X[indices])
             indicey = range(i, i+self.horizon)
             self.y_train.append(self.y[indicey])
            
            
          # Make testing set
        for i in range(split, end) :
             indices = range(i-self.window_size, i)
             self.X_test.append(self.X[indices])
             indicey = range(i, i+self.horizon)
             self.y_test.append(self.y[indicey])
            
        return np.array(self.X_train), np.array(self.X_test), np.array(self.y_train), np.array(self.y_test)
    
    """
     Define a function for the window :Input X should be an array with multiple elements (multi feature), and Output y should be a dataframe 1D
    """   
    def get_scaledwindow_multi(self):
        
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
        
        X_train_rnn = np.array(self.X_train)
        X_test_rnn = np.array(self.X_test)
        y_train_rnn = np.array(self.y_train)
        y_test_rnn = np.array(self.y_test)
        
        ## Create a MinMaxScaler object
        self.X_scaler = MinMaxScaler()
        self.Y_scaler = MinMaxScaler()
        
        # Fit the MinMaxScaler object with the training feature data X_train
        self.X_scaler.fit(X_train_rnn)
        # Scale the features training and testing sets
        X_train_scaled = self.X_scaler.transform(X_train_rnn)
        X_test_scaled = self.X_scaler.transform(X_test_rnn)

        # Fit the MinMaxScaler object with the training target data y_train
        self.Y_scaler.fit(y_train_rnn)
        # Scale the target training and testing sets
        y_train_scaled = self.Y_scaler.transform(y_train_rnn)
        y_test_scaled = self.Y_scaler.transform(y_test_rnn)
                               
        # # Reshape the features for the model
        X_train_reshaped = X_train_scaled.reshape((X_train_scaled.shape[0], X_train_scaled.shape[1], 1))
        X_test_reshaped = X_test_scaled.reshape((X_test_scaled.shape[0], X_test_scaled.shape[1], 1))
                               
        return X_train_reshaped, X_test_reshaped, y_train_scaled, y_test_scaled
          
    """
     Define a function to get the scalers
    """     
    def get_Xscaler(self):
        return self.X_scaler
    
                               
    def get_Yscaler(self):
        return self.Y_scaler
    

    
    

        