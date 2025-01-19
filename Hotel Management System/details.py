from tkinter import *
from PIL import Image, ImageTk #pip install pillow
from tkinter import ttk
import random
import pymysql
from tkinter import messagebox
from time import strftime
from datetime import datetime




class DetailsRoom:
    def __init__(self, root):
        self.root=root
        self.root.title("Hotel Management System")
        self.root.geometry("1295x550+230+220")


        # Database connection variables
        self.db_host = "localhost"
        self.db_user = "root"
        self.db_password = "dhuri"
        self.db_name = "dbms_project"



        self.var_floor=StringVar()
        self.var_roomno=StringVar()
        self.var_roomtype=StringVar()
        self.var_roomavailable=StringVar(value="1")


        # ========== TITLE ==========
        lbl_title=Label(self.root, text="NEW ROOM DETAILS", font=("times new roman", 18, "bold"), bg="black", fg="gold", bd=4, relief=RIDGE)
        lbl_title.place(x=0, y=0, width=1295, height=50)

        # ========== LOGO ==========
        img2=Image.open("images\logohotel.png")
        img2=img2.resize((100, 40))
        self.photoimg2=ImageTk.PhotoImage(img2)

        lblimg=Label(self.root, image=self.photoimg2, bd=0, relief=RIDGE)
        lblimg.place(x=5, y=5, width=100, height=40)

        # ========== LABEL FRAME ==========
        labelframeleft=LabelFrame(self.root, bd=2, relief=RIDGE, text="Adding New Room", font=("times new roman", 12, "bold"), padx=2)
        labelframeleft.place(x=5, y=50, width=540, height=350)



        # ========== LABELS AND ENTRIES ==========

        # ========== FLOOR ==========
        lbl_floor=Label (labelframeleft, text="Floor", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_floor.grid(row=0, column=0, sticky="w", padx=20)

        entry_floor=ttk.Entry(labelframeleft, font=("arial", 13, "bold"), textvariable=self.var_floor, width=20)
        entry_floor.grid(row=0, column=1, sticky="w")


        # ========== ROOM NUMBER ==========
        lbl_RoomNo=Label(labelframeleft, text="Room Number", font=("arial", 12, "bold"),padx=2, pady=6)
        lbl_RoomNo.grid(row=1, column=0, sticky=W, padx=20)

        entry_RoomNo=ttk.Entry(labelframeleft, font=("arial",13,"bold"), textvariable=self.var_roomno, width=20)
        entry_RoomNo.grid(row=1, column=1, sticky=W)


        # ========== ROOM TYPE ==========
        lbl_RoomType=Label(labelframeleft, text="Room Type", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_RoomType.grid(row=2, column=0, sticky=W, padx=20)

        entry_RoomType=ttk. Entry(labelframeleft, font=("arial",13,"bold"), textvariable=self.var_roomtype, width=20)
        entry_RoomType.grid(row=2, column=1, sticky=W)


        # ========== ROOM AVAILABILITY ==========
        lbl_RoomAvailable=Label(labelframeleft, text="Room Available", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_RoomAvailable.grid(row=3, column=0, sticky=W, padx=20)

        entry_RoomAvailable=ttk. Entry(labelframeleft, font=("arial",13,"bold"), textvariable=self.var_roomavailable, width=20)
        entry_RoomAvailable.grid(row=3, column=1, sticky=W)


        # ========== BUTTONS ==========
        btn_frame=Frame(labelframeleft, bd=2, relief=RIDGE) 
        btn_frame.place(x=0, y=200, width=412, height=40) 

        btnAdd=Button(btn_frame, text="Add", command=self.add_data, font=("arial", 11, "bold"), bg="black", fg="gold", width=10) 
        btnAdd.grid(row=0, column=0, padx=1, pady=3) 

        btnUpdate=Button(btn_frame, text="Update", command=self.update, font=("arial", 11,"bold"), bg="black", fg="gold", width=10) 
        btnUpdate.grid(row=0, column=1, padx=1, pady=3) 

        btnDelete=Button(btn_frame, text="Delete", command=self.mDelete, font=("arial", 11, "bold"), bg="black", fg="gold", width=10) 
        btnDelete.grid(row=0, column=2, padx=1, pady=3) 
        
        btnReset=Button(btn_frame, text="Reset", command=self.reset, font=("arial", 11, "bold"), bg="black", fg="gold", width=10) 
        btnReset.grid(row=0, column=3, padx=1, pady=3)



         # ========== TABLE FRAME SEARCH SYSTEM ==========
        Table_Frame=LabelFrame(self.root, bd=2, relief=RIDGE, text="Available Room Details", font=("times new roman", 12, "bold"), padx=2)
        Table_Frame.place(x=600, y=55, width=600, height=350)


        scroll_x=ttk.Scrollbar(Table_Frame, orient=HORIZONTAL) 
        scroll_y=ttk.Scrollbar(Table_Frame, orient=VERTICAL) 
        
        self.room_table=ttk.Treeview(Table_Frame, column=("floor", "roomno", "roomtype", "available"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.room_table.xview)
        scroll_y.config(command=self.room_table.yview)


        self.room_table.heading("floor", text="Floor")
        self.room_table.heading("roomno", text="Room Number")
        self.room_table.heading("roomtype", text="Room Type")
        self.room_table.heading("available", text="Room Availability")

        self.room_table["show"]="headings" 
        
        self.room_table.column("floor", width=100)
        self.room_table.column("roomno", width=100)
        self.room_table.column("roomtype", width=100)
        self.room_table.column("available", width=100)

        self.room_table.pack(fill=BOTH, expand=1)
        self.room_table.bind("<ButtonRelease-1>", self.get_cursor)
        self.fetch_data()




        # ========== ADD ROOM DATA ==========
    def add_data(self):
        if self.var_floor.get()=="" or self.var_roomtype.get()=="": 
            messagebox.showerror("Error", "All fields are required") 
        else: 
            try:
                conn = pymysql.connect(host=self.db_host, user=self.db_user, password=self.db_password, database=self.db_name)
                my_cursor=conn.cursor() 
                my_cursor.execute("insert into details values(%s,%s,%s,%s)", 
                                (self.var_floor.get(), 
                                self.var_roomno.get(), 
                                self.var_roomtype.get(),
                                self.var_roomavailable.get(),

                                ))

                conn.commit()
                self.fetch_data()
                conn.close()

                messagebox.showinfo("Success", "New Room Added Successfully.", parent=self.root)

            except Exception as es:
                messagebox.showwarning("Warning", f"Something went wrong. Try again.:{str(es)}", parent=self.root)



    # ========== FETCH DATA TO DISPLAY ==========
    def fetch_data(self): 
        conn = pymysql.connect(host=self.db_host, user=self.db_user, password=self.db_password, database=self.db_name)
        my_cursor=conn.cursor() 
        my_cursor.execute("select * from details") 
        rows=my_cursor.fetchall() 
        if len(rows) != 0:
            self.room_table.delete(*self.room_table.get_children()) 
            for i in rows: 
                self.room_table.insert("", END, values=i) 
            conn.commit()
        conn.close()



    # ========== GET CURSOR ==========
    def get_cursor(self, event=""): 
        cursor_row=self.room_table.focus() 
        content=self.room_table.item(cursor_row) 
        row=content["values"]     

        self.var_floor.set(row[0]), 
        self.var_roomno.set(row[1]), 
        self.var_roomtype.set(row[2])
        self.var_roomavailable.set(row[3])



    # ========== UPDATE DATA ==========
    def update(self): 
        if self.var_floor.get()=="":
            messagebox.showerror("Error", "Please enter floor number", parent=self.root) 
        else:
            conn = pymysql.connect(host=self.db_host, user=self.db_user, password=self.db_password, database=self.db_name)
            my_cursor=conn.cursor()
            my_cursor.execute("update details set floor=%s, roomtype=%s, availability=%s where roomno=%s",     (self.var_floor.get(), 
                            self.var_roomtype.get(),
                            self.var_roomavailable.get(),
                            self.var_roomno.get()
                            ))
            conn.commit()
            self.fetch_data()
            conn.close()
            messagebox.showinfo("Update", "New Room Details has been updated successfully", parent=self.root)





    # ========== DELETE DATA ==========
    def mDelete(self):
        mDelete=messagebox.askyesno("Hotel Management System", "Do you want delete this room details?", parent=self.root)
        if mDelete>0:
            conn = pymysql.connect(host=self.db_host, user=self.db_user, password=self.db_password, database=self.db_name)
            my_cursor=conn.cursor()
            query="delete from details where roomno=%s"
            value=(self.var_roomno.get(),)
            my_cursor.execute(query, value)
        else:
            if not mDelete:
                return
        conn.commit()
        self.fetch_data()
        self.reset()
        conn.close()



    # ========== RESET ==========
    def reset(self):
        self.var_floor.set(""), 
        self.var_roomno.set(""),
        self.var_roomtype.set("")
        self.var_roomavailable.set("1")



if __name__ == "__main__":
    root=Tk()
    obj=DetailsRoom(root)
    root.mainloop()