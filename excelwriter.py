import pandas as pd 
from pathlib import Path 


def write_to_excel():

    df_nested = pd.read_csv("optimized.csv", index_col=0)
    df_unnested = pd.read_csv("optimized_unnested.csv", index_col=0)
    df_sortednest = pd.read_csv("sorted_nestings.csv", index_col=0)

    writer = pd.ExcelWriter("Final_optimized.xlsx", engine = 'xlsxwriter')

    df_nested.to_excel(writer, sheet_name = "Nested_optimized")
    df_unnested.to_excel(writer, sheet_name = "Unnested")
    df_sortednest.to_excel(writer, sheet_name = "sorted by type")

    writer.save()

if __name__ == "__main__":

    write_to_excel()  
