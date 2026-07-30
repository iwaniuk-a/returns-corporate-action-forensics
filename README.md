# Returns and Corporate-Action Forensics

## Research question
How do stock splits and cash dividends distort calculated returns, statistical diagnostics, and predictive models when corporate actions are treated as ordinary price movements?

## Economic quantities

## Mathematical and financial foundations
A return measures the change in wealth relative to invested capital. The one-period simple return, for a price series $P_t>0$, is
$$r_t = \frac{P_t}{P_{t-1}}-1.$$

If $P$ rises from 100 to 105, the simple return is 5%.

The log price return is defined as
$$g_t = \log{P_t} - \log{P_{t-1}} = \log{(1+r_t)}.$$

Therefore, simple price return can be written as
$$r^{price}_t =\exp(g_t) - 1$$

Log returns add through time, because $\sum_{t=1}^{T} g_t = \log(\frac{P_T}{P_0}).$ They are useful for statistical modeling, but they do not aggregate across assets as directly as simple returns. For small returns, $g_t \approx r_t$, but the difference matters for large moves and exact portfolio accounting.

A price-only return ignores cash distributions. If a share closes at $P_{t-1}$, pays dividend $D_t$, and closes at $P_t$, the one-period total return is
$$r^{total}_t = \frac{P_t+D_t}{P_{t-1}} - 1$$
subject to the precise timing and reinvestment convention. Total return is the relevant economic return for an investor who receives the dividend.

*   **2-for-1 split:** One share at 100 becomes two shares at approximately 50 each. Wealth remains 100. A raw close series records a -50% price move unless adjusted, even though there was no economic loss.
*   **Cash dividend:** A stock closes at 100, pays a 1 dividend, and opens ex-dividend near 99. The raw price return is about -1%, while the total return is about 0%. Ignoring the cash payment misstates investor wealth.

For a split with ratio $s_t$, such as $s_t=2$ for a 2-for-1 split,
$$q_t = s_t \cdot q_{t-1}, \qquad P_t\approx \frac{P_{t-1}}{s_t}$$
where $q_t$ is the number of shares held. Investor wealth is therefore
$$W_t = q_t \cdot P_t \approx (s_t q_{t-1}) \frac{P_{t-1}}{s_t} = q_{t-1}P_{t-1} = W_{t-1}.$$

Thus a split may produce a large change in the quoted price per share while producing approximately zero economic return.

Corporate actions are issuer events that alter shares, cash flows, identifiers, or security terms. Common examples include splits, reverse splits, cash and stock dividends, spin-offs, mergers, tender offers, rights issues, and symbol changes. An adjusted price is a vendor-transformed historical price intended to create a continuous return series. Adjustment conventions differ, so store raw prices, action fields, and adjustment factors where possible.
   
## Mathematical invariants

## Data sources and vendor limitations
Synthetic data:

Let $V_t$ denote the economic value of the original investment. We generate a latent pattern using log returns:
$$V_t = V_{t-1}\exp(g_t), \qquad g_t \sim N(0, \sigma^2).$$

On the split date $t_s$, set $g_{t_s} = 0$. This deliberately removes any genuine market movement on the event date. Therefore, any apparent return on that date must come entirely from the split mechanics.

We define the number of shares held as
$$q_t = \begin{cases} 1, & t < t_s, \\ 2, & t \ge t_s. \end{cases}$$

The raw quoted price per share is 
$$P_t = \frac{V_t}{q_t}.$$

At the split 
$$q_{t_s} = 2q_{t_s-1}, \qquad P_{t_s} = \frac{P_{t_s-1}}{2}$$
but
$$q_{t_s} P_{t_s} = q_{t_s-1}P_{t_s-1}$$

The raw price appears to lose 50%, while investor wealth changes by 0%.

## Planned experiments

## Reproducibility policy
Raw data will be immutable and every transformation will be reproducible from code.