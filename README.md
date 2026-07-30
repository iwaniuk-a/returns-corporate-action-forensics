# Returns and Corporate-Action Forensics

A foundational quantitative-finance research project examining how stock splits and cash dividends can corrupt returns, cumulative wealth, rolling statistics, technical signals, and statistical models when they are treated as ordinary price movements.


## Research question

How severely can incorrect corporate-action treatment distort measured returns, risk diagnostics, technical signals, cumulative wealth, and predictive models?

## Main findings

The project combines controlled synthetic experiments with real Apple and Coca-Cola corporate actions.

- A synthetic 2-for-1 split produced a naive return of **-50%**, while shareholder wealth and the split-aware return were unchanged.
- The same false split return inflated 20-day rolling volatility by as much as **13.63×**.
- The raw split observation produced an ex-ante z-score of approximately **-46.17**, compared with approximately **0.19** after correct treatment.
- A ridge-regression pipeline trained on contaminated returns had approximately **6.44× higher RMSE** than the action-aware pipeline.
- For Coca-Cola over 2023–2025, dividend-inclusive wealth ended **9.42% above** price-only wealth.
- On **4 of 12** Coca-Cola dividend dates, price return was negative while total return was non-negative.
- Alpha Vantage and yfinance agreed on all **12 ex-dividend dates and dividend amounts** in the selected sample.
- Around Apple’s 2020 4-for-1 split, comparing prices expressed in different share units produced a naive return of **-74.15%**. Share-count accounting and the split-adjusted close both produced an economic return of **+3.39%**.

The central conclusion is that corporate-action adjustment is not cosmetic preprocessing. It determines the economic meaning of every downstream statistic and model input.

## Core mathematics

### Simple returns

For a strictly positive price series $P_t$, the one-period simple price return is

$$
r_t^{\mathrm{price}}=\frac{P_t}{P_{t-1}}-1.
$$

If a price rises from 100 to 105, then

$$
r_t^{\mathrm{price}}=5\%.
$$

### Log returns

The log return is

$$
g_t=\log P_t-\log P_{t-1}=\log\left(1+r_t^{\mathrm{price}}\right).
$$

Therefore,

$$
r_t^{\mathrm{price}}=\exp(g_t)-1.
$$

Log returns add through time:

$$\sum_{t=1}^{T}g_t=\log\left(\frac{P_T}{P_0}\right).$$

For small returns,

$$
g_t\approx r_t^{\mathrm{price}},
$$

but this is only an approximation.

### Dividend-inclusive total returns

If the shareholder receives cash dividend $D_t$, the one-period total return is

$$r_t^{\mathrm{total}}=\frac{P_t+D_t}{P_{t-1}}-1.$$

The dividend contribution to the return is therefore

$$
r_t^{\mathrm{total}}-r_t^{\mathrm{price}}=\frac{D_t}{P_{t-1}}.
$$

A stock can have a negative price return while still producing a non-negative total return.

### Split-aware returns

For a split with event ratio $s_t$, the split-aware return is

$$
r_t^{\mathrm{split}}=\frac{s_tP_t}{P_{t-1}}-1.
$$

Here $s_t=1$ on ordinary dates. For a 2-for-1 split, $s_t=2$ on the event date.

If the number of shares changes according to

$$
q_t=s_tq_{t-1},
$$

then investor wealth is

$$
W_t=q_tP_t.
$$

For a pure split,

$$
q_tP_t\approxq_{t-1}P_{t-1}.
$$

The quoted price per share changes, but investor wealth does not mechanically change.

## Experiments

### Experiment A — Synthetic split and model contamination

Main notebook:

[`notebooks/01_synthetic_split.ipynb`](notebooks/01_synthetic_split.ipynb)

A deterministic 2-for-1 split is used to study:

- raw versus split-aware returns
- simple and log-return identities
- compounding and investor wealth
- 20-day rolling-volatility contamination
- ex-ante rolling z-scores
- moving-average signal distortion
- supervised-learning feature and target contamination
- standard versus robust feature scaling
- ridge-regression coefficients and residuals
- concentration of model loss around corporate-action rows

The split simulation uses NumPy random seed `1108`.

### Experiment B — Cash-dividend accounting

Main notebook:

[`notebooks/02_cash_dividend.ipynb`](notebooks/02_cash_dividend.ipynb)

The experiment begins with a deterministic dividend identity and then studies Coca-Cola over 2023–2025.

It covers:

- price return versus total return
- explicit dividend accounting
- yfinance adjusted-close reconciliation
- price-only versus dividend-inclusive cumulative wealth
- dividend dates where price and total return have different signs
- Alpha Vantage versus yfinance event verification

### Experiment C — Real Apple stock split

Main notebook:

[`notebooks/03_real_corporate_actions.ipynb`](notebooks/03_real_corporate_actions.ipynb)

Apple’s 2020 4-for-1 split is used to:

- identify the split from the vendor action field
- distinguish split-adjusted prices from historical quote units
- reconstruct approximate pre-split quoted prices
- compare naive and split-aware returns
- reconstruct shareholder wealth from price and share count
- demonstrate that adjusted prices are analytical constructs rather than historical executable quotes

### Project synthesis

Main notebook:

[`notebooks/04_project_synthesis.ipynb`](notebooks/04_project_synthesis.ipynb)

The synthesis notebook loads saved evidence artifacts from Experiments A–C and presents:

- an artifact manifest;
- compact experiment summaries;
- a cross-experiment distortion table;
- project-level conclusions;
- limitations;
- technical and non-technical interview explanations.

## Headline evidence

| Experiment | Research object | Incorrect treatment | Action-aware result | Distortion |
|---|---|---:|---:|---|
| Synthetic 2-for-1 split | Split-date return | −50.00% | 0.00% | False 50 percentage-point loss |
| Synthetic 2-for-1 split | 20-day volatility | 13.63× action-aware volatility | Economic-return volatility | One event contaminates a full rolling window |
| Synthetic 2-for-1 split | Ex-ante z-score | −46.17 | 0.19 | Bookkeeping event appears as an extreme anomaly |
| Synthetic model | Ridge RMSE | 0.0656 | 0.0102 | 6.44× higher RMSE |
| Coca-Cola dividends | Dividend-date return sign | 4 apparent price-only losses | Non-negative total returns | 33.3% of dividend dates |
| Coca-Cola dividends | Three-year wealth | 1.111 | 1.215 | 9.42% higher total-return wealth |
| Apple 4-for-1 split | Split-date return | −74.15% | +3.39% | Positive day appears as a 74% collapse |
| Vendor verification | Event dates and amounts | Single-vendor records before verification | 12 of 12 events matched | Maximum amount difference: 0.000 |

The machine-readable version is stored at:

```text
reports/tables/project_cross_experiment_distortion.csv
```

## Data sources

### Synthetic data

Deterministic synthetic split and dividend datasets are stored under:

```text
data/raw/synthetic/
```

These files are committed because they are generated within the project and are fully reproducible.

### yfinance

Daily Apple and Coca-Cola data include:

- open
- high
- low
- close
- adjusted close
- volume
- dividends
- stock splits

Downloads use explicit settings:

```python
auto_adjust=False
actions=True
repair=False
```

The returned fields remain vendor-defined. In particular, yfinance `Close` is already normalized for stock splits even when `auto_adjust=False`.

Downloaded yfinance files are stored under:

```text
data/raw/yfinance/
```

They are excluded from Git and can be regenerated with:

```bash
python3 scripts/download_yfinance.py
```

### Alpha Vantage

The Alpha Vantage `DIVIDENDS` endpoint is used as an independent check of Coca-Cola:

- ex-dividend dates
- declaration dates
- record dates
- payment dates
- dividend amounts

Downloaded files are stored under:

```text
data/raw/alphavantage/
```

They are excluded from Git and can be regenerated with:

```bash
python3 scripts/download_alphavantage_actions.py
```

## Repository structure

```text
returns-corporate-action-forensics/
├── README.md
├── pyproject.toml
├── requirements-lock.txt
├── configs/
│   └── project.yaml
├── data/
│   ├── raw/
│   │   ├── synthetic/
│   │   ├── yfinance/
│   │   └── alphavantage/
│   ├── interim/
│   └── processed/
├── metadata/
│   ├── data_dictionary.md
│   └── source_log.csv
├── notebooks/
│   ├── 01_synthetic_split.ipynb
│   ├── 02_cash_dividend.ipynb
│   ├── 03_real_corporate_actions.ipynb
│   └── 04_project_synthesis.ipynb
├── reports/
│   ├── figures/
│   └── tables/
├── scripts/
│   ├── download_yfinance.py
│   └── download_alphavantage_actions.py
├── src/
│   └── returns_forensics/
│       ├── __init__.py
│       └── returns.py
└── tests/
    └── test_returns.py
```

## Reusable return functions

The core implementations are located in:

```text
src/returns_forensics/returns.py
```

The module includes:

```python
simple_returns(prices)
log_returns(prices)
split_aware_returns(raw_prices, split_ratios)
total_returns(prices, cash_dividends)
```

The functions validate:

- pandas Series inputs
- numeric dtypes
- strictly positive prices
- non-missing values
- non-negative dividends
- positive split factors
- exact index alignment

## Automated tests

The test suite covers:

- ordinary simple-return calculations
- the log/simple return identity
- synthetic split arithmetic
- split-aware return continuity
- cash-dividend total returns
- the difference between price and total return
- the zero-dividend identity
- missing values
- nonnumeric values
- invalid prices
- invalid split ratios
- mismatched indices
- invalid input types

Run the tests with:

```bash
python3 -m pytest -v
```

The current suite contains 14 passing tests.

## Reproducibility policy

- Raw vendor extracts are treated as immutable.
- Synthetic datasets are deterministic and generated from explicit parameters.
- Derived results are produced by code rather than edited manually.
- Corporate-action fields and adjusted prices are preserved separately.
- Mathematical identities are encoded in automated tests.
- Report tables and figures are generated by notebooks.
- Adjusted prices are treated as analytical constructs, not necessarily as historical executable quotes.
- API keys and local environment files are excluded from Git.
- Vendor data are regenerated through scripts rather than committed.

## Limitations

### Data limitations

- yfinance and Alpha Vantage are suitable for educational research but are not institutional-grade historical databases.
- Historical vendor records may be revised after the original event date.
- Exact agreement between vendors does not prove complete independence because they may use overlapping upstream sources.
- Apple’s historical as-traded price is reconstructed from the split-adjusted close and reported split ratio rather than obtained from an archival raw-quote database.

### Economic limitations

- Dividend calculations ignore taxes, withholding, transaction costs, and reinvestment frictions.
- Total-return growth assumes dividends remain part of the investment.
- A split has no mechanical effect on wealth, but the security can still move for ordinary market reasons over the same interval.
- Adjusted-close conventions may differ across vendors.

### Statistical limitations

- The synthetic experiments demonstrate mechanisms rather than estimate population effects.
- The ridge-regression experiment is an in-sample contamination diagnostic, not evidence of return predictability.
- Rolling-window distortion depends on the selected window length.
- Results from Apple and Coca-Cola should not be generalized automatically to all securities or events.

### Scope limitations

The project does not fully address:

- reverse splits
- special dividends
- stock dividends
- spin-offs
- rights offerings
- mergers
- ticker changes
- delistings
- reorganizations

These events may require different accounting conventions and additional security-level data.

## Final conclusion

A price series is meaningful only when its economic unit is understood.

Stock splits change the number of shares and the quoted price per share. Cash dividends transfer value from the company to the shareholder. Treating either event as an ordinary price movement can create false returns and contaminate every downstream stage of a quantitative research pipeline.

Correct corporate-action accounting must therefore occur before calculating risk metrics, creating trading signals, scaling features, fitting models, or evaluating performance.
