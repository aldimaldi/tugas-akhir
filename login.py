import pymysql
from tkinter import *
from tkinter import messagebox
from subprocess import call

def Ok():
    mysqldb = pymysql.connect(
        host='localhost',
        user='root',
        password='aldima15',
        db='inventaris'
    )
    mycursor = mysqldb.cursor()
    uname = e1.get()
    password = e2.get()

    sql = "SELECT level FROM user WHERE username = %s AND password = %s"
    mycursor.execute(sql, [(uname), (password)])
    result = mycursor.fetchone()  # Ambil satu baris hasil
    if result:
        user_level = result[0]  # Ambil nilai kolom level
        messagebox.showinfo("", "Login Success")
        root.destroy()
        if user_level == 'Admin':
            call(['python', 'admin.py', '--logged_in'])
        elif user_level == 'User':
            call(['python', 'app.py', '--logged_in'])
        else:
            messagebox.showerror("Error", "Invalid user level in database")
        return True
    else:
        messagebox.showinfo("", "Incorrect Username or password")
        return False

root = Tk()
root.title('login')
root.geometry('300x200')
global e1
global e2

Label(root, text='Username').place(x=10, y=10)
Label(root, text='Password').place(x=10, y=40)

e1 = Entry(root)
e1.place(x=140, y=10)

e2 = Entry(root)
e2.place(x=140, y=60)
e2.config(show='*')

Button(root, text='Login', command=Ok, height=3, width=13).place(x=10, y=100)

root.mainloop()
