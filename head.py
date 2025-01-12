from tkinter import*
from tkinter import ttk,messagebox,filedialog
import csv
import os
import sqlite3
import tempfile
title=[]
total=0


class headClass:
    def __init__(self,root):
        self.root=root
        self.root.title("KASHMIR MODERN CITY")
        self.root.geometry("1350x750+0+0")
        self.root.config(bg='white')
        self.root.iconbitmap("kmc.ico")
        title=Label(self.root,text="All heads", font=("times new roman",40,"bold"),bg="#010c48",fg="White").place(x=0,y=0,relwidth=1,height=70)
      
        #======variables
        
        self.enter_head=StringVar()
        self.head_income=StringVar()
        self.head_id=StringVar()
        self.head_date=StringVar()
        self.grand_total=StringVar()
        self.expense_searchType_var=StringVar()
        self.expense_searchtxt_var=StringVar()
        self.from_var=StringVar()
        self.to_var=StringVar()
        self.grand()
        self.check()
        global HEAD
        HEAD=["============HEADS============"]
        HEAD=[(HEAD)]
        #======Input 
        lbl_id_head=Label(self.root,text="ID", font=("goudy old style",14),bg="white").place(x=0,y=70,width=110,height=20)
        txt_id_head=Entry(self.root,textvariable=self.head_id, font=("goudy old style",25),bg="lightyellow").place(x=10,y=90,width=150,height=30)

        
        lbl_enter_head=Label(self.root,text="Head", font=("goudy old style",14),bg="white").place(x=170,y=70,width=110,height=20)
        txt_enter_head=Entry(self.root,textvariable=self.enter_head, font=("goudy old style",25),bg="lightyellow").place(x=175,y=90,width=150,height=30)
        
        lbl_head_income=Label(self.root,text="Income", font=("goudy old style",14),bg="white").place(x=340,y=70,width=110,height=20)
        txt_head_income=Entry(self.root,textvariable=self.head_income, font=("goudy old style",25),bg="lightyellow").place(x=340,y=90,width=150,height=30)
       
        lbl_head_date=Label(self.root,text="Date", font=("goudy old style",14),bg="white").place(x=510,y=70,width=110,height=20)
        txt_head_date=Entry(self.root,textvariable=self.head_date, font=("goudy old style",25),bg="lightyellow").place(x=510,y=90,width=150,height=30)

        txt_grand_head=Label(self.root,text=total, font=("goudy old style",14),bg="white").place(x=140,y=620,height=20)
        lbl_grand_head=Label(self.root,text="Grand Total: Rs", font=("goudy old style",14),bg="white").place(x=10,y=620,height=20)
        
        txt_grand_remain=Label(self.root,text=remain_total, font=("goudy old style",14),bg="white").place(x=550,y=620,height=20)
        lbl_grand_remain=Label(self.root,text="Remaining Total: Rs", font=("goudy old style",14),bg="white").place(x=380,y=620,height=20)

        #====Buttons
        
        btn_create=Button(self.root,text="Save",command=self.Save,font=("times new roman",15,"bold"),bg="green",fg="white",cursor="hand2").place(x=10,y=150,width=100,height=45)
        btn_upgrade=Button(self.root,text="Update",command=self.update,font=("times new roman",15,"bold"),bg="blue",fg="white",cursor="hand2").place(x=160,y=150,width=100,height=45)
        
        btn_delete=Button(self.root,text="Delete",command=self.delete,font=("times new roman",15,"bold"),bg="red",fg="white",cursor="hand2").place(x=310,y=150,width=100,height=45)
        btn_reset=Button(self.root,text="Reset",font=("times new roman",15,"bold"),bg="black",fg="white",cursor="hand2").place(x=460,y=230,width=170,height=45)
        btn_refresh=Button(self.root,text="Refresh",command=self.refresh,font=("times new roman",15,"bold"),bg="green",fg="white",cursor="hand2").place(x=490,y=150,width=100,height=45)
      #  self.refresh()
        #========Head Frame Details
       
        head_frame=Frame(self.root,bd=3,relief=RIDGE)
        head_frame.place(x=0,y=200,relwidth=1,height=400)
        head_frame.config(bg="black")
       
        scrolly=Scrollbar(head_frame,orient=VERTICAL)
        scrollx=Scrollbar(head_frame,orient=HORIZONTAL)
      #   style = ttk.Style(root)

      #   style.theme_use("clam")
      #   style.configure("Treeview", background="black", fieldbackground="black", foreground="white")
        self.suptable=ttk.Treeview(head_frame,columns=("head_Id","Hname","HIncome","Hdate"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.suptable.xview)
        scrolly.config(command=self.suptable.yview)
        
        self.suptable.heading("head_Id",text="ID")
        self.suptable.heading("Hname",text="Head name ")
        self.suptable.heading("HIncome",text="Head Income")
        self.suptable.heading("Hdate",text="Date")
        
            
            
        self.suptable["show"]="headings"
        self.suptable.column("head_Id",width=50)
        self.suptable.column("Hname",width=100)
        self.suptable.column("HIncome",width=100)
        self.suptable.column("Hdate",width=100)
        
        self.suptable.pack(expand=1,fill=BOTH)
        self.suptable.bind("<ButtonRelease-1>",self.get_data)
            
        self.show()
        self.grand()
       
        
        #====CRUD
     
        search_frame=LabelFrame(self.root,text="Search Head",bg="white",font=("Poppins",12),bd=2,relief=RIDGE)
        search_frame.place(x=750,y=70,width=550,height=130)  
       

       
        spin_search=ttk.Combobox(search_frame,textvariable=self.expense_searchType_var,values=("Select","ID","Head","Date"),state="readonly",justify=CENTER,font=("goudy old style",15))
        spin_search.place(x=10,y=10,width=100,height=30)
        spin_search.current(0)
       
        search_entry=Entry(search_frame,textvariable=self.expense_searchtxt_var,font=("goudy old style",15),bg="lightyellow").place(x=115,y=10,width=150,height=30)
        search_button=Button(search_frame,command=self.search,text="Search",font=("times new roman",15,"bold"),bg="#4caf50",fg="white",cursor="hand2").place(x=270,y=10,width=150,height=30)
        search_cal=Button(search_frame,command=self.search_cal,text="cal",font=("times new roman",15,"bold"),bg="#4caf50",fg="white",cursor="hand2").place(x=270,y=50,width=150,height=30)
        btn_Download=Button(search_frame,text="Print",command=self.print_all,font=("times new roman",15,"bold"),bg="blue",fg="white",cursor="hand2").place(x=430,y=20,width=115,height=50)
         #====Calender
       
        lbl_from_date=Label(search_frame,text="from: YYYY/MM/DD", font=("goudy old style",8),bg="white").place(x=5,y=75,width=110,height=30)
        txt_from_date=Entry(search_frame,textvariable=self.from_var, font=("goudy old style",15),bg="lightyellow").place(x=10,y=50,width=100,height=30)
        lbl_to_date=Label(search_frame,text="To: YYYY/MM/DD", font=("goudy old style",8),bg="white").place(x=135,y=80,width=110,height=20)

        txt_to_date=Entry(search_frame,textvariable=self.to_var, font=("goudy old style",15),bg="lightyellow").place(x=115,y=50,width=150,height=30)
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
         #   "head_Id","Hname","HIncome","Hdate"
           top='''================Heads=================\n
ID\t\t Name\t\t\t Income\t\t\t Date
'''
           self.txtprint.delete("1.0",END)
           self.txtprint.insert('1.0',top)
           
    def print_middle(self):
             
         #   for row in self.rows:
             for i in mydata:
                  I_D=str(i[0])
                  Name=str(i[1])
                  
                  
                  Income=str(i[2])
                  Date=str(i[3])
                  if len(Name)<15:
                        for i in range(len(Name),15):
                         Name=Name+" "
                  Name=str(Name)
                  self.txtprint.insert(END,"\n"+I_D+"\t\t"+Name+"\t\tRS."+Income+"\t\t"+Date)
                  
                  print(Name,"\t\t",Income,"\t\t",Date)
    def generate(self):
           new_file=tempfile.mktemp('.txt')
           open(new_file,'w').write(self.txtprint.get("1.0",END))
           os.startfile(new_file,'print')
               
    def Save(self):
          connection
          try:
             if self.head_id.get()=="":
                  messagebox.showerror("Error","Id must be required",parent=self.root)
             else:
                  cur.execute("Select * from Head where head_id=?",(self.head_id.get(),))
                  row=cur.fetchone()
                  if row!=None:
                         messagebox.showerror("Error","Id already exits, add different",parent=self.root)
                         
                  else:
                        cur.execute("Insert into Head (Hname,HIncome,Hdate) values(?,?,?)",(
                           self.enter_head.get(),
                           self.head_income.get(),
                           self.head_date.get(),
                          
                           
                        ))
                        con.commit()
                        messagebox.showinfo("Success","New Head Added",parent=self.root)
                        
                        self.show()
                       
          except Exception as ex:
             messagebox.showerror("Error",f"Error due to (save) :{str(ex)}",parent=self.root)
    def show(self):
          connection
          try:
             cur.execute("select * from Head")
             rows=cur.fetchall()
             
              
             
             self.suptable.delete(*self.suptable.get_children())
             for row in rows:
                  global mydata
                  mydata = rows
                  self.suptable.insert('',END,values=row)
                  
          except Exception as ex:
               messagebox.showerror("Error",f"Error  due to (show):{str(ex)}",parent=self.root)
    def export(self):
        if(len(mydata)) < 1:
            messagebox.showerror("No Data", "No data available to export")
            return False
        fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="save csv" , filetypes=(("CSV FILE", "*.csv"),("All Files","*.*")))
        with open(fln, mode='w') as myfile:
            exp_writer = csv.writer(myfile,delimiter=',')
            for i in mydata:
                exp_writer.writerow(i)
                
            messagebox.showinfo("Data Exported", "Your data has been exported to " +os.path.basename(fln)+ "Successfully")
                          
    def grand(self):
         connection
         try:
              cur.execute("Select SUM(HIncome) from Head")
              row=cur.fetchone()
              print(row)
              global total
              total=row[0]
              if total==None:
                  total=0
              
          
               
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
             
             cur.execute("Select SUM(Debit) from Expenses where Credit=?",(credit,))
             global sum_credit, remain_total
             sum_credit=cur.fetchall()  
             sum_credit=sum_credit[0][0]
             if sum_credit==None:
                    sum_credit=0
            
             remain_total=total
             remain_total+=sum_credit
             remain_total-=sum_debit
             
             
             
             
             
                   
          except Exception as ex:
             messagebox.showerror("Error",f"Error due to (check) :{str(ex)}",parent=self.root)           
    def update(self):
          connection
          try:
             if self.head_id.get()=="":
                  messagebox.showerror("Error","Id must be required",parent=self.root)
             else:
                  cur.execute("Select * from Head where head_id=?",(self.head_id.get(),))
                  row=cur.fetchone()

                  if row==None:
                         messagebox.showerror("Error","Invalid Id",parent=self.root)
                         
                  else:
                        cur.execute("Update Head set Hname=?,HIncome=?,Hdate=? where head_id=?",(
                           self.enter_head.get(),
                           self.head_income.get(),
                           self.head_date.get(),
                           self.head_id.get(),
                           
                        ))
                        con.commit()
                        messagebox.showinfo("Success","Ledger Updated Success",parent=self.root)
                        
                        self.show()
          except Exception as ex:
             messagebox.showerror("Error",f"Error due to (update):{str(ex)}",parent=self.root)
    def delete(self):
          connection
          try:
             if self.head_id.get()=="":
                  messagebox.showerror("Error","Id must be required",parent=self.root)
             else:
                  cur.execute("Select * from Head where head_id=?",(self.head_id.get(),))
                  row=cur.fetchone()
                  if row==None:
                         messagebox.showerror("Error","Invalid Id",parent=self.root)
                         
                  else:
                        confirmation=messagebox.askyesno("Confirm","Do you want to delete?",parent=self.root)
                        if confirmation==True:
                               cur.execute("delete from Head where head_id=?",(self.head_id.get(),))
                               con.commit()
                               messagebox.showinfo("Success","Deleted Successfully",parent=self.root)
                        
                       
                               
                               self.show()
          except Exception as ex:
             messagebox.showerror("Error",f"Error due to (delete):{str(ex)}",parent=self.root)          
    def show(self):
          connection
          try:
             cur.execute("select * from Head")
             rows=cur.fetchall()
            #  global test
            #  test=rows
            #  print("Test rows is :"+str(test))
             
             self.suptable.delete(*self.suptable.get_children())
             for row in rows:
                  global mydata
                  mydata = rows
                  self.suptable.insert('',END,values=row)
                  
          except Exception as ex:
               messagebox.showerror("Error",f"Error  due to (show):{str(ex)}",parent=self.root)
    def refresh(self):
       self.root.destroy()
       os.system('head.py')
    
    def search_cal(self):
      
         connection
         try:
            if  self.from_var.get()=="" or self.to_var.get()=="":
                  messagebox.showerror("Error","Dates can't be empty",parent=self.root)
            else:
                  start=self.from_var.get()
                  end=self.to_var.get()
                  cur.execute("Select * from Head where Hdate BETWEEN ? AND ?",(start,end))
                  
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
                        
                         cur.execute("Select * from Head where head_Id LIKE '%"+self.expense_searchtxt_var.get()+"%' ")
                  elif self.expense_searchType_var.get()=="Head":
                        
                        cur.execute("Select * from Head where Hname LIKE '%"+self.expense_searchtxt_var.get()+"%' ")
                  elif self.expense_searchType_var.get()=="Date":
                        
                        cur.execute("Select * from Head where Hdate LIKE '%"+self.expense_searchtxt_var.get()+"%' ")
                  #cur.execute("Select * from Head where Credit LIKE '%"+self.expense_searchtxt_var.get()+"%' ")
                  rows=cur.fetchall()
                  
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

    def get_data(self,ev):
          f=self.suptable.focus()
          content=(self.suptable.item(f))
          row=content['values']
          #print(row)
          self.head_id.set(row[0]),
          self.enter_head.set(row[1])
          self.head_income.set(row[2]),
          self.head_date.set(row[3]),
      #     self.var_Etype.set(row[3]),
      #     self.debit.set(row[4]),
      #     self.credit.set(row[5]),
      #     self.var_Edate.set(row[6]),
con=sqlite3.connect(database=r'test1.db')
cur=con.cursor()   



  
def connection():
             
       
             
       
       cur.execute("CREATE TABLE IF NOT EXISTS Head(head_id INTEGER PRIMARY KEY AUTOINCREMENT,Hname VARCHAR(100),HIncome VARCHAR(100),hdate DATE)")

       con.commit()
connection()       

if __name__=="__main__":
    root=Tk()
    obj=headClass(root)
    root.mainloop()
    