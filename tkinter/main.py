from tkinter import *
from tkinter import messagebox


def hello():
    messagebox.showinfo("Message Box", "Hello, how are you?")


tk = Tk()
canvas = Canvas(tk, width=1000, height=500)

canvas.create_text(512, 75, text='Hello World !', font=('Helvetica', 25))

canvas.create_line(200, 100, 800, 100)

for i in range(50, 101):
    print(i)
    canvas.create_line(100, 100, 200, i)

canvas.create_polygon(200, 300, 300, 400, 200, 400)

canvas.pack()

btn = Button(tk, text='Click me', command=hello).place(x=475, y=235)

tk.mainloop()