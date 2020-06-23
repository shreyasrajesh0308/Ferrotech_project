# Introduction.

The objective of the program is to obtain an automized solution to the optimum cutting of slabs as requested by customers. The problem uses customer requirements to generate a CSV file that gives the optimum solution to cut the slab.

# Algorithm 

The problem is similar to the [subset sum problem](https://en.wikipedia.org/wiki/Subset_sum_problem) which is NP complete but using dynamic programming we have a solution in Pseudo Polynomial time. 

For our problem we use a DP based approach that when given a list of numbers and a required sum gives out the maximum sum less than the required some possible with the given list of numbers. 

This involves building a DP matrix and once built we traverse the tree back from the last entry until the first entry with value one.

Building the DP matrix is discussed [here](https://www.geeksforgeeks.org/subset-sum-problem-dp-25/)

# Code

The codebase involves three files.

1. Algorithm file - Algo implementation
2. UI file - Takes input excel file and loadbar and framebar pitch.
3. Main file - Takes the input using the UI program cleans the data and uses the Algo file to write into a output CSV file.

:


