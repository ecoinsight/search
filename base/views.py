from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows',None)
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive',]
credentials=ServiceAccountCredentials.from_json_keyfile_name("lumigent-f618e674b8ed.json",scope)
client=gspread.authorize(credentials) # autorizes the json file having credentials


sheet=client.open("Copy of searchpo") # accessing "Maintenance tracker 2022" using open() method of gspread sheets
data=sheet.worksheet(".csv").get_all_values() #gets all the cell values with row(0....) and column indexes (0...) from "all" work sheet
data_all=pd.DataFrame(data) # converting to data frame
data_all.columns=data_all.iloc[0] # sets 0th row index of the spreadsheet to column headers  
df=data_all.loc[1:] # dropping 0th row index of the spreadsheet

# data_csv = pd.read_csv(r"C:\Users\Dell\OneDrive\Desktop\Personal\projects\py_projects\searchengine\Rabweb-Export.csv")
# df = pd.DataFrame(data_csv)
df = df.fillna("")

def main_page(request):
    return render(request,'main_page.html')

def search(request):
    po_input = request.GET['PO Number']
    brand_input = request.GET['Brand']
    if po_input == '' and brand_input == '':
        df_filt_po_brand = df[['PO','OEMname','Status','Quantity Ordered','QTY Shipped','Tracking Number']]
        html = df_filt_po_brand.to_html()
        text_file = open(r"C:\Users\Dell\searchengine\templates\searchengine.html", "w")
        text_file.write(html)
        text_file.close()

    elif po_input=="" and brand_input!='':
        filt_po_brand = df['OEMname'] == brand_input
        df_filt_po_brand = df.loc[filt_po_brand,['PO','OEMname','Status','Quantity Ordered','QTY Shipped','Tracking Number']]
        html = df_filt_po_brand.to_html()
        text_file = open(r"C:\Users\Dell\searchengine\templates\searchengine.html", "w")
        text_file.write(html)
        text_file.close()   
    
    elif po_input!="" and brand_input =="":
        filt_po_brand = df['PO'] == po_input
        df_filt_po_brand = df.loc[filt_po_brand,['PO','OEMname','Status','Quantity Ordered','QTY Shipped','Tracking Number']]
        html = df_filt_po_brand.to_html()
        text_file = open(r"C:\Users\Dell\searchengine\templates\searchengine.html", "w")
        text_file.write(html)
        text_file.close()

    elif po_input!="" and brand_input!="":
        filt_po_brand = (df['PO'] == po_input) & (df['OEMname'] == brand_input)
        df_filt_po_brand = df.loc[filt_po_brand,['PO','OEMname','Status','Quantity Ordered','QTY Shipped','Tracking Number']]
        html = df_filt_po_brand.to_html()
        text_file = open(r"C:\Users\Dell\searchengine\templates\searchengine.html", "w")
        text_file.write(html)
        text_file.close()


    return render(request,'search.html')


