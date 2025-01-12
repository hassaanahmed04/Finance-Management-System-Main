import tempfile
from tkinter import*
from tkinter import ttk,messagebox,filedialog
import csv
import os
import sqlite3
from Reports import reportsClass
from  head import headClass
# hea=headClass.grand.
# print(hea.total)

# report=reportsClass()

mydata = []

title=[]


class tranClass:
    def __init__(self,root): 
       self.root=root
       self.root.geometry("1350x750+0+0")
       self.root.title("Transactions") 
       self.root.config(bg="white")
       self.root.iconbitmap("kmc.ico")
       # title=Label(self.root,text="Finance Managment System ", font=("times new roman",40,"bold"),bg="#010c48",fg="white").place(x=0,y=0,relwidth=1,height=70)
       self.expense_searchType_var=StringVar()
       self.expense_searchtxt_var=StringVar()
       
       self.expense_id_var=StringVar()
       self.var_Ename=StringVar()
       self.var_Etype=StringVar()
       self.debit=StringVar()
       self.credit=StringVar()
       self.var_Edate=StringVar()
       self.bal_type=StringVar()
       self.debit=StringVar()
       self.debit_list=[]
       self.credit=StringVar()
       self.credit_debit=StringVar()
       self.credit_list=[]
       self.asset_list=[]
       self.getting_assets()
       self.from_var=StringVar()
       self.to_var=StringVar()
       self.remain_total=0
       self.grand()
       self.check()
       
       
       
       
       #Adding Expenses
           
       title=Label(self.root,text="Add Expenses Here", font=("times new roman",15,"bold"),bg="#010c48",fg="white",justify=CENTER).place(x=300,y=20,width=1050,height=40)
       
       #=======Search expenses
       
       search_frame=LabelFrame(self.root,text="Search expenses",bg="white",font=("Poppins",12),bd=2,relief=RIDGE)
       search_frame.place(x=10,y=20,width=270,height=350)   
      #  search_frame.config(bg="#0000FF")

       
       spin_search=ttk.Combobox(search_frame,textvariable=self.expense_searchType_var,values=("Select","ID","Name","Head","Type","Date"),state="readonly",justify=CENTER,font=("goudy old style",15))
       spin_search.place(x=10,y=10,width=250,height=30)
       spin_search.current(0)
       
       search_entry=Entry(search_frame,textvariable=self.expense_searchtxt_var,font=("goudy old style",15),bg="lightyellow").place(x=10,y=60,width=250,height=30)
       search_button=Button(search_frame,command=self.search,text="Search",font=("times new roman",15,"bold"),bg="#4caf50",fg="white",cursor="hand2").place(x=10,y=110,width=250,height=30)
       search_cal=Button(search_frame,command=self.search_cal,text="Search",font=("times new roman",15,"bold"),bg="#4caf50",fg="white",cursor="hand2").place(x=10,y=210,width=250,height=30)

         #====Calender
       
       lbl_from_date=Label(search_frame,text="from: YYYY/MM/DD", font=("goudy old style",8),bg="white").place(x=10,y=150,width=110,height=20)
       lbl_to_date=Label(search_frame,text="To: YYYY/MM/DD", font=("goudy old style",8),bg="white").place(x=150,y=150,width=110,height=20)
       txt_from_date=Entry(search_frame,textvariable=self.from_var, font=("goudy old style",15),bg="lightyellow").place(x=10,y=170,width=110,height=30)
       txt_to_date=Entry(search_frame,textvariable=self.to_var, font=("goudy old style",15),bg="lightyellow").place(x=150,y=170,width=110,height=30)

       #======Expense Details
       
       #         Row 1
       lbl_expense_name=Label(self.root,text="  Name :", font=("goudy old style",15),bg="white").place(x=300,y=90)
       lbl_expense_type=Label(self.root,text="  Head :", font=("goudy old style",15),bg="white").place(x=650,y=90)
       
       
       
       txt_expense_name=Entry(self.root,textvariable=self.var_Ename, font=("goudy old style",15),bg="lightyellow").place(x=400,y=90)
       txt_expense_head=ttk.Combobox(self.root,text="  Head ",textvariable=self.var_Etype,values=self.asset_list,state="readonly",justify=CENTER, font=("goudy old style",15))
       txt_expense_head.place(x=750,y=90,width=235)
       txt_expense_head.current(0)
       
       #======== Row 2
       lbl_expense_Debit=Label(self.root,text="  Price :", font=("goudy old style",15),bg="white").place(x=300,y=160)
       lbl_expense_Credit=Label(self.root,text="  Type :", font=("goudy old style",15),bg="white").place(x=650,y=160)
       
       txt_expense_Debit=Entry(self.root,textvariable=self.debit, font=("goudy old style",15),bg="lightyellow").place(x=400,y=160)
       txt_expense_Credit=Entry(self.root,textvariable=self.credit, font=("goudy old style",15),bg="lightyellow").place(x=750,y=160,width=235)
      
       txt_expense_type=ttk.Combobox(self.root,text="  Type ",textvariable=self.credit,values=("Select","Debit","Credit"),state="readonly",justify=CENTER, font=("goudy old style",15))
       txt_expense_type.place(x=750,y=160,width=235)
       txt_expense_type.current(0)
       
       #======== Row 3
       lbl_expense_date=Label(self.root,text="  Date :", font=("goudy old style",15),bg="white").place(x=300,y=240)
       lbl_expense_id=Label(self.root,text="  Id :", font=("goudy old style",15),bg="white").place(x=650,y=240)

       txt_expense_date=Entry(self.root,textvariable=self.var_Edate, font=("goudy old style",15),bg="lightyellow").place(x=400,y=240)
       txt_expense_id=Entry(self.root,textvariable=self.expense_id_var, font=("goudy old style",15),bg="lightyellow").place(x=750,y=240)
       
       lbl_bal_type=Label(self.root,text="  Category :", font=("goudy old style",15),bg="white").place(x=300,y=300)
       txt_bal_type=ttk.Combobox(self.root,textvariable=self.bal_type, values=("Select","Short-Term-Assets","Long-Term-Assets","Long-Term-Liabilities","Short-Term-Liabilities","Revenue","Expense"),state="readonly",justify=CENTER, font=("goudy old style",15))
       txt_bal_type.place(x=400,y=300,width=235)
       txt_bal_type.current(0)
       
       self.txt_grand_remain=Label(self.root,text=self.remain_total, font=("goudy old style",14),bg="white")
       self.txt_grand_remain.place(x=780,y=300,height=30)
       lbl_grand_remain=Label(self.root,text="Rs:", font=("goudy old style",14),bg="white").place(x=660,y=300,height=30)

       
       #======= CRUD

       btn_create=Button(self.root,text="Save",command=self.Save,font=("times new roman",15,"bold"),bg="green",fg="white",cursor="hand2").place(x=1100,y=90,width=170,height=45)
       btn_upgrade=Button(self.root,text="Upgrade",command=self.update,font=("times new roman",15,"bold"),bg="blue",fg="white",cursor="hand2").place(x=1100,y=160,width=170,height=45)
       btn_reset=Button(self.root,text="Reset",command=self.clear,font=("times new roman",15,"bold"),bg="black",fg="white",cursor="hand2").place(x=1100,y=230,width=170,height=45)
       btn_delete=Button(self.root,text="Delete",command=self.delete,font=("times new roman",15,"bold"),bg="red",fg="white",cursor="hand2").place(x=1100,y=300,width=170,height=45)
       btn_showall=Button(self.root,text="Show all",command=self.show,font=("times new roman",15,"bold"),bg="red",fg="white",cursor="hand2").place(x=900,y=300,width=170,height=45)
       btn_refresh=Button(self.root,text="Refresh",command=self.refresh,font=("times new roman",15,"bold"),bg="green",fg="white",cursor="hand2").place(x=990,y=230,width=80,height=45)
      #  self.refresh()
       global HEAD
       HEAD=  ["","","","EXPENSES"]
       HEAD=[(HEAD)]
      #  font2 = ('Arial', 50, 'bold')
      #  HEAD.font(font2)

      #  HEAD=[(HEAD)]
       #=======Download========
       
       btn_Download=Button(self.root,text="Print",command=self.print_all,font=("times new roman",15,"bold"),bg="Red",fg="white",cursor="hand2").place(x=10,y=290,width=270,height=45)

       
       #========expenses Frame Details
       
       emp_frame=Frame(self.root,bd=3,relief=RIDGE)
       emp_frame.place(x=0,y=350,relwidth=1,height=320)
       
       scrolly=Scrollbar(emp_frame,orient=VERTICAL)
       scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)
        
       self.suptable=ttk.Treeview(emp_frame,columns=("expen_Id","Ename","Type","Etype","Debit","Credit","Edate"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
       scrollx.pack(side=BOTTOM,fill=X)
       scrolly.pack(side=RIGHT,fill=Y)
       scrollx.config(command=self.suptable.xview)
       scrolly.config(command=self.suptable.yview)
        
       self.suptable.heading("expen_Id",text="ID")
       self.suptable.heading("Ename",text="Expense Name")
       self.suptable.heading("Type",text="Category")
       self.suptable.heading("Etype",text="Head")
       self.suptable.heading("Debit",text="Price")
       self.suptable.heading("Credit",text="Type")
       self.suptable.heading("Edate",text="Date")
        
        
       self.suptable["show"]="headings"
       self.suptable.column("expen_Id",width=50)
       self.suptable.column("Ename",width=100)
       self.suptable.column("Type",width=100)
       self.suptable.column("Etype",width=100)
       self.suptable.column("Debit",width=100)
       self.suptable.column("Credit",width=100)
       self.suptable.column("Edate",width=100)
       
       self.suptable.pack(expand=1,fill=BOTH)
       self.suptable.bind("<ButtonRelease-1>",self.get_data)
        
       self.show()
       self.check()
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
            self.generate()
    def print_top(self):
         #"expen_Id","Ename","Type","Etype","Debit","Credit","Edate"
           top='''================General Ledger=================\n
ID\t Name\t\t Cat\t\t\t Head\t\t Price\t Type\t  Date\n
'''
           self.txtprint.delete("1.0",END)
           self.txtprint.insert('1.0',top)
           
    def print_middle(self):
             
         #   for row in self.rows:
             for i in mydata:
                  I_D=str(i[0])
                  Name=str(i[1])
                  
                  
                  Cat=str(i[2])
                  Type=str(i[3])
                  Deb=str(i[4])
                  Cred=str(i[5])
                  Date=str(i[6])
                  if len(Name)<15:
                        for i in range(len(Name),15):
                         Name=Name+" "
                  if len(Cat)<21:
                        for i in range(len(Cat),22):
                         Cat=Cat+" "
                  if len(Type)<10:
                        for i in range(len(Type),10):
                         Type=Type+" "
                  
                  self.txtprint.insert(END,"\n"+I_D+"\t"+Name+"\t"+Cat+"\t"+Type+"\t"+ Deb+"\t  "+Cred+"\t  "+Date)
                  
                  
    def generate(self):
           new_file=tempfile.mktemp('.txt')
           open(new_file,'w').write(self.txtprint.get("1.0",END))
           os.startfile(new_file,'print')
       
    def refresh(self):
      
       self.root.destroy()
       os.system('Transactions.py')
      
       
       
    
    def getting_assets(self):
          connection
          try:
             cur.execute("Select Hname from Head")
             asset=cur.fetchall()
             
             self.asset_list.append("Empty")
             if len(asset)>0:
                   del self.asset_list[:]
                   self.asset_list.append("Select")
                   for i in asset:
                         
                         self.asset_list.append(i[0])
                   self.asset_list.append("Others")
          except Exception as ex:
             messagebox.showerror("Error",f"Error due to (save) :{str(ex)}",parent=self.root)
      
   
                
    def grand(self):
         connection
         try:
              cur.execute("Select SUM(HIncome) from Head")
              row=cur.fetchone()
            #   print(row)
              global total
              total=row[0]
              if total==None:
                   total=0
            #   print("Grand Total",total)
          
               
         except Exception as ex:
               messagebox.showerror("Error",f"Error  due to (show):{str(ex)}",parent=self.root)
    def check(self):
          connection
          debit="Debit"
          credit="Credit"
          try:
             cur.execute("Select SUM(Debit) from Expenses where Credit=?",(debit,))
             global sum_debit
             sum_debit=cur.fetchall()  
             sum_debit=sum_debit[0][0]
             if sum_debit==None:
                  sum_debit=0
            #  print("sum of debit is :",sum_debit)
             cur.execute("Select SUM(Debit) from Expenses where Credit=?",(credit,))
             global sum_credit, remain_total
             remain_total=0
             sum_credit=cur.fetchall()  
             sum_credit=sum_credit[0][0]
             if sum_credit==None:
                  sum_credit=0
             
            #  print("sum Credit :",sum_credit)
             
            
             remain_total=total
             remain_total+=sum_credit
             remain_total-=sum_debit
             
             #print("sum of Credit is :",sum_credit)
             #print(remain_total)
             
             
             
                   
          except Exception as ex:
             messagebox.showerror("Error",f"Error due to (check) :{str(ex)}",parent=self.root)   
    def export(self):
        if(len(mydata)) < 1:
            messagebox.showerror("No Data", "No data available to export")
            return False
        fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="save csv" , filetypes=(("CSV FILE", "*.csv"),("All Files","*.*")))
        with open(fln, mode='w') as myfile:
            exp_writer = csv.writer(myfile,delimiter=',')
            exp_writer.writerow(HEAD)
            for i in mydata:
                exp_writer.writerow(i)
                
            messagebox.showinfo("Data Exported", "Your data has been exported to " +os.path.basename(fln)+ "Successfully")
               
                
    def Save(self):
          connection
          try:
             if self.expense_id_var.get()=="":
                  messagebox.showerror("Error","Id must be required",parent=self.root)
             elif self.var_Etype.get()=="Select":
                  messagebox.showerror("Error","Please choose Head",parent=self.root)
             elif self.credit_debit.get()=="Select":
                  messagebox.showerror("Error","Please choose Debit/Credit",parent=self.root)
             else:
                  cur.execute("Select * from Expenses where expen_Id=?",(self.expense_id_var.get(),))
                  row=cur.fetchone()
                  if row!=None:
                         messagebox.showerror("Error","Id already exits, Expenses different",parent=self.root)
                         
                  else:
                        cur.execute("Insert into Expenses (Ename,Type,Etype,Debit,Credit,Edate) values(?,?,?,?,?,?)",(
                           self.var_Ename.get(),
                           self.bal_type.get(),
                           self.var_Etype.get(),
                           self.debit.get(),
                           self.credit.get(),
                           self.var_Edate.get(),
                        ))
                        con.commit()
                        messagebox.showinfo("Success","New Ledger Added Success",parent=self.root)
                        self.clear()
                        self.show()
                        self.check()
                        
          except Exception as ex:
             messagebox.showerror("Error",f"Error due to (save) :{str(ex)}",parent=self.root)
             
    def update(self):
          connection
          try:
             if self.expense_id_var.get()=="":
                  messagebox.showerror("Error","Id must be required",parent=self.root)
             else:
                  cur.execute("Select * from Expenses where expen_Id=?",(self.expense_id_var.get(),))
                  row=cur.fetchall()

                  if row==None:
                         messagebox.showerror("Error","Invalid Id",parent=self.root)
                         
                  else:
                        cur.execute("Update Expenses set Ename=?,Type=?,Etype=?,Debit=?,Credit=?,Edate=? where expen_Id=?",(
                           self.var_Ename.get(),
                           self.bal_type.get(),
                           self.var_Etype.get(),
                           self.debit.get(),
                           self.credit.get(),
                           self.var_Edate.get(),
                           self.expense_id_var.get()
                        ))
                        con.commit()
                        messagebox.showinfo("Success","Ledger Updated Success",parent=self.root)
                        self.clear()
                        self.show()
          except Exception as ex:
             messagebox.showerror("Error",f"Error due to (update):{str(ex)}",parent=self.root)
    def delete(self):
          connection
          try:
             if self.expense_id_var.get()=="":
                  messagebox.showerror("Error","Id must be required",parent=self.root)
             else:
                  cur.execute("Select * from Expenses where expen_Id=?",(self.expense_id_var.get(),))
                  row=cur.fetchone()
                  if row==None:
                         messagebox.showerror("Error","Invalid Id",parent=self.root)
                         
                  else:
                        confirmation=messagebox.askyesno("Confirm","Do you want to delete?",parent=self.root)
                        if confirmation==True:
                               cur.execute("delete from Expenses where expen_Id=?",(self.expense_id_var.get(),))
                               con.commit()
                               messagebox.showinfo("Success","Deleted Successfully",parent=self.root)
                        
                       
                               self.clear()
                               self.show()
          except Exception as ex:
             messagebox.showerror("Error",f"Error due to (delete):{str(ex)}",parent=self.root)          
    def show(self):
          connection
          try:
             cur.execute("select * from Expenses")
             rows=cur.fetchall()
             global title
             title=["Id","Ledger_name","Category","Type","Debit","Credit","Date"]
             title=[(title)]
             
           
             
             self.suptable.delete(*self.suptable.get_children())
             for row in rows:
                  global mydata
                  
                  mydata = rows
                  self.suptable.insert('',END,values=row)
                  
          except Exception as ex:
               messagebox.showerror("Error",f"Error  due to (show):{str(ex)}",parent=self.root)
               
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
                           self.suptable.delete(*self.suptable.get_children())
                           for i in rows:
                             global mydata
                             mydata = rows
                             self.suptable.insert('',END,values=i)     
                           messagebox.showinfo("Success","Data Shown",parent=self.root)                   
                        
                  
                  else:
                        messagebox.showerror("Error","No, Record Found try different",parent=self.root)
         except Exception as ex:
            messagebox.showerror("Error",f"Error due to (search_cal) :{str(ex)}",parent=self.root)
    def search(self):
            
         connection
         try:
            if self.expense_searchType_var.get()=="Select":
                  messagebox.showerror("Error","Select some type ",parent=self.root)
            elif self.expense_searchtxt_var.get()=="":
                  messagebox.showerror("Error","Search field can't be empty",parent=self.root)
            else:
                  if self.expense_searchType_var.get()=="ID":
                        
                        cur.execute("Select * from Expenses where expen_Id LIKE '%"+self.expense_searchtxt_var.get()+"%' ")
                  elif self.expense_searchType_var.get()=="Name":
                        
                        cur.execute("Select * from Expenses where Ename LIKE '%"+self.expense_searchtxt_var.get()+"%' ")
                  elif self.expense_searchType_var.get()=="Head":
                        
                        cur.execute("Select * from Expenses where Etype LIKE '%"+self.expense_searchtxt_var.get()+"%' ")
                  elif self.expense_searchType_var.get()=="Date":
                        
                        cur.execute("Select * from Expenses where Edate LIKE '%"+self.expense_searchtxt_var.get()+"%' ")
                  elif self.expense_searchType_var.get()=="Type":
                        
                        cur.execute("Select * from Expenses where Credit LIKE '%"+self.expense_searchtxt_var.get()+"%' ")
                  rows=cur.fetchall()
                  lis=[]
                  for i in range(0,len(rows)):
                        lis.append(rows[i][4])
                  
                  lis=[eval(i) for i in lis]
                  # print(lis)
                  # print(rows)
                  self.remain_total=sum(lis)
                 # print(self.remain_total)
                  self.remain_total=str(self.remain_total)
                  self.txt_grand_remain.config(text=self.remain_total, font=("goudy old style",14),bg="white")
                  
      
                 # print(self.remain_total)
                  # print(rows)
                  
                  if len(rows)!=0:
                           self.suptable.delete(*self.suptable.get_children())
                           for i in rows:
                             global mydata
                             mydata = rows
                             self.suptable.insert('',END,values=i)                        
                        
                  # elif self.expense_searchtxt_var.get()==None:
                  else:
                        messagebox.showerror("Error","No, Record Found try different",parent=self.root)
         except Exception as ex:
            messagebox.showerror("Error",f"Error due to (search) :{str(ex)}",parent=self.root)
               
    def export(self):
        if(len(mydata)) < 1:
            messagebox.showerror("No Data", "No data available to export")
            return False
        fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="save csv" , filetypes=(("CSV FILE", "*.csv"),("All Files","*.*")))
        with open(fln, mode='w') as myfile:
            exp_writer = csv.writer(myfile,delimiter=',')
            for i in mydata:
                exp_writer.writerow(i)
                
            messagebox.showinfo("Data Exported", "Your data has been exported to " +os.path.basename(fln)+ " Successfully")
               
    def get_data(self,ev):
          f=self.suptable.focus()
          content=(self.suptable.item(f))
          row=content['values']
          #print(row)
          self.expense_id_var.set(row[0]),
          self.var_Ename.set(row[1]),
          self.bal_type.set(row[2]),
          self.var_Etype.set(row[3]),
          self.debit.set(row[4]),
          self.credit.set(row[5]),
          self.var_Edate.set(row[6]),
          
          
    def clear(self):
          self.expense_id_var.set(""),
          self.var_Ename.set(""),
          self.bal_type.set(""),
          self.var_Etype.set(""),
          self.debit.set(""),
          self.credit.set(""),
          self.var_Edate.set(""),
          self.expense_searchtxt_var.set("")
          
          self.show()
          
          
       
                            
                  
con=sqlite3.connect(database=r'test1.db')
cur=con.cursor()                  
def connection():
             
       cur.execute("CREATE TABLE IF NOT EXISTS Expenses(expen_Id INTEGER PRIMARY KEY AUTOINCREMENT ,Ename VARCHAR(100),Type VARCHAR(100),Etype VARCHAR(100),Debit VARCHAR(200),Credit VARCHAR(100),Edate DATE)")
       
       con.commit()
connection()
    
       
if __name__=="__main__":
    root=Tk()
    obj=tranClass(root)
    root.mainloop()
    