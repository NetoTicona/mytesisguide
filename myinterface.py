from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class Feedback:

    def __init__(self, mainframe):
        mainframe.title('Add Your Comment')
        mainframe.resizable(False, False)
        mainframe.configure(background='#f7f7f7')

        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f7f7f7')
        self.style.configure('TButton', background='#e1d8b9')
        self.style.configure(
            'TLabel', background='#f7f7f7', font=('Arial', 12))
        self.style.configure('Header.TLabel', font=('Arial', 18, 'bold'))

        self.header_frame = ttk.Frame(mainframe)
        self.header_frame.pack()

        self.logo = PhotoImage(file='pyton.png')
        ttk.Label(self.header_frame, image=self.logo).grid(
            row=0, column=0, rowspan=2)

        ttk.Label(self.header_frame, wraplength=300,
                  text=(
                      'Diseño E Implementación De Un Sistema Clasificador De Mangos Usando Una Red Neuronal Y Vision Por Computadora')).grid(
            row=1, column=1)

        ttk.Button(self.content_in_frame, text='Submit',
                   command=self.submit).grid(row=4, column=0, padx=5, pady=5, sticky='e')

        self.content_in_frame = ttk.Frame(mainframe)
        self.content_in_frame.pack()

    def submit(self):
        print(f'Name: {self.comment_name.get()}')
        print(f'Email: {self.comment_email.get()}')
        print(f'Comments: {self.comments.get(1.0, "end")}')
        self.clear()
        messagebox.showinfo(title='Comment info',
                            message='Thanks for your comment!')


def main():
    root = Tk()
    root.geometry('600x400')
    feedback = Feedback(root)
    root.mainloop()


if __name__ == '__main__':
    main()
