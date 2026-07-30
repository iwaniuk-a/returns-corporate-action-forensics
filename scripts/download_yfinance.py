import yfinance as yf
from pathlib import Path
import pandas as pd

def get_project_root(current_path: Path) -> Path:
    """Search upwards for the project root containing pyproject.toml."""
    for parent in [current_path] + list(current_path.parents):
        if (parent / "pyproject.toml").exists():
            return parent
    raise FileNotFoundError(
        "Could not locate project root containing pyproject.toml"
    )



def main():
    # 1. Project Root and Directory Setup
    # Path(__file__).resolve() gets the absolute path of this script
    script_path = Path(__file__).resolve() if "__file__" in globals() else Path.cwd()
    project_root = get_project_root(script_path)
    
    output_dir = project_root / "data" / "raw" / "yfinance"
    output_dir.mkdir(parents=True, exist_ok=True)
 
    ticker_symbol = "KO"
    start_date = "2023-01-01"
    end_date = "2026-01-01"
    
    ticker = yf.Ticker(ticker_symbol)
    
    df = ticker.history(
        start=start_date,
        end=end_date,
        interval="1d",
        auto_adjust=False,
        actions=True,
        repair=False
    )
    
    df.index.name = "date"
    df = df.reset_index()

    assert not df.empty
    assert df["Close"].notna().all()
    assert df["Dividends"].notna().all()
    assert df["Stock Splits"].notna().all()
    assert df["date"].is_monotonic_increasing
    assert not df["date"].duplicated().any()

    output_filename = f"{ticker_symbol}_{start_date}_{end_date}.csv"
    output_path = output_dir / output_filename
    
    df.to_csv(output_path, index=False)

    print(f"Saved raw data to: {output_path.resolve()}")
    print(f"Column names: {df.columns.to_list()}")
    print(f"Number of rows: {len(df)}")
    print(f"The first and last date: {df["date"].min(), df["date"].max()}")
    print(f"Rows where Dividends > 0: {df[df['Dividends']>0]}")
    print(f"Rows where Stock Splits > 0: {df[df['Stock Splits']>0]}")
    df['year'] = pd.to_datetime(df['date']).dt.year
    yearly_divs = df.groupby('year')['Dividends'].sum()
    print(f"Total dividends grouped by calendar year: {yearly_divs.to_string()}")
    
if __name__ == "__main__":
    main()