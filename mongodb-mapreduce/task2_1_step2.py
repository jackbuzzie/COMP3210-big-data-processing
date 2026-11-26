# select the top 3 platforms

platform_sales = {}

# read task 2.1 step 1 output
with open("task2_1_step1_output.txt") as f:
    for line in f:
        platform, total = line.strip().split("\t")
        platform_sales[platform.strip('"')] = float(total)

# sort descending and take top 3
top3 = sorted(platform_sales.items(), key=lambda x: x[1], reverse=True)[:3]

print(top3)

# py task2_1_step2.py
# ('PS3', 957.8399999999987)]