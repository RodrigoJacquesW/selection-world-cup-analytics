# Beyond FIFA Rankings ⚽📊

An analytical model designed to evaluate which national teams currently arrive strongest for the World Cup based on underlying performance metrics rather than raw results.

This project was built to answer a simple question:

> **Which national teams are actually performing at the highest structural level heading into the World Cup?**

Instead of relying only on:

* wins,
* goals,
* or FIFA rankings,

the model focuses on **how teams perform on the pitch** through metrics related to:

* chance creation,
* territorial control,
* defensive stability,
* possession quality,
* and sustainable dominance.

---

# Project Philosophy

Traditional rankings heavily reward results.

This model attempts to measure:

* **structural strength**
* **consistency**
* **game control**
* and **repeatable performance patterns**

The core idea is:

> Teams that consistently control matches and create sustainable offensive pressure tend to be stronger than teams that rely purely on finishing efficiency or isolated moments.

Because of this philosophy:

* attacking volume is prioritized over finishing variance,
* territorial dominance is rewarded,
* and efficiency receives lower weight due to its volatility in smaller samples.

---

# Scope

* **29 National Teams**
* **Last 20 Matches per Team**
* Only finished matches included

The project currently analyzes:

* Argentina
* Brazil
* France
* England
* Spain
* Germany
* Portugal
* Netherlands
* Morocco
* Japan
* and other top national teams.

---

# Methodology

## 1. Data Collection

Match and performance data were collected using:

* Python
* Playwright
* SofaScore API

The pipeline automatically retrieves:

* match results,
* team statistics,
* possession data,
* shots,
* big chances,
* passing metrics,
* and defensive metrics.

---

## 2. Feature Engineering

Metrics were grouped into five core dimensions:

| Pillar       | Description                             |
| ------------ | --------------------------------------- |
| Attack       | Offensive volume and chance creation    |
| Efficiency   | Quality and conversion of opportunities |
| Defense      | Ability to suppress opponent attacks    |
| Control      | Possession and territorial management   |
| Differential | Overall dominance versus opponents      |

---

## 3. Opponent Strength Adjustment

All statistics are weighted using:

* **World Football Elo Ratings**

This allows the model to contextualize performance quality.

Example:

* creating 5 big chances against France
  carries more value than doing the same against weaker opposition.

The weighting function:

```sql
POW(elo_rating / 2000, 4)
```

---

## 4. Z-Score Normalization

Metrics operate on completely different scales:

* possession (%)
* shots (volume)
* goals conceded (rate)

To make everything comparable, all variables are transformed into Z-Scores.

This measures:

* how far above or below average a team performs
* in units of standard deviation.

---

## 5. Final Scoring Model

The final score combines all five pillars through weighted aggregation:

| Component    | Weight |
| ------------ | ------ |
| Attack       | 30%    |
| Defense      | 25%    |
| Control      | 20%    |
| Differential | 15%    |
| Efficiency   | 10%    |

The final score is also adjusted for:

* opponent strength,
* sample reliability,
* and metric normalization.

---

# Key Insights

Some interesting outcomes from the model:

* 🇪🇸 Spain ranked #1 due to elite territorial dominance and sustained attacking pressure
* 🏴 England performed exceptionally well in control and defensive stability
* 🇲🇦 Morocco emerged as one of the most structurally solid teams
* 🇫🇷 France ranked lower than expected due to lower territorial control metrics
* 🇧🇷 Brazil underperformed due to inconsistent collective offensive structure

---

# Tech Stack

## Data Collection

* Python
* Playwright

## Data Engineering

* BigQuery
* Dataform
* SQLX

## Analytics & Visualization

* Power BI
* Gama App

---

# Repository Structure

```plaintext
selection-world-cup-analytics/
│
├── scraping/
│   ├── matches.py
│   ├── stats.py
│   └── teams.py
│
├── sql/
│   ├── staging/
│   ├── intermediate/
│   └── marts/
│
├── presentation/
│   └── Beyond-FIFA-Rankings.pdf
│
├── images/
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

# Current Limitations

The current version still has important limitations:

* No expected goals (xG)
* Friendlies are included
* No home vs away adjustment
* No temporal weighting
* No match importance weighting
* Limited sample size

---

# Future Improvements

Planned next steps:

* Add xG and xThreat models
* Introduce temporal decay weighting
* Differentiate match importance
* Separate volume from chance quality
* Build predictive simulations
* Add tournament forecasting

---

# Final Thoughts

This project was an attempt to combine:

* football analytics,
* data engineering,
* statistical modeling,
* and storytelling

into a single analytical framework.

Rather than trying to predict results directly, the model focuses on identifying which teams consistently demonstrate sustainable, high-level performance patterns heading into international tournaments.

---

# Author

## Rodrigo Wolff

Data Analytics / Analytics Engineering 

LinkedIn: www.linkedin.com/in/rodrigo-jacques-wolff
