from tkinter import *
from PIL import Image, ImageTk #pip install pillow
from tkinter import ttk
import random
import pymysql
from tkinter import messagebox
from time import strftime
from datetime import datetime
import qrcode



# Global variable to store the final bill amount
final_bill = None


class Roombooking:
    def __init__(self, root):
        self.root=root
        self.root.title("Hotel Management System")
        self.root.geometry("1295x550+230+220")


        # Database connection variables
        self.db_host = "localhost"
        self.db_user = "root"
        self.db_password = "dhuri"
        self.db_name = "dbms_project"


        # ========== VARIABLES ==========
        self.var_contact=StringVar()
        self.var_checkin=StringVar()
        self.var_checkout=StringVar()
        self.var_roomtype=StringVar()
        self.var_roomavailable=StringVar()
        self.var_meal=StringVar()
        self.var_noofdays=StringVar()
        self.var_paidtax=StringVar()
        self.var_actualtotal=StringVar()
        self.var_total=StringVar()


        # ========== TITLE ==========
        lbl_title=Label(self.root, text="ROOM BOOKINGS DETAILS", font=("times new roman", 18, "bold"), bg="black", fg="gold", bd=4, relief=RIDGE)
        lbl_title.place(x=0, y=0, width=1295, height=50)

        # ========== LOGO ==========
        img2=Image.open("images\logohotel.png")
        img2=img2.resize((100, 40))
        self.photoimg2=ImageTk.PhotoImage(img2)

        lblimg=Label(self.root, image=self.photoimg2, bd=0, relief=RIDGE)
        lblimg.place(x=5, y=5, width=100, height=40)

        # ========== LABEL FRAME ==========
        labelframeleft=LabelFrame(self.root, bd=2, relief=RIDGE, text="Room Booking Details", font=("times new roman", 12, "bold"), padx=2)
        labelframeleft.place(x=5, y=50, width=425, height=490)

        # ========== LABELS AND ENTRIES ==========

        # ========== CUSTOMER CONTACT ==========
        lbl_cust_contact=Label (labelframeleft, text="Customer Contact", font=("arial", 12, "bold"), padx=2, pady=6)
        lbl_cust_contact.grid(row=0, column=0, sticky="w")

        entry_contact=ttk.Entry(labelframeleft, font=("arial", 13, "bold"),   width=18, textvariable=self.var_contact)
        entry_contact.grid(row=0, column=1, sticky="w")

        # ========== FETCH DATA BUTTON ==========
        btnFetchData=Button(labelframeleft, command=self.fetch_contact, text="Fetch Data", font=("arial", 11, "bold"), bg="black", fg="gold", width=8) 
        btnFetchData.place(x=331, y=4) 


        # ========== CHECK_IN DATE ==========
        check_in_date=Label(labelframeleft,font=("arial",12,"bold"),text="Check_in Date:",padx=2, pady=6)
        check_in_date.grid(row=1,column=0,sticky="w")
        txtcheck_in_date=ttk.Entry(labelframeleft, font=("arial",13,"bold"),width=29, textvariable=self.var_checkin)
        txtcheck_in_date.grid(row=1, column=1)

        # ========== CHECK_OUT DATE ==========
        lbl_Check_out=Label(labelframeleft, font=("arial", 12, "bold"), text="Check_Out Date:",padx=2, pady=6)
        lbl_Check_out.grid(row=2, column=0, sticky="w")
        txt_Check_out=ttk.Entry(labelframeleft, font=("arial",13,"bold"),width=29, textvariable=self.var_checkout)
        txt_Check_out.grid(row=2, column=1)

        # ========== ROOM TYPE ==========
        label_RoomType = Label(labelframeleft, font=("arial", 12, "bold"), text="Room Type:", padx=2, pady=6)
        label_RoomType.grid(row=3, column=0, sticky="w")

        combo_RoomType = ttk.Combobox(
            labelframeleft,
            font=("arial", 12, "bold"),
            width=27,
            state="readonly",
            textvariable=self.var_roomtype
        )
        combo_RoomType["value"] = ("Single", "Double", "Luxury")
        combo_RoomType.current(0)
        combo_RoomType.grid(row=3, column=1)

        # ========== AVAILABLE ROOM ==========
        lblRoomAvailable = Label(labelframeleft, font=("arial", 12, "bold"), text="Available Room: ", padx=2, pady=6)
        lblRoomAvailable.grid(row=4, column=0, sticky="w")

        combo_RoomNumber = ttk.Combobox(
            labelframeleft,
            font=("arial", 12, "bold"),
            width=27,
            state="readonly",
            textvariable=self.var_roomavailable
        )
        combo_RoomNumber.grid(row=4, column=1)

        # Function to update available rooms based on selected room type
        def update_available_rooms(event):
            selected_room_type = self.var_roomtype.get()
            try:
                conn = pymysql.connect(host=self.db_host, user=self.db_user, password=self.db_password, database=self.db_name)
                my_cursor = conn.cursor()
                query = """
                    SELECT roomno 
                    FROM details 
                    WHERE roomtype = %s AND availability = 1
                """
                my_cursor.execute(query, (selected_room_type,))
                rows = my_cursor.fetchall()
                conn.close()

                # Update the combo box with available rooms
                combo_RoomNumber["value"] = [row[0] for row in rows]
                if rows:
                    combo_RoomNumber.current(0)
                else:
                    combo_RoomNumber.set("No rooms available")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to fetch available rooms: {str(e)}")

        # Bind the event to Room Type combo box
        combo_RoomType.bind("<<ComboboxSelected>>", update_available_rooms)

    
        # ========== MEAL ==========
        lblMeal=Label(labelframeleft, font=("arial", 12, "bold"), text="Meal: ",padx=2, pady=6)
        lblMeal.grid(row=5, column=0, sticky="w")
        txtMeal=ttk.Entry(labelframeleft, font=("arial", 13, "bold"), width=29, textvariable=self.var_meal)
        txtMeal.grid(row=5, column=1)

        # ========== NO OF DAYS ==========
        lblNoOfDays=Label(labelframeleft, font=("arial", 12, "bold"), text="No Of Days: ", padx=2,pady=6)
        lblNoOfDays.grid(row=6, column=0, sticky="w")
        txtNoOfDays=ttk.Entry(labelframeleft, font=("arial", 13, "bold"),width=29, textvariable=self.var_noofdays)
        txtNoOfDays.grid(row=6, column=1)

        # ========== PAID TAX ==========
        lblNoOfDays=Label(labelframeleft, font=("arial", 12, "bold"), text="Paid Tax:",padx=2, pady=6)
        lblNoOfDays.grid(row=7, column=0, sticky="w")
        txtNoOfDays=ttk.Entry(labelframeleft, font=("arial", 13, "bold"), width=29, textvariable=self.var_paidtax)
        txtNoOfDays.grid(row=7, column=1)

        # ========== SUB TOTAL ==========
        lblNoOfDays=Label(labelframeleft, font=("arial", 12, "bold"), text="Sub Total: ", padx=2, pady=6)
        lblNoOfDays.grid(row=8, column=0, sticky="w")
        txtNoOfDays=ttk.Entry(labelframeleft, font=("arial", 13, "bold"),width=29, textvariable=self.var_actualtotal)
        txtNoOfDays.grid(row=8, column=1)

        # ========== TOTAL COST ==========
        lblIdNumber=Label(labelframeleft, font=("arial", 12, "bold"), text="Total Cost: ", padx=2, pady=6)
        lblIdNumber.grid(row=9, column=0, sticky="w")
        txtIdNumber=ttk.Entry(labelframeleft, font=("arial", 13, "bold"), width=29, textvariable=self.var_total)
        txtIdNumber.grid(row=9, column=1)


        # ========== BILL BUTTON ==========
        btnBill=Button(labelframeleft, text="Bill", command=self.total_bill, font=("arial", 11, "bold"), bg="black", fg="gold", width=10) 
        btnBill.grid(row=10, column=0, padx=1, pady=3, sticky="w") 
        
        
        # ========== QRCODE BUTTON ==========
        btnQr=Button(labelframeleft, text="QR", command=self.generate_qr_code, font=("arial", 11, "bold"), bg="black", fg="gold", width=10) 
        btnQr.grid(row=10, column=1, padx=1, pady=3, sticky="w") 


        # ========== BUTTONS ==========
        btn_frame=Frame(labelframeleft, bd=2, relief=RIDGE) 
        btn_frame.place(x=0, y=400, width=412, height=40) 

        btnAdd=Button(btn_frame, text="Add", command=self.add_data, font=("arial", 11, "bold"), bg="black", fg="gold", width=10) 
        btnAdd.grid(row=0, column=0, padx=1, pady=3) 

        btnUpdate=Button(btn_frame, text="Update", command=self.update, font=("arial", 11,"bold"), bg="black", fg="gold", width=10) 
        btnUpdate.grid(row=0, column=1, padx=1, pady=3) 

        btnDelete=Button(btn_frame, text="Delete", command=self.mDelete, font=("arial", 11, "bold"), bg="black", fg="gold", width=10) 
        btnDelete.grid(row=0, column=2, padx=1, pady=3) 
        
        btnReset=Button(btn_frame, text="Reset", command=self.reset, font=("arial", 11, "bold"), bg="black", fg="gold", width=10) 
        btnReset.grid(row=0, column=3, padx=1, pady=3)


        # ========== RIGHT SIDE IMAGE ==========
        img3=Image.open(r"images\bed.jpg")
        img3=img3.resize((400, 300))
        self.photoimg3=ImageTk.PhotoImage(img3)

        lblimg=Label(self.root, image=self.photoimg3, bd=0, relief=RIDGE)
        lblimg.place(x=860, y=55)

        # ========== TABLE FRAME SEARCH SYSTEM ==========
        Table_Frame=LabelFrame(self.root, bd=2, relief=RIDGE, text="View Details and Search System", font=("times new roman", 12, "bold"), padx=2)
        Table_Frame.place(x=435, y=280, width=860, height=260)

        lblSearchBy=Label(Table_Frame, font=("arial", 12, "bold"), text="Search By:", bg="red", fg="white") 
        lblSearchBy.grid(row=0, column=0, sticky="w", padx=2)

        self.search_var=StringVar()

        combo_Search=ttk.Combobox(Table_Frame, textvariable=self.search_var, font=("arial", 12, "bold"), width=24, state="readonly") 
        combo_Search["value"]=("Contact", "Room") 
        combo_Search.current(0) 
        combo_Search.grid(row=0, column=1, padx=2)  

        self.txt_search=StringVar()
        txtSearch=ttk.Entry(Table_Frame, textvariable=self.txt_search, font=("arial", 13, "bold"), width=24) 
        txtSearch.grid(row=0, column=2, padx=2)

        btnSearch=Button(Table_Frame, text="Search", command=self.search, font=("arial", 11, "bold"), bg="black", fg="gold", width=10) 
        btnSearch.grid(row=0, column=3, padx=1) 

        btnShowAll=Button(Table_Frame, text="Show All", command=self.fetch_data, font=("arial", 11, "bold"), bg="black", fg="gold", width=10) 
        btnShowAll.grid(row=0, column=4, padx=1)



        # ========== SHOW DATA TABLE ==========

        details_table=Frame(Table_Frame, bd=2, relief=RIDGE) 
        details_table.place(x=0, y=50, width=860, height=180) 
        
        scroll_x=ttk.Scrollbar(details_table, orient=HORIZONTAL) 
        scroll_y=ttk.Scrollbar(details_table, orient=VERTICAL) 
        
        self.room_table=ttk.Treeview(details_table, column=("contact", "checkin", "checkout", "roomtype", "roomavailable", "meal", "noOfdays"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.room_table.xview)
        scroll_y.config(command=self.room_table.yview)

        self.room_table.heading("contact", text="Contact")
        self.room_table.heading("checkin", text="Check-in")
        self.room_table.heading("checkout", text="Check-out")
        self.room_table.heading("roomtype", text="Room Type")
        self.room_table.heading("roomavailable", text="Room Number")
        self.room_table.heading("meal", text="Meal")
        self.room_table.heading("noOfdays", text="No Of Days")

        self.room_table["show"]="headings" 
        
        self.room_table.column("contact", width=60)
        self.room_table.column("checkin", width=60)
        self.room_table.column("checkout", width=60)
        self.room_table.column("roomtype", width=50)
        self.room_table.column("roomavailable", width=60)
        self.room_table.column("meal", width=150)
        self.room_table.column("noOfdays", width=100)

        self.room_table.pack(fill=BOTH, expand=1)

        self.room_table.bind("<ButtonRelease-1>", self.get_cursor)
        self.fetch_data()


    # ========== ADD DATA ==========
    def add_data(self):
        if self.var_contact.get()=="" or self.var_checkin.get()=="": 
            messagebox.showerror("Error", "All fields are required") 
        else: 
            try:
                conn = pymysql.connect(host=self.db_host, user=self.db_user, password=self.db_password, database=self.db_name) 
                my_cursor=conn.cursor() 
                my_cursor.execute("insert into room values(%s,%s,%s,%s,%s,%s,%s)", 
                                (self.var_contact.get(), 
                                self.var_checkin.get(), 
                                self.var_checkout.get(), 
                                self.var_roomtype.get(), 
                                self.var_roomavailable.get(), 
                                self.var_meal.get(), 
                                self.var_noofdays.get()
                                ))
                my_cursor.execute("update details set availability = 0 where roomno = %s;", self.var_roomavailable.get())
                conn.commit()
                self.fetch_data()
                conn.close()

                messagebox.showinfo("Success", "Room Booked.", parent=self.root)

            except Exception as es:
                messagebox.showwarning("Warning", f"Something went wrong. Try again.:{str(es)}", parent=self.root)


    # ========== FETCH DATA TO DISPLAY ==========
    def fetch_data(self): 
        conn = pymysql.connect(host=self.db_host, user=self.db_user, password=self.db_password, database=self.db_name)  
        my_cursor=conn.cursor() 
        my_cursor.execute("select * from room") 
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

        self.var_contact.set(row[0]), 
        self.var_checkin.set(row[1]), 
        self.var_checkout.set(row[2]), 
        self.var_roomtype.set(row[3]), 
        self.var_roomavailable.set(row[4]), 
        self.var_meal.set(row[5]), 
        self.var_noofdays.set(row[6])



    # ========== UPDATE DATA ==========
    def update(self): 
        if self.var_contact.get() == "":
            messagebox.showerror("Error", "Please enter mobile number", parent=self.root) 
        else:
            try:
                conn = pymysql.connect(host=self.db_host, user=self.db_user, password=self.db_password, database=self.db_name)
                my_cursor = conn.cursor()

                # Fetch the currently assigned room for the given contact
                query_fetch = "SELECT roomavailable FROM room WHERE contact=%s"
                my_cursor.execute(query_fetch, (self.var_contact.get(),))
                current_room = my_cursor.fetchone()

                if current_room:
                    current_room_number = current_room[0]

                    # Check if the room number is being changed
                    if current_room_number != self.var_roomavailable.get():
                        # Update availability of the previous room to 1 (available)
                        query_update_previous = "UPDATE details SET availability=1 WHERE roomno=%s"
                        my_cursor.execute(query_update_previous, (current_room_number,))

                        # Update the new room availability to 0 (booked)
                        query_update_new = "UPDATE details SET availability=0 WHERE roomno=%s"
                        my_cursor.execute(query_update_new, (self.var_roomavailable.get(),))

                # Update the room details for the user
                query_update_room = """
                    UPDATE room 
                    SET check_in=%s, check_out=%s, roomtype=%s, roomavailable=%s, meal=%s, noOfdays=%s 
                    WHERE contact=%s
                """
                my_cursor.execute(query_update_room, (
                    self.var_checkin.get(),
                    self.var_checkout.get(),
                    self.var_roomtype.get(),
                    self.var_roomavailable.get(),
                    self.var_meal.get(),
                    self.var_noofdays.get(),
                    self.var_contact.get()
                ))

                conn.commit()
                self.fetch_data()  # Refresh the displayed data
                conn.close()
                messagebox.showinfo("Update", "Room details have been updated successfully", parent=self.root)

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}", parent=self.root)





    # ========== DELETE DATA ==========
    def mDelete(self):
        mDelete=messagebox.askyesno("Hotel Management System", "Do you want delete this customer", parent=self.root)
        if mDelete>0:
            conn = pymysql.connect(host=self.db_host, user=self.db_user, password=self.db_password, database=self.db_name)
            my_cursor=conn.cursor()
            query="delete from room where contact=%s"
            value=(self.var_contact.get(),)
            my_cursor.execute(query, value)
            my_cursor.execute("update details set availability = 1 where roomno = %s;", self.var_roomavailable.get())
        else:
            if not mDelete:
                return
        conn.commit()
        self.fetch_data()
        conn.close()



    # ========== RESET ==========
    def reset(self):
        self.var_contact.set(""), 
        self.var_checkin.set(""), 
        self.var_checkout.set(""), 
        self.var_roomtype.set(""), 
        self.var_roomavailable.set(""), 
        self.var_meal.set(""), 
        self.var_noofdays.set("")
        self.var_paidtax.set("")
        self.var_actualtotal.set("")
        self.var_total.set("")




    # ========== FETCH DATA USING CONTACT ==========
    def fetch_contact(self):
        if self.var_contact.get() =="":
            messagebox.showerror("Error", "Please enter Contact Number", parent=self.root)
        else:
            conn = pymysql.connect(host=self.db_host, user=self.db_user, password=self.db_password, database=self.db_name) 
            my_cursor=conn.cursor() 
            query=("select name from customer where Mobile=%s")
            value=(self.var_contact.get(),)
            my_cursor.execute(query, value)
            row=my_cursor.fetchone()

            if row==None:
                messagebox.showerror("Error", "This number is not present in the Database", parent=self.root)
            else:
                conn.commit()
                conn.close()

                showDataframe=Frame(self.root, bd=4, relief=RIDGE, padx=2)
                showDataframe.place(x=450,y=55,width=400,height=180)

                # ========== NAME ==========
                lblName=Label(showDataframe, text="Name:", font=("arial", 12, "bold"))
                lblName.place(x=0, y=0)

                lbl1=Label(showDataframe, text=row[0], font=("arial", 12, "bold"))
                lbl1.place(x=90, y=0)

                # ========== GENDER ==========
                conn = pymysql.connect(host=self.db_host, user=self.db_user, password=self.db_password, database=self.db_name) 
                my_cursor=conn.cursor() 
                query=("select gender from customer where Mobile=%s")
                value=(self.var_contact.get(),)
                my_cursor.execute(query, value)
                row=my_cursor.fetchone()

                lblGender=Label(showDataframe, text="Gender:", font=("arial", 12, "bold"))
                lblGender.place(x=0, y=30)

                lbl2=Label(showDataframe, text=row, font=("arial", 12, "bold"))
                lbl2.place(x=90, y=30)

                # ========== EMAIL ==========
                conn = pymysql.connect(host=self.db_host, user=self.db_user, password=self.db_password, database=self.db_name) 
                my_cursor=conn.cursor() 
                query=("select email from customer where Mobile=%s")
                value=(self.var_contact.get(),)
                my_cursor.execute(query, value)
                row=my_cursor.fetchone()

                lblemail=Label(showDataframe, text="Email:", font=("arial", 12, "bold"))
                lblemail.place(x=0, y=60)

                lbl3=Label(showDataframe, text=row, font=("arial", 12, "bold"))
                lbl3.place(x=90, y=60)

                # ========== NATIONALITY ==========
                conn = pymysql.connect(host=self.db_host, user=self.db_user, password=self.db_password, database=self.db_name)
                my_cursor=conn.cursor() 
                query=("select nationality from customer where Mobile=%s")
                value=(self.var_contact.get(),)
                my_cursor.execute(query, value)
                row=my_cursor.fetchone()

                lblnationality=Label(showDataframe, text="Nationality:", font=("arial", 12, "bold"))
                lblnationality.place(x=0, y=90)

                lbl4=Label(showDataframe, text=row, font=("arial", 12, "bold"))
                lbl4.place(x=90, y=90)
                
                # ========== ADDRESS ==========
                conn = pymysql.connect(host=self.db_host, user=self.db_user, password=self.db_password, database=self.db_name) 
                my_cursor=conn.cursor() 
                query=("select address from customer where Mobile=%s")
                value=(self.var_contact.get(),)
                my_cursor.execute(query, value)
                row=my_cursor.fetchone()

                lbladdress=Label(showDataframe, text="Address:", font=("arial", 12, "bold"))
                lbladdress.place(x=0, y=120)

                lbl5=Label(showDataframe, text=row[0], font=("arial", 12, "bold"))
                lbl5.place(x=90, y=120)


    # ========== CALCULATE TOTAL NUMBER OF DAYS AND BILL ==========
    def total_bill(self):
        inDate=self.var_checkin.get()
        outDate=self.var_checkout.get()
        if inDate <= outDate:
            inDate=datetime.strptime(inDate, "%d/%m/%Y")
            outDate=datetime.strptime(outDate, "%d/%m/%Y")
            num_days=(outDate-inDate).days + 1
            self.var_noofdays.set(str(num_days))
        else:
            self.var_noofdays.set("Invalid dates")

        room_rates = {
            "single": 1000,
            "double": 1800,
            "luxury": 4000
        }
        
        room_tax_rates = {
            "single": 0.12,
            "double": 0.18,
            "luxury": 0.28
        }

        meal_rates = {
            "breakfast": 250,
            "lunch": 500,
            "dinner": 750,
            "": 0
        }

        meal_tax_rates = 0.18

        total_days = float(self.var_noofdays.get())
        # Calculate the total room cost
        room_booked = self.var_roomtype.get().lower()
        if room_booked in room_rates:
            room_cost = room_rates[room_booked] * total_days
            
        else:
            print("Invalid room type.")
            return -1

        # Calculate the total meal cost
        meal_cost = 0
        for meal in self.var_meal.get().split(","):
            meal = meal.strip().lower()
            if meal in meal_rates:
                meal_cost += meal_rates[meal] * total_days
            else:
                print(f"Invalid meal type: {meal}.")
                return -1

        # Calculate the total bill
        total_cost = room_cost + meal_cost
        room_tax = round(room_tax_rates[room_booked] * room_cost, 2)
        meal_tax = round(meal_cost * meal_tax_rates, 2)
        tax_cost = room_tax + meal_tax
        global final_bill
        final_bill = total_cost + tax_cost

        PT = "Rs. " + str(tax_cost)
        AC = "Rs. " + str(total_cost)
        TC = "Rs. " + str(final_bill)

        self.var_paidtax.set(PT)
        self.var_actualtotal.set(AC)
        self.var_total.set(TC)

    # ========== GENERATE QR CODE ==========
    def generate_qr_code(self, event=None):
        try:
            if final_bill is None:
                messagebox.showerror("Error", "Total bill has not been calculated. Please calculate the bill first.")
            
            else:
                # print(f"The final bill has been generated successfully and the amount is: ₹{final_bill}")
                # Create the QR code
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=15,
                    border=4,
                )
                qr.add_data(f"Total Amount: ₹{final_bill}")
                qr.make(fit=True)
                
                # Generate the QR code image
                img = qr.make_image(fill_color="black", back_color="white")
                
                # Save the QR code to a file
                img.save("bill_qrcode.png")

                # Create a new window to display the QR code
                self.new_window = Toplevel(self.root)
                self.new_window.title("QR Code")
                self.new_window.geometry("400x400+1080+250")  # Adjust size and position of the new window

                # Display the QR code in the new window
                qr_img = ImageTk.PhotoImage(img)
                qr_label = Label(self.new_window, image=qr_img)
                qr_label.image = qr_img  # Keep a reference to prevent garbage collection
                qr_label.pack(pady=10)  # Add some padding if needed

                # print("QR code for the bill has been generated successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))





    # ========== SEARCH BAR ==========
    def search(self):
        conn = pymysql.connect(host=self.db_host, user=self.db_user, password=self.db_password, database=self.db_name)
        my_cursor=conn.cursor()
        search_id = self.search_var.get()
        if search_id.lower() == "room":
            search_id = "roomavailable"
        my_cursor.execute("select * from room where "+str(search_id)+" LIKE '%"+str(self.txt_search.get())+"%'")
        rows=my_cursor.fetchall()
        if len(rows) != 0:
            self.room_table.delete(*self.room_table.get_children())
            for i in rows:
                self.room_table.insert("", END, values=i)
            conn.commit()
        else:
            messagebox.showinfo("Search", "No Customer Details found", parent=self.root)
        conn.close()



# WORK ON SEARCH BY ROOM
        






if __name__ == "__main__":
    root=Tk()
    obj=Roombooking(root)
    root.mainloop()