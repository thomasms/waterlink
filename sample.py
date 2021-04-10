from datetime import date
from compute import generate_report, print_report

rp1 = generate_report(
    reading=292,
    data=[
        {"start": date(2020, 2, 19), "end": date(2020, 12, 31), "we": 3, "dom": 5},
        {"start": date(2021, 1, 1), "end": date(2021, 2, 4), "we": 3, "dom": 6},
    ],
)

print_report(rp1)
