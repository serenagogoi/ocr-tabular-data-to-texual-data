from cProfile import label
import sys
import numpy as np
from cv2 import *
import time
import os
import threading
import pytesseract
import imutils
import cv2
from tkinter import *
from PIL import Image
from tabula.io import read_pdf
import tabula
import pandas as pd
import ocrmypdf
import cx_Oracle
from random import random
import connect_trainee
import random



con = cx_Oracle.connect('trainee/trainee@10.203.187.51/epijrt')
def image_convert(img_path):
     # Read image using opencv
    #img_path = r"C:\img_txt\internship_project\images\img3.jpg"
    file_name = os.path.basename(img_path)
    # file name without extension
    filename =os.path.splitext(file_name)[0]
    img = cv2.imread(img_path)
   # Extract the file name without the file extension
    file_name = os.path.splitext(img_path)[0]
    #file_name = file_name
#print(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #Removing Shadows

    rgb_planes = cv2.split(img)
    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:

        dilated_img = cv2.dilate(plane, np.ones((7,7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        result_planes.append(diff_img)
    img = cv2.merge(result_planes)

#Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)#increases the white region in the image 
    img = cv2.erode(img, kernel, iterations=1) #erodes away the boundaries of foreground object

# Apply threshold to get image with only b&w (binarization)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    img = cv2.imwrite(r'C:\img_txt\internship_project\images\1.png',img)

#image to pdf
    img = Image.open(r'C:\img_txt\internship_project\images\1.png')
    img_pfd = img.save(r'C:\img_txt\internship_project\images\1.pdf')

#image pdf to text pdf
    def scannedPdfConverter(file_path, save_path):
        ocrmypdf.ocr(file_path, save_path, skip_text=True)
        print('File converted successfully!')

    file_path = r'C:\img_txt\internship_project\images\1.pdf'
    save_path =r'C:\img_txt\internship_project\images\11.pdf'
    scannedPdfConverter(file_path, save_path)

# text pdf to csv file 
    df = tabula.read_pdf(r'C:\img_txt\internship_project\images\11.pdf', pages='all')[0]
    df1 = pd.DataFrame(df)
    df1.to_csv(r'C:\img_txt\internship_project\images\11.csv', index=False)
    #df1.to_html()


    

#removing unnecessary files 
    os.remove(r"C:\img_txt\internship_project\images\1.pdf")
    os.remove(r"C:\img_txt\internship_project\images\1.png")
    os.remove(r"C:\img_txt\internship_project\images\11.pdf")

    df2=pd.read_csv(r'C:\img_txt\internship_project\images\11.csv')
    df3 = df2.convert_dtypes(convert_string=True)
    #print(df3.dtypes)
    df3.rename(columns = {'R,':'Rt'}, inplace = True)
    df3.rename(columns = {'PIGN(®,)':'PIGN'}, inplace = True)
    cursor=con.cursor()
    #print("you are connected")
    #create table 
    num_cols = len(df3.axes[1])
    print(num_cols)
    tablenumber = random.randrange(1,999)
    query = "CREATE TABLE tdata{} (".format(tablenumber)
    for name in range(0, num_cols):
        query += "{} varchar(20), ".format(df3.columns[name])
    query =query.rstrip(" ,")
    query += ")"
    #print(query)
    cursor.execute(query)
    print("table is created")
    #inert data in table 
    query1 = "INSERT INTO tdata{} (".format(tablenumber)
    print(tablenumber)
    for name in range(0, num_cols):
        query1 += "{} , ".format(df3.columns[name])
    query1 =query1.rstrip(" ,")
    query1 += ") VALUES "

    tb = ""


    for i , row in df3.iterrows():
        val  = tuple(row)
        tb = query1 + "{}".format(val)
        cursor.execute(tb)
        con.commit()
    query2= "SELECT * From tdata{}".format(tablenumber)
    #cursor.execute(query2)
    #im = cursor.fetchall()
    #rows = []
    
    #window = tk.Tk()
    #window.title = ("table")

    """for x in range(0,len(df3)):
        for y in range(0, num_cols):
            frame = th.Frame(master=window,relief=tk.RAISED,borderwidth=1)
            frame.grid(row=x,column=y)
            label = tk.label(master=frame, text=f"\n\nrow {x}\t\t column {y}\n\n")
            label.pack"""
    df4 = pd.read_sql_query(query2, con=con)
    df5 = pd.DataFrame(df4)
    html = df5.to_html()

    htmltext = open(r"C:\img_txt\internship_project\templates\index.html","w")
    htmltext.write(html)
    htmltext.close()
    #append the file name of the original image 
    filename_suffix = 'csv'
    new_path = os.path.join(r'C:\img_txt\internship_project\image', filename + '.' + filename_suffix)
    source= r'C:\img_txt\internship_project\images\11.csv'
    os.rename(source, new_path)
    #os.remove(r"C:\img_txt\internship_project\images\11.csv")


    






  






