# yearly sales for top 3 platforms

from mrjob.job import MRJob
class task2_1_step3(MRJob):
    def configure_args(self):
        super().configure_args()
        self.add_passthru_arg("--platforms")

    def mapper(self, _, line):
        
        parts = line.strip().split("\t")

        if  len(parts) != 5:
            return
        
        genre, platform, publisher, global_sales, year = parts
        top_platforms = self.options.platforms.split(",")

        if platform not in top_platforms:
            return
        
        try:
            global_sales = float(global_sales)
            year = int(year)
        except:
            return
        
        yield(platform, year), global_sales

    def reducer(self, key, values):
        yield key, sum(values)

if __name__ == "__main__":
    task2_1_step3.run()

# py task2_1_step3.py task1_1_output.txt --platforms=PS2,X360,PS3 > task2_1_output.txt