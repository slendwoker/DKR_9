import tkinter as tk
import psycopg2
from tkinter import ttk
from PIL import ImageTk, Image

host = "127.0.0.1"
user = "postgres"
password = "5gcv783nz"
db_name = "Call_of_Duty"
port = "5432"

root = tk.Tk()
root.title("Лучший справочник для фанатов Call of Duty")
root.configure(background='#8C8C8C')
root.resizable(False, False)

connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name,
    port = port
)
connection.autocommit = True
cursor = connection.cursor()
def add_window():
    def add_entry():
        name = name1_entry.get()
        squad = squad1_entry.get()
        nickname = nickname1_entry.get()
        first_appearance = first_appearance1_combobox.get()

        if name and squad and nickname and first_appearance:
            insert_query = "INSERT INTO duty (Имя, Отряд, Позывной, Первое_появление) VALUES (%s, %s, %s, %s)"
            data = (name, squad, nickname, first_appearance)
            cursor.execute(insert_query, data)
            connection.commit()
            name1_entry.delete(0, tk.END)
            squad1_entry.delete(0, tk.END)
            nickname1_entry.delete(0, tk.END)
            first_appearance1_combobox.delete(0, tk.END)
            output_table()
        window_add.destroy()

    window_add = tk.Tk()
    window_add.title("Добавление записи")
    window_add.geometry("400x300")
    window_add.configure(background='#636363')
    window_add.resizable(False, False)
    redac_label = ttk.Label(window_add, text="Имя:", background='#636363')
    redac_label.pack()
    name1_entry = ttk.Entry(window_add)
    name1_entry.pack()

    squad1_label = ttk.Label(window_add, text="Отряд:", background='#636363')
    squad1_label.pack()
    squad1_entry = ttk.Entry(window_add)
    squad1_entry.pack()

    nickname1_label = ttk.Label(window_add, text="Позывной:", background='#636363')
    nickname1_label.pack()
    nickname1_entry = ttk.Entry(window_add)
    nickname1_entry.pack()

    first_appearance1_label = ttk.Label(window_add, text="Первое появление:", background='#636363')
    first_appearance1_label.pack()
    first_appearance1_combobox = ttk.Combobox(window_add, values=["Call of Duty Modern Warfare 2", "Call of Duty Modern Warfare 3", "Call of Duty Modern Warfare 4", "Call of Duty Black Ops ", "Call of Duty Black Ops 2"], width=27)
    first_appearance1_combobox.pack()

    add1_button = tk.Button(window_add, text="Добавить", command=add_entry, bg='#17301A')
    add1_button.pack(pady=5)

def delete_entry():
    selected_item = treeview.focus()
    if selected_item:
        name = treeview.item(selected_item, "text")
        delete_query = "DELETE FROM duty WHERE Имя = %s"
        cursor.execute(delete_query, (name,))
        connection.commit()
        treeview.delete(selected_item)
        output_table()

def output_table():
    treeview.delete(*treeview.get_children())
    select_query = "SELECT * FROM duty"
    cursor.execute(select_query)
    records = cursor.fetchall()
    for row in records:
        name = row[0]
        squad = row[1]
        nickname = row[2]
        first_appearance = row[3]
        treeview.insert("", tk.END, text=name, values=(squad, nickname, first_appearance))
def search_entry():
    def perform_search():
        search_value = search_entry.get()
        select_query = "SELECT * FROM duty WHERE Имя ILIKE %s OR Отряд ILIKE %s OR Позывной ILIKE %s OR Первое_появление ILIKE %s"
        cursor.execute(select_query, ('%' + search_value + '%', '%' + search_value + '%', '%' + search_value + '%', '%' + search_value + '%'))
        records = cursor.fetchall()
        treeview.delete(*treeview.get_children())
        for row in records:
            name = row[0]
            squad = row[1]
            nickname = row[2]
            first_appearance = row[3]
            treeview.insert("", tk.END, text=name, values=(squad, nickname, first_appearance))

    search_window = tk.Toplevel(root)
    search_window.title("Поиск")
    search_window.geometry("400x100")
    search_window.configure(background='#636363')
    search_window.resizable(False, False)

    search_label = ttk.Label(search_window, text="Введите запрос:", background='#636363')
    search_label.pack()

    search_entry = ttk.Entry(search_window)
    search_entry.pack()

    search_button = tk.Button(search_window, text="Поиск", command=perform_search, bg='#17301A', width=15, height=2)
    search_button.pack(pady=5)
def refresh_table():
    output_table()
def edit_entry():
    selected_item = treeview.focus()
    if selected_item:
        name = treeview.item(selected_item, "text")
        squad = treeview.item(selected_item, "values")[0]
        nickname = treeview.item(selected_item, "values")[1]
        first_appearance = treeview.item(selected_item, "values")[2]
        
        # Создайте окно для редактирования записи с предварительно заполненными полями
        window_edit = tk.Tk()
        window_edit.title("Редактирование записи")
        window_edit.geometry("400x300")
        window_edit.configure(background='#636363')
        window_edit.resizable(False, False)
        
        name_label = ttk.Label(window_edit, text="Имя:", background='#636363')
        name_label.pack()
        name_entry = ttk.Entry(window_edit)
        name_entry.pack()
        name_entry.insert(0, name)
        
        squad_label = ttk.Label(window_edit, text="Отряд:", background='#636363')
        squad_label.pack()
        squad_entry = ttk.Entry(window_edit)
        squad_entry.pack()
        squad_entry.insert(0, squad)
        
        nickname_label = ttk.Label(window_edit, text="Позывной:", background='#636363')
        nickname_label.pack()
        nickname_entry = ttk.Entry(window_edit)
        nickname_entry.pack()
        nickname_entry.insert(0, nickname)
        
        first_appearance_label = ttk.Label(window_edit, text="Первое появление:", background='#636363')
        first_appearance_label.pack()
        first_appearance1_combobox = ttk.Combobox(window_edit, values=["Call of Duty Modern Warfare 2", "Call of Duty Modern Warfare 3", "Call of Duty Modern Warfare 4", "Call of Duty Black Ops ", "Call of Duty Black Ops 2"], width=27)
        first_appearance1_combobox.pack()
        first_appearance1_combobox.insert(0, first_appearance)
        
        def save_changes():
            updated_name = name_entry.get()
            updated_squad = squad_entry.get()
            updated_nickname = nickname_entry.get()
            updated_first_appearance = first_appearance1_combobox.get()
            
            update_query = "UPDATE duty SET Имя = %s, Отряд = %s, Позывной = %s, Первое_появление = %s WHERE Имя = %s"
            data = (updated_name, updated_squad, updated_nickname, updated_first_appearance, name)
            cursor.execute(update_query, data)
            connection.commit()
            window_edit.destroy()
            output_table()
        
        save_button = tk.Button(window_edit, text="Сохранить", command=save_changes, bg='light blue')
        save_button.pack(pady=5)
        
        window_edit.mainloop()

    
treeview = ttk.Treeview(root)
treeview["columns"] = ("squad", "nickname", "first_appearance")
treeview.heading("#0", text="Имя")
treeview.heading("squad", text="Отряд")
treeview.heading("nickname", text="Позывной")
treeview.heading("first_appearance", text="Первое появление")
treeview.pack(pady=10)

# Create a frame to hold the buttons
button_frame = tk.Frame(root, bg='#8C8C8C')
button_frame.pack(pady=5)

add_button = tk.Button(button_frame, text="Добавить", command=add_window, bg='#17301A', width=15, height=3)
add_button.grid(row=0, column=1, padx=5)

delete_button = tk.Button(button_frame, text="Удалить", command=delete_entry, bg='#17301A', width=15, height=3)
delete_button.grid(row=0, column=3, padx=5)

output_button = tk.Button(button_frame, text="Выход", command=root.destroy, bg='#981916', width=15, height=3)
output_button.grid(row=0, column=4, padx=5)
edit_button = tk.Button(button_frame, text="Изменить", command=edit_entry, bg='#17301A', width=15, height=3)
edit_button.grid(row=0, column=2, padx=5)

refresh_button = tk.Button(button_frame, text="Обновить",command=refresh_table, bg='#17301A', width=15, height=3)
refresh_button.grid(row=0, column=6, padx=5)
searh_button = tk.Button(button_frame, text="Поиск",command=search_entry, bg='#17301A', width=15, height=3)
searh_button.grid(row=0, column=7, padx=5)

def on_closing():
    cursor.close()
    connection.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
output_table()
root.mainloop()

