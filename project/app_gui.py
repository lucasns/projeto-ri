from Tkinter import *
import tkMessageBox
from ScrolledText import ScrolledText
from utils import MovieTime
import app

class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        
        self.pack()
        master.bind('<Return>', self.key_press)

        self.message = Label(self, text=" Search for movies ", font=('Arial', '10'))
        self.message.grid(row=0, column=2, padx=(0, 50), pady=(20, 20))

        self.title_entry_label = Label(self, text="Title: ")
        self.title_entry_label.grid(row=1, column=1, padx=(10, 5), pady=(0,10), sticky=W)

        self.title_entry = Entry(self, width=50, font=1)
        self.title_entry.grid(row=1, column=2, padx=(0, 20), pady=(0,10))

        self.genre_entry_label = Label(self, text="Genre: ", justify=LEFT)
        self.genre_entry_label.grid(row=3, column=1, padx=(10, 5), pady=(0,10), sticky=W)

        self.genre_entry = Entry(self, width=50, font=1)
        self.genre_entry.grid(row=3, column=2, padx=(0, 20), pady=(0,10))

        self.director_entry_label = Label(self, text="Director: ", justify=LEFT)
        self.director_entry_label.grid(row=4, column=1, padx=(10, 5), pady=(0,10), sticky=W)

        self.director_entry = Entry(self, width=50, font=1)
        self.director_entry.grid(row=4, column=2, padx=(0, 20), pady=(0,10))

        self.date_entry_label = Label(self, text="Date (Year): ", justify=LEFT)
        self.date_entry_label.grid(row=5, column=1, padx=(10, 5), pady=(0,10), sticky=W)

        self.date_entry = Entry(self, width=50, font=1)
        self.date_entry.grid(row=5, column=2, padx=(0, 20), pady=(0,10))

        self.runtime_entry_label = Label(self, text="Runtime: ", justify=LEFT)
        self.runtime_entry_label.grid(row=6, column=1, padx=(10, 5), pady=(0,10), sticky=W)

        self.runtime_var = StringVar(master)
        self.runtime_var.set("None")
        self.options = ["None", "Less than 1h", "Between 1h and 2h", "Between 2h and 3h", "More than 4h"]
        self.runtime_entry = OptionMenu(self, self.runtime_var, *self.options)
        self.runtime_entry.config(width=18)
        self.runtime_entry.grid(row=6, column=2, padx=(0, 320))

        self.id_entry_label = Label(self, text="ID: ", justify=LEFT)
        self.id_entry_label.grid(row=7, column=1, padx=(10, 5), pady=(20,10), sticky=W)

        self.id_entry = Entry(self, width=5, font=1)
        self.id_entry.grid(row=7, column=2, padx=(0, 20), pady=(20,10), sticky=W)

        self.search_in_button = Button(self, text="Search", width=30, command=self.search_cmd)
        self.search_in_button.grid(row=9, column=2, padx=(0, 50), pady=(30, 20))
            
    def key_press(self, event):
        self.search_cmd()

    def search_cmd(self):
        query = {}
        query['title'] = self.title_entry.get()
        query['genre'] = self.genre_entry.get()
        query['director'] = self.director_entry.get()
        query['date'] = self.date_entry.get()
        runtime = self.options.index(self.runtime_var.get()) * 60 - 1

        query['runtime'] = MovieTime(runtime).quartile()

        is_empty = True
        for v in query.itervalues():
            if v != "" and v != "None":
                is_empty = False

        if self.id_entry.get() != "":
            is_empty = False

        self.runtime_var.get()
        if is_empty:
            tkMessageBox.showerror("Error", "At least one field should be provided.")
        else:
            if self.id_entry.get() != "":
                docs = app.get_documents([int(self.id_entry.get())])
            else:
                docs = app.search(query)

            # Create results window
            results_window = Toplevel(self)
            results_window.resizable(width=False, height=False)
            results_window.wm_title(str(len(docs)) + " Results")
            results_window.focus_set()
            
            text = ScrolledText(results_window, width=60, height=40)
            text.grid(padx=20, pady=20)

            docs_str = ""

            for doc in docs:
                docs_str += doc + '\n\n'

            docs_str = docs_str[:len(docs_str)-2]

            text.insert(END, docs_str)

            text.config(state=DISABLED)


if __name__ == '__main__':
    root = Tk()
    root.resizable(width=False, height=False)
    myapp = App(root)
    myapp.master.title("Search Engine Application")
    myapp.mainloop()
