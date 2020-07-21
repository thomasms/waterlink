from datetime import date
import numpy as np
import pandas as pd

"""
You are charged at two rates: basic and comfort.
The former is below the recommended limit from government,
while the latter is anything above the threshold. This is
usually charged double the comfort rate.

The threshold is:
30 m3 per household + 30 m3 per person in that household

For example, if there are three apartments sharing the same
meter, each with one resident the threshold is: 180 m3 (30+30)*3 m3

If there is two apartments each with one resident and the other has 4
residents then the threshold is higher at: 270 m3.
Since (30 + (30*1)) + (30 + (30*1))  + (30 + (30*4)).

Another example is in the case of 3 apartments each having 3 people.
This would then be:
Since (30 + (30*3))*3 = 360 m3.

This is very important when it comes to the cost, since the comfort rate
is double that of the basic rate.

Unfortunatly the DOM (gedomicilieerde), or people per residence, is determined
from the 1st January. Therefore if someone moves out on 2 January and a family
of 4 moves in on the same day (or next day) then the threshold is still at 
180 m3 instead of 270 m3 for 364 days of the year.

This program takes all this into account based on the rates and fees specified
in the data.csv file.

"""

# 30 m3 per year per household
BASIC_LIMIT_PER_HOUSEHOLD = 30
# 30 m3 per year per person in each household
BASIC_LIMIT_PER_PERSON = 30

df_rates = pd.read_csv("data.csv")

# make an effective rate as the sum of all three rates per basic and comfort
def compute_effective_rate(df):
    basic_cols = [
        c for c in df.columns if c.startswith("rate") and c.endswith("basic_eur_per_m3")
    ]
    df["rate_basic_effective_eur_per_m3"] = df[basic_cols].sum(axis=1)
    return df


# inclusive
def compute_days_between_dates(startdate, enddate, includeenddate=True):
    if includeenddate:
        return (enddate - startdate).days + 1
    else:
        return (enddate - startdate).days


def prorate_scale(startdate=None, enddate=None):
    """
    This could be a decorator
    """
    # we have a problem...
    if startdate is None and enddate is None:
        raise RuntimeError("You have a problem.")

    # assume first day of year if no startdate specified
    sd = startdate
    if sd is None:
        sd = date(enddate.year, 1, 1)

    # assume last day of year if no enddate specified
    ed = enddate
    if ed is None:
        ed = date(sd.year, 12, 31)

    scale = compute_days_between_dates(sd, ed) / compute_days_between_dates(
        date(sd.year, 1, 1), date(sd.year, 12, 31)
    )
    return scale


def compute_basic_threshold(startdate=None, enddate=None, we=3, dom=3):
    """
    This must be done per year. 
    Since the threshold is pro rated if not started on the 1st January.

    Need to compute days between and rate based on this.

    """
    full_year_threshold = BASIC_LIMIT_PER_HOUSEHOLD * we + BASIC_LIMIT_PER_PERSON * dom
    return full_year_threshold * prorate_scale(startdate=startdate, enddate=enddate)


def compute_fees(
    df,
    startdate=None,
    enddate=None,
    we=3,
    dom=3,
    fee_col="fee1_eur_per_year",
    discount_col="discount1_eur_per_year",
):
    """
        You get a discount of discount1_eur_per_year per dom
    """
    year = None
    if startdate is None:
        year = enddate.year
    else:
        year = startdate.year
    scale = prorate_scale(startdate=startdate, enddate=enddate)
    sdf = df[df["year"] == year]
    fee = sdf[fee_col].values[0] * scale * we
    discount = min(sdf[discount_col].values[0] * scale * dom, fee)
    return fee, discount


# some simple tests
START_DATE = date(2019, 2, 14)

# strictly this should be 2020 but since this was a leap year and the bill
# doesn't take this into account we ignore it here so that the numbers
# match up exactly
END_DATE = date(2019, 2, 18)


READING = 449

entries = [
    {"start": START_DATE, "end": date(START_DATE.year, 12, 31), "we": 3, "dom": 3},
    {"start": date(END_DATE.year, 1, 1), "end": END_DATE, "we": 3, "dom": 5},
]
"""
 algorithm outline:
   - start date from last bill
   - end date is last reading submitted for bill
   - the reading is the difference from end date to start date
   - work out the number of people per apartment per each year
        + [(year, we, dom), (year, we, dom)] - should not exceed 2 years, 
           since each bill covers roughly 365 days just doesn't start on Jan 1 always.
           But we will implement it to allow any number of years. However, still
           we consider that WE of DOM changes only on Jan 1st.
   - split the reading linearly across years
        For example if it has 321 days in 2019 and 49 days in 2020, then we work
        out thresholds based on 321/365 for WE1 and DOM1 and then 49/365 for WE2 and DOM2
        for each year and split it

"""

for entry in entries:
    scale = prorate_scale(startdate=entry["start"], enddate=entry["end"])
    threshold = compute_basic_threshold(
        startdate=entry["start"], enddate=entry["end"], we=entry["we"], dom=entry["dom"]
    )
    fees = [
        compute_fees(
            df_rates,
            startdate=entry["start"],
            enddate=entry["end"],
            we=entry["we"],
            dom=entry["dom"],
            fee_col=f"fee{i}_eur_per_year",
            discount_col=f"discount{i}_eur_per_year",
        )
        for i in range(1, 4)
    ]
    fees_with_discount = [f - d for f, d in fees]
    # print(threshold, np.sum(fees_with_discount))
    print(threshold, fees)
