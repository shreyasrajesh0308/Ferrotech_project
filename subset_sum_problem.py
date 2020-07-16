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

def quantity_adder(new_df):
 
            new_df = new_df.groupby(new_df.columns.tolist()).size().reset_index().rename(columns = {0:"Quantity"})
            #print("post addition of qty \n\n")
            #print(new_df)
            return new_df

def input_function(input_df, req_sum, input_width_value, Area_sum, old_df = []):
    '''
    Main function that takes in the input dataframe and outputs the optimized csv file, this function is called from the main problem
    '''

    input_list = list(input_df["SPAN"])
    return_df = 0
    min_sum = 0
    if len(old_df) != 0:
        min_sum = min(input_df.SPAN)
    while(len(input_list)!=0):


        dp_table = np.zeros((len(input_list)+1, req_sum + 1))
        dp_table[:, 0] = 1
        max_sum, list_of_numbers = check_sum(input_list, req_sum, dp_table)
        if len(list_of_numbers) == 0 and len(input_list) != 0 :

            print("list of numbers {}, input list{}".format(list_of_numbers, input_list))
            dp_table = np.zeros((len(input_list)+1, 5930 + 1))
            dp_table[:, 0] = 1
            max_sum, list_of_numbers = check_sum(input_list, 5930, dp_table)
        print("For sum {} the list of numbers are {}".format(max_sum, list_of_numbers))

        if len(list_of_numbers) != 0:

            input_df = input_df.reset_index(drop=True)
            if len(old_df) == 0:
                new_df = df_maker(input_df, list_of_numbers)
                new_df = new_df.reset_index(drop=True)
                new_df = quantity_adder(new_df)
            else:
                inter_df = df_maker(input_df, list_of_numbers)
                inter_df = inter_df.reset_index(drop=True)
                inter_df = quantity_adder(inter_df)

                old_df = old_df.append(inter_df, ignore_index = True, sort = False)
                new_df = old_df

            Area_sum =  sum(new_df["Area"]*new_df["Quantity"])
            max_area = new_df.loc[0, "New_Widths"]*5930
            new_df["DIMENSIONS"] = "{}X{}".format(5930, int(new_df.loc[0, "New_Widths"]))

            # print("New Sheet: \n \n \n")
            # print(new_df)
            # print(" \n \n \n")
            #
            total_area_percentage = (max_area - Area_sum)*100 / max_area
            print("Wastage area percentage is {}".format(total_area_percentage))

            if total_area_percentage >= 10:
                 req_sum = 5930 - sum(new_df["SPAN"]*new_df["Quantity"])
                 return_df = 1
                 new_df["Area_percentage_wastage"] = [total_area_percentage]*len(new_df)

                 if req_sum < min_sum:
                     new_df["Area_percentage_wastage"] = [total_area_percentage]*len(new_df)
                     req_sum = 5930
                     Area_sum = 0
                     return_df = 0
                     old_df = []
                     new_df = new_df.append(pd.Series(), ignore_index=True)

                     if not os.path.isfile("optimized.csv"):
                        new_df.to_csv("optimized.csv", header='column_names')
                     else:
                        new_df.to_csv("optimized.csv", mode='a', header=False)
            else:
                 new_df["Area_percentage_wastage"] = [total_area_percentage]*len(new_df)
                 req_sum = 5930
                 Area_sum = 0
                 return_df = 0
                 old_df = []


            if total_area_percentage < 10:
                new_df = new_df.append(pd.Series(), ignore_index=True)

                if not os.path.isfile("optimized.csv"):
                    new_df.to_csv("optimized.csv", header='column_names')
                else:
                    new_df.to_csv("optimized.csv", mode='a', header=False)


            input_list = modifier(input_list, list_of_numbers)

        else:
            if return_df == 0:
                 req_sum = 5930
                 Area_sum = 0
                 return_df = 0
                 old_df = []
                 return  req_sum, Area_sum, []
            else:
                return req_sum, Area_sum, new_df

    if return_df == 0:
        return  req_sum, Area_sum, []
    else:
        return req_sum, Area_sum, new_df

