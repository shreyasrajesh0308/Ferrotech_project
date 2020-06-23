import numpy as np
import pandas as pd
import random
import os

def df_maker(df, numbers):
    
    counter = 0
    for number in numbers:
        for i in range(len(df)):
            if df.iloc[i].SPAN == number and counter == 0:
                new_df = df.iloc[i:i+1]
                counter+=1
                break
            elif df.iloc[i].SPAN == number and counter!=0:
                new_df = new_df.append(df.iloc[i:i+1])
                break
            
    return new_df
def modifier(main_list, sub_list):

    for number in sub_list:
        main_list.remove(number)

    return main_list

def check_sum(input_list, req_sum, state_array):

    # print(state_array)

    for i in range(1, len(input_list)+1):
        for j in range(req_sum+1):

            if input_list[i-1] > j:
                state_array[i, j] = state_array[i-1, j]
            else:
                # state_array[i][j] = max_finder(state_array, i, j, req_sum, input_list)
                state_array[i][j] = state_array[i-1, j-input_list[i-1]] or state_array[i-1, j]

    # print(state_array)
 
    counter = 0

    for j in range(req_sum, -1, -1): 
        if counter == 0:
            for i in range(0, len(input_list) + 1):
                if counter == 0:
                    if state_array[i][j] == 1:
                        counter = 1
                        # print("The maximum number is {}".format(j))
                        max_sum = j
                        numbers_in_the_list = i
                else:
                    break
        else:
            break
    
    # print(max_sum, input_list[numbers_in_the_list - 1])
    numbers_in_the_list = input_list[numbers_in_the_list -1]
    list_of_numbers = []
    current_sum = max_sum
    flag = 0 
    while(current_sum!=0):

        # print(current_sum)
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

    # print("The list that gives the numbers is {}".format(list_of_numbers))

    print(max_sum)
    print(list_of_numbers)
    return(max_sum, list_of_numbers)

#if __name__ == "__main__":
def input_function(input_df, req_sum, sheet_number, input_width_value):
    # input_list = list(map(int, input().split()))

    #input_list = [random.randint(1,500) for _ in range(100)]
    number_of_sheets = 0
    # input_list = [3,4,5,7]*4
    input_list = list(input_df["SPAN"])
    print("The input list of lengths is {}".format(input_list))
    #req_sum = 1500 
    cumulative_wastage = 0
    initial_list = input_list.copy()
    while(len(input_list)!=0):
        dp_table = np.zeros((len(input_list)+1, req_sum + 1))
        dp_table[:, 0] = 1

        max_sum, list_of_numbers = check_sum(input_list, req_sum, dp_table)
        percentage_wastage = ((req_sum - max_sum)/req_sum) * 100
        percentage_wastage = round(percentage_wastage,2)
        cumulative_wastage += percentage_wastage
        input_df = input_df.reset_index(drop=True)
        new_df = df_maker(input_df, list_of_numbers)
        # new_df = input_df[input_df["SPAN"].isin(list_of_numbers)]
        print(new_df)
        # new_df = new_df.set_index("Sheet_no", append=True).swaplevel(0,1)
        new_df = new_df.sort_values(by = ["SPAN"], ascending = True)
        dups = new_df.pivot_table(index = ["SPAN", "ERECTION_MARK", "WIDTH"], aggfunc='size')
        new_df = new_df.drop_duplicates()
        print(len(new_df))
        print(len(dups))
        print(new_df)
        print(dups)
        new_df["Quantity"] = list(dups)
        new_df["Dimensions"] = ["{}x{}".format(req_sum, input_width_value)]*len(new_df)
        new_df["Sheet_no"] = [sheet_number + number_of_sheets]*len(new_df)
        new_df["wastage"] = [percentage_wastage]*len(new_df) 


        new_df = new_df.append(pd.Series(), ignore_index=True)
        new_df = new_df.drop(columns=new_df.columns[0])

        if not os.path.isfile("optimized.csv"):
            new_df.to_csv("optimized.csv", header='column_names')
        else:
            new_df.to_csv("optimized.csv", mode='a', header=False)

        number_of_sheets+=1

        print("For sheet number {}, the maximum length is {}, the percentage wastage is {}% and the lengths that give that sum is {}".format(number_of_sheets, max_sum, percentage_wastage, list_of_numbers))
        input_list = modifier(input_list, list_of_numbers)
        if len(input_list) == 0:
            print("The total number of sheets is {}".format(number_of_sheets))
        # print(input_list)

    total_wastage = req_sum*number_of_sheets - sum(initial_list)
    total_wastage_percentage = total_wastage/(req_sum*number_of_sheets)
    print("\n The total wastage is {}%".format(total_wastage_percentage*100))

    return number_of_sheets 

