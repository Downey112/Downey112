<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
  <img src="assets/header-light.svg" width="100%" alt="Luqman Syahrulnizam. Statistics, Kuala Lumpur. I look for the residual: the part the headline doesn't explain. Beside the text, a scatter plot with a fitted line and one point far above it, labelled the residual.">
</picture>

In a regression, the **residual** is what's left after the model has said everything it can.
That's the part I like: take a headline number, find the public data behind it, and see what
it leaves out.

I'm a final-year Statistics student at UiTM, and most of what's here is built on Malaysian
open data: OpenDOSM, the Ministry of Higher Education, MetMalaysia and the Budget documents.

**Looking for a Data Analyst internship in Kuala Lumpur, available now until January 2027.**
&nbsp;[LinkedIn](https://linkedin.com/in/luqmansyahrulnizam) · [Portfolio](https://downey112.github.io)

## One finding, drawn

Budget 2027 announced a RM2,500 wage floor for graduates. Half of 2024's first-degree
graduates were already at or below it, but that half is not spread evenly.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/graduate-floor-dark.svg">
  <img src="assets/graduate-floor-light.svg" width="100%" alt="Bar chart: share of 2024 first-degree graduates earning RM2,500 a month or less, by field of study. Education 77.2%, arts and humanities 75.0%, agriculture 73.3%, services 59.9%, natural sciences, mathematics and statistics 58.1%, social sciences 52.5%, business 47.5%, engineering 39.6%, health 39.4%, ICT 27.7%. All first-degree graduates: 49.7%.">
</picture>

The numbers behind the chart are in [`data/`](data/graduates_at_or_below_rm2500.csv), and the
full analysis is in [fresh-grad-salary-model](https://github.com/Downey112/fresh-grad-salary-model).

## Questions I've put to the data

| The question | What the data said | Built with |
|---|---|---|
| How many graduates does a RM2,500 wage floor reach, and what does it cost? | 49.7% earned RM2,500 or less in 2024. In simulation the graduate wage bill rises 7.1% to 14.4%, depending on who is covered. [fresh-grad-salary-model](https://github.com/Downey112/fresh-grad-salary-model) | Python, statsmodels, Excel |
| Which fields of study leave graduates most exposed? | No field is near failing (every field had 88%+ of its labour-force graduates in work in 2025); the fields differ far more in job quality. Services, Agriculture, Education and Arts sit at the risky end. [program-risk-my](https://github.com/Downey112/program-risk-my) · [live](https://programriskmy.streamlit.app/) | Python, Streamlit |
| What does a graduate hire cost an employer at the new wage benchmarks? | Employer cost and take-home pay at RM2,000, RM2,500 and RM3,400 a month, in a formula-driven workbook. [belanjawan-2027-wage-cost-model](https://github.com/Downey112/belanjawan-2027-wage-cost-model) | Excel, Python |
| Which months of Malaysian trade don't fit the pattern? | 320 months of OpenDOSM trade data, with 8 export anomaly months and 25 sector spikes flagged. [dosm_trade_engine](https://github.com/Downey112/dosm_trade_engine) | Python, pandas, Power BI |
| How much do grocery prices really differ by store format? | A 16-staple basket is 14% cheaper in hypermarkets (RM110.96) than wet markets (RM126.58), but within-format shop dispersion dominates. 20M+ PriceCatcher rows modeled with two-way fixed effects. [pricecatcher-retail-pricing](https://github.com/Downey112/pricecatcher-retail-pricing) | DuckDB, Python, Power BI |
| Can store sales be forecast as they stream in? | Real M5 Walmart demand, replayed through Kafka and Spark as a live stream; the stock, costs and transaction lines are **simulated**. Next-day WAPE was 0.725 on the replay, close to the 0.710 backtest of the champion random forest (seasonal naive: 0.868). [retail-demand-rt](https://github.com/Downey112/retail-demand-rt) · [dashboard](https://downey112.github.io/retail-demand-rt/dashboard/) | Kafka, PySpark, Power BI |
| Which online shoppers are about to leave, and what do they buy together? | Real UCI Online Retail II data: on 4,350 active customers in the held-out month, a logistic model ranks 30-day churn with AUC 0.755 vs 0.684 for recency alone (its probabilities need recalibrating for the holiday season). Apriori finds 249 bundle rules, cross-checked in SQL. [ecom-churn-basket](https://github.com/Downey112/ecom-churn-basket) | PostgreSQL, Python |
| Who quits a job, and is it worth paying to keep them? | Real survey data on 1,116 employees: staff on partly undeclared ("grey") pay stay a median 26 months vs 54. A Cox model ranks risk only modestly (C-index 0.60), and a back-test of the retention cost rule beats "nobody" or "everybody" in just 4 of 45 cost scenarios, so measuring the intervention's effect matters more than the model. [hr-attrition-decision](https://github.com/Downey112/hr-attrition-decision) | Python, lifelines, Power BI |
| Do marketing-mix methods recover the truth? | A **simulation study** with known true parameters: promo lifts and the profit-optimal budget are recovered well across 100 Monte Carlo runs, while the response curve's ceiling is weakly identified. [Multi-Channel ROI](https://github.com/Downey112/Multi-Channel-Retail-Demand-Forecasting-Marketing-ROI-Optimizer) | PostgreSQL, statsmodels |
| How far is the market fuel price from the subsidised one this week? | A live tracker of the gap for RON95 and diesel, refreshed twice a week. [budi-pulse](https://github.com/Downey112/budi-pulse) · [live](https://budi-pulse.streamlit.app) | Python, PostgreSQL, Streamlit |
| Who leaves a telco, and when? | 26.54% churn across 7,043 customers; month-to-month contracts are 88.55% of those who left. [DSC651-TelcoChurn-PowerBI](https://github.com/Downey112/DSC651-TelcoChurn-PowerBI) | Power BI |
| Can a model catch fraud that is 0.17% of transactions? | A detection pipeline for a heavily imbalanced dataset. [audit-fraud-detection](https://github.com/Downey112/audit-fraud-detection) | Python, SQL |
| How honest is a published paper's "90% range"? | Re-examining arXiv:2610.13588 on EV charging: an honest method would pass only ~53% of the paper's scorecard, so its recommended method wins by being wider. Three code discrepancies were reported to the authors. [ev-conformal](https://github.com/Downey112/ev-conformal) | Python, conformal prediction |
| What does the Budget actually say? | Answers drawn from the official Budget 2026 documents, with page-level citations. [belanjawan-bot](https://github.com/Downey112/belanjawan-bot) | Python, RAG |

Also here: [perasaan-malaysia](https://github.com/Downey112/perasaan-malaysia), a scheduled
pipeline for MetMalaysia's 7-day forecasts; [malaysia-inclusive-economy-blueprint](https://github.com/Downey112/malaysia-inclusive-economy-blueprint) · [live](https://Downey112.github.io/malaysia-inclusive-economy-blueprint/), an interactive fiscal policy simulator; [esg-multiagent-auditor](https://github.com/Downey112/esg-multiagent-auditor), an event-driven Scope 1-3 GHG auditing architecture; [free-worker](https://github.com/Downey112/free-worker), an MCP worker for Claude Code that routes tasks across free AI models and falls back when one hits its quota; [threads-mcp](https://github.com/Downey112/threads-mcp), a read-only Threads API connector for topic analysis; [hf-agents-course-gaia](https://github.com/Downey112/hf-agents-course-gaia), my Hugging Face Agents Course final agent that scored 85% on GAIA level-1 questions; and [wealthwatch](https://github.com/Downey112/wealthwatch), a personal finance tracker that is [live](https://wealthwatch-six.vercel.app).

## What I work in

**Analysis** Python (pandas, statsmodels), R, SQL (PostgreSQL, T-SQL), SAS, SPSS<br>
**Reporting** Power BI (DAX, star schemas), Excel, Tableau, Looker Studio, Streamlit<br>
**Methods** multiple linear regression, hypothesis testing, regression diagnostics, anomaly detection

<img src="assets/metrics.svg" width="480" alt="Languages used across my repositories, mostly Python, and a 3D calendar of my GitHub contributions over the last six months, refreshed daily.">

```
                        Model summary: luqman
======================================================================
Dep. variable:   answers you can check
Method:          least squares
Sample:          Oct 2023 - Feb 2027, B.Sc. (Hons.) Statistics, UiTM
----------------------------------------------------------------------
Notes:
[1] Every number comes from a linked repository or from GitHub.
[2] Simulated data is labelled as simulated.
[3] The header and chart are drawn by scripts/build_assets.py;
    the activity image is refreshed daily by lowlighter/metrics.
======================================================================
```
