# Module imports
import os 
import pandas as pd
import subset_sum_problem
import UI_inter
import numpy as np
import excelwriter

def weight_adder(df):

    df["WEIGHT"] = df.ORIGINAL_SPAN*df.WIDTH*weight
    return df
def Area_calculator(df):

    df["Alternate_Width"] = df["WIDTH"]
    df.loc[df.Alternate_Width > max_width, "Alternate_Width"] = max_width
    df["Area"] = df["SPAN"]*df["Alternate_Width"]
    df = df.drop("Alternate_Width", axis = 1)
    return df
def difference(df):

     df["DIFFERENCE"] = df["WIDTH"] - df["New_Widths"]
     df.loc[df.WIDTH < 1000, "DIFFERENCE"] = np.nan

     return df 
def newinput_checker(i):

   if i <= max_width:
       return i 
   # elif i > max_width and i < upper_bound:
   #      return max_width
   # # elif i > max_width:
   # #     return max_width
   # else:
   #      return np.nan
   else:
       return max_width


def grouper(df):
    counter = 0 
    for i in range(len(df)):
        if np.isnan(df.iloc[i].New_Widths) and counter == 0:
            new_df = df.iloc[i:i+1]
            counter += 1
        elif np.isnan(df.iloc[i].New_Widths) and counter != 0:
            new_df = new_df.append(df.iloc[i:i+1])
            counter+=1
    new_df.append(pd.Series(), ignore_index = True) 
    new_df = new_df.reset_index(drop=True)
    new_df.to_csv("optimized_unnested.csv")
    df.dropna(subset = ["New_Widths"])
    return df
def frame_generator(df, df_count): 
    '''
    This function calls the dp algorithm in the file subset_sum_problem and writes the optimized patter onto a csv file called optimized.csv
    '''
    new_req_sum = 5930
    Area_sum = 0
    df_count  = df_count.sort_values(by = ["value"], ascending = False)
    df_count = df_count.reset_index(drop=True)
    return_df = []
    print("DF_count is \n \n")
    print(df_count)
    for i in range(len(df_count["value"])): 

        df_chunk = df[df.New_Widths == df_count["value"][i]]
        if len(return_df) != 0:
             new_req_sum  , Area_sum, return_df =  subset_sum_problem.input_function(df_chunk, new_req_sum, df_count["value"][i-1], Area_sum, return_df)
        else:
             new_req_sum, Area_sum, return_df =  subset_sum_problem.input_function(df_chunk, new_req_sum, df_count["value"][i], Area_sum, return_df)


    print("File Generated!")

    if len(return_df) != 0:
        if not os.path.isfile("optimized.csv"):
            return_df.to_csv("optimized.csv", header='column_names')
        else:
            return_df.to_csv("optimized.csv", mode='a', header=False)



def rounder(x, loadbar_pitch):

   divided_value = x/loadbar_pitch

   if divided_value - int(divided_value) < 0.4:
       return int(divided_value)
   else:
       return int(divided_value) + 1

def sheet_no():

    df = pd.read_csv("optimized.csv")
    df["sheet_no"] = (pd.isna(df.SPAN).cumsum()) + 1
    df.to_csv("optimized.csv")

def type_writer():

    df_nested = pd.read_csv("optimized.csv", index_col = 0)
    df_nested = df_nested.dropna()
    df_nested = df_nested.sort_values(by = ["TYPE"], ascending = False)
    df_nested = df_nested.reset_index(drop=True)
    df_nested.to_csv("sorted_nestings.csv")

    # df_sorted = pd.DataFrame()
    # df_sorted = df_sorted.append(pd.Series(), ignore_index = True)
    # df_sorted = df_sorted.append(pd.Series(), ignore_index = True)
    # df_sorted.to_csv("optimized_unnested.csv", mode='a', header=False)
    #
    # df_nested.to_csv("optimized_unnested.csv", mode='a', header=True)


def framebar_cut():

    df_opt = pd.read_csv("optimized.csv")
    df_table = df_opt.loc[:, ["ERECTION_MARK", "DRAWING_NO", "New_Widths", "SPAN"]]
    table = pd.pivot_table(df_table, index = ["ERECTION_MARK", "DRAWING NO"], aggfunc = "size")
    table.append(pd.Series(), ignore_index = True)
    table.append(pd.Series(), ignore_index = True)
    table.to_csv("framebar_cut.csv")

    print(table)

    df_framebar = df_opt.loc[:, ["ERECTION_MARK", "New_Widths"]]
    df_framebar["Framebar_Quantity"] = df_framebar["Quantity"]*2
    df_framebar.append(pd.Series(), ignore_index = True)
    df_framebar.append(pd.Series(), ignore_index = True)
    df_framebar.to_csv("framebar_cut.csv", mode="a", header = True)

if __name__ == "__main__":

    # Deleting the file we write to incase it exits initially
    if os.path.isfile("optimized.csv"):
        os.remove("optimized.csv")

    #Read from excel file
    global loadbar_pitch, weight
    df, loadbar_pitch, framebar_thickness, weight = UI_inter.main()
    df["ORIGINAL_SPAN"] = df.SPAN
    df.SPAN = df.SPAN - 2*framebar_thickness

    #Variables for the system
    panel_max_width = 1000
    input_widths = list(df["WIDTH"])

    # Calculating new width values
    global max_width, upper_bound
    max_width = int(panel_max_width/loadbar_pitch)*loadbar_pitch + framebar_thickness
    upper_bound = (int(panel_max_width/loadbar_pitch) + 0.4)*loadbar_pitch
 
    new_input_widths = [rounder(x,loadbar_pitch)*loadbar_pitch + framebar_thickness for x in input_widths]
    new_input_widths = [newinput_checker(i) for i in new_input_widths]

    df["New_Widths"] = new_input_widths

    #df = difference(df)



    # if max(df.WIDTH) > upper_bound:
    #     df = grouper(df)
    # else:
    #     empty_df = pd.DataFrame(columns = df.columns)
    #     empty_df.to_csv("optimized_unnested.csv")


    #df["Area"] = df["WIDTH"]*df["SPAN"]

    df = Area_calculator(df)
    df = weight_adder(df)

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

    #Function call to add sheet number to generated dataframe
    sheet_no()

    #Function call to create Framebar cutting sheet
    #framebar_cut()

    # Function to write by different types of TYPE
    type_writer()

    # Writing into excel file
    excelwriter.write_to_excel()
