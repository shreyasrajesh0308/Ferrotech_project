import numpy as np
import pandas as pd
import os


def df_maker(df_imported, numbers):
    '''
    This function takes as input the input dataframe and checks if span exists in the list of numbers given also as input. It returns a new dataframe with only the specified span values as given in input list of numbers.
    '''
    counter = 0
    len_of_frame = len(df_imported)
    for number in numbers:
        for i in range(len_of_frame):
            #print(i)
            if df_imported.iloc[i].SPAN == number and counter == 0:
                new_df = df_imported.iloc[i:i+1]
                counter += 1
                df_imported.drop(df_imported.index[i], inplace = True)
                break
            elif df_imported.iloc[i].SPAN == number and counter != 0:
                new_df = new_df.append(df_imported.iloc[i:i+1])
                df_imported.drop(df_imported.index[i], inplace = True)
                break
    return new_df


def modifier(main_list, sub_list):
    '''
    Function to remove contents of one list from another
    '''
    for number in sub_list:
        main_list.remove(number)

    return main_list

def check_sum(input_list, req_sum, state_array):
    '''
    Function that builds the dp table and returns the list of numbers that are optimum for given input list and required sum.
    '''

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

def input_function(input_df, req_sum, sheet_number, input_width_value):
    '''
    Main function that takes in the input dataframe and outputs the optimized csv file, this function is called from the main problem
    '''

    number_of_sheets = 0
    input_list = list(input_df["SPAN"])
    cumulative_wastage = 0
    initial_list = input_list.copy()
    print("THIS IS THE NEW DATAFRAME BOOM \n")
    print(input_df)
    max_area = req_sum*input_width_value

    while(len(input_list)!=0):

        Area_sum = 0
        dp_table = np.zeros((len(input_list)+1, req_sum + 1))
        dp_table[:, 0] = 1

        max_sum, list_of_numbers = check_sum(input_list, req_sum, dp_table)
        percentage_wastage = ((req_sum - max_sum)/req_sum) * 100
        percentage_wastage = round(percentage_wastage,2)
        cumulative_wastage += percentage_wastage
        input_df = input_df.reset_index(drop=True)
        new_df = df_maker(input_df, list_of_numbers)
        Area_sum = sum(new_df["Area"])

        new_df = new_df.sort_values(by = ["SPAN"], ascending = True)
        dups = new_df.pivot_table(index = ["DRAWING NO","SPAN", "ERECTION_MARK", "WIDTH"], aggfunc='size')
        new_df = new_df.drop_duplicates()
        total_area_percentage = (max_area - Area_sum)*100 / max_area


        new_df["Quantity"] = list(dups)
        new_df["Dimensions"] = ["{}x{}".format(req_sum, input_width_value)]*len(new_df)
        new_df["Sheet_no"] = [sheet_number + number_of_sheets]*len(new_df)
        new_df["wastage"] = [percentage_wastage]*len(new_df) 
        new_df["Area_Wastage"] = [total_area_percentage]*len(new_df)
        new_df = new_df.drop(["Area"], axis = 1 )

        new_df = new_df.append(pd.Series(), ignore_index=True)
        #new_df = new_df.drop(columns=new_df.columns[0])

        if not os.path.isfile("optimized.csv"):
            new_df.to_csv("optimized.csv", header='column_names')
        else:
            new_df.to_csv("optimized.csv", mode='a', header=False)

        number_of_sheets+=1

        input_list = modifier(input_list, list_of_numbers)

    total_wastage = req_sum*number_of_sheets - sum(initial_list)
    total_area_percentage = (max_area - Area_sum)*100 / max_area
    total_wastage_percentage = total_wastage/(req_sum*number_of_sheets)

    return number_of_sheets 

