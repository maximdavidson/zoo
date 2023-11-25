import tkinter as tk
from tkinter import messagebox
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



btn_1 = tk.Button(window, text = 'Сотрудники', width = '20', height = '1', fg = 'black', bg = 'gray')
btn_1.place(x = 20, y = 10)

btn_2 = tk.Button(window, text = 'Животные', width = '20', height = '1', fg = 'black', bg = 'gray')
btn_2.place(x = 200, y = 10)

btn_3 = tk.Button(window, text = 'Поставщики', width = '20', height = '1', fg = 'black', bg = 'gray')
btn_3.place(x = 400, y = 10)

btn_4 = tk.Button(window, text = 'Изолятор', width = '20', height = '1', fg = 'black', bg = 'gray')
btn_4.place(x = 600, y = 10)


btn_add = tk.Button(window, text = 'Добавить', width = '20', height = '1', fg = 'black', bg = 'gray')
btn_add.place(x = 800, y = 20)

btn_clean = tk.Button(window, text = 'Удалить', width = '20', height = '1', fg = 'black', bg = 'gray')
btn_clean.place(x = 800, y = 60)

btn_find = tk.Button(window, text = 'Искать', width = '20', height = '1', fg = 'black', bg = 'gray')
btn_find.place(x = 800, y = 100)

btn_filter = tk.Button(window, text = 'Фильтрация', width = '20', height = '1', fg = 'black', bg = 'gray')
btn_filter.place(x = 800, y = 140)



window.mainloop()
cursor.close()
db_connector.close()