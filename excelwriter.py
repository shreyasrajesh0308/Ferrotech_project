import pandas as pd 
from pathlib import Path 

def col_modification(df):

    cols = df.columns.to_list()
    
    df["ORIGINAL_WIDTH"] = df["WIDTH"]
    df["CUTTING_SPAN"] = df["SPAN"]
    df["STD_WIDTH"] = df["New_Widths"]
    df["ORIGINAL_AREA"] = df["ORIGINAL_SPAN"]*df["ORIGINAL_WIDTH"]/10**6
    df["PANEL_SIZE"] = df["DIMENSIONS"]
    df["QUANTITY"] = df["Quantity"]
    df["SHEET_NO"] = df["sheet_no"]
    df["WEIGHT"] = df["WEIGHT"]/10**6
    #df["ADD_WIDTH"] = df["DIFFERENCE"]

    df = df.drop(["WIDTH", "SPAN", "New_Widths", "Area", "DIMENSIONS", "Quantity", "sheet_no"], axis = 1)
    #df = df[["DRAWING NO", "ERECTION_MARK", "TYPE", "ORIGINAL_SPAN", "ORIGINAL_WIDTH", "CUTTING_SPAN", "STD_WIDTH", "QUANTITY", "ORIGINAL_AREA","WEIGHT", "PANEL_SIZE", "SHEET_NO", "Area_percentage_wastage", "ADD_WIDTH"]]
    df = df[["DRAWING NO", "ERECTION_MARK", "TYPE", "ORIGINAL_SPAN", "ORIGINAL_WIDTH", "CUTTING_SPAN", "STD_WIDTH", "QUANTITY", "ORIGINAL_AREA","WEIGHT", "PANEL_SIZE", "SHEET_NO", "Area_percentage_wastage",]]
    return df

def write_to_excel():

    df_nested = pd.read_csv("optimized.csv", index_col=0)
    df_nested = col_modification(df_nested)
    #df_unnested = pd.read_csv("optimized_unnested.csv", index_col=0)
    #df_unnested = col_modification(df_unnested)
    df_sortednest = pd.read_csv("sorted_nestings.csv", index_col=0)
    df_sortednest = col_modification(df_sortednest)

    writer = pd.ExcelWriter("Final_optimized.xlsx", engine = 'xlsxwriter')

    df_nested.to_excel(writer, sheet_name = "Nested_optimized")
    #df_unnested.to_excel(writer, sheet_name = "Unnested")
    df_sortednest.to_excel(writer, sheet_name = "sorted by type")

    writer.save()

if __name__ == "__main__":

    write_to_excel()  
