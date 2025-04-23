import customtkinter
from tkinter import ttk

# Пример данных для таблицы лидеров
leaderboard_data = [
    ("Игрок1", 150),
    ("Игрок2", 120),
    ("Игрок3", 100),
    ("Игрок4", 90),
    ("Игрок5", 75),
]




def open_leaderboard_window():
    # Создаем новое окно для таблицы лидеров
    leaderboard_window = customtkinter.CTkToplevel(app)
    leaderboard_window.title("Таблица лидеров")
    leaderboard_window.geometry("400x400")

    # Заголовок формы
    leaderboard_label = customtkinter.CTkLabel(leaderboard_window, text="Таблица лидеров", font=("Arial", 20))
    leaderboard_label.pack(pady=10)

    # Создание таблицы
    treeview = ttk.Treeview(leaderboard_window, columns=("Nick", "Score"), show="headings", height=10)
    treeview.pack(pady=10, padx=10, fill="both", expand=True)

    # Настройка столбцов
    treeview.heading("Nick", text="Никнейм")
    treeview.heading("Score", text="Очки")

    treeview.column("Nick", width=150, anchor="center")
    treeview.column("Score", width=100, anchor="center")

    # Добавляем данные в таблицу
    for row in leaderboard_data:
        treeview.insert("", "end", values=row)

def open_help_window():
    # Создаем новое окно для помощи
    help_window = customtkinter.CTkToplevel(app)
    help_window.title("Помощь")
    help_window.geometry("400x400")

    # Заголовок формы
    help_label = customtkinter.CTkLabel(help_window, text="Инструкции для новичков", font=("Arial", 20))
    help_label.pack(pady=10)

    # Инструкции
    instructions = """
    Добро пожаловать в игру! Вот что вам нужно делать:
    1. Выберите буквы для составления слов.
    2. Используйте подсказки, если не знаете слово.
    3. Соберите как можно больше слов.
    """
    instructions_label = customtkinter.CTkLabel(help_window, text=instructions, font=("Arial", 12), justify="left")
    instructions_label.pack(pady=10)

    # Переключатель для подсказок
    hint_label = customtkinter.CTkLabel(help_window, text="Включить подсказки:")
    hint_label.pack(pady=(10, 5))
    hint_switch = customtkinter.CTkSwitch(help_window, text="Подсказки", command=lambda: toggle_hint(hint_switch))
    hint_switch.pack(pady=(0, 20))

    # Создание списка для словаря
    word_list_label = customtkinter.CTkLabel(help_window, text="Статичный словарь:", font=("Arial", 12))
    word_list_label.pack(pady=10)

    # Создание Scrollable Frame
    scrollable_frame = customtkinter.CTkFrame(help_window)
    scrollable_frame.pack(pady=10, fill="both", expand=True)

    # Добавляем Listbox для отображения слов
    word_listbox = customtkinter.CTkListbox(scrollable_frame, height=10, width=35)
    word_listbox.pack(padx=10, pady=5)

    # Добавляем слова и их определения в Listbox
    for word, definition in word_dict.items():
        word_listbox.insert("end", f"{word} - {definition}")

    # Ввод пользователя для проверки слова
    user_word_label = customtkinter.CTkLabel(help_window, text="Введите слово для проверки:", font=("Arial", 12))
    user_word_label.pack(pady=5)

    user_word_entry = customtkinter.CTkEntry(help_window, width=200)
    user_word_entry.pack(pady=5)

    def check_word():
        user_input = user_word_entry.get().upper()  # Приводим к верхнему регистру для проверки
        if user_input in word_dict:
            result_label.config(text=f"Слово '{user_input}' найдено в словаре! Определение: {word_dict[user_input]}")
        else:
            result_label.config(text=f"Слово '{user_input}' не найдено в словаре.")

    check_button = customtkinter.CTkButton(help_window, text="Проверить слово", command=check_word)
    check_button.pack(pady=10)

    # Метка для отображения результата проверки слова
    result_label = customtkinter.CTkLabel(help_window, text="", font=("Arial", 12))
    result_label.pack(pady=10)

def toggle_hint(switch):
    # Функция для включения/выключения подсказок
    if switch.get():
        print("Подсказки включены.")
    else:
        print("Подсказки выключены.")

def open_user_window():
    # Создаем новое окно
    user_window = customtkinter.CTkToplevel(app)
    user_window.title("Пользователь")
    user_window.geometry("400x400")  # Размер окна

    # Заголовок формы
    welcome_label = customtkinter.CTkLabel(user_window, text="Добро пожаловать", font=("Arial", 20))
    welcome_label.pack(pady=10)

    # Метка и поле ввода email
    email_label = customtkinter.CTkLabel(user_window, text="E-mail:")
    email_label.pack(pady=(10, 5))
    email_entry = customtkinter.CTkEntry(user_window, width=250)
    email_entry.pack(pady=(0, 10))

    # Метка и поле ввода пароля
    password_label = customtkinter.CTkLabel(user_window, text="Password:")
    password_label.pack(pady=(10, 5))
    password_entry = customtkinter.CTkEntry(user_window, width=250, show="*")
    password_entry.pack(pady=(0, 20))

    # Кнопка "Войти"
    submit_button = customtkinter.CTkButton(user_window, text="Войти", 
                                            command=lambda: print("Email:", email_entry.get(), "Пароль:", password_entry.get()))
    submit_button.pack(pady=(5, 10))

    # Кнопка "Забыл пароль"
    forgot_password_button = customtkinter.CTkButton(user_window, text="Забыл пароль", command=lambda: print("Забыл пароль"))
    forgot_password_button.pack(pady=(5, 10))

    # Кнопка "Регистрация"
    register_button = customtkinter.CTkButton(user_window, text="Регистрация", command=lambda: print("Регистрация"))
    register_button.pack(pady=(5, 10))

    # Заглушки для регистрации через внешние сервисы (Telegram, VK, Gmail)
    button_frame = customtkinter.CTkFrame(user_window)
    button_frame.pack(pady=10)

    telegram_button = customtkinter.CTkButton(button_frame, text="Telegram", command=lambda: print("Регистрация через Telegram"))
    telegram_button.grid(row=0, column=0, padx=10)

    vk_button = customtkinter.CTkButton(button_frame, text="Vk", command=lambda: print("Регистрация через VK"))
    vk_button.grid(row=0, column=1, padx=10)

    gmail_button = customtkinter.CTkButton(button_frame, text="G-mail", command=lambda: print("Регистрация через Gmail"))
    gmail_button.grid(row=0, column=2, padx=10)

def button_click(btn_num):
    print(f"Нажата кнопка {btn_num}")

def start_game():
    print("Игра началась!")

def add_letter(letter):
    current_word.set(current_word.get() + letter)
    print("Текущее слово:", current_word.get())

def remove_letter():
    current_word.set(current_word.get()[:-1])  # Удаление последней буквы
    print("Текущее слово после удаления:", current_word.get())

# Создание главного окна приложения
app = customtkinter.CTk()
app.geometry("400x500")
app.title("Игра в слова")

# Создание фрейма для группировки кнопок
top_frame = customtkinter.CTkFrame(master=app)
top_frame.pack(side="top", fill="x", padx=0, pady=0)

# Размещение 4 кнопок в одном ряду внутри top_frame с помощью grid
button1 = customtkinter.CTkButton(master=top_frame, text="Пользователь", command=open_user_window)
button1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

button2 = customtkinter.CTkButton(master=top_frame, text="Режим игры", command=lambda: button_click(2))
button2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

button3 = customtkinter.CTkButton(master=top_frame, text="Помощь", command=open_help_window)
button3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

button4 = customtkinter.CTkButton(master=top_frame, text="Таблица лидеров", command=open_leaderboard_window)
button4.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

# Равномерное распределение кнопок по горизонтали
for col in range(4):
    top_frame.grid_columnconfigure(col, weight=1)

# Создание плитки с буквами
letter_tile_frame = customtkinter.CTkFrame(master=app)
letter_tile_frame.pack(side="top", fill="x", padx=10, pady=20)

# Список букв для плитки (русский алфавит)
letters = "АБВГГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЭЮЯ"

# Размещение кнопок с буквами
for index, letter in enumerate(letters):
    letter_button = customtkinter.CTkButton(master=letter_tile_frame, text=letter, command=lambda letter=letter: add_letter(letter))
    letter_button.grid(row=index // 6, column=index % 6, padx=5, pady=5, sticky="nsew")

# Создание фрейма для кнопки "Начать игру"
bottom_frame = customtkinter.CTkFrame(master=app)
bottom_frame.pack(side="bottom", fill="x", padx=10, pady=10)

# Кнопка "Начать игру"
start_button = customtkinter.CTkButton(master=bottom_frame, text="Начать игру", command=start_game)
start_button.pack()

# Кнопка "Удалить букву"
backspace_button = customtkinter.CTkButton(master=bottom_frame, text="Удалить букву", command=remove_letter)
backspace_button.pack()

# Текущий вводимый текст
current_word = customtkinter.StringVar()

# Метка для отображения текущего слова
word_label = customtkinter.CTkLabel(master=app, textvariable=current_word, font=("Arial", 16))
word_label.pack(pady=10)

# Заполнение строк в плитке с буквами
for col in range(6):
    letter_tile_frame.grid_columnconfigure(col, weight=1)

# Центрируем плитку с буквами
letter_tile_frame.place(relx=0.5, rely=0.45, anchor="center")

app.mainloop()
