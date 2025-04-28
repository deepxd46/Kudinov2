import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import time
from pymorphy3 import MorphAnalyzer
import os

class LetterGridApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Puzzle")
        
        self.grid_size = 5
        self.letters = [
            ['А', 'Б', 'В', 'Г', 'Д', 'Е'],
            ['Ж', 'З', 'И', 'Й', 'К', 'Л'],
            ['М', 'Н', 'О', 'П', 'Р', 'С'],
            ['Т', 'У', 'Ф', 'Х', 'Ц', 'Ч'],
            ['Ш', 'Щ', 'Ы', 'Э', 'Ю', 'Я']
        ]

        self.selected_letters = []
        self.start_time = None
        self.timer_running = False
        self.elapsed_time = 0
        self.user_name = None
        self.score = 0
        self.checked_words = []
        self.grid_buttons = []

        self.current_word_label = None
        self.check_button = None
        self.score_label = None
        self.words_listbox = None

        self.dictionary_file = "словарь.txt"
        self.create_dictionary_file()  # Создаем файл при запуске
        
        # Инициализируем морфологический анализатор
        self.morph = MorphAnalyzer()

        self.create_ui()

    def create_dictionary_file(self):
        """Создает файл словаря если его нет"""
        if not os.path.exists(self.dictionary_file):
            with open(self.dictionary_file, 'w', encoding='utf-8') as f:
                f.write("")
    
    def add_to_dictionary(self, word):
        """Добавляет слово в файл словаря без дубликатов"""
        with open(self.dictionary_file, 'r+', encoding='utf-8') as f:
            existing_words = [line.strip().lower() for line in f.readlines()]
            if word not in existing_words:
                f.write(f"{word}\n")

    def create_ui(self):
        # Верхний фрейм для кнопок
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=10, fill=tk.X)  # Растягиваем фрейм по горизонтали

        # Кнопка "Пользователь"
        self.user_button = tk.Button(top_frame, text="Пользователь", command=self.show_user_window)
        self.user_button.grid(row=0, column=0, padx=5, sticky="ew")

        # Выпадающий список для выбора режима
        self.modes = ['Режим 1', 'Режим 2', 'Режим 3']
        self.selected_mode = tk.StringVar(value=self.modes[0])
        self.mode_menu = tk.OptionMenu(top_frame, self.selected_mode, *self.modes)
        self.mode_menu.grid(row=0, column=1, padx=5, sticky="ew")

        # Кнопка "Помощь"
        self.help_button = tk.Button(top_frame, text="Помощь", command=self.show_help_window)
        self.help_button.grid(row=0, column=2, padx=5, sticky="ew")

        # Кнопка "Таблица лидеров"
        self.leaderboard_button = tk.Button(top_frame, text="Таблица лидеров", command=self.show_leaderboard)
        self.leaderboard_button.grid(row=0, column=3, padx=5, sticky="ew")

        # Устанавливаем одинаковую ширину для всех колонок
        top_frame.grid_columnconfigure(0, weight=1)
        top_frame.grid_columnconfigure(1, weight=1)
        top_frame.grid_columnconfigure(2, weight=1)
        top_frame.grid_columnconfigure(3, weight=1)

        # Фрейм для текущего слова и кнопки проверки
        word_frame = tk.Frame(self.root)
        word_frame.pack(pady=10, fill=tk.X)  # Явно размещаем фрейм

        # Метка для отображения текущего слова
        self.current_word_label = tk.Label(
            word_frame, 
            text="Текущее слово: ", 
            font=("Helvetica", 14),
            anchor="w",
            width=20
        )
        self.current_word_label.pack(side=tk.LEFT, padx=10)

        # Кнопка проверки слова
        self.check_button = tk.Button(
            word_frame, 
            text="Проверить слово", 
            command=self.check_word,
            state=tk.DISABLED,
            width=15
        )
        self.check_button.pack(side=tk.RIGHT, padx=10)

        # Метка счета
        self.score_label = tk.Label(
            self.root,
            text=f"Очки: {self.score}",
            font=("Helvetica", 14),
            pady=10
        )
        self.score_label.pack()

        # Список проверенных слов
        self.words_listbox = tk.Listbox(
            self.root,
            width=30,
            height=5,
            font=("Helvetica", 12)
        )
        self.words_listbox.pack(pady=10)

        # Нижний фрейм для сетки
        self.grid_frame = tk.Frame(self.root)  # Делаем атрибутом класса
        self.grid_frame.pack(pady=20)
        self.create_grid(self.grid_frame)  # Передаем фрейм в метод

        # Кнопка "Начать игру"
        self.start_button = tk.Button(self.root, text="Начать игру", command=self.start_game)
        self.start_button.pack(pady=10)

        # Метка для отображения времени
        self.time_label = tk.Label(self.root, text="Время: 0 секунд", font=("Helvetica", 12))
        self.time_label.pack(pady=10)

    def check_word(self):
        if not self.selected_letters:
            messagebox.showwarning("Пусто", "Выберите буквы!")
            return
            
        word = "".join(self.selected_letters).lower()
        
        # Проверка слова через Pymorphy3
        is_valid = self.pymorphy_check(word)
        
        if is_valid:
            self.add_to_dictionary(word)

            points = len(word)
            self.score += points
            self.score_label.config(text=f"Очки: {self.score}")
            self.checked_words.append(word)
            self.words_listbox.insert(tk.END, word)
            messagebox.showinfo("Успех!", f"Слово принято! +{points} очков")
        else:
            messagebox.showwarning("Ошибка", "Такого слова не существует!")
        
        self.selected_letters = []
        self.highlight_word()
        self.current_word_label.config(text="Текущее слово: ")

    def pymorphy_check(self, word):
        """Проверка слова через морфологический анализатор"""
        parsed = self.morph.parse(word)
        print(parsed)
        print(parsed[0].tag.POS)
        if parsed[0].tag.POS == None:
            return False
        
        return parsed[0].score >= 0.5


    def create_grid(self, frame):
        self.grid_buttons = []  # Инициализируем список кнопок
        for i in range(self.grid_size):
            row_buttons = []
            for j in range(6):
                letter = self.letters[i][j]
                button = tk.Button(frame, text=letter, width=5, height=2,
                                   command=lambda i=i, j=j: self.on_click(i, j))
                button.grid(row=i, column=j, padx=5, pady=5)
                row_buttons.append(button)
            self.grid_buttons.append(row_buttons)

    def on_click(self, i, j):
        letter = self.letters[i][j]
        if letter not in self.selected_letters:
            self.selected_letters.append(letter)
            self.highlight_word()
            # Обновляем отображение текущего слова
            self.current_word_label.config(
                text=f"Текущее слово: {' '.join(self.selected_letters)}"
            )
            # Активируем кнопку проверки если есть выбранные буквы
            self.check_button.config(state=tk.NORMAL)

    def highlight_word(self):
        # Сбрасываем все цвета
        for i in range(self.grid_size):
            for j in range(6):
                self.grid_buttons[i][j].config(bg='SystemButtonFace')

        # Подсвечиваем выбранные буквы
        for letter in self.selected_letters:
            for i in range(self.grid_size):
                for j in range(6):
                    if self.letters[i][j] == letter:
                        self.grid_buttons[i][j].config(bg='lightgreen')
                        break

    def start_game(self):
        """Запуск игры"""
        if not self.timer_running:  # Если таймер не запущен
            self.start_time = time.time()  # Засекаем время
            self.timer_running = True
            self.elapsed_time = 0
            self.update_timer()  # Обновляем таймер

    def update_timer(self):
        """Обновление таймера"""
        if self.timer_running:
            self.elapsed_time = time.time() - self.start_time  # Рассчитываем прошедшее время
            self.time_label.config(text=f"Время: {int(self.elapsed_time)} секунд")  # Обновляем текст на метке
            self.root.after(1000, self.update_timer)  # Обновление каждую секунду

    def show_user_window(self):
        """Окно для входа и регистрации"""
        user_window = tk.Toplevel(self.root)
        user_window.title("Вход / Регистрация")
        user_window.geometry("350x400")  # Задаем размер окна

        # Добро пожаловать
        welcome_label = tk.Label(user_window, text="Добро пожаловать", font=("Helvetica", 16))
        welcome_label.pack(pady=10)

        # Поле для почты
        email_label = tk.Label(user_window, text="E-mail")
        email_label.pack(pady=5)
        self.email_entry = tk.Entry(user_window, width=30)
        self.email_entry.pack(pady=5)

        # Поле для пароля
        password_label = tk.Label(user_window, text="Пароль")
        password_label.pack(pady=5)
        self.password_entry = tk.Entry(user_window, width=30, show="*")
        self.password_entry.pack(pady=5)

        # Кнопки
        button_frame = tk.Frame(user_window)
        button_frame.pack(pady=10)

        # Кнопка входа
        login_button = tk.Button(button_frame, text="Войти", command=self.login)
        login_button.grid(row=0, column=0, padx=5)

        # Кнопка регистрации
        register_button = tk.Button(button_frame, text="Зарегистрироваться", command=self.register)
        register_button.grid(row=0, column=1, padx=5)

        # Социальные кнопки и другие действия
        social_frame = tk.Frame(user_window)
        social_frame.pack(pady=10)

        telegram_button = tk.Button(social_frame, text="Телеграмм", command=self.open_telegram)
        telegram_button.grid(row=0, column=0, padx=5)

        vk_button = tk.Button(social_frame, text="ВКонтакте", command=self.open_vk)
        vk_button.grid(row=0, column=1, padx=5)

        email_button = tk.Button(social_frame, text="E-mail", command=self.send_email)
        email_button.grid(row=0, column=2, padx=5)

        forgot_password_button = tk.Button(user_window, text="Забыли пароль?", command=self.forgot_password)
        forgot_password_button.pack(pady=10)

    def login(self):
        """Обработчик для входа"""
        email = self.email_entry.get()
        password = self.password_entry.get()
        if email and password:
            messagebox.showinfo("Вход", f"Добро пожаловать, {email}!")
        else:
            messagebox.showwarning("Ошибка", "Введите все данные!")

    def register(self):
        """Обработчик для регистрации"""
        email = self.email_entry.get()
        password = self.password_entry.get()
        if email and password:
            messagebox.showinfo("Регистрация", f"Вы успешно зарегистрированы, {email}!")
        else:
            messagebox.showwarning("Ошибка", "Введите все данные!")

    def open_telegram(self):
        """Пример ссылки на Телеграм"""
        messagebox.showinfo("Телеграмм", "Открытие Телеграмм...")

    def open_vk(self):
        """Пример ссылки на ВКонтакте"""
        messagebox.showinfo("ВКонтакте", "Открытие ВКонтакте...")

    def send_email(self):
        """Пример отправки E-mail"""
        messagebox.showinfo("E-mail", "Отправка письма...")

    def forgot_password(self):
        """Обработчик для кнопки 'Забыли пароль?'"""
        messagebox.showinfo("Забыли пароль?", "Восстановление пароля...")

    def show_help_window(self):
        """Окно помощи"""
        help_window = tk.Toplevel(self.root)
        help_window.title("Помощь")
        help_window.geometry("400x400")

        # Заголовок окна помощи
        help_title = tk.Label(help_window, text="Помощь", font=("Helvetica", 16))
        help_title.pack(pady=10)

        # Переключатель для подсказок
        self.hints_enabled = tk.BooleanVar(value=False)
        hints_switch = tk.Checkbutton(help_window, text="Включить подсказки", variable=self.hints_enabled)
        hints_switch.pack(pady=10)

        # Словарь
        dictionary_button = tk.Button(help_window, text="Таблица (словарь)", command=self.show_dictionary)
        dictionary_button.pack(pady=10)

        # Гайд с правилами игры
        rules_button = tk.Button(help_window, text="Гайд (Правила игры)", command=self.show_rules)
        rules_button.pack(pady=10)

    def show_dictionary(self):
        """Показать словарь из файла"""
        dictionary_window = tk.Toplevel(self.root)
        dictionary_window.title("Таблица (словарь)")
        dictionary_window.geometry("400x300")

        # Создаем скроллбар
        scrollbar = tk.Scrollbar(dictionary_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Создаем список для слов
        listbox = tk.Listbox(
            dictionary_window, 
            yscrollcommand=scrollbar.set,
            font=("Helvetica", 12),
            width=40
        )
        listbox.pack(fill=tk.BOTH, expand=True)

        # Загружаем слова из файла
        try:
            with open(self.dictionary_file, 'r', encoding='utf-8') as f:
                words = sorted([line.strip() for line in f.readlines() if line.strip()])
                for word in words:
                    listbox.insert(tk.END, word.capitalize())
        except FileNotFoundError:
            listbox.insert(tk.END, "Словарь пуст")

        scrollbar.config(command=listbox.yview)

    def show_rules(self):
        """Показать правила игры"""
        rules_window = tk.Toplevel(self.root)
        rules_window.title("Правила игры")
        rules_window.geometry("400x300")

        rules_text = """1. Выберите буквы из сетки.
2. Составьте слова, используя выбранные буквы.
3. Если слово правильно, оно засчитывается.
4. Для получения подсказок, включите переключатель.
5. Попробуйте составить как можно больше слов за ограниченное время."""
        rules_label = tk.Label(rules_window, text=rules_text, font=("Helvetica", 12), justify="left")
        rules_label.pack(pady=10)

    def show_leaderboard(self):
        """Окно таблицы лидеров"""
        leaderboard_window = tk.Toplevel(self.root)
        leaderboard_window.title("Таблица лидеров")
        leaderboard_window.geometry("400x300")

        # Заголовок таблицы лидеров
        leaderboard_title = tk.Label(leaderboard_window, text="Таблица лидеров", font=("Helvetica", 16))
        leaderboard_title.pack(pady=10)

        # Создаем таблицу с двумя колонками: Никнейм и Очки
        columns = ("Никнейм", "Очки")

        # Treeview для отображения таблицы
        tree = ttk.Treeview(leaderboard_window, columns=columns, show="headings")
        tree.pack(fill=tk.BOTH, expand=True)

        tree.heading("Никнейм", text="Никнейм")
        tree.heading("Очки", text="Очки")

        # Добавляем примерные данные
        tree.insert("", "end", values=("Игрок1", 100))
        tree.insert("", "end", values=("Игрок2", 90))
        tree.insert("", "end", values=("Игрок3", 80))

if __name__ == "__main__":
    root = tk.Tk()
    app = LetterGridApp(root)
    root.mainloop()