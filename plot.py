from cycler import cycler
import matplotlib.pyplot as plt
import numpy as np
from datetime import date

from compute import compute_total_cost

# plt.style.use('ggplot')
plt.rc("lines", linewidth=2)
plt.rc("grid", alpha=0.6, linewidth=0.9, color="a9a9a9")
plt.rc(
    "axes",
    facecolor=(0.9, 0.9, 0.9, 0.3),
    prop_cycle=(cycler("color", ["r", "g", "b", "c", "k", "y"])),
)
# plt.rc("figure.subplot.left")

WE = 3
START_DATE = date(2020, 2, 14)
END_DATE = date(2021, 2, 13)

doms = range(3, 8)
colors = []

fig1, ax1 = plt.subplots(figsize=(12, 7))
fig2, ax2 = plt.subplots(figsize=(12, 7))
for dom in doms:
    readings = np.linspace(0, 500, 100)
    costs = np.array(
        [
            compute_total_cost(
                reading=reading,
                data=[
                    {
                        "start": START_DATE,
                        "end": date(START_DATE.year, 12, 31),
                        "we": WE,
                        "dom": dom,
                    },
                    {
                        "start": date(END_DATE.year, 1, 1),
                        "end": END_DATE,
                        "we": WE,
                        "dom": dom,
                    },
                ],
            )
            for reading in readings
        ]
    )

    ax1.plot(readings, costs, label=f"dom={dom}", alpha=0.7)
    ax2.plot(readings, costs / dom, label=f"dom={dom}", alpha=0.7)

ax12 = ax1.twinx()
ax22 = ax2.twinx()

ax2.set_title("Per building costs", fontsize=16)
ax1.set_xlabel("m3 per year", fontsize=16)
ax1.set_ylabel("EUR per year", fontsize=16)
ax12.set_ylabel("EUR per month", fontsize=16)
ax12.set_ylim([ax1.get_ylim()[0] / 12.0, ax1.get_ylim()[1] / 12.0])
ax1.legend()
ax1.grid()

ax2.set_title("Per person costs", fontsize=16)
ax2.set_xlabel("m3 per year", fontsize=16)
ax2.set_ylabel("EUR per year per person", fontsize=16)
ax22.set_ylabel("EUR per month per person", fontsize=16)
ax22.set_ylim([ax2.get_ylim()[0] / 12.0, ax2.get_ylim()[1] / 12.0])
ax2.legend()
ax2.grid()

plt.show()
