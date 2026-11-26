# plot the yearly sales trend as line chart

import matplotlib.pyplot as plt
data = {}

with open("task2_1_step3_output.txt") as f:
    for line in f:
        key, value = line.strip().split("\t")
        platform, year = eval(key)
        year = int(year)
        value = float(value)

        if platform not in data:
            data[platform] = {}
        data[platform][year] = value

# plot
plt.figure(figsize=(10,6))

# one line per platform
for platform, yearly_data in data.items():
    years = sorted(yearly_data.keys())
    sales = [yearly_data[y] for y in years]
    plt.plot(years, sales, marker="o", label=platform)

plt.xlabel("Year") # years on x axis 
plt.ylabel("Global Sales") # sales on y axis
plt.title("Yearly Sales Trend for Top 3 Platforms")
plt.legend()
plt.grid(True)

plt.savefig("task2_1_step4_output.pdf")

# py task2_1_step4.py