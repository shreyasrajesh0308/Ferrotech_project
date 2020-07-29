# Introduction.

The objective of the program is to obtain an automized solution to the optimum cutting of slabs as requested by customers. The problem uses customer requirements to generate a CSV file that gives the optimum solution to cut the slab.

# Algorithm 

The problem is similar to the [subset sum problem](https://en.wikipedia.org/wiki/Subset_sum_problem) which is NP complete but using dynamic programming we have a solution in Pseudo Polynomial time. 

For our problem we use a DP based approach that when given a list of numbers and a required sum gives out the maximum sum less than the required some possible with the given list of numbers. 

This involves building a DP matrix and once built we traverse the tree back from the last entry until the first entry with value one.

Building the DP matrix is discussed [here](https://www.geeksforgeeks.org/subset-sum-problem-dp-25/)

# Running the Code

Run the Ferrotech_project.py file this will open a dialogue box where we load the required excel file along with certain input parameters. The output is written into an excel file.

# Code structure

Code base consists of two files.

UI_inter - For all UI related tasks.

Ferrotech_project - Contains everything else, from adding required colums to calling the algorithm and writing into excel file.

For any modifications and experimentation run the jupyternotebook of the same name before integrating into the python file.






