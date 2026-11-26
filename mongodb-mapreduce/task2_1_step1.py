# total global sales per platform

from mrjob.job import MRJob

class task2_1_step1(MRJob):

    def mapper(self, _, line):
        parts = line.strip().split("\t")
        if len(parts) != 5:
            return
        
        platform = parts[1]
        global_sales = parts[3]

        try:
            global_sales = float(global_sales)
        except ValueError:
            return
        
        yield platform, global_sales

    def reducer(self, platform, sales_values):
        yield platform, sum(sales_values)

if __name__ == "__main__":
    task2_1_step1.run()

# py task2_1_step1.py task1_1_output.txt > task2_1_step1_output.txt