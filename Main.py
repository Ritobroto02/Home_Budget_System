from tkinter import *;
from tkinter import ttk, messagebox
import datetime as dt
from MainDb import *;
import pandas as pd
import matplotlib.pyplot as plt
from tkinter.simpledialog import askstring,askinteger
from tkinter.messagebox import showinfo



data = Database(db='myexpense2.db')
data.save_to_csv('expense_records.csv')

count = 0 
selectedRowid = 0

ws = Tk()
ws.title('Home Budget Expenses')
ws.columnconfigure(0, weight=1)  # Allow column 0 to expand
ws.rowconfigure(0, weight=1)

# Variables definition 
f =('Times new roman', 14)
namevar = StringVar()
amtvar = IntVar()
dopvar = StringVar()

# Widget

f2 = Frame(ws)
f2.pack(side=TOP,expand=True, fill='both')

f1 = Frame(ws,padx=10, pady=10)
f1.pack(side=BOTTOM)

# Label
Label(f1,text='ITEM NAME', font = f).grid(row = 0,column=0,sticky=W)
Label(f1,text='ITEM PRICE', font = f).grid(row = 1,column=0,sticky=W)
Label(f1,text='PURCHASE DATE', font = f).grid(row = 2,column=0,sticky=W)

itemName = Entry(f1,font=f,textvariable=namevar)
itemAmt = Entry(f1,font=f,textvariable=amtvar)
transactionDate = Entry(f1,font=f,textvariable=dopvar)

# placemnt

itemName.grid(row=0,column=1,sticky=EW,padx=(10,0))
itemAmt.grid(row=1,column=1,sticky=EW,padx=(10,0))
transactionDate.grid(row=2,column=1,sticky=EW,padx=(10,0))


# functions

    
def saveRecord():
    try:
        global data
        data.insertRecord(itemName=itemName.get(), itemPrice=itemAmt.get(), purchaseDate=transactionDate.get())
        data.save_to_csv('expense_records.csv')  # Save to CSV 
        refreshData()
        clearEntries()
    except Exception as e:
        messagebox.showerror('Error', str(e))


def setDate():
    date = dt.datetime.now()
    dopvar.set(f'{date:%d %B %Y}')

def clearEntries():
    itemName.delete(0,'end')
    itemAmt.delete(0,'end')
    transactionDate.delete(0,'end')

def fetchRecords():
     global count
     for rec in data.fetchRecord('select rowid, * from expenseRecord'):
        tv.insert(parent="", index='0', iid=count, values=(rec[0], rec[1], rec[2], rec[3]))
        count = count + 1


def selectRecord(event):
    global selectedRowid
    selected = tv.focus()
    val =tv.item(selected,'values')
    try:
        selectedRowid=val[0]
        d=val[3]
        namevar.set(val[1])
        amtvar.set(val[2])
        dopvar.set(str(d))
    except Exception as ep:
        pass


def updateRecord():
    global selectedRowid
    selected = tv.focus()
    try:
        data.updateRecord(namevar.get(), amtvar.get(),dopvar.get(),selectedRowid)
        tv.item(selected, values=(namevar.get(),amtvar.get(), dopvar.get()))
        refreshData()
        clearEntries()
    except Exception as ep:
        messagebox.showerror('Error',  ep)

    # itemName.delete(0, END)
    # itemAmt.delete(0, END)
    # transactionDate.delete(0, END)
    # tv.after(400, refreshData)

def set_budget():
    b = askinteger('Set Budget', 'Set budget')
    showinfo('Output',f'Your Budget is set to {b}')
    # budget = set_budget()
    f = data.fetchRecord(query="Select sum(itemPrice) from expenseRecord")
    
    for i in f:
        for j in i:
            
            messagebox.showinfo('Current Balance: ', f"Total Expense: {j} \nBalance Remaining: {b -j}")
    # total_expense = data.fetchRecord(query="SELECT sum(itemPrice) FROM expenseRecord")
    # messagebox.showinfo('Current Balance', f"Total Expense: {total_expense}")
            # return bal

def total_Balance(total):
    messagebox.showinfo('Welcome',f'Current Balance: {total}')

def refreshData():
    for item in tv.get_children():
      tv.delete(item)
    fetchRecords()
    
def deleteRow():
    global selectedRowid
    selected = tv.focus()
    data.removeRecord(selectedRowid)
    data.save_to_csv('expense_records.csv')  # Update CSV file
    refreshData()

def theChart():
    #Read data from excel and store it in var: df [dataframe]
    plt.style
    df = pd.read_csv('expense_records.csv') 
    
    # All Brands
    x = df['itemName']
    y = df['itemPrice']

    # Pie chart
    plt.pie(y, labels=x, radius=1.2,autopct='%0.01f%%')

    plt.show()
    showinfo
    
# Buttons

curDate=Button(f1,
    text='Current Date',
    font=f,
    #background='#04C4D9',
    command=setDate,
    width=15
)

submitBtn = Button(
    f1,
    text='Save Record',
    font =f,
    command=saveRecord,
    # bg='#42602D',
)

clrBtn = Button(   
    f1, 
    text='Clear Entry', 
    font=f, 
    command=clearEntries, 
    # bg='#D9B036', 
    )

quitBtn =Button(
    f1, 
    text='Exit', 
    font=f, 
    command=lambda:ws.destroy(), 
    # bg='#D33532', 
)

setBudget = Button(
    f1,
    text='Set Budget',
    font=f,
    bg='pink',
    command=set_budget
)

totalSpent = Button(
    f1,
    text='Total Spent',
    font=f,
    command=lambda:data.fetchRecord('select sum(ite)')
)

updateBtn = Button(
    f1, 
    text='Update',
    # bg='#C2BB00',
    command=updateRecord,
    font=f
)

delBtn = Button(
    f1, 
    text='Delete',
    # bg='#BD2A2E',
    command=deleteRow,
    font=f
)

genChart = Button(
    f1,
    text='Analysis',
    font=f, 
    command=theChart
)

totalBal=Button(
    f1,
    text='Total Balance',
    font=f,
    command=total_Balance
      
)


# Button Placement
curDate.grid(row=0, column=2,sticky=EW,padx=(10,0))
submitBtn.grid(row=3, column=1,sticky=EW,padx=(10,0),pady=(10,0))
genChart.grid(row=3, column=2,sticky=EW,padx=(10,0),pady=(10,0))
clrBtn.grid(row=1, column=2,sticky=EW,padx=(10,0))
quitBtn.grid(row=2, column=2,sticky=EW,padx=(10,0))
setBudget.grid(row=0, column=3,sticky=EW,padx=(10,0))
updateBtn.grid(row=1, column=3,sticky=EW,padx=(10,0))
delBtn.grid(row=2, column=3,sticky=EW,padx=(10,0))
totalBal.grid(row=3,column=3,sticky=EW,padx=(10,0),pady=(10,0))

# TreeView Budget
tv = ttk.Treeview(f2,columns=(1,2,3,4),show='headings',height=8)
tv.pack(expand=True, fill='both')

# Heading
tv.column(1,anchor=CENTER,stretch=NO,width=70)
tv.column(2,anchor=CENTER)
tv.column(3,anchor=CENTER)
tv.column(4,anchor=CENTER)
tv.heading(1,text='Serial No')
tv.heading(2,text='Item Name')
tv.heading(3,text='Item Price')
tv.heading(4,text='Purchase Date')

tv.bind("<ButtonRelease-1>", selectRecord)

style = ttk.Style()
style.theme_use('default')
style.map('Treeview')

scrollbar= Scrollbar(f2,orient='vertical')
scrollbar.configure(command=tv.yview)
scrollbar.pack(side='right',fill='y')
tv.config(yscrollcommand=scrollbar.set)

fetchRecords()
ws.mainloop()