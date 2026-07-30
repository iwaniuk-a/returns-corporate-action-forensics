import pandas as pd
import numpy as np

def _validate_prices(prices: pd.Series) -> None:
    if not isinstance(prices, pd.Series):
        raise TypeError("prices must be a pandas Series")
    
    if not pd.api.types.is_numeric_dtype(prices):
        raise ValueError("Prices column contains non-numeric types")
    
    if prices.isna().any():
        raise ValueError("Prices must not contain NaN values")
        
    if (prices <= 0).any():
        raise ValueError("Prices must be positive")

def simple_returns(prices: pd.Series) -> pd.Series:
    _validate_prices(prices)
    
    return prices / prices.shift(1) - 1

def log_returns(prices: pd.Series) -> pd.Series:
    _validate_prices(prices)

    return np.log(prices) - np.log(prices.shift(1))

def split_aware_returns(raw_prices: pd.Series, split_ratios: pd.Series) -> pd.Series:
    _validate_prices(raw_prices)

    if not isinstance(split_ratios, pd.Series):
        raise TypeError("split_ratios must be a pandas Series")
    
    if not raw_prices.index.equals(split_ratios.index):
        raise ValueError("Indices of raw_prices and split_ratios must match")
        
    if not pd.api.types.is_numeric_dtype(split_ratios):
        raise ValueError("Split ratios must be numeric")
        
    if (split_ratios <= 0).any():
        raise ValueError("Split ratios must be positive")

    if split_ratios.isna().any():
        raise ValueError("Split ratios must not contain NaN values")
        
    return (split_ratios * raw_prices) / raw_prices.shift(1) - 1

def total_returns(prices: pd.Series, cash_dividends: pd.Series,) -> pd.Series:
    _validate_prices(prices)
    
    if not isinstance(cash_dividends, pd.Series):
        raise TypeError("Cash dividents must be a pandas Series")
    
    if not prices.index.equals(cash_dividends.index):
        raise ValueError("Indices of cash dividents and prices must match")
    
    if not pd.api.types.is_numeric_dtype(cash_dividends):
        raise ValueError("Cash dividents must be numeric")
        
    if cash_dividends.isna().any():
        raise ValueError("Cash dividents must not contain NaN values")

    if (cash_dividends < 0).any():
        raise ValueError("Cash dividents must be non negative")

    return (prices + cash_dividends) / prices.shift(1) - 1