from datetime import date

from compute import compute_total_cost


# m3 for the period above
# it is odd since the bill has both 443 and 449, but 442.94 seems
# to match perfectly with amounts in bill
print(
    compute_total_cost(
        reading=442.936,
        data=[
            {"start": date(2019, 2, 14), "end": date(2019, 12, 31), "we": 3, "dom": 3},
            {"start": date(2020, 1, 1), "end": date(2020, 2, 18), "we": 3, "dom": 5},
        ],
    )
)

# if they had registered the correct number of people
print(
    compute_total_cost(
        reading=443,
        data=[
            {"start": date(2019, 2, 14), "end": date(2019, 12, 31), "we": 3, "dom": 5},
            {"start": date(2020, 1, 1), "end": date(2020, 2, 18), "we": 3, "dom": 6},
        ],
    )
)

print(
    compute_total_cost(
        reading=50,
        data=[
            {"start": date(2019, 2, 14), "end": date(2019, 12, 31), "we": 1, "dom": 1},
            {"start": date(2020, 1, 1), "end": date(2020, 2, 18), "we": 1, "dom": 1},
        ],
    )
)