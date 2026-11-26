from mrjob.job import MRJob

class task1_2(MRJob):
    def mapper(self, _, line):
        parts = line.strip().split("\t")

        # skip invalid lines
        if len(parts) != 5:
            return
        
        genre = parts[0]
        global_sales = parts[3]

        # skip invalid numbers
        try: 
            global_sales = float(global_sales)
        except ValueError:
            return
        
        yield genre, global_sales

    def reducer(self, genre, sales_values):
        total_sales = sum(sales_values)
        yield genre, total_sales

if __name__ == "__main__":
    task1_2.run() 

# mapper
# reads each tuple from task 1.1
# extracts key = genre and value = global_sales
# shuffle and sort
# reducer sums each list

# py task1_2.py task1_1_output.txt > task1_2_output.txt

# mrjob_env\Scripts\activate.bat