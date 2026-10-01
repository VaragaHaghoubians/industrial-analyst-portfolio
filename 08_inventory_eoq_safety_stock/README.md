# Project 8, inventory, EOQ and safety stock

A beginner operations project for one year of synthetic spare-part and finished-good demand. Python calculates the economic order quantity, safety stock and reorder point, then flags what to buy and what is sitting too high.

The folder layout matches the steel manufacturing project: data, notebooks, `src`, reports, docs, a short dashboard note and tests. The data is synthetic. It is not a real purchasing decision.

## Result on the sample data

Reorder now: BEARING, SEAL-KIT and HYDRAULIC-HOSE.

SUPPORT is above the reorder point plus one order quantity, so the stock should be reviewed before buying more.

BRACKET has the highest safety stock, 49 units, because its weekly demand moves around. HYDRAULIC-HOSE has the higher service level, 99%, but a small safety stock in units because demand is small. Service level and units are not the same thing.

Order quantity for BRACKET is 850 units. Total relevant order-and-hold cost across the eight SKUs is about 6,796 euro per year. That cost leaves out the purchase price of the parts.

The calculated table is in [reports/inventory_summary.md](reports/inventory_summary.md).

## How to run it

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe .\src\main.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Open [START_HERE.md](START_HERE.md) before the notebooks. The portfolio MIT license in the repository root covers this folder.

## What I learned

EOQ is the quantity where the yearly ordering cost and the yearly cycle-stock holding cost meet.

Safety stock is `z × weekly standard deviation × square root of lead time`. A longer lead time needs more buffer, and the growth is the square root, not a straight line.

The reorder point is expected demand during the lead time plus safety stock. On-hand stock at or below that point is the buy signal in this project.

## Repository structure

```text
08_inventory_eoq_safety_stock/
├── README.md, START_HERE.md, requirements.txt
├── data/raw/                 # SKU master and 52 weeks of demand
├── data/processed/           # policy table and service-level curve
├── notebooks/                # four short walkthroughs
├── src/                      # generate, check, calculate, chart, report
├── reports/                  # charts, summary, metrics.json
├── docs/                     # formulas, examples, interview questions
├── dashboard/README.md       # optional Excel view
└── tests/                    # formula checks
```
