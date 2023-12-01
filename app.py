import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector


# Создание окна
window = tk.Tk()
window.resizable(width = False, height = False)
window.title('Your ZOO')
window.geometry('1200x520')
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

    labels = ['Вид', 'Имя', 'Гендер', 'Возраст', 'Пара']
    entries = []

    for i, label in enumerate(labels):
        tk.Label(input_window, text=label).grid(row=i)
        entries.append(tk.Entry(input_window))
        entries[-1].grid(row=i, column=1) 

    def submit():
        animal_data = {label: entry.get() for label, entry in zip(labels, entries)}
        cursor.execute('INSERT INTO Animals (kind, name, gender, age, pair) VALUES (%s, %s, %s, %s, %s)',
                (animal_data['Вид'], animal_data['Имя'], animal_data['Гендер'], animal_data['Возраст'], animal_data['Пара']))
        db_connector.commit()
        input_window.destroy()
    
    tk.Button(input_window, text='Submit', command=submit).grid(row = len(labels), column = 1)


def add_animal_health():
    input_window = tk.Toplevel(window)
    input_window.title('Добавить информацию о здоровье животного')
    input_window.geometry('300x200')

    labels = ['Болезнь', 'Прививка', 'Время в зоопарке', 'Количество потомства']
    entries = []

    for i, label in enumerate(labels):
        tk.Label(input_window, text=label).grid(row=i)
        entries.append(tk.Entry(input_window))
        entries[-1].grid(row=i, column=1) 

    # Создаем выпадающий список с именами животных
    cursor.execute('SELECT animalId, name FROM Animals')
    animals = cursor.fetchall()
    animal_names = [animal[1] for animal in animals]
    animal_var = tk.StringVar(input_window)
    animal_var.set(animal_names[0])  # устанавливаем значение по умолчанию
    animal_dropdown = tk.OptionMenu(input_window, animal_var, *animal_names)
    animal_dropdown.grid(row=len(labels), column=1)

    def submit():
        health_data = {label: entry.get() for label, entry in zip(labels, entries)}
        selected_animal_name = animal_var.get()
        selected_animal_id = [animal[0] for animal in animals if animal[1] == selected_animal_name][0]
        cursor.execute('INSERT INTO AnimalHealth (animalId, disease, vaccination, durationInZoo, offspringCount) VALUES (%s, %s, %s, %s, %s)',
                (selected_animal_id, health_data['Болезнь'], health_data['Прививка'], health_data['Время в зоопарке'], health_data['Количество потомства']))
        db_connector.commit()
        input_window.destroy()
    
    tk.Button(input_window, text='Submit', command=submit).grid(row = len(labels) + 1, column = 1)


def add_suppliers():
    input_window = tk.Toplevel(window)
    input_window.title('Добавить поставщиков')
    input_window.geometry('300x200')

    labels = ['Имя', 'Тип корма', 'Период', 'Количество', 'Стоимость', 'Дата поставки']   
    entries = []

    for i, label in enumerate(labels):
        tk.Label(input_window, text=label).grid(row=i)
        entries.append(tk.Entry(input_window))
        entries[-1].grid(row=i, column=1)

    def submit():
        suppliers_data = {label: entry.get() for label, entry in zip(labels, entries)}
        cursor.execute('INSERT INTO Suppliers (organization_name, type_of_feed, period, quantity, price, delivery_time) VALUE (%s,%s,%s,%s,%s,%s)',
                (suppliers_data['Имя'], suppliers_data['Тип корма'], suppliers_data['Период'], suppliers_data['Количество'], suppliers_data['Стоимость'], suppliers_data['Дата поставки']))
        db_connector.commit()
        input_window.destroy()

    tk.Button(input_window, text='Submit', command=submit).grid(row = len(labels), column = 1)

def add_EmployeeAccess():
    input_window = tk.Toplevel(window)
    input_window.title('Добавить доступ')
    input_window.geometry('300x200')

    # Получить список всех работников и животных
    cursor.execute('SELECT employeeId, firstName, lastName FROM Employee')
    employees = cursor.fetchall()
    cursor.execute('SELECT animalId, name FROM Animals')
    animals = cursor.fetchall()

    # Создать выпадающие списки с именами работников и животных
    employee_var = tk.StringVar()
    employee_dropdown = ttk.Combobox(input_window, textvariable=employee_var)
    employee_dropdown['values'] = [f'{id} - {first} {last}' for id, first, last in employees]
    employee_dropdown.grid(row=0, column=1)
    tk.Label(input_window, text='Работник:').grid(row=0)

    animal_var = tk.StringVar()
    animal_dropdown = ttk.Combobox(input_window, textvariable=animal_var)
    animal_dropdown['values'] = [f'{id} - {name}' for id, name in animals]
    animal_dropdown.grid(row=1, column=1)
    tk.Label(input_window, text='Животное:').grid(row=1)

    def submit():
        # Получить ID работника и животного из выбранных элементов
        employee_id = int(employee_var.get().split(' - ')[0])
        animal_id = int(animal_var.get().split(' - ')[0])

        cursor.execute('INSERT INTO EmployeeAccess (employeeId, animalId) VALUES (%s, %s)', (employee_id, animal_id))
        db_connector.commit()
        input_window.destroy()
    
    tk.Button(input_window, text='Submit', command=submit).grid(row=2, column=1)

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
tree_anl['columns']=('one','two','three','four','five')
tree_anl.column('#0', width=1, minwidth=1, stretch=tk.NO)
tree_anl.column('one', width=150, minwidth=150, stretch=tk.NO)
tree_anl.column('two', width=150, minwidth=150, stretch=tk.NO)
tree_anl.column('three', width=150, minwidth=100, stretch=tk.NO)
tree_anl.column('four', width=120, minwidth=80, stretch=tk.NO)
tree_anl.column('five', width=80, minwidth=80, stretch=tk.NO)

tree_anl.heading('#0',text='ID',anchor=tk.W)
tree_anl.heading('one', text='Вид',anchor=tk.W)
tree_anl.heading('two', text='Имя',anchor=tk.W)
tree_anl.heading('three', text='Гендер',anchor=tk.W)
tree_anl.heading('four', text='Возраст',anchor=tk.W)
tree_anl.heading('five', text='Пара',anchor=tk.W)



tree_health = ttk.Treeview(window)
tree_health['columns']=('one','two','three','four', 'five')
tree_health.column('#0', width=1, minwidth=1, stretch=tk.NO)
tree_health.column('one', width=150, minwidth=150, stretch=tk.NO)
tree_health.column('two', width=150, minwidth=150, stretch=tk.NO)
tree_health.column('three', width=150, minwidth=150, stretch=tk.NO)
tree_health.column('four', width=150, minwidth=100, stretch=tk.NO)
tree_health.column('five', width=150, minwidth=80, stretch=tk.NO)

tree_health.heading('#0',text='ID',anchor=tk.W)
tree_health.heading('one', text='Имя животного',anchor=tk.W)
tree_health.heading('two', text='Болезнь',anchor=tk.W)
tree_health.heading('three', text='Прививка',anchor=tk.W)
tree_health.heading('four', text='Время в зоопарке',anchor=tk.W)
tree_health.heading('five', text='Количество потомства',anchor=tk.W)



tree_sup = ttk.Treeview(window)
tree_sup['columns']=('one','two','three','four','five', 'six')
tree_sup.column('#0', width=1, minwidth=1, stretch=tk.NO)
tree_sup.column('one', width=150, minwidth=150, stretch=tk.NO)
tree_sup.column('two', width=150, minwidth=150, stretch=tk.NO)
tree_sup.column('three', width=150, minwidth=100, stretch=tk.NO)
tree_sup.column('four', width=120, minwidth=80, stretch=tk.NO)
tree_sup.column('five', width=80, minwidth=80, stretch=tk.NO)
tree_sup.column('six', width=90, minwidth=80, stretch=tk.NO)

tree_sup.heading('#0',text='ID',anchor=tk.W)
tree_sup.heading('one', text='Имя',anchor=tk.W)
tree_sup.heading('two', text='Тип корма',anchor=tk.W)
tree_sup.heading('three', text='Период',anchor=tk.W)
tree_sup.heading('four', text='Количество',anchor=tk.W)
tree_sup.heading('five', text='Стоимость',anchor=tk.W)
tree_sup.heading('six', text='Дата поставки',anchor=tk.W)


tree_EA = ttk.Treeview(window)
tree_EA['columns']=('one','two')
tree_EA.column('#0', width=1, minwidth=1, stretch=tk.NO)
tree_EA.column('one', width=150, minwidth=150, stretch=tk.NO)
tree_EA.column('two', width=150, minwidth=150, stretch=tk.NO)

tree_EA.heading('#0',text='ID',anchor=tk.W)
tree_EA.heading('one', text='ID работника',anchor=tk.W)
tree_EA.heading('two', text='ID животного',anchor=tk.W)

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
    tree_anl.place_forget()
    tree_sup.place_forget()
    tree_health.place_forget()
    tree_EA.place_forget()

def show_animals():
    for row in tree_anl.get_children():
        tree_anl.delete(row)
    
    cursor.execute('SELECT * FROM Animals')
    animals = cursor.fetchall()

    for animal in animals:
        tree_anl.insert('', 0, text=animal[0], value=(animal[1], animal[2], animal[3], animal[4], animal[5]))

    tree_anl.place(x=10, y=80)
    tree_emp.place_forget() 
    tree_sup.place_forget()
    tree_health.place_forget()
    tree_EA.place_forget()

def show_animal_health():
    for row in tree_health.get_children():
        tree_health.delete(row)
    
    cursor.execute('SELECT AnimalHealth.healthId, Animals.name, AnimalHealth.disease, AnimalHealth.vaccination, AnimalHealth.durationInZoo, AnimalHealth.offspringCount FROM AnimalHealth INNER JOIN Animals ON AnimalHealth.animalId = Animals.animalId;')
    health_data = cursor.fetchall()

    for health in health_data:
        tree_health.insert('', 0, text=health[0], value=(health[1], health[2], health[3], health[4], health[5]))

    tree_health.place(x=10, y=80)
    tree_anl.place_forget()
    tree_sup.place_forget()
    tree_emp.place_forget()
    tree_EA.place_forget()

def show_suppliers():
    for row in tree_sup.get_children():
      tree_sup.delete(row)
    
    cursor.execute('SELECT * FROM Suppliers')
    suppliers = cursor.fetchall()

    for supplier in suppliers:
        tree_sup.insert('', 0, text=supplier[0], value=(supplier[1], supplier[2], supplier[3], supplier[4], supplier[5], supplier[6]))

    tree_sup.place(x=10, y=80)
    tree_emp.place_forget()
    tree_anl.place_forget()
    tree_health.place_forget()
    tree_EA.place_forget()

def show_EmployeeAccess():
    for row in tree_EA.get_children():
      tree_EA.delete(row)
    
    cursor.execute('''
        SELECT EmployeeAccessID, E.firstName, E.lastName, A.kind, A.name 
        FROM EmployeeAccess EA
        JOIN Employee E ON EA.employeeId = E.employeeId
        JOIN Animals A ON EA.animalId = A.animalId
    ''')
    accesses = cursor.fetchall()

    for access in accesses:
        tree_EA.insert('', 0, text=access[0], value=(access[1], access[2], access[3], access[4]))

    tree_EA.place(x=10, y=80)
    
    tree_sup.place_forget()
    tree_anl.place_forget()
    tree_health.place_forget()
    tree_emp.place_forget()
    

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
        tree_anl.insert('', 0, text=animal[0], values=(animal[1], animal[2], animal[3], animal[4], animal[5]))

def update_animal_health_table():
    # Удаляем все текущие строки из таблицы
    for row in tree_health.get_children():
        tree_health.delete(row)

    # Извлекаем данные из базы данных
    cursor.execute('SELECT * FROM AnimalHealth')
    health = cursor.fetchall()

    # Добавляем данные в таблицу
    for healthes in health:
        tree_health.insert('', 0, text=healthes[0], values=(healthes[1], healthes[2], healthes[3], healthes[4], healthes[5]))

def update_suppliers_table():
    for row in tree_sup.get_children():
        tree_sup.delete(row)

    cursor.execute('SELECT * FROM Suppliers')
    suppliers = cursor.fetchall()

    for supplier in suppliers:
        tree_sup.insert('', 0, text=supplier[0], value=(supplier[1], supplier[2], supplier[3], supplier[4], supplier[5], supplier[6]))

def update_EmployeeAccess_table():
    for row in tree_EA.get_children():
        tree_EA.delete(row)

    cursor.execute('''
        SELECT EmployeeAccessID, E.firstName, E.lastName, A.kind, A.name 
        FROM EmployeeAccess EA
        JOIN Employee E ON EA.employeeId = E.employeeId
        JOIN Animals A ON EA.animalId = A.animalId
    ''')
    accesses = cursor.fetchall()

    for access in accesses:
        tree_EA.insert('', 0, text=access[0], value=(access[1] + ' ' + access[2], access[3] + ': ' + access[4]))

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

def delete_health():
    selected_item = tree_health.selection()

    if not selected_item:
        messagebox.showinfo('Удаление.', 'Сначала выберете поле, а затем нажмите на кнопку удалить.')
        return
    
    health_id = tree_health.item(selected_item, 'text')

    cursor.execute('DELETE FROM AnimalHealth WHERE healthId = %s', (health_id,))
    db_connector.commit()

    tree_health.delete(selected_item)

    # Снимаем выделение
    tree_health.selection_remove(selected_item)

def delete_suppliers():
    selected_item = tree_sup.selection()

    if not selected_item:
        messagebox.showinfo('Удаление.', 'Сначала выберете поле, а затем нажмите на кнопку удалить.')
        return
    
    supplier_id = tree_sup.item(selected_item, 'text')

    cursor.execute('DELETE FROM Suppliers WHERE suppliersId = %s', (supplier_id,))
    db_connector.commit()

    tree_sup.delete(selected_item)

    # Снимаем выделение
    tree_sup.selection_remove(selected_item)

def delete_EmployeeAccess():
    selected_item = tree_EA.selection()

    if not selected_item:
        messagebox.showinfo('Удаление.', 'Сначала выберете поле, а затем нажмите на кнопку удалить.')
        return
    
    access_id = tree_EA.item(selected_item, 'text')

    cursor.execute('DELETE FROM EmployeeAccess WHERE EmployeeAccessID = %s', (access_id,))
    db_connector.commit()

    tree_EA.delete(selected_item)

    # Снимаем выделение
    tree_EA.selection_remove(selected_item)

def search_employee():
    search_params_window = tk.Toplevel(window)
    search_params_window.title('Настройка параметров поиска')
    search_params_window.geometry('350x250')

    # Добавляем элементы управления для установки параметров поиска
    tk.Label(search_params_window, text='Имя или Фамилия:').grid(row=0, column=0, padx=10, pady=10)
    entry_name = tk.Entry(search_params_window)
    entry_name.grid(row=0, column=1)

    tk.Label(search_params_window, text='Возраст:').grid(row=1, column=0, padx=1, pady=15)
    entry_age = tk.Entry(search_params_window)
    entry_age.grid(row=1, column=1)

    tk.Label(search_params_window, text='Зарплата:').grid(row=2, column=0, padx=1, pady=20)
    entry_salary = tk.Entry(search_params_window)
    entry_salary.grid(row=2, column=1)

    def execute_search():
        # Получаем значение параметра поиска
        search_name = entry_name.get()
        search_age = entry_age.get()
        search_salary = entry_salary.get()

        # Выполняем запрос с учетом фильтров
        if not search_name and not search_age and not search_salary:
        # If both fields are empty, fetch all records
         cursor.execute('SELECT * FROM Employee')
        elif not search_name and not search_salary:
        # If at least one field is not empty, apply filters
         cursor.execute('SELECT * FROM Employee WHERE age LIKE %s', (f'%{search_age}%',))
        elif not search_age and not search_salary:
         cursor.execute('SELECT * FROM Employee WHERE firstName LIKE %s OR lastName LIKE %s', (f'%{search_name}%', f'%{search_name}%'))
        elif not search_name and not search_age:
         cursor.execute('SELECT * FROM Employee WHERE salary LIKE %s', (f'%{search_salary}%',))
        else:
         cursor.execute('SELECT * FROM Employee WHERE firstName LIKE %s OR lastName LIKE %s OR age LIKE %s', (f'%{search_name}%', f'%{search_name}%', f'%{search_age}%', f'%{search_salary}'))  
        
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
    tk.Button(search_params_window, text='Искать', command=execute_search).grid(row=3, column=1, pady=10)  


def search_animal():
    search_params_window = tk.Toplevel(window)
    search_params_window.title('Настройка параметров поиска')
    search_params_window.geometry('350x250')

    tk.Label(search_params_window, text='Вид:').grid(row=0, column=0,padx=5, pady=10)
    entry_kind = tk.Entry(search_params_window)
    entry_kind.grid(row=0,column=1)

    tk.Label(search_params_window, text='Гендер:').grid(row=1, column=0,padx=5, pady=15)
    entry_gender = tk.Entry(search_params_window)
    entry_gender.grid(row=1,column=1)

    tk.Label(search_params_window, text='Возраст:').grid(row=2, column=0,padx=5, pady=20)
    entry_age = tk.Entry(search_params_window)
    entry_age.grid(row=2,column=1)

    def execute_search():
        search_kind = entry_kind.get()
        search_gender = entry_gender.get()
        search_age = entry_age.get()

        if not search_age and not search_gender and not search_kind:
            cursor.execute('SELECT * FROM Animals')
        elif not search_gender and not search_age:
            cursor.execute('SELECT * FROM Animals WHERE kind LIKE %s', (f'%{search_kind}%',))
        elif not search_kind and not search_age:
            cursor.execute('SELECT * FROM Animals WHERE gender LIKE %s', (f'%{search_gender}%',))
        elif not search_kind and not search_gender:
            cursor.execute('SELECT * FROM Animals WHERE age LIKE %s', (f'%{search_age}%',))
        else:
            cursor.execute('SELECT * FROM Animals WHERE name LIKE %s OR gender LIKE %s OR age LIKE %s', (f'%{search_kind}%', f'%{search_gender}', f'%{search_age}') )

        search_results = cursor.fetchall()

        for row in tree_anl.get_children():
            tree_anl.delete(row)

        for result in search_results:
            tree_anl.insert('', 0, text=result[0], values=(result[1], result[2], result[3], result[4], result[5]))

        search_params_window.destroy()
    
    tk.Button(search_params_window, text='Искать', command=execute_search).grid(row=3, column=1, pady=10)  

def search_health():
    search_params_window = tk.Toplevel(window)
    search_params_window.title('Настройка параметров поиска')
    search_params_window.geometry('350x250')

    tk.Label(search_params_window, text='Имя животного:').grid(row=0, column=0,padx=5, pady=10)
    entry_name = tk.Entry(search_params_window)
    entry_name.grid(row=0,column=1)

    def execute_search():
        search_name = entry_name.get()

        if search_name:
            cursor.execute('''
    SELECT AnimalHealth.healthId, Animals.name, AnimalHealth.disease, AnimalHealth.vaccination, AnimalHealth.durationInZoo, AnimalHealth.offspringCount
    FROM AnimalHealth
    INNER JOIN Animals ON AnimalHealth.animalId = Animals.animalId
    WHERE Animals.name LIKE %s
''', (f'%{search_name}%',))

        search_results = cursor.fetchall()

        for row in tree_health.get_children():
            tree_health.delete(row)

        for result in search_results:
            tree_health.insert('', 0, text=result[0], values=(result[1], result[2], result[3], result[4], result[5]))

        search_params_window.destroy()
    
    tk.Button(search_params_window, text='Искать', command=execute_search).grid(row=1, column=1, pady=10)  

def search_suppliers():
    search_params_window = tk.Toplevel(window)
    search_params_window.title('Настройка параметров поиска')
    search_params_window.geometry('350x250')

    tk.Label(search_params_window, text='Имя:').grid(row=0, column=0,padx=5, pady=10)
    entry_name = tk.Entry(search_params_window)
    entry_name.grid(row=0,column=1)

    tk.Label(search_params_window, text='Тип Корма:').grid(row=1, column=0,padx=5, pady=15)
    entry_type = tk.Entry(search_params_window)
    entry_type.grid(row=1,column=1)

    tk.Label(search_params_window, text='Стоимость:').grid(row=2, column=0,padx=5, pady=20)
    entry_price = tk.Entry(search_params_window)
    entry_price.grid(row=2,column=1)

    def execute_search():
        search_name = entry_name.get()
        search_type = entry_type.get()
        search_price = entry_price.get()

        if not search_name and not search_type and not search_price:
            cursor.execute('SELECT * FROM Suppliers')
        elif not search_type and not search_price:
            cursor.execute('SELECT * FROM Suppliers WHERE organization_name LIKE %s', (f'%{search_name}%',))
        elif not search_name and not search_price:
            cursor.execute('SELECT * FROM Suppliers WHERE type_of_feed LIKE %s', (f'%{search_type}%',))
        elif not search_name and not search_type:
            cursor.execute('SELECT * FROM Suppliers WHERE price LIKE %s', (f'%{search_price}%',))
        else:
            cursor.execute('SELECT * FROM Suppliers WHERE organization_name LIKE %s OR type_of_feed LIKE %s OR price LIKE %s', (f'%{search_name}%', f'%{search_type}', f'%{search_price}') )

        search_results = cursor.fetchall()

        for row in tree_sup.get_children():
            tree_sup.delete(row)

        for result in search_results:
            tree_sup.insert('', 0, text=result[0], values=(result[1], result[2], result[3], result[4], result[5], result[6]))

        search_params_window.destroy()
    
    tk.Button(search_params_window, text='Искать', command=execute_search).grid(row=3, column=1, pady=10) 

def search_EmployeeAccess():
    search_params_window = tk.Toplevel(window)
    search_params_window.title('Настройка параметров поиска')
    search_params_window.geometry('350x250')

    tk.Label(search_params_window, text='Имя работника:').grid(row=0, column=0,padx=5, pady=10)
    entry_name = tk.Entry(search_params_window)
    entry_name.grid(row=0,column=1)

    def execute_search():
        search_name = entry_name.get()

        if search_name:
            cursor.execute('''
    SELECT EmployeeAccessID, E.firstName, E.lastName, A.kind, A.name 
    FROM EmployeeAccess EA
    JOIN Employee E ON EA.employeeId = E.employeeId
    JOIN Animals A ON EA.animalId = A.animalId
    WHERE E.firstName LIKE %s OR E.lastName LIKE %s
''', (f'%{search_name}%', f'%{search_name}%'))

        search_results = cursor.fetchall()

        for row in tree_EA.get_children():
            tree_EA.delete(row)

        for result in search_results:
            tree_EA.insert('', 0, text=result[0], values=(result[1] + ' ' + result[2], result[3] + ': ' + result[4]))

        search_params_window.destroy()
    
    tk.Button(search_params_window, text='Искать', command=execute_search).grid(row=1, column=1, pady=10)



current_mode = None  # переменная для отслеживания текущего режима

def set_mode(mode):
    global current_mode
    current_mode = mode

def set_mode_employee():
    set_mode('employee')

def set_mode_animal():
    set_mode('animal')

def set_mode_suppliers():
    set_mode('suppliers')

def set_mode_health():
    set_mode('health')

def set_mode_EmployeeAccess():
    set_mode('EmployeeAccess')

def add_data():
    if current_mode == 'employee':
        add_employee()
    elif current_mode == 'animal':
        add_animal()
    elif current_mode == 'suppliers':
        add_suppliers()
    elif current_mode == 'health':
        add_animal_health()
    elif current_mode == 'EmployeeAccess':
        add_EmployeeAccess()


# Горизонтальные кнопки
btn_1 = tk.Button(window, text='Сотрудники', width='20', height='1', fg='black', bg='gray', command=lambda: (show_employees(), set_mode_employee()))
btn_1.place(x = 20, y = 10)

btn_2 = tk.Button(window, text = 'Животные', width = '20', height = '1', fg = 'black', bg = 'gray', command=lambda: (show_animals(), set_mode_animal()))
btn_2.place(x = 200, y = 10)

btn_3 = tk.Button(window, text = 'Поставщики', width = '20', height = '1', fg = 'black', bg = 'gray', command=lambda: (show_suppliers(), set_mode_suppliers()))
btn_3.place(x = 400, y = 10)

btn_4 = tk.Button(window, text = 'Клинические данные', width = '20', height = '1', fg = 'black', bg = 'gray', command=lambda: (show_animal_health(), set_mode_health()))
btn_4.place(x = 600, y = 10)

btn_5 = tk.Button(window, text = 'Доступ', width = '20', height = '1', fg = 'black', bg = 'gray', command=lambda: (show_EmployeeAccess(), set_mode_EmployeeAccess()))
btn_5.place(x = 800, y = 10)


# Вертикальные кнопки
btn_add = tk.Button(window, text = 'Добавить', width = '20', height = '1', fg = 'black', bg = 'gray', command=add_data)
btn_add.place(x = 1000, y = 20)

btn_update = tk.Button(window, text='Обновить данные', width='20', height='1', fg='black', bg='gray', command=lambda: update_employee_table() if current_mode == 'employee' else (update_animal_table() if current_mode == 'animal' else (update_suppliers_table() if current_mode == 'suppliers' else (update_animal_health_table() if current_mode == 'health' else update_EmployeeAccess_table()))))
btn_update.place(x=1000, y=60)

btn_clean = tk.Button(window, text = 'Удалить', width = '20', height = '1', fg = 'black', bg = 'gray', command=lambda: delete_animal() if current_mode == 'animal' else (delete_employee() if current_mode == 'employee' else (delete_suppliers() if current_mode == 'suppliers' else (delete_health() if current_mode == 'health' else delete_EmployeeAccess()))))
btn_clean.place(x = 1000, y = 100)

btn_find = tk.Button(window, text = 'Искать', width = '20', height = '1', fg = 'black', bg = 'gray', command=lambda: search_employee() if current_mode == 'employee' else (search_animal() if current_mode == 'animal' else (search_suppliers() if current_mode == 'suppliers' else (search_health() if current_mode == 'health' else search_EmployeeAccess()))))
btn_find.place(x = 1000, y = 140)

# btn_filter = tk.Button(window, text = 'Фильтрация', width = '20', height = '1', fg = 'black', bg = 'gray')
# btn_filter.place(x = 1000, y = 180)


window.mainloop()
cursor.close()
db_connector.close()