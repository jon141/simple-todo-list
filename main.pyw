import customtkinter as ctk
import json

root = ctk.CTk()
root.title("TodoList")
root.geometry("500x600")
ctk.set_appearance_mode('Light')
#todolist
#togglelist

todo_dict = json.load(open('todos.json', 'r', encoding='utf-8'))

#print(todo_dict['1'][0])

class ToDo(ctk.CTkFrame):
    def __init__(self, master, key: str):
        super().__init__(master, fg_color='transparent')

        self.key = key
        self.todo = todo_dict[key][0]
        self.toggle_bool = todo_dict[key][1]

        self.overstrike_font = ctk.CTkFont(overstrike=True, size=14)
        self.normal_font = ctk.CTkFont(size=14)

        if self.toggle_bool == False:
            self.check_var = ctk.StringVar(value="off")
            self.font = self.normal_font
        else:
            self.check_var = ctk.StringVar(value="on")
            self.font = self.overstrike_font
        self.checkbox = ctk.CTkCheckBox(self, text=self.todo, command=self.mark_todo, variable=self.check_var, width=316, onvalue="on", offvalue="off", corner_radius=0, checkbox_width=20, checkbox_height=20, font=self.font)#, fg_color='#2f5a80')
        self.checkbox.grid(sticky='w', pady=(5, 0), padx=(5, 0), column=0, row=0)

        self.del_button = ctk.CTkButton(self, text='del', width=50, corner_radius=0, height=0, command=self.del_todo, fg_color=('#c93a3a', '#c93a3a'))
        self.del_button.grid(column=1, sticky='e', row=0, padx=(5, 0))

    def mark_todo(self):
        #print("checkbox toggled, current value:", self.check_var.get())
        if self.check_var.get() == 'on':
            self.checkbox.configure(font=self.overstrike_font)
            todo_dict[self.key][1] = True
        else:
            self.checkbox.configure(font=self.normal_font)
            todo_dict[self.key][1] = False
        json.dump(todo_dict, open('todos.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)


    def del_todo(self):
        self.grid_forget()
        del todo_dict[self.key]
        print(todo_dict)
        json.dump(todo_dict, open('todos.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)


class ToDoList(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color='transparent', corner_radius=0)#, width=400, height=400)

        self.rows = 2
        self.heading_add_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.heading_add_frame.grid(row=0, pady=(0, 1))
        self.heading_lable = ctk.CTkLabel(self.heading_add_frame, text="ToDo's:", text_color='white', fg_color='#32558a')
        self.heading_lable.grid(row=0, columnspan=2, sticky='news')
        self.add_todo_entry = ctk.CTkEntry(self.heading_add_frame, placeholder_text='ToDo', corner_radius=0, width=350, border_width=1, fg_color='white')
        self.add_todo_entry.grid(row=1, column=0)

        self.add_todo_button = ctk.CTkButton(self.heading_add_frame, text='add', command=self.add_todo, corner_radius=0, width=50, fg_color=('#c93a3a', '#c93a3a'))

        self.add_todo_entry.bind("<Return>", self.add_todo)

        self.add_todo_button.grid(row=1, column=1)
        self.init_todo()


    def init_todo(self):

        self.scrollable_todos_frame = ctk.CTkScrollableFrame(self, width=384, height=400, corner_radius=0, fg_color='white')
        self.scrollable_todos_frame.grid(row=1)

        for key in list(todo_dict.keys()):
            if key != 'c':
                todo = ToDo(self.scrollable_todos_frame, key)
                todo.grid(row=self.rows, sticky='w')
                self.rows += 1


    def add_todo(self, event=None):
        #print(self.add_todo_entry.get())
        if self.add_todo_entry.get() != '':
            todo_dict[(todo_dict['c'] + 1)] = [self.add_todo_entry.get(), False]
            todo_dict['c'] += 1
            todo = ToDo(self.scrollable_todos_frame, todo_dict['c'])
            todo.grid(row=self.rows, columnspan=2, sticky='w')
            self.rows += 1

            self.add_todo_entry.delete(0, 'end')
            print(todo_dict)
            json.dump(todo_dict, open('todos.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=4)


root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

todolist = ToDoList(root)
todolist.grid(columnspan=2, rowspan=2, pady=10)




#todo = ToDo(root, '1')
#todo1 = ToDo(root, '2')
#todo2 = ToDo(root, '3')
#todo.grid()
#todo1.grid()
#todo2.grid()




root.mainloop()
