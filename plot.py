from cycler import cycler
import matplotlib.pyplot as plt
import numpy as np
from datetime import date

from compute import compute_total_cost

# 1. Setting prop cycle on default rc parameter
plt.rc("lines", linewidth=4)
plt.rc(
    "axes",
    prop_cycle=(
        cycler("color", ["r", "g", "b", "y", "k", "c"])
    ),
)

WE = 3
START_DATE = date(2019, 2, 14)
END_DATE = date(2020, 2, 18)

doms = range(6)
colors = []

fig, ax = plt.subplots(figsize=(12, 7))
for dom in doms:
    readings = range(0, 500, 50)
    costs = [
        compute_total_cost(
            reading=reading,
            data=[
                {"start": START_DATE, "end": date(2019, 12, 31), "we": WE, "dom": dom},
                {"start": date(2020, 1, 1), "end": END_DATE, "we": WE, "dom": dom},
            ],
        )
        for reading in readings
    ]

    ax.plot(readings, costs, label=f"dom={dom}", alpha=0.8)

plt.legend()
plt.show()
