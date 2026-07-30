import os
from io import StringIO
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv


EXPECTED_COLUMNS = {
    "ex_dividend_date",
    "declaration_date",
    "record_date",
    "payment_date",
    "amount",
}


def find_project_root(start: Path) -> Path:
    for candidate in (start.resolve(), *start.resolve().parents):
        if (candidate / "pyproject.toml").exists():
            return candidate

    raise FileNotFoundError(
        "Could not locate project root containing pyproject.toml"
    )


def main() -> None:
    project_root = find_project_root(Path(__file__).resolve().parent)

    load_dotenv(project_root / ".env")

    api_key = os.getenv("ALPHAVANTAGE_API_KEY")
    if not api_key:
        raise RuntimeError("ALPHAVANTAGE_API_KEY is not configured")

    response = requests.get(
        "https://www.alphavantage.co/query",
        params={
            "function": "DIVIDENDS",
            "symbol": "KO",
            "datatype": "csv",
            "apikey": api_key,
        },
        timeout=30,
    )
    response.raise_for_status()

    dividends = pd.read_csv(StringIO(response.text))

    missing_columns = EXPECTED_COLUMNS.difference(dividends.columns)
    if missing_columns:
        raise ValueError(
            "Unexpected Alpha Vantage response. "
            f"Missing columns: {sorted(missing_columns)}. "
            f"Response begins: {response.text[:200]!r}"
        )

    output_path = (
        project_root
        / "data"
        / "raw"
        / "alphavantage"
        / "KO_dividends.csv"
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save the raw parsed response without filtering or renaming.
    dividends.to_csv(output_path, index=False)

if __name__ == "__main__":
    main()