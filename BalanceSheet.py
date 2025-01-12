import tempfile
from tkinter import*
from tkinter import ttk,messagebox,filedialog
import sqlite3
import csv
import os

balance_sheet=[]

st_liabilities=None
st_Assets=None
lt_liabilities=None
lt_Assets=None
t_assets=None
t_liab=None
class balanceClass:
    def __init__(self,root):
       self.root=root
       self.root.geometry("1350x750+0+0")
       self.root.title("Reports") 
       self.root.config(bg="white")
       self.root.iconbitmap("kmc.ico")
       
       #=======Title
       
       title=Label(self.root,text="Balance Sheet ", font=("times new roman",15,"bold"),bg="#010c48",fg="white",justify=CENTER).place(x=0,y=0,width=1350)
       
       
       
       self.entry_name=StringVar()
       self.id_var=StringVar()
       self.debit_var=StringVar()
       self.credit_var=StringVar()
       self.from_var=StringVar()
       self.to_var=StringVar()
       
       self.bal()
       
       #=======Search expenses
       
       search_frame=LabelFrame(self.root,text="Search Trail Balance",bg="white",font=("Poppins",12),bd=2,relief=RIDGE)
       search_frame.place(x=10,y=480,width=400,height=100)     
       
      #  spin_search=ttk.Combobox(search_frame,textvariable=self.expense_searchType_var,values=("Select","expen_Id","Ename","Etype","Edate"),state="readonly",justify=CENTER,font=("goudy old style",15))
      #  spin_search.place(x=10,y=10,width=250,height=30)
      #  spin_search.current(0)
       
      #  search_entry=Entry(search_frame,textvariable=self.expense_searchtxt_var,font=("goudy old style",15),bg="lightyellow").place(x=10,y=60,width=250,height=30)
      #  search_button=Button(search_frame,command=self.search,text="Search",font=("times new roman",15,"bold"),bg="#4caf50",fg="white",cursor="hand2").place(x=10,y=110,width=250,height=30)
       search_cal=Button(search_frame,command=self.search_cal,text="Search",font=("times new roman",15,"bold"),bg="#4caf50",fg="white",cursor="hand2").place(x=300,y=20,width=80,height=30)
        
       lbl_from_date=Label(search_frame,text="from: YYYY/MM/DD", font=("goudy old style",8),bg="white").place(x=10,y=0,width=110,height=20)
       lbl_to_date=Label(search_frame,text="To: YYYY/MM/DD", font=("goudy old style",8),bg="white").place(x=150,y=0,width=110,height=20)
       txt_from_date=Entry(search_frame,textvariable=self.from_var, font=("goudy old style",15),bg="lightyellow").place(x=10,y=20,width=110,height=30)
       txt_to_date=Entry(search_frame,textvariable=self.to_var, font=("goudy old style",15),bg="lightyellow").place(x=150,y=20,width=110,height=30)
       search_cal=Button(self.root,command=self.print_all,text="Print",font=("times new roman",15,"bold"),bg="#4caf50",fg="white",cursor="hand2").place(x=1150,y=480,width=150,height=60)
       refresh=Button(self.root,command=self.refresh,text="Refresh",font=("times new roman",15,"bold"),bg="#4caf50",fg="white",cursor="hand2").place(x=980,y=480,width=150,height=60)
       
       trail_frame=LabelFrame(self.root,text="Balance sheet Total",bg="white",font=("Poppins",12),bd=2,relief=RIDGE)
       trail_frame.place(x=440,y=480,width=400,height=170)
       #search_cal=Button(trail_frame,command=self.search_cal,text="Search",font=("times new roman",15,"bold"),bg="#4caf50",fg="white",cursor="hand2").place(x=300,y=20,width=80,height=30)
       lbl_Grand=Label(trail_frame,text="Total", font=("goudy old style",15),bg="white").place(x=10,y=100,width=110,height=20)

       lbl_S_liab=Label(trail_frame,text="S_Liabilities", font=("goudy old style",9),bg="black",fg="white").place(x=150,y=0,width=110,height=20)
       lbl_S_Assets=Label(trail_frame,text="S_Assets", font=("goudy old style",9),bg="black",fg="white").place(x=280,y=0,width=110,height=20)
       txt_S_liab=Label(trail_frame,text=st_liabilities, font=("goudy old style",15),bg="lightyellow").place(x=150,y=20,width=110,height=30)
       txt_S_Assets=Label(trail_frame,text=st_Assets, font=("goudy old style",15),bg="lightyellow").place(x=280,y=20,width=110,height=30)
       
       lbl_total_L_Assets=Label(trail_frame,text="L_Liabilities", font=("goudy old style",9),bg="black",fg="white").place(x=150,y=50,width=110,height=20)
       lbl_total_L_Liabilities=Label(trail_frame,text="L_Assets", font=("goudy old style",9),bg="black",fg="white").place(x=280,y=50,width=110,height=20)
       txt_Total_L_Liabilities=Label(trail_frame,text=lt_liabilities, font=("goudy old style",15),bg="lightyellow").place(x=150,y=70,width=110,height=30)
       txt_Total_L_Assets=Label(trail_frame,text=lt_Assets, font=("goudy old style",15),bg="lightyellow").place(x=280,y=70,width=110,height=30)

       txt_Total_Liabilities=Label(trail_frame,text=t_liab, font=("goudy old style",15),fg="white",bg="black").place(x=150,y=100,width=110,height=30)
       txt_Total_Assets=Label(trail_frame,text=t_assets, font=("goudy old style",15),fg="white",bg="black").place(x=280,y=100,width=110,height=30)

       #========Entry Frame Details
       
       
       entry_frame=Frame(self.root,bd=3,relief=RIDGE)
       entry_frame.place(x=0,y=30,relwidth=1,height=440)
       
       scrolly=Scrollbar(entry_frame,orient=VERTICAL)
       scrollx=Scrollbar(entry_frame,orient=HORIZONTAL)
        
       self.enytryTable=ttk.Treeview(entry_frame,columns=("Eid","Type","Debit"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
       scrollx.pack(side=BOTTOM,fill=X)
       scrolly.pack(side=RIGHT,fill=Y)
       scrollx.config(command=self.enytryTable.xview)
       scrolly.config(command=self.enytryTable.yview)
        
       self.enytryTable.heading("Eid",text="ID")
    #    self.enytryTable.heading("Ename",text="Entry Name")
       self.enytryTable.heading("Type",text="Type")
    #    self.enytryTable.heading("Etype",text="Entry Type ")
       self.enytryTable.heading("Debit",text="Amount")
    #    self.enytryTable.heading("Credit",text="Credit")
    #    self.enytryTable.heading("Edate",text="Date")
       
        
       self.enytryTable["show"]="headings"
       self.enytryTable.column("Eid",width=50)
    #    self.enytryTable.column("Ename",width=100)
       self.enytryTable.column("Type",width=100)
    #    self.enytryTable.column("Etype",width=100)
       self.enytryTable.column("Debit",width=100)
    #    self.enytryTable.column("Credit",width=100)
    #    self.enytryTable.column("Edate",width=100)
       self.enytryTable.pack(expand=1,fill=BOTH)
       
       
       self.sum_debit()
       
        #====print
       print_frame=Frame(self.root,bd=3,relief=RIDGE)
       print_frame.place()
       scrolly=Scrollbar(print_frame,orient=VERTICAL)
       
       
       scrolly.pack(side=RIGHT,fill=Y)
       self.txtprint =Text(print_frame,yscrollcommand=scrolly.set)
       self.txtprint.pack(fill=BOTH,expand=1)
       scrolly.config(command=self.txtprint.yview)
        
        
    def print_all(self):
            #print top
            self.print_top()
            self.print_middle()
            self.trail_total()
            self.generate()
    def print_top(self):
         #"Eid","Ename","Type","Etype","Debit","Credit"
           top='''================BALANCE SHEET=================\n
ID\t Category\t\t Amount\n
           '''
           self.txtprint.delete("1.0",END)
           self.txtprint.insert('1.0',top)
           
    def print_middle(self):
             
         #   for row in self.rows:
             for i in balance_sheet:
                  I_D=str(i[0])
                  Cat=str(i[1])
                  
                  
                  Amount=str(i[2])
                  
                  
                  
                  if len(Cat)<21:
                        for i in range(len(Cat),22):
                         Cat=Cat+" "
                  
                  
                  self.txtprint.insert(END,"\n"+I_D+"\t\t"+Cat+"\t\t"+Amount)
                  
    def trail_total(self):
           st_liabilities,st_Assets,lt_liabilities,lt_Assets
           
           bottom=f'''\n\n
===============================================
         |    Short-Term-Liabilities  : {st_liabilities}          
         |    Short-Term-Assets  : {st_Assets}
         |------------------------------------     
         |    Long-Term-Assets   : {lt_Assets}    
         |    Long-Term-Liabilities    : {lt_liabilities}
Total:   |
         |=================================================
         | 
         |    Total-Assets   : {t_assets}    
         |    Total-Liabilities    : {t_liab}
          ''' 
           self.txtprint.insert(END,bottom)
       
    def generate(self):
           new_file=tempfile.mktemp('.txt')
           open(new_file,'w').write(self.txtprint.get("1.0",END))
           os.startfile(new_file,'print')
    
    def sum_debit(self):
        connection
        
        
        try:
            cur.execute("DELETE FROM Balance")
            con.commit()
            cur.execute("INSERT INTO Balance(bal_Id ,Ename ,Type ,Etype ,Debit ,Credit ,Edate ) Select expen_Id, Ename,Type, Etype, SUM(Debit),Credit, Edate from Expenses  GROUP BY Type")

            con.commit()
            cur.execute("Select bal_Id,Type, SUM(Debit) from Balance GROUP BY Type")
            row=cur.fetchall() 
            
            
            global trowlbl,trowresult,titles,treslbl,tresresult
            titles=["ID","Category","Amount"]
            titles=[(titles)]
            trowlbl=["st_liabilities","st_Assets","lt_liabilities","lt_Assets"]
            trowlbl=[(trowlbl)]
            trowresult=[st_liabilities,st_Assets,lt_liabilities,lt_Assets]
            trowresult=[(trowresult)]
            treslbl=["","Total Assets","Total Liabilities"]
            treslbl=[(treslbl)]
            tresresult=["Total",t_assets,t_liab]
            tresresult=[(tresresult)]
            
            HEAD=["============BALANCE SHEET============"]
            HEAD=[(HEAD)]
            
            self.enytryTable.delete(*self.enytryTable.get_children())
            for i in row:
                  global balance_sheet
                  balance_sheet = row
                  self.enytryTable.insert('',END,values=i)
            
            
                  
        except Exception as ex:
             messagebox.showerror("Error",f"Error due to (save) :{str(ex)}",parent=self.root)
      
    def bal(self):
        connection
        try:
            cur.execute("Select SUM(Debit) from Balance where Type='Expense'")
            sum_expense=cur.fetchall()
            sum_expense=sum_expense[0][0]
            if sum_expense==None:
                sum_expense=0
            cur.execute("Select SUM(Debit) from Balance where Type='Revenue'")
            sum_revenue=cur.fetchall()
            sum_revenue=sum_revenue[0][0]
            if sum_revenue==None:
                sum_revenue=0
            cur.execute("Select SUM(Debit) from Balance where Type='Short-Term-Assets'")
            stAssets=cur.fetchall()
            stAssets=stAssets[0][0]
            if stAssets==None:
                stAssets=0
            cur.execute("Select SUM(Debit) from Balance where Type='Short-Term-Liabilities'")
            stliab=cur.fetchall()
            stliab=stliab[0][0]
            if stliab==None:
                stliab=0
            cur.execute("Select SUM(Debit) from Balance where Type='Long-Term-Assets'")
            ltAssets=cur.fetchall()
            ltAssets=ltAssets[0][0]
            if ltAssets==None:
                ltAssets=0
            cur.execute("Select SUM(Debit) from Balance where Type='Long-Term-Liabilities'")
            ltliab=cur.fetchall()
            ltliab=ltliab[0][0]
            if ltliab==None:
                ltliab=0
            
            global st_liabilities,st_Assets,lt_liabilities,lt_Assets,t_liab,t_assets
            
            st_liabilities=sum_expense+stliab
            st_Assets=stAssets+sum_revenue
            lt_liabilities=ltliab
            lt_Assets=ltAssets
            #print(st_liabilities," ",st_Assets," ",lt_liabilities," ",ltAssets)
            t_liab=st_liabilities+lt_liabilities
            t_assets=st_Assets+lt_Assets
            
                  
        except Exception as ex:
             messagebox.showerror("Error",f"Error due to (save) :{str(ex)}",parent=self.root)
            
    def export(self):
        if(len(balance_sheet)) < 1:
            messagebox.showerror("No Data", "No data available to export")
            return False
        fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="save csv" , filetypes=(("CSV FILE", "*.csv"),("All Files","*.*")))
        with open(fln, mode='w') as myfile:
            exp_writer = csv.writer(myfile,delimiter=',')
            for i in balance_sheet:
                exp_writer.writerow(i)
                
     
            messagebox.showinfo("Data Exported", "Your data has been exported to " +os.path.basename(fln)+ "Successfully")
    def search_cal(self):
          
         connection
         try:
            if  self.from_var.get()=="" or self.to_var.get()=="":
                  messagebox.showerror("Error","Dates can't be empty",parent=self.root)
            else:
                  start=self.from_var.get()
                  end=self.to_var.get()
                  cur.execute("Select * from Expenses where Edate BETWEEN ? AND ?",(start,end))
                  
                  rows=cur.fetchall()
                  
                  if len(rows)!=0:
                           self.enytryTable.delete(*self.enytryTable.get_children())
                           for i in rows:
                             global mydata
                             mydata = rows
                             self.enytryTable.insert('',END,values=i)     
                           messagebox.showinfo("Success","Data Shown",parent=self.root)                   
                        
                  
                  else:
                        messagebox.showerror("Error","No, Record Found try different",parent=self.root)
         except Exception as ex:
            messagebox.showerror("Error",f"Error due to (search_cal) :{str(ex)}",parent=self.root)           
    def refresh(self):
        self.root.destroy()
        os.system("BalanceSheet.py") 
       
   
       
con=sqlite3.connect(database=r'test1.db')
cur=con.cursor()                  
def connection():
             
       
       cur.execute("CREATE TABLE IF NOT EXISTS Expenses(expen_Id INTEGER PRIMARY KEY AUTOINCREMENT ,Ename VARCHAR(100),Type VARCHAR(100),Etype VARCHAR(100),Debit VARCHAR(200),Credit VARCHAR(100),Edate DATE)")
       
       
       cur.execute("CREATE TABLE IF NOT EXISTS Balance(bal_Id ,Ename VARCHAR(100),Type VARCHAR(100),Etype VARCHAR(100),Debit VARCHAR(200),Credit VARCHAR(100),Edate DATE)")

       con.commit()
connection()
if __name__=="__main__":
    root=Tk()
    obj=balanceClass(root)
    root.mainloop()
    
 
    
