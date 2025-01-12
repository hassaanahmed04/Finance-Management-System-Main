from tkinter import *
from tkinter import ttk,messagebox
from PIL import Image, ImageTk
from msilib.schema import SelfReg
from tkinter import*
from PIL import Image,ImageTk

from Transactions import tranClass
from Reports import reportsClass
from BalanceSheet import balanceClass
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import sqlite3
import pandas as pd
from head import headClass
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os



from head import headClass




class KMC:
    def __init__(self,root):
        self.root=root
        self.root.title("KASHMIR MODERN CITY ")
        self.root.geometry("1350x750+0+0")
        self.root.config(bg='white')
        # self.root.option_add('*Font', '25')
        title=Label(self.root,text="Finance Managment System ", font=("times new roman",40,"bold"),bg="#010c48",fg="white").place(x=0,y=0,relwidth=1,height=70)
        self.grand()
        self.remain_total=0
        self.check()
        self.root.iconbitmap("kmc.ico")
        
        # 

        self.min_w = 50 # Minimum width of the frame
        self.max_w = 220 # Maximum width of the frame
        self.cur_width = self.min_w # Increasing width of the frame
        self.expanded = False # Check if it is completely exanded
        
        
        
        

        
        self.head = Image.open('images/head.png').resize((40,40),Image.Resampling.LANCZOS)
        self.head=ImageTk.PhotoImage(self.head)
        self.Gleger = ImageTk.PhotoImage(Image.open('images/Gleger.png').resize((40,40),Image.Resampling.LANCZOS))
        self.trail = ImageTk.PhotoImage(Image.open('images/home.png').resize((40,40),Image.Resampling.LANCZOS))
        self.h1 = ImageTk.PhotoImage(Image.open('images/bsb.png').resize((40,40),Image.Resampling.LANCZOS))
        self.login_pic=ImageTk.PhotoImage(Image.open('images/logo.png').resize((40,40),Image.Resampling.LANCZOS))
        self.login_show=ImageTk.PhotoImage(Image.open('images/logo.png').resize((150,150),Image.Resampling.LANCZOS))
        root.update() # For the width to get updated
        self.frame = Frame(self.root,bg='#010c48',width=50,height=root.winfo_height())
        self.frame.place(x=0,y=10)
        self.photo = PhotoImage(file = r"images/logo.png")
        self.photo = self.photo.subsample(12,12)

        # Make the buttons with the icons to be shown
        self.login_b=Label(self.frame,image=self.photo,bg='#010c48')
        self.head_b = Button(self.frame,image=self.head,bg='#010c48',command=self.Head,fg="white",relief='flat')
        self.Gleger_b = Button(self.frame,image=self.Gleger,bg='#010c48',command=self.Tran,fg="white",relief='flat')
        self.trail_b = Button(self.frame,image=self.trail,bg='#010c48',command=self.Reports,fg="white",relief='flat')
        self.h1_b = Button(self.frame,image=self.h1,bg='#010c48',fg="white",command=self.balance,relief='flat')
      
        # Put them on the self.frame
        self.login_b.grid(row=0,column=0,pady=40)
        self.head_b.grid(row=1,column=0,pady=20)
        self.Gleger_b.grid(row=2,column=0,pady=20)
        self.trail_b.grid(row=3,column=0,pady=20)
        self.h1_b.grid(row=4,column=0,pady=20)
       
        # Bind to the self.frame, if entered or left
        self.frame.bind('<Enter>',lambda e: self.expand())
        self.frame.bind('<Leave>',lambda e: self.contract())

        # So that it does not depend on the widgets inside the self.frame
        self.frame.grid_propagate(False)
        # self.remain_total=total

        txt_grand_head=Label(self.root,text=total, font=("goudy old style",14),bg="white").place(x=430,y=70,height=30)
        lbl_grand_head=Label(self.root,text="Grand Total: Rs", font=("goudy old style",14),bg="white").place(x=300,y=70,height=30)

        txt_grand_remain=Label(self.root,text=self.remain_total, font=("goudy old style",14),bg="white").place(x=840,y=70,height=30)
        lbl_grand_remain=Label(self.root,text="Remaining Total: Rs", font=("goudy old style",14),bg="white").place(x=670,y=70,height=30)
        btn_refresh=Button(self.root,text="Refresh",command=self.refresh,font=("times new roman",15,"bold"),bg="green",fg="white",cursor="hand2").place(x=990,y=70,width=80,height=30)


        #======Head
        
        self.data()
    
    def balance(self):
        
         self.bal_win=Toplevel(self.root)
         self.bal_obj=balanceClass(self.bal_win)     
    
    def Tran(self):
        self.tran_win=Toplevel(self.root)
        self.tran_obj=tranClass(self.tran_win)
    def Reports(self):
        self.report_win=Toplevel(self.root)
        self.report_obj=reportsClass(self.report_win)
    def Head(self):
        self.head_win=Toplevel(self.root)
        self.head_obj=headClass(self.head_win)
        
    #========Slider Menu

    def expand(self):
        
        self.cur_width += 10 # Increase the width by 10
        rep = root.after(5,self.expand) # Repeat this func every 5 ms
        self.frame.config(width=self.cur_width) # Change the width to new increase width
        if self.cur_width >= self.max_w: # If width is greater than maximum width 
            self.expanded = True # self.frame is expended
            root.after_cancel(rep) # Stop repeating the func
            self.fill()

    def contract(self):
       
        self.cur_width -= 10 # Reduce the width by 10 
        rep = root.after(5,self.contract) # Call this func every 5 ms
        self.frame.config(width=self.cur_width) # Change the width to new reduced width
        if self.cur_width <= self.min_w: # If it is back to normal width
            self.expanded = False # self.frame is not self.expanded
            root.after_cancel(rep) # Stop repeating the func
            self.fill()

    def fill(self):
        if self.expanded: # If the self.frame is exanded
            # Show a text, and remove the image
            self.login_b.config(image=self.login_show,font=(100,100),bg="#010c48")
            self.head_b.config(text='Head',image='',font=(0,21))
            self.Gleger_b.config(text='G-Ledger',image='',font=(0,21))
            self.trail_b.config(text='Trail-Balance',image='',font=(0,21))
            self.h1_b.config(text='Balance-Sheet',image='',font=(0,21))
            
        else:
            # Btrail the image back
            self.login_b.config(image=self.photo,font=(0,21),bg="#010c48")
            self.head_b.config(image=self.head,font=(0,21))
            self.Gleger_b.config(image=self.Gleger,font=(0,21))
            self.trail_b.config(image=self.trail,font=(0,21))
            self.h1_b.config(image=self.h1,font=(0,21))
            
    def refresh(self):
        
        self.root.destroy()
        os.system('dashboard.py')
    def data(self):
        connection
    #======Getting Data from database
        debit="Debit"
        credit="Credit"
        xaxis=[]
        yaxis=[]
        name=[]
        checks=[]
        cks=[]
    
        cur.execute("Select Debit from Trail where Credit=?",(debit,))
        row_debit=cur.fetchall()
        
        for i in row_debit:
            xaxis.append(i[0])
        cur.execute("Select Debit from Trail where Credit=?",(credit,))
        row=cur.fetchall()
        
        for i in row:
            
            yaxis.append(i[0])
        print(xaxis)
        print(yaxis)

        xaxis = [eval(i) for i in xaxis]
        yaxis = [eval(i) for i in yaxis]
        cur.execute("Select Type from Balance")
        check=cur.fetchall()
        # print(check)
        for i in check:
            checks.append(i[0])
        # print(checks)

        cur.execute("Select Debit from Balance")
        ck=cur.fetchall()
        # print(ck)
        for i in ck:
            cks.append(i[0])
        # print(cks)
        cur.execute("Select Ename from Trail")
        names=cur.fetchall()
        for i in names:
            name.append(i[0])
        
        #======PIE Chart 
        
        frameChartsLT = Frame(root)
        frameChartsLT.place(x=700,y=130)
        
        # print("pie chart values",pie_chart)

        fig = Figure() # create a figure object
        ax = fig.add_subplot(111) # add an Axes to the figure

        ax.pie(cks, radius=0.8,labels=checks, autopct='%0.2f%%',)

        chart1 = FigureCanvasTkAgg(fig,frameChartsLT)
        chart1.get_tk_widget().pack()
        
        for i in range(len(xaxis),len(yaxis)):
            xaxis.append(0)
        # print("xaxis is :",xaxis)
        for i in range(len(yaxis),len(xaxis)):
            yaxis.append(0)
        # print("yaxis is :",yaxis)
        

        # # ==== BAR Chart
        xaxis.append(0)
        yaxis.append(0)
       
           

        data1 = {'Debit': yaxis,
        'Credit': xaxis
        }
        df1 = pd.DataFrame(data1)
        print(data1)
        

        
        figure1 = plt.Figure(figsize=(7, 4), dpi=90)
        ax1 = figure1.add_subplot(111)
        
        bar1 = FigureCanvasTkAgg(figure1, root)
        bar1.get_tk_widget().pack(side=LEFT,padx=220)
        df1 = df1[['Debit', 'Credit']].groupby('Debit').sum()
        df1.plot(kind='bar', legend=True , ax=ax1 )
        ax1.set_title('Debit Vs Credit')
        ax1.set_xlabel('Debit')
        ax1.set_ylabel('Credit')        
            
        
        
   



#======Grand Total

    def grand(self):
            
            try:
                cur.execute("Select SUM(HIncome) from Head")
                row=cur.fetchone()
                
                global total
                total=row[0]
                if total==None:
                   total=0
                print(total)
            
                
            except Exception as ex:
                messagebox.showerror("Error",f"Error  due to (show):{str(ex)}",parent=root)
    
    def check(self):
            connection
            debit="Debit"
            credit="Credit"
            try:
                cur.execute("Select SUM(Debit) from Expenses where Credit=?",(debit,))
                
                sum_debit=cur.fetchall()  
                print(sum_debit)
                sum_debit=sum_debit[0][0]
                if sum_debit==None:
                    sum_debit=0
                print(type(sum_debit))

                
                cur.execute("Select SUM(Debit) from Expenses where Credit=?",(credit,))
                
                sum_credit=cur.fetchall()  
                sum_credit=sum_credit[0][0]
                
                if sum_credit==None:
                    sum_credit=0
                self.remain_total=total
                self.remain_total+=sum_credit
                self.remain_total-=sum_debit
                
                
                
                
                    
            except Exception as ex:
                messagebox.showerror("Error",f"Error due to (check) :{str(ex)}",parent=root)
    

        


     

con=sqlite3.connect(database=r'test1.db')
cur=con.cursor()   

def connection():
             
       
       cur.execute("CREATE TABLE IF NOT EXISTS Expenses(expen_Id INTEGER PRIMARY KEY AUTOINCREMENT ,Ename VARCHAR(100),Type VARCHAR(100),Etype VARCHAR(100),Debit VARCHAR(200),Credit VARCHAR(100),Edate DATE)")
       
       
       cur.execute("CREATE TABLE IF NOT EXISTS Balance(bal_Id ,Ename VARCHAR(100),Type VARCHAR(100),Etype VARCHAR(100),Debit VARCHAR(200),Credit VARCHAR(100),Edate DATE)")

       con.commit()
connection()




    
if __name__=="__main__":
    root=Tk()
    obj=KMC(root)
    root.mainloop()
    