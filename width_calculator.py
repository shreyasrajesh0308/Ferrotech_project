# Module imports
import os 
import random
import pandas as pd
import subset_sum_problem

# Keeping the data repeatable 
random.seed(5000)
def frame_generator(df, df_count): 
    # This function calls the algorithm in the subset sum problem to provide optimum length values
    number_of_sheets = 1
    for i in df_count["value"]: 
        
        df_chunk = df[df.New_Widths == i]
        print("For width {} this is the optimised solution \n".format(i))
        sheet_counter =  subset_sum_problem.input_function(df_chunk, 6000, number_of_sheets, i)
        number_of_sheets+=sheet_counter
def rounder(x, loadbar_pitch):

   divided_value = x/loadbar_pitch

   if divided_value - int(divided_value) < 0.3:
       return int(divided_value)
   else:
       return int(divided_value) + 1

if __name__ == "__main__":

    # input_widths = list(map(int,input().split()))
    # Input Paramters
    if os.path.isfile("optimized.csv"):
        os.remove("optimized.csv")
    path_to_excel_file = "/home/shreyas/Adi_project/Data/fwdsamplenestingfiles/test_input.xlsx"
    df = pd.read_excel(path_to_excel_file, index = False)
    # input_widths = [random.randint(500, 1000) for _ in range(100)]
    # loadbar_pitch = 6
    # framebar_pitch = 41
    # lengths = [random.randint(1000,2000) for _ in range(100)]
    # quantity = [random.randint(1,5) for _ in range(100)]
    #
    panel_max_width = 1000
    framebar_pitch = 30
    loadbar_pitch = 5
    input_widths = df["WIDTH"]
    # Calculating new width values
    max_width = int(panel_max_width/framebar_pitch)*framebar_pitch + loadbar_pitch*1
    new_input_widths = [rounder(x,framebar_pitch)*framebar_pitch + loadbar_pitch for x in input_widths]
    new_input_widths = [max_width if i > max_width else i for i in new_input_widths]
    
    df["New_Widths"] = new_input_widths
    df = df.sort_values(by = ['New_Widths'], ascending = False)
    df = df.loc[df.index.repeat(df.QTY)]
    df = df.drop(['QTY'], axis=1)
    
    # New width values with count
    new_widths_column = df['New_Widths']
    count_of_widths = new_widths_column.value_counts().values
    value_of_widths = new_widths_column.value_counts().index
    df_count = pd.DataFrame(list(zip(value_of_widths, count_of_widths)), columns = ["value", "count"])
    df_count = df_count.sort_values( by = ['value'] , ascending = False)
    # Function call to call Algorithm that return suitable lengths

    frame_generator(df, df_count) 

