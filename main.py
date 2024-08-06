# import modules 
from tkinter import *
from tkinter import ttk
import datetime as dt
from mydb import *
from tkinter import messagebox

# object for database
data = Database(db='test.db')

# global variables
count = 0
selected_rowid = 0

# functions
def saveRecord():
    global data
    data.insertRecord(item_name=item_name.get(), item_price=item_amt.get(), purchase_date=transaction_date.get())
    refreshData()
    clearEntries()

def setDate():
    date = dt.datetime.now()
    dopvar.set(f'{date:%d %B %Y}')

def clearEntries():
    item_name.delete(0, 'end')
    item_amt.delete(0, 'end')
    transaction_date.delete(0, 'end')

def fetch_records():
    global count
    f = data.fetchRecord('select rowid, * from expense_record')
    for rec in f:
        tv.insert(parent='', index='0', iid=count, values=(rec[0], rec[1], rec[2], rec[3]))
        count += 1

def select_record(event):
    global selected_rowid
    selected = tv.focus()
    val = tv.item(selected, 'values')
    try:
        selected_rowid = val[0]
        d = val[3]
        namevar.set(val[1])
        amtvar.set(val[2])
        dopvar.set(str(d))
    except Exception as ep:
        pass

def update_record():
    global selected_rowid
    selected = tv.focus()
    try:
        data.updateRecord(namevar.get(), amtvar.get(), dopvar.get(), selected_rowid)
        tv.item(selected, text="", values=(namevar.get(), amtvar.get(), dopvar.get()))
        refreshData()
        clearEntries()
    except Exception as ep:
        messagebox.showerror('Error', ep)

def totalBalance():
    f = data.fetchRecord(query="Select sum(item_price) from expense_record")
    for i in f:
        for j in i:
            messagebox.showinfo('Current Balance', f"Total Expense: {j}\nBalance Remaining: {5000 - j}")

def refreshData():
    for item in tv.get_children():
        tv.delete(item)
    fetch_records()
    
def deleteRow():
    global selected_rowid
    data.removeRecord(selected_rowid)
    refreshData()
    clearEntries()

# create tkinter object
ws = Tk()
ws.title('Daily Expenses')
ws.geometry('800x600')
ws.config(bg='#F0F0F0')

# variables
f = ('Arial', 14)
namevar = StringVar()
amtvar = IntVar()
dopvar = StringVar()

# Frame widgets
frame1 = Frame(ws, bg='#F0F0F0', padx=10, pady=10)
frame1.pack(fill=X, pady=10)

frame2 = Frame(ws, bg='#F0F0F0', padx=10, pady=10)
frame2.pack(fill=BOTH, expand=True)

# Label widgets
Label(frame1, text='ITEM NAME', font=f, bg='#F0F0F0').grid(row=0, column=0, sticky=W, pady=5)
Label(frame1, text='ITEM PRICE', font=f, bg='#F0F0F0').grid(row=1, column=0, sticky=W, pady=5)
Label(frame1, text='PURCHASE DATE', font=f, bg='#F0F0F0').grid(row=2, column=0, sticky=W, pady=5)

# Entry widgets
item_name = ttk.Entry(frame1, font=f, textvariable=namevar)
item_amt = ttk.Entry(frame1, font=f, textvariable=amtvar)
transaction_date = ttk.Entry(frame1, font=f, textvariable=dopvar)

# Entry grid placement
item_name.grid(row=0, column=1, sticky=EW, padx=(10, 0))
item_amt.grid(row=1, column=1, sticky=EW, padx=(10, 0))
transaction_date.grid(row=2, column=1, sticky=EW, padx=(10, 0))

# Action buttons
cur_date = ttk.Button(frame1, text='Current Date', command=setDate, width=15)
submit_btn = ttk.Button(frame1, text='Save Record', command=saveRecord)
clr_btn = ttk.Button(frame1, text='Clear Entry', command=clearEntries)
quit_btn = ttk.Button(frame1, text='Exit', command=ws.destroy)
total_bal = ttk.Button(frame1, text='Total Balance', command=totalBalance)
update_btn = ttk.Button(frame1, text='Update', command=update_record)
del_btn = ttk.Button(frame1, text='Delete', command=deleteRow)

# Button grid placement
cur_date.grid(row=3, column=1, sticky=EW, padx=(10, 0), pady=5)
submit_btn.grid(row=0, column=2, sticky=EW, padx=(10, 0), pady=5)
clr_btn.grid(row=1, column=2, sticky=EW, padx=(10, 0), pady=5)
quit_btn.grid(row=2, column=2, sticky=EW, padx=(10, 0), pady=5)
total_bal.grid(row=0, column=3, sticky=EW, padx=(10, 0), pady=5)
update_btn.grid(row=1, column=3, sticky=EW, padx=(10, 0), pady=5)
del_btn.grid(row=2, column=3, sticky=EW, padx=(10, 0), pady=5)

# Treeview widget
tv = ttk.Treeview(frame2, columns=(1, 2, 3, 4), show='headings', height=8)
tv.pack(side=LEFT, fill=BOTH, expand=True)

# Treeview column configuration
tv.column(1, anchor=CENTER, stretch=NO, width=70)
tv.column(2, anchor=CENTER)
tv.column(3, anchor=CENTER)
tv.column(4, anchor=CENTER)
tv.heading(1, text="Serial no")
tv.heading(2, text="Item Name")
tv.heading(3, text="Item Price")
tv.heading(4, text="Purchase Date")

# Treeview binding
tv.bind("<ButtonRelease-1>", select_record)

# Treeview style
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#E1E1E1", foreground="black", rowheight=25, fieldbackground="#E1E1E1")
style.map("Treeview", background=[('selected', '#347083')])

# Vertical scrollbar
scrollbar = ttk.Scrollbar(frame2, orient='vertical', command=tv.yview)
scrollbar.pack(side=RIGHT, fill='y')
tv.config(yscrollcommand=scrollbar.set)

# Initialize data fetching
fetch_records()

# Start the application
ws.mainloop()

