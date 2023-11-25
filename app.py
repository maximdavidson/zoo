import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector


# Создание окна
window = tk.Tk()
window.resizable(width = False, height = False)
window.title('Your ZOO')
window.geometry('1000x500')
window['bg'] = 'gray'


# Подключение к базе данных
try:
   db_connector = mysql.connector.connect(
      host = 'localhost',
      user = 'root',
      password = 'plsworklaba123@',
      database = 'zoo'
   )

   # Создаем объект для выполнения SQL-запросов
   cursor = db_connector.cursor()
   print('Successfully')
except mysql.connector.Error as err:
   print(f'Error: {err}')
   messagebox.showerror('Error')


def add_employee():
    # Создаем всплывающее окно для ввода данных
    input_window = tk.Toplevel(window)
    input_window.title("Добавить сотрудников")
    input_window.geometry('300x200')

    labels = ['Имя', 'Фамилия', 'Должность', 'Доступ к клетке']
    entries = []

    for i, label in enumerate(labels):
        tk.Label(input_window, text=label).grid(row=i)
        entries.append(tk.Entry(input_window))
        entries[-1].grid(row=i, column=1)

    def submit():
        employee_data = {label: entry.get() for label, entry in zip(labels, entries)}

        # Добавляем данные в базу данных
        cursor.execute(f"INSERT INTO Employee (firstName, lastName, position, access) VALUES ('{employee_data['Имя']}', '{employee_data['Фамилия']}', '{employee_data['Должность']}', {employee_data['Доступ к клетке']})")
        db_connector.commit()
        input_window.destroy()

    tk.Button(input_window, text='Submit', command=submit).grid(row=len(labels), column=1)


# Создаем таблицу
tree = ttk.Treeview(window)
tree["columns"]=("one","two","three","four")
tree.column("#0", width=50, minwidth=10, stretch=tk.NO)
tree.column("one", width=150, minwidth=150, stretch=tk.NO)
tree.column("two", width=150, minwidth=150, stretch=tk.NO)
tree.column("three", width=150, minwidth=100, stretch=tk.NO)
tree.column("four", width=80, minwidth=80, stretch=tk.NO)

tree.heading("#0",text="ID",anchor=tk.W)
tree.heading("one", text="First name",anchor=tk.W)
tree.heading("two", text="Last name",anchor=tk.W)
tree.heading("three", text="Position",anchor=tk.W)
tree.heading("four", text="Access",anchor=tk.W)

def show_employees():
    # Извлекаем данные из базы данных
    cursor.execute("SELECT * FROM Employee")
    employees = cursor.fetchall()

    # Добавляем данные в таблицу
    for employee in employees:
        tree.insert("", 0, text=employee[0], values=(employee[1], employee[2], employee[3], employee[4]))

    tree.place(x=10, y=80)

def update_table():
    # Удаляем все текущие строки из таблицы
    for row in tree.get_children():
        tree.delete(row)

    # Извлекаем данные из базы данных
    cursor.execute("SELECT * FROM Employee")
    employees = cursor.fetchall()

    # Добавляем данные в таблицу
    for employee in employees:
        tree.insert("", 0, text=employee[0], values=(employee[1], employee[2], employee[3], employee[4], employee[5]))


# Горизонтальные кнопки
btn_1 = tk.Button(window, text = 'Сотрудники', width = '20', height = '1', fg = 'black', bg = 'gray', command=show_employees)
btn_1.place(x = 20, y = 10)

btn_2 = tk.Button(window, text = 'Животные', width = '20', height = '1', fg = 'black', bg = 'gray')
btn_2.place(x = 200, y = 10)

btn_3 = tk.Button(window, text = 'Поставщики', width = '20', height = '1', fg = 'black', bg = 'gray')
btn_3.place(x = 400, y = 10)

btn_4 = tk.Button(window, text = 'Изолятор', width = '20', height = '1', fg = 'black', bg = 'gray')
btn_4.place(x = 600, y = 10)


# Вертикальные кнопки
btn_add = tk.Button(window, text = 'Добавить', width = '20', height = '1', fg = 'black', bg = 'gray', command=add_employee)
btn_add.place(x = 800, y = 20)

btn_update = tk.Button(window, text = 'Обновить данные', width = '20', height = '1', fg = 'black', bg = 'gray', command=update_table)
btn_update.place(x = 800, y = 60)

btn_clean = tk.Button(window, text = 'Удалить', width = '20', height = '1', fg = 'black', bg = 'gray')
btn_clean.place(x = 800, y = 100)

btn_find = tk.Button(window, text = 'Искать', width = '20', height = '1', fg = 'black', bg = 'gray')
btn_find.place(x = 800, y = 140)

btn_filter = tk.Button(window, text = 'Фильтрация', width = '20', height = '1', fg = 'black', bg = 'gray')
btn_filter.place(x = 800, y = 180)


window.mainloop()
cursor.close()
db_connector.close()