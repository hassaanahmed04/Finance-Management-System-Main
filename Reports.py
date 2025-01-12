import tempfile
from tkinter import*
from tkinter import ttk,messagebox,filedialog
import sqlite3
import csv
import os

trail_balance=[]

sum_credit=None
loan=None
net=None

class reportsClass:
    def __init__(self,root):
       self.root=root
       self.root.geometry("1350x750+0+0")
       self.root.title("Reports") 
       self.root.config(bg="white")
       self.root.iconbitmap("kmc.ico")
       
       #=======Title
       
       title=Label(self.root,text="Trail Balance ", font=("times new roman",15,"bold"),bg="#010c48",fg="white",justify=CENTER).place(x=0,y=0,width=1350)
       
       global HEAD
       HEAD=["============TRAIL BALANCE============"]
       HEAD=[(HEAD)]
       
       self.entry_name=StringVar()
       self.id_var=StringVar()
       self.debit_var=StringVar()
       self.credit_var=StringVar()
       self.from_var=StringVar()
       self.to_var=StringVar()
       self.sum_debit=StringVar()
       self.check()
       self.Head=StringVar()
    #    self.trail_total()
       
           
       
       
       #=======Search expenses
       
       search_frame=LabelFrame(self.root,text="Search Trail Balance",bg="white",font=("Poppins",12),bd=2,relief=RIDGE)
       search_frame.place(x=10,y=480,width=400,height=130)     
       
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
       download_btn=Button(self.root,command=self.print_all,text="Print",font=("times new roman",15,"bold"),bg="#4caf50",fg="white",cursor="hand2").place(x=1150,y=480,width=150,height=60)
       refresh=Button(self.root,command=self.refresh,text="Refresh",font=("times new roman",15,"bold"),bg="#4caf50",fg="white",cursor="hand2").place(x=990,y=480,width=150,height=60)
       
       trail_frame=LabelFrame(self.root,text="Total Trail Balance",bg="white",font=("Poppins",12),bd=2,relief=RIDGE)
       trail_frame.place(x=440,y=480,width=400,height=130)
       #search_cal=Button(trail_frame,command=self.search_cal,text="Search",font=("times new roman",15,"bold"),bg="#4caf50",fg="white",cursor="hand2").place(x=300,y=20,width=80,height=30)
       lbl_Grand=Label(trail_frame,text="Total", font=("goudy old style",15),bg="white").place(x=10,y=20,width=110,height=20)

       lbl_total_debit=Label(trail_frame,text="Debit", font=("goudy old style",9),bg="black",fg="white").place(x=150,y=0,width=110,height=20)
       lbl_total_credit=Label(trail_frame,text="Credit", font=("goudy old style",9),bg="black",fg="white").place(x=280,y=0,width=110,height=20)
       txt_Total_Debit=Label(trail_frame,text=self.sum_debit, font=("goudy old style",15),bg="lightyellow").place(x=150,y=20,width=110,height=30)
       txt_Total_Credit=Label(trail_frame,text=sum_credit, font=("goudy old style",15),bg="lightyellow").place(x=280,y=20,width=110,height=30)
       
       lbl_total_loan=Label(trail_frame,text="Net", font=("goudy old style",9),bg="black",fg="white").place(x=150,y=50,width=110,height=20)
       lbl_total_Net=Label(trail_frame,text="Loan", font=("goudy old style",9),bg="black",fg="white").place(x=280,y=50,width=110,height=20)
       txt_Total_Net=Label(trail_frame,text=net, font=("goudy old style",15),bg="lightyellow").place(x=150,y=70,width=110,height=30)
       txt_Total_Loan=Label(trail_frame,text=loan, font=("goudy old style",15),bg="lightyellow").place(x=280,y=70,width=110,height=30)
      #====== refresh
       btn_refresh=Button(self.root,text="Refresh",command=self.refresh,font=("times new roman",15,"bold"),bg="green",fg="white",cursor="hand2").place(x=990,y=230,width=80,height=45)
       
       #========Entry Frame Details
       
       
       entry_frame=Frame(self.root,bd=3,relief=RIDGE)
       entry_frame.place(x=0,y=30,relwidth=1,height=440)
       
       scrolly=Scrollbar(entry_frame,orient=VERTICAL)
       scrollx=Scrollbar(entry_frame,orient=HORIZONTAL)
        
       self.enytryTable=ttk.Treeview(entry_frame,columns=("Eid","Ename","Type","Etype","Debit","Credit"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
       scrollx.pack(side=BOTTOM,fill=X)
       scrolly.pack(side=RIGHT,fill=Y)
       scrollx.config(command=self.enytryTable.xview)
       scrolly.config(command=self.enytryTable.yview)
        
       self.enytryTable.heading("Eid",text="ID")
       self.enytryTable.heading("Ename",text="Entry Name")
       self.enytryTable.heading("Type",text="Category")
       self.enytryTable.heading("Etype",text="Head")
       self.enytryTable.heading("Debit",text="Total")
       self.enytryTable.heading("Credit",text="Type")
    #    self.enytryTable.heading("Edate",text="Date")
       
        
       self.enytryTable["show"]="headings"
       self.enytryTable.column("Eid",width=50)
       self.enytryTable.column("Ename",width=100)
       self.enytryTable.column("Type",width=100)
       self.enytryTable.column("Etype",width=100)
       self.enytryTable.column("Debit",width=100)
       self.enytryTable.column("Credit",width=100)
    #    self.enytryTable.column("Edate",width=100)
       self.enytryTable.pack(expand=1,fill=BOTH)
       
       
       
       self.Trail_show()
       
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
           top='''================Trail Balance=================\n
ID\t Name\t\t Cat\t\t\t Head\t\t Total\t Type\n'''
           self.txtprint.delete("1.0",END)
           self.txtprint.insert('1.0',top)
           
    def print_middle(self):
             
         #   for row in self.rows:
             for i in trail_balance:
                  I_D=str(i[0])
                  Name=str(i[1])
                  
                  
                  Cat=str(i[2])
                  Head=str(i[3])
                  Tota=str(i[4])
                  Type=str(i[5])
                  
                  if len(Name)<15:
                        for i in range(len(Name),15):
                         Name=Name+" "
                  if len(Cat)<21:
                        for i in range(len(Cat),22):
                         Cat=Cat+" "
                  if len(Head)<10:
                        for i in range(len(Head),10):
                         Head=Head+" "
                  
                  self.txtprint.insert(END,"\n"+I_D+"\t"+Name+"\t"+Cat+"\t"+Head+"\t"+ Tota+"\t  "+Type)
                  
    def trail_total(self):
           
           
           bottom=f'''\n\n
===============================================
         |    Debit  : {self.sum_debit}          
         |    Crebit : {sum_credit}
Total    |------------------------------------     
         |    Loan   : {loan}    
         |    Net    : {net}
          ''' 
           self.txtprint.insert(END,bottom)
    def generate(self):
           new_file=tempfile.mktemp('.txt')
           open(new_file,'w').write(self.txtprint.get("1.0",END))
           os.startfile(new_file,'print')
       
   
            
                
    def Trail_show(self):
        connection
        
        
        try:
            cur.execute("DELETE FROM Trail")
            con.commit()
            debit='Debit'
            credit="Credit"
            
            #=====Inserting Data In Trail data
            
            cur.execute("INSERT INTO Trail(trail_Id ,Ename ,Type ,Etype ,Debit,Credit) Select expen_Id, Ename,Type, Etype, SUM(Debit),Credit from Expenses where Credit=? GROUP BY Ename",(credit,))
            cur.execute("INSERT INTO Trail(trail_Id ,Ename ,Type ,Etype ,Debit,Credit) Select expen_Id, Ename,Type, Etype, SUM(Debit),Credit from Expenses where Credit=? GROUP BY Ename",(debit,))
            con.commit()
                       #=============Getting Values
            
            cur.execute("Select trail_Id, Ename,Type, Etype, SUM(Debit),Credit from Trail where Credit=? GROUP BY Ename ",(credit,))
            row1=cur.fetchall() 
            # print("Debit is ",row1)
            cur.execute("Select trail_Id, Ename,Type, Etype, SUM(Debit),Credit from Trail where Credit=? GROUP BY Ename ",(debit,))

            row=cur.fetchall()
            # print("Trail data is :",row)
            for i in range(0,len(row1)):
                row.append(row1[i])
            # print("Debit is ",row)
            global tot_result
            global tot
            tot=["Total","T_Debit","T_Credit","Net","Loan"]
            tot=[(tot)]
            tot_result=["Values",self.sum_debit,sum_credit,net,loan]
            tot_result=[(tot_result)]

            global title
            title=["Id","Name","Category","Head","Total","Type"]
            title=[(title)]
            self.enytryTable.delete(*self.enytryTable.get_children())
            for i in row:
                  global trail_balance
                  trail_balance = row
                  self.enytryTable.insert('',END,values=i)
                  
        except Exception as ex:
             messagebox.showerror("Error",f"Error due to (save) :{str(ex)}",parent=self.root)

      
    def check(self):
             connection
             debit="Debit"
             credit="Credit"
         #  try:
             cur.execute("Select SUM(HIncome) from Head")
             row=cur.fetchone()
            
             
             self.Head=row[0]
             print("head ",self.Head)
             head=self.Head
             print("head ",head)
             if head==None:
               head=0
             cur.execute("Select SUM(Debit) from Expenses where Credit=?",(debit,))
             global sum_debit
             self.sum_debit=cur.fetchall()  
             self.sum_debit=self.sum_debit[0][0]
             
            # print("sum of debit is :",self.sum_debit)
             cur.execute("Select SUM(Debit) from Expenses where Credit=?",(credit,))
             global sum_credit
             sum_credit=cur.fetchall()  
             sum_credit=sum_credit[0][0]
             
             if sum_credit==None:
               sum_credit=0
             if self.sum_debit==None:
               self.sum_debit=0
             sum_credit=head+sum_credit
           #  print("Sum of debit is :",self.sum_debit)
             print("Sum of Credit is :",sum_credit)
             global loan
             global net
             
             if self.sum_debit>sum_credit:
                loan=self.sum_debit-sum_credit
                net=0
                sum_credit=loan+sum_credit
             elif sum_credit>self.sum_debit:
                net=sum_credit-self.sum_debit
                loan=0
                self.sum_debit=self.sum_debit+net
            
            
             
             
                   
         #  except Exception as ex:
         #     messagebox.showerror("Error",f"Error due to (check) :{str(ex)}",parent=self.root)
    
    def export(self):
        if(len(trail_balance)) < 1:
            messagebox.showerror("No Data", "No data available to export")
            return False
        fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="save csv" , filetypes=(("CSV FILE", "*.csv"),("All Files","*.*")))
        with open(fln, mode='w') as myfile:
            exp_writer = csv.writer(myfile,delimiter=',')
            for i in trail_balance:
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
                             mydata = HEAD+rows
                             self.enytryTable.insert('',END,values=i)     
                           messagebox.showinfo("Success","Data Shown",parent=self.root)                   
                        
                  
                  else:
                        messagebox.showerror("Error","No, Record Found try different",parent=self.root)
         except Exception as ex:
            messagebox.showerror("Error",f"Error due to (search_cal) :{str(ex)}",parent=self.root)           
   #  def refresh(self):
   #      root.destroy()
   #      os.popen("Reports.py") 
   
    
    def refresh(self):
      
       self.root.destroy()
       os.system('Reports.py')
           
       
   
       
con=sqlite3.connect(database=r'test1.db')
cur=con.cursor()                  
def connection():
             
       
       cur.execute("CREATE TABLE IF NOT EXISTS Expenses(expen_Id INTEGER PRIMARY KEY AUTOINCREMENT ,Ename VARCHAR(100),Type VARCHAR(100),Etype VARCHAR(100),Debit VARCHAR(200),Credit VARCHAR(100),Edate DATE)")
       
       
       cur.execute("CREATE TABLE IF NOT EXISTS Trail(trail_Id ,Ename VARCHAR(100),Type VARCHAR(100),Etype VARCHAR(100),Debit VARCHAR(200),Credit VARCHAR(100),Edate DATE)")

       con.commit()
connection()
if __name__=="__main__":
    root=Tk()
    obj=reportsClass(root)
    root.mainloop()
    
 
    
