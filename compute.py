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

# df_rates = pd.read_csv("data.csv")
df_rates = pd.DataFrame.from_dict(
    {
        "discount1_eur_per_year": {0: 10, 1: 10},
        "discount2_eur_per_year": {0: 6, 1: 6},
        "discount3_eur_per_year": {0: 4, 1: 4},
        "fee1_eur_per_year": {0: 50, 1: 50},
        "fee2_eur_per_year": {0: 30, 1: 30},
        "fee3_eur_per_year": {0: 20, 1: 20},
        "rate1_basic_eur_per_m3": {0: 1.4084, 1: 1.4139},
        "rate1_comfort_eur_per_m3": {0: 2.8168, 1: 2.8278},
        "rate2_basic_eur_per_m3": {0: 1.0606, 1: 1.0657},
        "rate2_comfort_eur_per_m3": {0: 2.1212, 1: 2.1314},
        "rate3_basic_eur_per_m3": {0: 0.9939, 1: 0.9977},
        "rate3_comfort_eur_per_m3": {0: 1.9878, 1: 1.9954},
        "year": {0: 2019, 1: 2020},
    }
)


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


def prorate_scale(startdate=None, enddate=None, naive=True):
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

    denom = (
        365
        if naive
        else compute_days_between_dates(date(sd.year, 1, 1), date(sd.year, 12, 31))
    )

    scale = compute_days_between_dates(sd, ed) / denom
    return scale


def compute_basic_threshold(
    startdate=None,
    enddate=None,
    we=3,
    dom=3,
    basic_limit_household=30,
    basic_limit_person=30,
):
    """
    This must be done per year. 
    Since the threshold is pro rated if not started on the 1st January.

    Need to compute days between and rate based on this.

    - 30 m3 per year per household - fixed value for all years
    basic_limit_household = 30

    - 30 m3 per year per person in each household - fixed value for all years
    basic_limit_person = 30

    """

    full_year_threshold = basic_limit_household * we + basic_limit_person * dom
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
    year = enddate.year if startdate is None else startdate.year
    scale = prorate_scale(startdate=startdate, enddate=enddate)
    sdf = df[df["year"] == year]
    fee = sdf[fee_col].values[0] * scale * we
    discount = min(sdf[discount_col].values[0] * scale * dom, fee)
    return fee, discount


def compute_total_cost(reading, data, df=df_rates):
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

        Parameters
        ----------
        # m3 for the period above
        reading = 442.936

        data = [
            {"start": START_DATE, "end": date(START_DATE.year, 12, 31), "we": 3, "dom": 3},
            {"start": date(END_DATE.year, 1, 1), "end": END_DATE, "we": 3, "dom": 5},
        ]

        Returns
        -------
        single value representing total cost in EUR
    """
    total_cost = 0
    fees_index = range(1, 4)
    for entry in data:
        sdf = df[df["year"] == entry["start"].year]
        scale = prorate_scale(startdate=entry["start"], enddate=entry["end"])
        threshold = compute_basic_threshold(
            startdate=entry["start"],
            enddate=entry["end"],
            we=entry["we"],
            dom=entry["dom"],
        )

        scaled_reading = reading * scale
        comfort_amount = max(scaled_reading - threshold, 0)
        basicreading = scaled_reading if scaled_reading < threshold else threshold

        fees_with_discount = []
        basic_costs = []
        comfort_costs = []
        for i in fees_index:
            f, d = compute_fees(
                df,
                startdate=entry["start"],
                enddate=entry["end"],
                we=entry["we"],
                dom=entry["dom"],
                fee_col=f"fee{i}_eur_per_year",
                discount_col=f"discount{i}_eur_per_year",
            )
            fees_with_discount.append(f - d)
            basic_costs.append(
                basicreading * sdf[f"rate{i}_basic_eur_per_m3"].values[0]
            )
            comfort_costs.append(
                comfort_amount * sdf[f"rate{i}_comfort_eur_per_m3"].values[0]
            )

        total = np.sum(basic_costs) + np.sum(comfort_costs) + np.sum(fees_with_discount)

        # print(threshold, np.sum(fees_with_discount))
        # print(f'{entry["start"].year}: {threshold}, {comfort_amount}')
        # for i in range(3):
        #     print(" * ", fees[i][0], fees[i][1], basic_costs[i], comfort_costs[i])
        # print(total)
        total_cost += total
    return total_cost
