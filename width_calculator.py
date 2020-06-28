# Module imports
import os 
import pandas as pd
import subset_sum_problem
import UI_inter
import numpy as np

def newinput_checker(i):

   if i <= max_width:
       return i 
   elif i > max_width and i < upper_bound:
       return max_width
   else:
       return np.nan
def grouper(df):
    counter = 0 
    for i in range(len(df)):
        if np.isnan(df.iloc[i].New_Widths) and counter == 0:
            print(counter)
            new_df = df.iloc[i:i+1]
            counter += 1
        elif np.isnan(df.iloc[i].New_Widths) and counter != 0:
            new_df = new_df.append(df.iloc[i:i+1])
            counter+=1
            print(counter)
    print(new_df) 
    new_df.append(pd.Series(), ignore_index = True) 
    new_df.to_csv("optimized_unnested.csv")
    df.dropna(subset = ["New_Widths"])
    return df
def frame_generator(df, df_count): 
    '''
    This function calls the dp algorithm in the file subset_sum_problem and writes the optimized patter onto a csv file called optimized.csv
    '''
    number_of_sheets = 1
    for i in df_count["value"]: 

        df_chunk = df[df.New_Widths == i]
        sheet_counter =  subset_sum_problem.input_function(df_chunk, 5930, number_of_sheets, i)
        number_of_sheets+=sheet_counter

    print("File Generated!")

def rounder(x, loadbar_pitch):

   divided_value = x/loadbar_pitch

   if divided_value - int(divided_value) < 0.3:
       return int(divided_value)
   else:
       return int(divided_value) + 1

if __name__ == "__main__":

    # Deleting the file we write to incase it exits initially
    if os.path.isfile("optimized.csv"):
        os.remove("optimized.csv")

    #Read from excel file
    global loadbar_pitch
    df, loadbar_pitch, framebar_thickness = UI_inter.main()
    df.SPAN = df.SPAN - 2*framebar_thickness

    #Variables for the system
    panel_max_width = 1000
    input_widths = list(df["WIDTH"])

    # Calculating new width values
    global max_width, upper_bound
    max_width = int(panel_max_width/loadbar_pitch)*loadbar_pitch + framebar_thickness
    upper_bound = (int(panel_max_width/loadbar_pitch) + 0.3)*loadbar_pitch
 
    new_input_widths = [rounder(x,loadbar_pitch)*loadbar_pitch + framebar_thickness for x in input_widths]
    new_input_widths = [newinput_checker(i) for i in new_input_widths]

    df["New_Widths"] = new_input_widths

    df = grouper(df)

    df["Area"] = df["WIDTH"]*df["SPAN"]

    # Adding a new_widths column and repeat the rows based on quantity
    df = df.sort_values(by = ['New_Widths'], ascending = False)
    df = df.loc[df.index.repeat(df.QTY)]
    df = df.drop(['QTY'], axis=1)

    # New width values with count, creates a new DataFrame
    new_widths_column = df['New_Widths']
    count_of_widths = new_widths_column.value_counts().values
    value_of_widths = new_widths_column.value_counts().index
    df_count = pd.DataFrame(list(zip(value_of_widths, count_of_widths)), columns = ["value", "count"])
    df_count = df_count.sort_values( by = ['value'] , ascending = False)


    #Function call to call Algorithm that return suitable lengths
    frame_generator(df, df_count) 

