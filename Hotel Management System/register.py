from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import pymysql




class Register:
    def __init__(self, root):
        self.root=root
        self.root.title("Register")
        self.root.geometry("1600x900+0+0")


        # Database connection variables
        self.db_host = "localhost"
        self.db_user = "root"
        self.db_password = "dhuri"
        self.db_name = "dbms_project"


        # ========== VARIABLES ==========
        self.var_fname = StringVar()
        self.var_lname = StringVar()
        self.var_contact = StringVar()
        self.var_email = StringVar()
        self.var_securityQ = StringVar()
        self.var_securityA = StringVar()
        self.var_pass = StringVar()
        self.var_confpass = StringVar()

        self.var_check = IntVar()

        
        # ========== BACKGROUND IMAGE ==========
        self.bg=ImageTk.PhotoImage(file = r"images\0-3450_3d-nature-wallpaper-hd-1080p-free-download-new.jpg")

        bg_lbl=Label(self.root,image=self.bg)
        bg_lbl.place(x=0,y=0, relwidth=1, relheight=1)


        # ========== LEFT IMAGE ==========
        self.bg1=ImageTk.PhotoImage(file = r"images\thought-good-morning-messages-LoveSove.jpg")

        left_lbl=Label(self.root,image=self.bg1)
        left_lbl.place(x=50,y=100, width=470, height=550)


        # ========== MAIN FRAME ==========
        frame=Frame(self.root, bg="white")
        frame.place(x=520,y=100, width=800,height=550)
        register_lbl=Label(frame, text="REGISTER HERE", font=("times new roman",20,"bold"), fg="darkgreen", bg="white")
        register_lbl.place(x=20,y=20)


        # ========== LABEL AND ENTRY ==========

        # ========== ROW 1 ==========
        fname=Label(frame, text="First Name", font=("times new roman", 15, "bold"), bg="white")
        fname.place(x=50,y=100)

        self.fname_entry=ttk.Entry (frame, font=("times new roman", 15), textvariable=self.var_fname)
        self.fname_entry.place (x=50,y=130, width=250)

        l_name=Label(frame, text="Last Name", font=("times new roman", 15, "bold"), bg="white",fg="black")
        l_name.place(x=370,y=100)

        self.txt_lname=ttk.Entry (frame, font=("times new roman", 15), textvariable=self.var_lname)
        self.txt_lname.place(x=370,y=130, width=250)


        # ========== ROW 2 ==========
        contact=Label(frame, text="Contact Number", font=("times new roman", 15, "bold"), bg="white", fg="black")
        contact.place(x=50,y=170)

        self.txt_contact=ttk.Entry(frame, font=("times new roman", 15), textvariable=self.var_contact)
        self.txt_contact.place(x=50,y=200, width=250)

        email=Label(frame, text="Email", font=("times new roman", 15, "bold"), bg="white",fg="black")
        email.place(x=370,y=170)
        
        self.txt_email=ttk.Entry (frame, font=("times new roman", 15), textvariable=self.var_email)
        self.txt_email. place (x=370,y=200, width=250)


        # ========== ROW 3 ==========
        security_Q=Label (frame, text="Select Security Questions", font=("times new roman", 15, "bold"), bg="white",fg="black")
        security_Q.place(x=50,y=240)


        self.combo_security_Q=ttk.Combobox(frame, font=("times new roman", 15, "bold"), textvariable=self.var_securityQ, state="readonly")
        self.combo_security_Q["values"]=("Select", "Your Birth Place", "Your Girlfriend name", "Your Pet Name")
        self.combo_security_Q.place(x=50,y=270, width=250)
        self.combo_security_Q.current(0)


        security_A=Label (frame, text="Security Answer", font=("times new roman", 15, "bold"), bg="white", fg="black")
        security_A.place(x=370,y=240)

        self.txt_security=ttk.Entry(frame, font=("times new roman", 15), textvariable=self.var_securityA, show="*")
        self.txt_security.place (x=370,y=270, width=250)
        
        
        # ========== ROW 4 ==========
        pswd=Label(frame, text="Password", font=("times new roman", 15, "bold"), bg="white", fg="black")
        pswd.place(x=50,y=310)

        self.txt_pswd=ttk.Entry(frame, font=("times new roman", 15), textvariable=self.var_pass, show="*")
        self.txt_pswd.place (x=50,y=340, width=250)

        confirm_pswd=Label (frame, text="Confirm Password", font=("times new roman", 15, "bold"), bg="white",fg="black")
        confirm_pswd.place (x=370,y=310)

        self.txt_confirm_pswd=ttk.Entry(frame, font=("times new roman", 15), textvariable=self.var_confpass, show="*")
        self.txt_confirm_pswd.place(x=370, y=340, width=250)    


        
        # ========== CHECKBUTTON ==========
        checkbtn = Checkbutton (frame, variable=self.var_check, text="I agree to all terms and conditions.", font=("times new roman", 12, "bold"),bg="white", onvalue=1, offvalue=0)
        checkbtn.place(x=50, y=380)



        # ========== BUTTONS ==========
        img=Image.open(r"images\register-now-button1.jpg")
        img=img.resize((200, 50))
        self.photoimage= ImageTk.PhotoImage(img)
        b1=Button(frame, image=self.photoimage, command=self.register_data, borderwidth=0, bg="white", cursor="hand2")
        b1.place(x=60, y=420, width=200)


        img1=Image.open(r"images\loginpng.png")
        img1=img1.resize((200, 40))
        self.photoimage1= ImageTk.PhotoImage(img1)
        b1=Button(frame, image=self.photoimage1, command=self.return_to_login, borderwidth=0, bg="white", cursor="hand2")
        b1.place(x=400, y=420, width=200)




    # ========== FUNCTION DECLARATION ==========
    def register_data(self):
        if self.var_fname.get() =="" or self.var_email.get() =="" or self.var_securityQ.get()=="Select":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        elif self.var_pass.get() !=self.var_confpass.get():
            messagebox.showerror("Error","Password and Confirm Password must be same", parent=self.root)
        elif self.var_check.get()==0:
            messagebox.showerror("Error", "Please agree to our terms and conditions", parent=self.root)
        else:
            conn = pymysql.connect(host=self.db_host, user=self.db_user, password=self.db_password, database=self.db_name) 
            my_cursor=conn.cursor()
            query=("select * from register where email = %s")
            value=(self.var_email.get(),)
            my_cursor.execute(query, value)
            row=my_cursor.fetchone()
            if row != None:
                messagebox.showerror("Error", "User already exists. Please try another email.", parent=self.root)
            else:
                my_cursor.execute("insert into register values (%s, %s, %s, %s, %s, %s, %s )",     (self.var_fname.get(), 
                                                                                                    self.var_lname.get(), 
                                                                                                    self.var_contact.get(), 
                                                                                                    self.var_email.get(), 
                                                                                                    self.var_securityQ.get(), 
                                                                                                    self.var_securityA.get(), 
                                                                                                    self.var_pass.get()
                                                                                                    ))
            
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "User registered successfully", parent=self.root)


    def return_to_login(self):
        self.root.destroy()





if __name__ ==  "__main__":
    root=Tk()
    app=Register(root)
    root.mainloop()