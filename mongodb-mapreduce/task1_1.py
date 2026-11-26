from pymongo import MongoClient

# connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["comp3210a1"]

# input collection (original dataset)
input_collection = db["VideoGameSales"]

# output collection (required by assignment)
output_collection = db["game_extracted"]

# clear output collection if it already exists
output_collection.delete_many({})

# open output text file
output_file = open("task1_1_output.txt", "w", encoding="utf-8")

# process each record
valid_records = []

for record in input_collection.find():
    genre = record.get("Genre")
    platform = record.get("Platform")
    publisher = record.get("Publisher")
    global_sales = record.get("Global_Sales")
    year = record.get("Year")

    # validate required fields
    if not genre or not platform or not publisher:
        continue
    if global_sales is None or global_sales == "":
        continue
    if year is None or year == "":
        continue

    # write to text file (tab-delimited)
    output_file.write(
        f"{genre}\t{platform}\t{publisher}\t{global_sales}\t{year}\n"
    )

    # prepare for MongoDB insertion
    valid_records.append({
        "genre": genre,
        "platform": platform,
        "publisher": publisher,
        "global_sales": global_sales,
        "year": year
    })

# insert all valid tuples into MongoDB
if valid_records:
    output_collection.insert_many(valid_records)

# close file
output_file.close()

# MUST SAVE OUTPUT FILES WITH UTF-8 ENCODING