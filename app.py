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
    input_window.title('Добавить сотрудников')
    input_window.geometry('300x200')

    labels = ['Имя', 'Фамилия', 'Гендер', 'Возраст', 'Должность', 'Доступ к клетке', 'Категория', 'Зарплата']
    entries = []

    for i, label in enumerate(labels):
        tk.Label(input_window, text=label).grid(row=i)
        entries.append(tk.Entry(input_window))
        entries[-1].grid(row=i, column=1)

    def submit():
        employee_data = {label: entry.get() for label, entry in zip(labels, entries)}

        # Добавляем данные в базу данных
        cursor.execute('INSERT INTO Employee (firstName, lastName, gender, age, position, access, category, salary) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
               (employee_data['Имя'], employee_data['Фамилия'], employee_data['Гендер'], employee_data['Возраст'], employee_data['Должность'], employee_data['Доступ к клетке'], employee_data['Категория'], employee_data['Зарплата']))
        db_connector.commit()
        input_window.destroy()

    tk.Button(input_window, text='Submit', command=submit).grid(row=len(labels), column=1)


def add_animal():
    input_window = tk.Toplevel(window)
    input_window.title('Добавить животных')
    input_window.geometry('300x200')

    labels = ['Вид', 'Имя', 'Гендер', 'Возраст', 'Пара', 'Статус']
    entries = []

    for i, label in enumerate(labels):
        tk.Label(input_window, text=label).grid(row=i)
        entries.append(tk.Entry(input_window))
        entries[-1].grid(row=i, column=1) 

    def submit():
        animal_data = {label: entry.get() for label, entry in zip(labels, entries)}
        cursor.execute('INSERT INTO Animals (kind, name, gender, age, pair, status) VALUES (%s, %s, %s, %s, %s, %s)',
                (animal_data['Вид'], animal_data['Имя'], animal_data['Гендер'], animal_data['Возраст'], animal_data['Пара'], animal_data['Статус']))
        db_connector.commit()
        input_window.destroy()
    
    tk.Button(input_window, text='Submit', command=submit).grid(row = len(labels), column = 1)

# Создаем таблицу
tree_emp = ttk.Treeview(window)
tree_emp['columns']=('one','two','three','four','five', 'six', 'seven', 'eight')
tree_emp.column('#0', width=1, minwidth=1, stretch=tk.NO)
tree_emp.column('one', width=110, minwidth=110, stretch=tk.NO)
tree_emp.column('two', width=110, minwidth=110, stretch=tk.NO)
tree_emp.column('three', width=100, minwidth=100, stretch=tk.NO)
tree_emp.column('four', width=60, minwidth=80, stretch=tk.NO)
tree_emp.column('five', width=80, minwidth=80, stretch=tk.NO)
tree_emp.column('six', width=120, minwidth=80, stretch=tk.NO)
tree_emp.column('seven', width=80, minwidth=80, stretch=tk.NO)
tree_emp.column('eight', width=80, minwidth=80, stretch=tk.NO)

tree_emp.heading('#0',text='ID',anchor=tk.W)
tree_emp.heading('one', text='Имя',anchor=tk.W)
tree_emp.heading('two', text='Фамилия',anchor=tk.W)
tree_emp.heading('three', text='Гендер',anchor=tk.W)
tree_emp.heading('four', text='Возраст',anchor=tk.W)
tree_emp.heading('five', text='Должность',anchor=tk.W)
tree_emp.heading('six', text='Доступ к клетке',anchor=tk.W)
tree_emp.heading('seven', text='Категория',anchor=tk.W)
tree_emp.heading('eight', text='Зарплата',anchor=tk.W)



tree_anl = ttk.Treeview(window)
tree_anl['columns']=('one','two','three','four','five', 'six')
tree_anl.column('#0', width=1, minwidth=1, stretch=tk.NO)
tree_anl.column('one', width=150, minwidth=150, stretch=tk.NO)
tree_anl.column('two', width=150, minwidth=150, stretch=tk.NO)
tree_anl.column('three', width=150, minwidth=100, stretch=tk.NO)
tree_anl.column('four', width=120, minwidth=80, stretch=tk.NO)
tree_anl.column('five', width=80, minwidth=80, stretch=tk.NO)
tree_anl.column('six', width=80, minwidth=80, stretch=tk.NO)

tree_anl.heading('#0',text='ID',anchor=tk.W)
tree_anl.heading('one', text='Вид',anchor=tk.W)
tree_anl.heading('two', text='Имя',anchor=tk.W)
tree_anl.heading('three', text='Гендер',anchor=tk.W)
tree_anl.heading('four', text='Возраст',anchor=tk.W)
tree_anl.heading('five', text='Пара',anchor=tk.W)
tree_anl.heading('six', text='Статус',anchor=tk.W)

def show_employees():
    # Очищаем таблицу перед добавлением новых данных
    for row in tree_emp.get_children():
        tree_emp.delete(row)

    # Извлекаем данные из базы данных
    cursor.execute('SELECT * FROM Employee')
    employees = cursor.fetchall()

    # Добавляем данные в таблицу
    for employee in employees:
        tree_emp.insert('', 0, text=employee[0], values=(employee[1], employee[2], employee[3], employee[4], employee[5], employee[6], employee[7], employee[8]))

    tree_emp.place(x=10, y=80)
    tree_anl.place_forget()  # Скрываем таблицу с животными

def show_animals():
    for row in tree_anl.get_children():
        tree_anl.delete(row)
    
    cursor.execute('SELECT * FROM Animals')
    animals = cursor.fetchall()

    for animal in animals:
        tree_anl.insert('', 0, text=animal[0], value=(animal[1], animal[2], animal[3], animal[4], animal[5], animal[6]))

    tree_anl.place(x=10, y=80)
    tree_emp.place_forget()  # Скрываем таблицу с сотрудниками


def update_employee_table():
    # Удаляем все текущие строки из таблицы
    for row in tree_emp.get_children():
        tree_emp.delete(row)

    # Извлекаем данные из базы данных
    cursor.execute('SELECT * FROM Employee')
    employees = cursor.fetchall()

    # Добавляем данные в таблицу
    for employee in employees:
        tree_emp.insert('', 0, text=employee[0], values=(employee[1], employee[2], employee[3], employee[4], employee[5], employee[6], employee[7], employee[8]))

def update_animal_table():
    # Удаляем все текущие строки из таблицы
    for row in tree_anl.get_children():
        tree_anl.delete(row)

    # Извлекаем данные из базы данных
    cursor.execute('SELECT * FROM Animals')
    animals = cursor.fetchall()

    # Добавляем данные в таблицу
    for animal in animals:
        tree_anl.insert('', 0, text=animal[0], values=(animal[1], animal[2], animal[3], animal[4], animal[5], animal[6]))

def delete_employee():
    # Получаем выбранный элемент в таблице
    selected_item = tree_emp.selection()

    if not selected_item:
        messagebox.showinfo('Удаление.', 'Сначала выберете поле, а затем нажмите на кнопку удалить.')
        return
     
    # Получаем ID сотрудника из выбранной строки
    employee_id = tree_emp.item(selected_item, 'text')

    # Удаляем сотрудника из базы данных
    cursor.execute('DELETE FROM Employee WHERE employeeId = %s', (employee_id,))
    db_connector.commit()

    # Удаляем строку из таблицы
    tree_emp.delete(selected_item)

    # Снимаем выделение
    tree_emp.selection_remove(selected_item)

def delete_animal():
    selected_item = tree_anl.selection()

    if not selected_item:
        messagebox.showinfo('Удаление.', 'Сначала выберете поле, а затем нажмите на кнопку удалить.')
        return
    
    animal_id = tree_anl.item(selected_item, 'text')

    cursor.execute('DELETE FROM Animals WHERE animalId = %s', (animal_id,))
    db_connector.commit()

    tree_anl.delete(selected_item)

    # Снимаем выделение
    tree_anl.selection_remove(selected_item)

def search_employee():
    search_params_window = tk.Toplevel(window)
    search_params_window.title('Настройка параметров поиска')
    search_params_window.geometry('300x200')

    # Добавляем элементы управления для установки параметров поиска
    tk.Label(search_params_window, text='Имя или Фамилия:').grid(row=0, column=0, padx=10, pady=10)
    entry_name = tk.Entry(search_params_window)
    entry_name.grid(row=0, column=1)

    def execute_search():
        # Получаем значение параметра поиска
        search_name = entry_name.get()

        # Выполняем запрос с учетом фильтров
        cursor.execute('SELECT * FROM Employee WHERE firstName LIKE %s OR lastName LIKE %s', (f'%{search_name}%', f'%{search_name}%'))
        search_results = cursor.fetchall()

        # Очищаем таблицу перед добавлением результатов поиска
        for row in tree_emp.get_children():
            tree_emp.delete(row)

        # Добавляем результаты поиска в таблицу
        for result in search_results:
            tree_emp.insert('', 0, text=result[0], values=(result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8]))

        # Закрываем окно настройки параметров поиска
        search_params_window.destroy()

    # Добавляем кнопку для запуска поиска
    tk.Button(search_params_window, text='Искать', command=execute_search).grid(row=1, column=1, pady=10)




current_mode = None  # переменная для отслеживания текущего режима

def set_mode(mode):
    global current_mode
    current_mode = mode

def set_mode_employee():
    set_mode('employee')

def set_mode_animal():
    set_mode('animal')

def add_data():
    if current_mode == 'employee':
        add_employee()
    elif current_mode == 'animal':
        add_animal()


# Горизонтальные кнопки
btn_1 = tk.Button(window, text='Сотрудники', width='20', height='1', fg='black', bg='gray', command=lambda: (show_employees(), set_mode_employee()))
btn_1.place(x = 20, y = 10)

btn_2 = tk.Button(window, text = 'Животные', width = '20', height = '1', fg = 'black', bg = 'gray', command=lambda: (show_animals(), set_mode_animal()))
btn_2.place(x = 200, y = 10)

btn_3 = tk.Button(window, text = 'Поставщики', width = '20', height = '1', fg = 'black', bg = 'gray')
btn_3.place(x = 400, y = 10)

btn_4 = tk.Button(window, text = 'Изолятор', width = '20', height = '1', fg = 'black', bg = 'gray')
btn_4.place(x = 600, y = 10)


# Вертикальные кнопки
btn_add = tk.Button(window, text = 'Добавить', width = '20', height = '1', fg = 'black', bg = 'gray', command=add_data)
btn_add.place(x = 800, y = 20)

btn_update = tk.Button(window, text='Обновить данные', width='20', height='1', fg='black', bg='gray', command=lambda: (update_employee_table() if current_mode == 'employee' else update_animal_table()))
btn_update.place(x=800, y=60)

btn_clean = tk.Button(window, text = 'Удалить', width = '20', height = '1', fg = 'black', bg = 'gray', command=lambda:(delete_animal() if current_mode == 'animal' else delete_employee()))
btn_clean.place(x = 800, y = 100)

btn_find = tk.Button(window, text = 'Искать', width = '20', height = '1', fg = 'black', bg = 'gray', command=search_employee)
btn_find.place(x = 800, y = 140)

btn_filter = tk.Button(window, text = 'Фильтрация', width = '20', height = '1', fg = 'black', bg = 'gray')
btn_filter.place(x = 800, y = 180)


window.mainloop()
cursor.close()
db_connector.close()