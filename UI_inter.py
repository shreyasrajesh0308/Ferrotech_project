#imports
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

import pandas as pd
import math
import regex as re

root = tk.Tk()
#defines a window
canvas1 = tk.Canvas(root, width=600, height=800, bg='lightsteelblue')
canvas1.pack()

#input the excel sheet
# def getExcel():
#     global data
#     import_file_path = filedialog.askopenfilename()
#     data = pd.read_excel(import_file_path)
#
#pre-processing data
def get_save_Excel():
    
    global data, import_file_path
    import_file_path = filedialog.askopenfilename()
    data = pd.read_excel(import_file_path)


    global df
    df=pd.DataFrame()
    global col 
    global row
    col=len(data.columns)
    row=len(data.index)
    arr_str=["TYPE",  "DRAWING NO", "ERECTION MARK", "SPAN (mm)", "WIDTH (mm)", "QTY (Nos)", "TOE PLATE LENGTH"]
    for f in range(len(arr_str)):
        for j in range(col):
            for i in range(row):
                if(data.iloc[i, j]== arr_str[f]):
                    df[arr_str[f]]= data.iloc[i+1 :row, j]
    df = df[df['SPAN (mm)'].notna()]
    df = df.fillna(0)
    #df = df.dropna()

    df.reset_index(drop=True, inplace=True)
    df.index += 1 
    df = df.rename(columns={'ERECTION MARK' : 'ERECTION_MARK', 'SPAN (mm)' : 'SPAN', 'WIDTH (mm)' : 'WIDTH', 'QTY (Nos)' : 'QTY'})
    #export_file_path= 'Filtered_file.xlsx'
    #df.to_excel(export_file_path)

#save and exit button
def save():
    global lb_pitch
    lb_pitch = str(entry1.get())
    lb_pitch = int(lb_pitch)
    global frame_bar
    frame_bar= str(entry2.get())
    frame_bar = int(frame_bar)
    global weight
    weight = str(entry3.get())
    weight = float(weight)
    global max_sum 
    max_sum = str(entry4.get())
    max_sum = int(max_sum)
    root.destroy()

#button definition
def main():
    # Main Function 

    browseButton_Excel = tk.Button(text='Import Excel File', command=get_save_Excel, bg='white', fg='black', font=('times', 40, 'bold'))
    #browseButton_Excel_2 = tk.Button(text='Search Excel File', command=search, bg='white', fg='black', font=('times', 40, 'bold'))
    browseButton_Excel_3 = tk.Button(text='Save & Exit', command=save, bg='white', fg='black', font=('times', 30, 'bold'))

    #text_field definition
    global entry1, entry2, entry3, entry4
    entry1 = tk.Entry(root)
    label1 = tk.Label(root, text = 'LB Pitch', bg = 'lightsteelblue', font = ('times', 20, 'bold'))
    entry2 = tk.Entry(root)
    label2 = tk.Label(root, text = 'Frame Bar', bg = 'lightsteelblue', font = ('times', 20, 'bold'))
    entry3 = tk.Entry(root)
    label3 = tk.Label(root, text = 'Weight_sqmeter', bg = 'lightsteelblue', font = ('times', 20, 'bold'))
    entry4 = tk.Entry(root)
    label4 = tk.Label(root, text = 'Max Length', bg = 'lightsteelblue', font = ('times', 20, 'bold'))

    #creating a window
    canvas1.create_window(300, 100, window=browseButton_Excel)
    #canvas1.create_window(300, 300, window=browseButton_Excel_2)
    canvas1.create_window(400, 500, window=entry1)
    canvas1.create_window(200, 500, window=label1)
    canvas1.create_window(400, 600, window=entry2)
    canvas1.create_window(200, 600, window=label2)
    canvas1.create_window(400, 400, window=entry3)
    canvas1.create_window(200, 400, window=label3)
    canvas1.create_window(400, 200, window=entry4)
    canvas1.create_window(200, 200, window=label4)
    canvas1.create_window(300, 700, window=browseButton_Excel_3)

    root.mainloop()
    return df, lb_pitch,frame_bar, weight, max_sum,  import_file_path
