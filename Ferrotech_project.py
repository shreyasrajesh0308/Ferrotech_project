#!/usr/bin/env python
# coding: utf-8

# # Ferrotech optimization problem.
# 
# A toy notebook to test different ideas for the width optimization problem. The input csv is taken from the Filtered excel file, essentially taking the output from the UI_inter program.
# 

# Library imports

# In[39]:


import pandas as pd
import numpy as np 
import UI_inter
import math




# In[18]:


def rounder(x, loadbar_pitch):

   divided_value = x/loadbar_pitch

   if divided_value - int(divided_value) < 0.4:
       return int(divided_value)
   else:
       return int(divided_value) + 1


# In[19]:


def newinput_checker(i):

   if i <= max_width:
       return i 
   else:
       return max_width






# In[21]:


def Area_calculator(df):

    df["Alternate_Width"] = df["WIDTH"]
    df.loc[df.Alternate_Width > max_width, "Alternate_Width"] = max_width
    df["Area"] = df["SPAN"]*df["Alternate_Width"]
    df = df.drop("Alternate_Width", axis = 1)
    return df





# Adding Weight

# In[23]:


def weight_adder(df):

    df["WEIGHT"] = df.ORIGINAL_SPAN*df.WIDTH*weight
    return df



# #  Optimizing and writing into optimized file

# Algorithm that optimizes, takes in required sum to optimize and input list of numbers and returns list of numbers that provide the maximum sum less than or equal to required sum.

# In[26]:


def check_sum(input_list, req_sum):
    '''
    Function that builds the dp table and returns the list of numbers that are optimum for given input list and required sum.
    '''
    dp_table = np.zeros((len(input_list)+1, req_sum + 1))
    dp_table[:, 0] = 1
    state_array = dp_table

    for i in range(1, len(input_list)+1):
        for j in range(req_sum+1):

            if input_list[i-1] > j:
                state_array[i, j] = state_array[i-1, j]
            else:
                state_array[i][j] = state_array[i-1, j-input_list[i-1]] or state_array[i-1, j]

 
    counter = 0

    for j in range(req_sum, -1, -1): 
        if counter == 0:
            for i in range(0, len(input_list) + 1):
                if counter == 0:
                    if state_array[i][j] == 1:
                        counter = 1
                        max_sum = j
                        numbers_in_the_list = i
                else:
                    break
        else:
            break
 
    numbers_in_the_list = input_list[numbers_in_the_list -1]
    list_of_numbers = []
    current_sum = max_sum
    flag = 0 
    while(current_sum!=0):

        if flag == 0:
            list_of_numbers.append(numbers_in_the_list)
            current_sum = current_sum - numbers_in_the_list
            flag+=1
        else:
            for i in range(1, len(input_list)+1):
                if(state_array[i][current_sum] == 1):
                    list_of_numbers.append(input_list[i-1])
                    current_sum = current_sum - input_list[i-1]
                    break


    return(max_sum, list_of_numbers)


# Adding Quantity

# In[27]:


def quantity_adder(new_df):
 
            new_df = new_df.groupby(new_df.columns.tolist()).size().reset_index().rename(columns = {0:"QUANTITY"})
            #print("post addition of qty \n\n")
            return new_df


# Function that rounds to the nearest 100

# In[40]:


def roundup_100(span_display):

    return int(math.ceil(span_display / 100.0)) * 100


#  Splitting dataframe based on returned list of numbers

# In[41]:


def df_maker(df_imported, numbers):
    '''
    This function takes as input the input dataframe and checks if span exists in the list of numbers given also as input. It returns a new dataframe with only the specified span values as given in input list of numbers.
    '''
    counter = 0
    len_of_frame = len(df_imported)
    for number in numbers:
        for i in range(len_of_frame):

            if df_imported.iloc[i].SPAN == number and counter == 0:
                new_df = df_imported.iloc[i:i+1]
                counter += 1
                df_imported = df_imported.drop(df_imported.index[i])
                break
            elif df_imported.iloc[i].SPAN == number and counter != 0:
                new_df = new_df.append(df_imported.iloc[i:i+1])
                df_imported = df_imported.drop(df_imported.index[i])
                break
    return new_df, df_imported


# Function to sort by required parameters
def type_writer(df_nested):

    df_nested = df_nested[df_nested['CUTTING_SPAN'].notna()]
    df_nested = df_nested.sort_values(by = ["TYPE", "DRAWING NO", "ERECTION_MARK"], ascending = False)
    df_nested = df_nested.reset_index(drop=True)
    df_nested.to_csv("sorted_nestings.csv")
    return df_nested

def excel_writer(final_df,  sortednest_df, input_file_name):

    writer = pd.ExcelWriter(input_file_name[0:-4] + "_optimized.xlsx", engine = 'xlsxwriter')

    final_df.to_excel(writer, sheet_name = "Nested_optimized")
    sortednest_df.to_excel(writer, sheet_name = "sorted by type")

    writer.save()



if __name__ == "__main__":

    df_original, loadbar_pitch, framebar_thickness, weight, input_file_name = UI_inter.main()

    # Defining input parameters.

    # In[13]:


    #loadbar_pitch = 30
    #framebar_thickness = 5
    #weight = 100
    panel_max_width = 1000
    max_sum = 5930
    threshold = 200



    # # Modifying the dataframe, adding required columns and duplicating rows

    # Adding original span and altering span value

    # In[16]:


    df_original["ORIGINAL_SPAN"] = df_original.SPAN
    df_original.SPAN = df_original.SPAN - 2*framebar_thickness


    # Creating new width

    


    max_width = int(panel_max_width/loadbar_pitch)*loadbar_pitch + framebar_thickness
    upper_bound = (int(panel_max_width/loadbar_pitch) + 0.4)*loadbar_pitch
    
    new_input_widths = [rounder(x,loadbar_pitch)*loadbar_pitch + framebar_thickness for x in df_original.WIDTH]
    new_input_widths = [newinput_checker(i) for i in new_input_widths]
    df_original["New_Widths"] = new_input_widths

    # Adding Area

    df_original = Area_calculator(df_original)

    # Adding Weight

    df_original = weight_adder(df_original)




    # Duplicatiing Quantity

    df_original = df_original.loc[df_original.index.repeat(df_original.QTY)]
    df_original = df_original.drop(['QTY'], axis=1)
    df_original = df_original.reset_index(drop=True)


    # Running the Algorithm and building optimized dataframe
    final_df = pd.DataFrame()
    all_new_widths = sorted(df_original.New_Widths.unique(), reverse=True)
    counter_for_widths = 0
    current_width_value = all_new_widths[counter_for_widths]
    df_current_width = df_original.loc[df_original.New_Widths == current_width_value]
    counter = 0
    sheet_no = 0
    while len(df_current_width) != 0:
        
        return_sum, list_of_spans = check_sum(list(df_current_width.SPAN), max_sum)
        length_percentage_wastage = (max_sum - return_sum)*100/max_sum
        
        
        if counter > 0 and length_percentage_wastage > 0:
            
            
            list_of_new_widths = df_current_width.New_Widths.unique()
            list_of_new_widths = list_of_new_widths[~np.isnan(list_of_new_widths)]
            difference_in_width = max(list_of_new_widths) - min(list_of_new_widths)
        
            if difference_in_width > threshold:
                
                new_df, df_current_width = df_maker(df_current_width, list_of_spans)
                new_df = new_df.reset_index(drop=True)
                sheet_no+=1
                new_df["PERCENTAGE_LENGTH_WASTAGE"] = length_percentage_wastage
                new_df["SHEET_NO"] = int(sheet_no) 
                if sum(new_df.SPAN) > 5600:
                    new_df["PANEL_SIZE"] = "{}X{}".format(6000, max(new_df.New_Widths))
                else:
                    new_df["PANEL_SIZE"] = "{}X{}".format(roundup_100(sum(new_df.SPAN)), max(new_df.New_Widths))
                    
                new_df = quantity_adder(new_df)
                
                new_df = new_df.append(pd.Series(), ignore_index=True)
                final_df = final_df.append(new_df)
                counter+=1
                
            elif difference_in_width <= threshold and  counter_for_widths < len(all_new_widths) - 1:
                
                counter_for_widths+=1
                current_width_value = all_new_widths[counter_for_widths]
                df_current_width = df_current_width.append(df_original.loc[df_original.New_Widths == current_width_value])
            
            else:
                
                new_df, df_current_width = df_maker(df_current_width, list_of_spans)
                new_df = new_df.reset_index(drop=True)
                sheet_no+=1
                new_df["PERCENTAGE_LENGTH_WASTAGE"] = length_percentage_wastage
                new_df["SHEET_NO"]=int(sheet_no)
                if sum(new_df.SPAN) > 5600:
                    new_df["PANEL_SIZE"] = "{}X{}".format(6000, max(new_df.New_Widths))
                else:
                    new_df["PANEL_SIZE"] = "{}X{}".format(roundup_100(sum(new_df.SPAN)), max(new_df.New_Widths))
                new_df = quantity_adder(new_df)
                new_df = new_df.append(pd.Series(), ignore_index=True)
                final_df = final_df.append(new_df)
                counter+=1
        
        else:
            
            new_df, df_current_width = df_maker(df_current_width, list_of_spans)
            new_df = new_df.reset_index(drop=True)
            sheet_no+=1
            new_df["PERCENTAGE_LENGTH_WASTAGE"] = length_percentage_wastage
            new_df["SHEET_NO"]=int(sheet_no)
            if sum(new_df.SPAN) > 5600:
                    new_df["PANEL_SIZE"] = "{}X{}".format(6000, max(new_df.New_Widths))
            else:
                    new_df["PANEL_SIZE"] = "{}X{}".format(roundup_100(sum(new_df.SPAN)), max(new_df.New_Widths))
            new_df = quantity_adder(new_df)
            new_df = new_df.append(pd.Series(), ignore_index=True)
            final_df = final_df.append(new_df)
            counter+=1
        
        if len(df_current_width) == 0 and not (len(df_original) == sum(final_df.dropna().QUANTITY)) :
            counter_for_widths+=1
            current_width_value = all_new_widths[counter_for_widths]
            df_current_width = df_current_width.append(df_original.loc[df_original.New_Widths == current_width_value])

    


    # Adding Difference when the width exceeds max_width

    # In[44]:


    final_df["ADD_WIDTH"] = final_df["WIDTH"] - final_df["New_Widths"]
    final_df.loc[final_df.WIDTH <= max_width, "ADD_WIDTH"] = np.nan


    # Adding into the preferred format, columns are placed in a specific order. Also, changing names of a few columns

    # In[50]:


    final_df["ORIGINAL_WIDTH"] = final_df["WIDTH"]
    final_df["CUTTING_SPAN"] = final_df["SPAN"]
    final_df["STD_WIDTH"] = final_df["New_Widths"]
    final_df["ORIGINAL_AREA"] = final_df["ORIGINAL_SPAN"]*final_df["ORIGINAL_WIDTH"]/10**6   
    final_df["WEIGHT"] = final_df["WEIGHT"]/10**6


    final_df = final_df.drop(["WIDTH", "SPAN", "New_Widths", "Area"], axis = 1)
        #df = df[["DRAWING NO", "ERECTION_MARK", "TYPE", "ORIGINAL_SPAN", "ORIGINAL_WIDTH", "CUTTING_SPAN", "STD_WIDTH", "QUANTITY", "ORIGINAL_AREA","WEIGHT", "PANEL_SIZE", "SHEET_NO", "Area_percentage_wastage", "ADD_WIDTH"]]
    if "TOE PLATE LENGTH" in final_df.columns:
        final_df = final_df[["DRAWING NO", "ERECTION_MARK", "TYPE", "ORIGINAL_SPAN", "ORIGINAL_WIDTH", "CUTTING_SPAN", "STD_WIDTH", "QUANTITY", "ORIGINAL_AREA","WEIGHT", "TOE PLATE LENGTH", "PANEL_SIZE", "SHEET_NO", "PERCENTAGE_LENGTH_WASTAGE","ADD_WIDTH"]]
    else:
        final_df = final_df[["DRAWING NO", "ERECTION_MARK", "TYPE", "ORIGINAL_SPAN", "ORIGINAL_WIDTH", "CUTTING_SPAN", "STD_WIDTH", "QUANTITY", "ORIGINAL_AREA","WEIGHT", "PANEL_SIZE", "SHEET_NO", "PERCENTAGE_LENGTH_WASTAGE","ADD_WIDTH"]]

    
    # Creating a sorted list based on requirments

    sortednest_df = type_writer(final_df)        


    # Outputting the optimized dataframe and removing from original dataframe

    # In[49]:


    final_df.to_csv(input_file_name[0:-4] + "_optimized.csv")

    excel_writer(final_df, sortednest_df, input_file_name)






