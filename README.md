# Big Data Processing

MongoDB, MapReduce and spatial query processing in Python.

> Coursework for COMP3210 (Big Data), Macquarie University, 2026.

## 1. MongoDB + MapReduce: [`mongodb-mapreduce/`](mongodb-mapreduce)

Analysis of a video game sales dataset:

- `task1_1.py` validates and extracts records from MongoDB (dropping rows with missing genre, platform, publisher, sales or year) and writes them to a new collection and a tab-delimited file
- `task1_2.py` is an `mrjob` MapReduce job that aggregates global sales by genre
- `task2_1_step1-4.py` is a multi-stage pipeline: total sales per platform (MapReduce), then the top 3 platforms, then yearly sales for those platforms (MapReduce with a passed-in argument), then a line chart of the trend

## 2. Spatial nearest-neighbour search: [`spatial-nearest-neighbour/`](spatial-nearest-neighbour)

`task1.py` finds the nearest shop to each query point using three methods, each timed with `perf_counter`:

- a sequential-scan baseline
- an **R-tree** built from scratch, searched with **branch-and-bound** (pruning nodes by minimum distance to their bounding rectangle)
- branch-and-bound with **divide-and-conquer** over partitions of the dataset

 This was part of a group assignment; this file is my task.

## Tech

Python · MongoDB (pymongo) · mrjob (Hadoop-style MapReduce)
