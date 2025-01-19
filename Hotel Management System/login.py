from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk               #pip install pillow
from tkinter import messagebox
import random
import time
import datetime
import pymysql
from hotel import HotelManagementSystem
from register import Register


class Login_Window:
    def __init__(self, root) :
        self.root = root
        self.root.title("Login")
        self.root.geometry("1550x800+0+0")
        
        # Database connection variables
        self.db_host = "localhost"
        self.db_user = "root"
        self.db_password = "dhuri"
        self.db_name = "dbms_project"
    
        self.bg = ImageTk.PhotoImage(file=r"images\SDT_Zoom-Backgrounds_April-8_Windansea-1-logo-1.jpg")
        lbl_bg = Label(self.root, image=self.bg)
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)

        frame = Frame(self.root, bg="black")
        frame.place(x=610, y=170, width=340, height=430)

        img1 = Image.open(r"images\LoginIconAppl.png")
        img1 = img1.resize((100, 100))
        self.photoimage1 = ImageTk.PhotoImage(img1)
        lblimg1 = Label(image=self.photoimage1, bg="black", borderwidth=0)
        lblimg1.place(x=730, y=170, width=100, height=100)

        get_str = Label(frame, text="Get Started", font=("times new roman", 20, "bold"), fg="white", bg="black")
        get_str.place(x=95, y=100)

        # ========== LABEL ========== 
        username = Label(frame, text="Username", font=("times new roman", 15, "bold"), fg="white", bg="black")
        username.place(x=70, y=155)

        self.txtuser = ttk.Entry(frame, font=("times new roman", 15, "bold"))
        self.txtuser.place(x=40, y=180, width=270)

        password = Label(frame, text="Password", font=("times new roman", 15, "bold"), fg="white", bg="black")
        password.place(x=70, y=225)

        self.txtpass = ttk.Entry(frame, font=("times new roman", 15, "bold"), show="*")
        self.txtpass.place(x=40, y=250, width=270)

        # ========== LOGIN BUTTON ========== 
        loginbtn = Button(frame, text="Login", command=self.login, font=("times new roman", 15, "bold"), bd=3, relief=RIDGE, fg="white", bg="red", activeforeground="white", activebackground="red")
        loginbtn.place(x=110, y=300, width=120, height=35)

        # ========== REGISTER BUTTON ========== 
        registerbtn = Button(frame, text="New User Register", command=self.register_window, font=("times new roman", 10, "bold"), borderwidth=0, fg="white", bg="black", activeforeground="white", activebackground="black")
        registerbtn.place(x=17, y=350, width=160)

        # ========== FORGOT BUTTON ========== 
        forgotbtn = Button(frame, text="Forgot Password", command=self.forgot_password_window, font=("times new roman", 10, "bold"), borderwidth=0, fg="white", bg="black", activeforeground="white", activebackground="black")
        forgotbtn.place(x=10, y=380, width=160)


    # ========== REGISTER BUTTON FUNCTION ========== 
    def register_window(self):
        self.new_window = Toplevel(self.root)
        self.app = Register(self.new_window)

    # ========== LOGIN BUTTON FUNCTION ========== 
    def login(self):
        if self.txtuser.get() == "" or self.txtpass.get() == "":
            messagebox.showerror("Error", "All fields are required")
        elif self.txtuser.get() == "Anurag" and self.txtpass.get() == "Anurag":
            messagebox.showinfo("Success", "Welcome to Anurag Group of Hotels")
        else:
            conn = pymysql.connect(host=self.db_host, user=self.db_user, password=self.db_password, database=self.db_name)
            my_cursor = conn.cursor()
            my_cursor.execute("select * from register where email=%s and password=%s", (self.txtuser.get(), self.txtpass.get()))
            row = my_cursor.fetchone()
            if row == None:
                messagebox.showerror("Error", "Invalid username or password")
            else:
                open_main = messagebox.askyesno("YesNo", "Admin Access only")
                if open_main > 0:
                    self.new_window = Toplevel(self.root)
                    self.app = HotelManagementSystem(self.new_window)
                else:
                    if not open_main:
                        return
            conn.commit()
            conn.close()

    # ========== FORGOT PASSWORD WINDOW ========== 
    def forgot_password_window(self):
        if self.txtuser.get() == "":
            messagebox.showerror("Error", "Please enter the email address to reset password")
        else:
            conn = pymysql.connect(host=self.db_host, user=self.db_user, password=self.db_password, database=self.db_name)
            my_cursor = conn.cursor()
            query = "select * from register where email = %s"
            value = (self.txtuser.get(),)
            my_cursor.execute(query, value)
            row = my_cursor.fetchone()

            if row == None:
                messagebox.showerror("Error", "Please enter the valid email address")
            else:
                conn.close()
                self.root2 = Toplevel()
                self.root2.title("Forgot Password")
                self.root2.geometry("340x450+610+170")

                l = Label(self.root2, text="Forgot Password", font=("times new roman", 25, "bold"), fg="red")
                l.place(x=0, y=10, relwidth=1)

                security_Q = Label(self.root2, text="Select Security Questions", font=("times new roman", 15, "bold"), fg="black")
                security_Q.place(x=50, y=80)

                self.combo_security_Q = ttk.Combobox(self.root2, font=("times new roman", 15, "bold"), state="readonly")
                self.combo_security_Q["values"] = ("Select", "Your Birth Place", "Your Girlfriend name", "Your Pet Name")
                self.combo_security_Q.place(x=50, y=110, width=250)
                self.combo_security_Q.current(0)

                security_A = Label(self.root2, text="Security Answer", font=("times new roman", 15, "bold"), fg="black")
                security_A.place(x=50, y=150)

                self.txt_security = ttk.Entry(self.root2, font=("times new roman", 15))
                self.txt_security.place(x=50, y=180, width=250)

                new_password = Label(self.root2, text="New Password", font=("times new roman", 15, "bold"), fg="black")
                new_password.place(x=50, y=220)

                self.txt_new_password = ttk.Entry(self.root2, font=("times new roman", 15, "bold"))
                self.txt_new_password.place(x=50, y=250, width=250)

                btn = Button(self.root2, text="Reset", command=self.reset_pass, font=("times new roman", 15, "bold"), bg="green", fg="white")
                btn.place(x=130, y=290)

    # ========== RESET PASSWORD FUNCTION ========== 
    def reset_pass(self):
        if self.combo_security_Q.get() == "Select":
            messagebox.showerror("Error", "Select Security Question", parent=self.root2)
        elif self.txt_security.get() == "":
            messagebox.showerror("Error", "Please enter the answer", parent=self.root2)
        elif self.txt_new_password.get() == "":
            messagebox.showerror("Error", "Please enter the new password", parent=self.root2)
        else:
            conn = pymysql.connect(host=self.db_host, user=self.db_user, password=self.db_password, database=self.db_name)
            my_cursor = conn.cursor()

            query = "select * from register where email=%s and securityQ=%s and securityA=%s"
            value = (self.txtuser.get(), self.combo_security_Q.get(), self.txt_security.get())
            my_cursor.execute(query, value)
            row = my_cursor.fetchone()

            if row == None:
                messagebox.showerror("Error", "Please enter correct answer", parent=self.root2)
            else:
                query = "update register set password = %s where email = %s"
                value = (self.txt_new_password.get(), self.txtuser.get())
                my_cursor.execute(query, value)

                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Your password has been reset successfully", parent=self.root2)
                self.root2.destroy()


if __name__ == "__main__":
    root = Tk()
    obj = Login_Window(root)
    root.mainloop()
