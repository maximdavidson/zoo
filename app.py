import tkinter as tk
from tkinter import messagebox
import mysql.connector


def show_animal_info():
   animal_info_frame.pack_forget()  # Скрыть предыдущий фрейм (если есть)
   # animal_info_frame.pack(pady=100)
   animal_info_frame.place(x=20, y=50)
   # animal_info_frame.pack(side='left', fill='y')


    # Список полей информации
   info_labels = ['Имя животного:', 'Вид:', 'Пол:', 'Возраст:', 'Клетка:', 'Статус:']

    # Создание и расположение виджетов Label и Entry
   for label_text in info_labels:
      label = tk.Label(animal_info_frame, text=label_text, bg='lightgray')
      label.pack(anchor='w', pady=5)

      entry = tk.Entry(animal_info_frame, width=30)
      entry.pack(anchor='w', pady=5)

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

btn_2 = tk.Button(window, text = 'Животные', width = '20', height = '1', fg = 'black', bg = 'gray', command = show_animal_info)
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



# Фрейм для отображения информации о животных
animal_info_frame = tk.Frame(window, bg='lightgray')


window.mainloop()
cursor.close()
db_connector.close()