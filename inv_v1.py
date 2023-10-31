import pandas as pd
import bigcommerce
from tkinter import *
from tkinter import filedialog
import tkinter as tk
from tkinter import ttk
import os
from tkinter import messagebox
from threading import *


window = Tk()
window.title('H2O-Warehouse Update')
window.geometry('500x300')

frm = ttk.Frame(window,borderwidth=0, relief='raised', padding=(10, 10, 10, 10))
frm.grid(column=3,row=5)

txtfrm = ttk.Frame(window,borderwidth=0, relief='raised', padding=(10, 10, 10, 10))
txtfrm.grid(column=3,row=1)

# progressbar = ttk.Progressbar(frm, orient='horizontal', mode='indeterminate', length=280)
# progressbar.grid(column=0,row=0,padx=0,pady=0)

def threading(): 
    # Call work function 
    t1=Thread(target=run) 
    t1.start()

def upload_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        # Get the file name
        global file_name
        file_name = file_path.split("/")[-1]
        global destination_directory
        destination_directory = "input"
        # Get the destination directory
        if os.path.exists(destination_directory):
            pass
        else:
            os.mkdir(destination_directory)
        

        # Save the file to the destination directory
        with open(f"{destination_directory}/{file_name}", "wb") as f:
            with open(file_path, "rb") as f_src:
                f.write(f_src.read())

liFrame =ttk.Frame(window, width=10,height=10)
liFrame.grid(column = 0, row = 2, padx=10,pady=10)
scrollbar = ttk.Scrollbar(liFrame)
theList = tk.Listbox(liFrame,width=50,heigh=15,yscrollcommand=scrollbar.set)
scrollbar.configure(command=theList.yview)
theList.pack (side="left")
scrollbar.pack(side="right", fill="y")       



#funtion to use the uploaded file to run the inventory updates
def run():
    
    # progressbar.grid(column=0, row=5, padx=0, pady=0)
    df = pd.read_excel(f"{destination_directory}/{file_name}")
    # print(file_name)
    
    skus=list(df['Item.Number'])
    inventory = list(df['Item.Total On Hand Qty API'])
    ctrl=len(skus)==len(inventory)
    step_val=100/len(skus)
    # print(ctrl)
    diction={}
    #To check if the number rows in sku and inventory are same if not then theres a duplicate SKU present
    if ctrl==True: 
        diction = {key: value for key, value in zip(skus, inventory)}

    api = bigcommerce.api.BigcommerceApi(client_id='e2e79uybfwdi226lvr7afi8uor7jwig', store_hash='gnuypjm22u', access_token='a9v8tzqdfjhtw2q4paaemrgwuqvd854')

    if ctrl==True:
      text="Success!! \n Error listed below : \n"
      # progressbar.start()
      for key in diction:
          window.update()
          try:
              print('Updating stock qty of ',key)
              k='Updating stock qty of ',key
              # progressbar.step()
              p=api.Products.all(sku=key)[0]
              id=p['id']
              api.Products.get(id).update(inventory_tracking='simple')
              api.Products.get(id).update(inventory_level=diction[key])
              theList.insert('end',k)   
          except KeyError:
            # progressbar.step()
            k=f'sku: {key} not found in Bigcommmerce product list'
            text=text+f'sku: {key} not found in Bigcommmerce product list \n'
            theList.insert('end',k) 
          except:
            #   progressbar.stop()
              print('some error') 

          # progressbar['value']+=step_val
          # progressbar.update_idletasks()
    #   progressbar.grid_forget()
      messagebox.showinfo(title="Information", message=text)
        
    else:
      print('Please check if all skus have accurate number of quantities mentioned')
      # progressbar.stop()
    #   progressbar.grid_forget()
      messagebox.showinfo(title="Information", message='Please check if all skus have accurate number of quantities mentioned')
    frm.grid_forget()  
    




file_upload_button=tk.Button(window, text="Upload File", command=upload_file).grid(column = 0,row=0,padx=10,pady=0)
# file_upload_button.pack()
execute_button = tk.Button(window , text="RUN", command=threading).grid(column = 1,row=0,padx=0,pady=0)
# execute_button.pack()



window.mainloop()

