from cycler import cycler
import matplotlib.pyplot as plt
import numpy as np
from datetime import date

from compute import compute_total_cost

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

doms = range(3, 8)
colors = []

fig1, ax1 = plt.subplots(figsize=(12, 7))
fig2, ax2 = plt.subplots(figsize=(12, 7))
ax12 = ax1.twinx()
ax22 = ax2.twinx()
for dom in doms:
    readings = np.linspace(0, 500, 100)
    costs = np.array([
        compute_total_cost(
            reading=reading,
            data=[
                {"start": START_DATE, "end": date(START_DATE.year, 12, 31), "we": WE, "dom": dom},
                {"start": date(END_DATE.year, 1, 1), "end": END_DATE, "we": WE, "dom": dom},
            ],
        )
        for reading in readings
    ])

    ax1.plot(readings, costs, label=f"dom={dom}", alpha=0.8)
    ax2.plot(readings, costs/dom, label=f"dom={dom}", alpha=0.8)

ax1.set_ylabel("EUR per year")
ax12.set_ylabel("EUR per month")
ax12.set_ylim([0, ax1.get_ylim()[1]/12.])
ax1.legend()

ax2.set_ylabel("EUR per year per person")
ax22.set_ylabel("EUR per month per person")
ax22.set_ylim([0, ax2.get_ylim()[1]/12.])
ax2.legend()

plt.show()
