import pandas as pd
import numpy as np
import pytest
from returns_forensics.returns import simple_returns, log_returns, split_aware_returns, total_returns


def test_ordinary_price_path():

    price = pd.Series([100, 105, 102.9])
    expected = pd.Series([np.nan, 0.05, -0.02])

    np.testing.assert_allclose(
    simple_returns(price),
    expected,
    err_msg="Simple returns should be calculated correctly for ordinary price paths"
)
    
def test_log_simple_identity():
    price = pd.Series([100, 105, 102.9])

    sr_result = simple_returns(price)
    log_result = log_returns(price)

    converted_result = np.expm1(log_result)

    np.testing.assert_allclose(
        converted_result,
        sr_result,
        err_msg="Log returns converted to simple returns should match simple returns"
    )

def test_synthetic_split():
    raw_prices = pd.Series([100.0, 50.0, 51.0])
    split_ratios = pd.Series([1.0, 2.0, 1.0])
    
    expected_raw_returns = pd.Series([np.nan, -0.5, 0.02])
    expected_split_aware = pd.Series([np.nan, 0.0, 0.02])
    
    actual_raw = simple_returns(raw_prices)
    actual_split_aware = split_aware_returns(raw_prices, split_ratios)
    
    pd.testing.assert_series_equal(
        actual_raw, 
        expected_raw_returns
    )
    
    pd.testing.assert_series_equal(
        actual_split_aware, 
        expected_split_aware
    )

def test_invalid_input_raises_value_error():
    invalid_cases = [
        pd.Series([100.0, 0.0, 101.0]),     # Zero price
        pd.Series([100.0, -5.0, 101.0]),    # Negative price
        pd.Series([100.0, np.nan, 101.0]),  # Missing price
        pd.Series([100.0, "105.0", 101.0])  # Non-numeric type
    ]
    
    for case in invalid_cases:
        with pytest.raises(ValueError):
            simple_returns(case)

def test_non_series_prices_raise_type_error():
    with pytest.raises(TypeError):
        simple_returns([100.0, 101.0])


def test_missing_split_ratio_raises_value_error():
    prices = pd.Series([100.0, 50.0])
    split_ratios = pd.Series([1.0, np.nan])

    with pytest.raises(ValueError):
        split_aware_returns(prices, split_ratios)


def test_mismatched_indices_raise_value_error():
    prices = pd.Series(
        [100.0, 50.0],
        index=["day_1", "day_2"],
    )
    split_ratios = pd.Series(
        [1.0, 2.0],
        index=["day_1", "wrong_day"],
    )

    with pytest.raises(ValueError):
        split_aware_returns(prices, split_ratios)


def test_log_returns_reject_invalid_prices():
    with pytest.raises(ValueError):
        log_returns(pd.Series([100.0, 0.0]))

###
def test_total_returns_with_cash_dividend():
    prices = pd.Series([100.0, 99.0, 100.0])
    dividends = pd.Series([0.0, 1.0, 0.0])

    expected = pd.Series([np.nan, 0.0, 100.0 / 99.0 - 1.0,
    ])

    actual = total_returns(prices, dividends)

    np.testing.assert_allclose(
        actual,
        expected,
        err_msg="Total returns should include cash dividends",
    )

def test_dividend_distinguishes_price_and_total_return():
    prices = pd.Series([100.0, 99.0])
    dividends = pd.Series([0.0, 1.0])

    price_return = simple_returns(prices)
    total_return = total_returns(prices, dividends)

    np.testing.assert_allclose(
        price_return.iloc[1],
        -0.01,
    )

    np.testing.assert_allclose(
        total_return.iloc[1],
        0.0,
    )

def test_zero_dividends_recover_price_returns():
    prices = pd.Series([100.0, 103.0, 101.0])
    dividends = pd.Series([0.0, 0.0, 0.0])

    np.testing.assert_allclose(
        total_returns(prices, dividends),
        simple_returns(prices),
    )

def test_mismatched_indices_dividends():
    prices = pd.Series(
        [100.0, 50.0],
        index=["day_1", "day_2"],
    )
    dividends = pd.Series(
        [1.0, 2.0],
        index=["day_1", "wrong_day"],
    )

    with pytest.raises(ValueError):
        total_returns(prices, dividends)

def test_invalid_input_dividends():
    prices = pd.Series([100.0, 99.0, 100.0])
    invalid_cases = [
        pd.Series([1.0, -5.0, 0.0]),    # Negative dividentd
        pd.Series([1.0, np.nan, 0.0]),  # Missing dividend
        pd.Series([1.0, "1.0", 0.0])  # Non-numeric type
    ]
    
    for case in invalid_cases:
        with pytest.raises(ValueError):
            total_returns(prices, case)

def test_non_series_dividends():
    prices = pd.Series([100.0, 99.0, 100.0])
    with pytest.raises(TypeError):
        total_returns(prices, [100.0, 101.0])
