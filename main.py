from collections import UserDict
from datetime import datetime
import pickle
import re


#Об'єкти класу "адресна книга"
class AddressBook(UserDict):
    #Функція, що записує контакт до адресної книги
    def add_record(self, Record):
        self.update({Record.Name.name: Record})
        return "Done!"

    #Функція, що виводить Номери телефону певного контакту
    def show_number(self, Name):
        return self.data[Name.name].Phones.phone

    #Функція, що вовидить за раз N-ну кількість контактів із адресної книги (за замовчуванням виведе всі)
    def iterator(self, N=None):
        index = 0
        N = len(self.data) if not N else N
        while index < len(self.data):
            yield list(self.data)[index: index + N]
            index += N

    #Функція, що виводить спісок всіх контактів, що містяться у адресній книзі
    def show_all(self):
        for name, numbers in self.data.items():
            yield f'{name}: {numbers.Phones.phone}'

    #Функція, що шукає контакти, які містять певну послідовність літер в умені контакту, або чисел у його телефонних номерах
    def find(self, piece_of_info):
        res = []
        for name, numbers in self.data.items():
            if piece_of_info in name or piece_of_info in str(numbers.Phones.phone):
                res.append(name)
        if res:
            for name in res:
                print(f'{name}: {self.data[name].Phones.phone}')
        else:
            print('No matches')

    #Функція, що дозволяє зберігти наявну адресну книгу у файл на ПК
    def save_to_file(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self, file)

    #Функція, що дозволяє завантажити адресну книгу з файлу на ПК
    def read_from_file(self, filename):
        with open(filename, "rb") as file:
            content = pickle.load(file)
        return content


#Об'єкти класу "контакт", що міститеме всю інформацію про нього
class Record:
    def __init__(self, Name, Phones=None, Birthday=None):
        self.Name = Name
        self.Phones = Phones
        self.Birthday = Birthday

    #функція, що додає номер телефону до контакту
    def add_phone(self, Phone):
        self.Phones.phone = list(set(self.Phones.phone) | set(Phone.phone))
        return "Done!"

    #Функція, що змінює наявні номери телефону на нові
    def change_phone(self, Phone):
        self.Phones = Phone
        return "Done!"

    #Функція, що видаляє наявний номер телефону
    def delite_phone(self, Phone):
        self.Phones.phone = list(set(self.Phones.phone) - set(Phone.phone))
        return "Done!"

    #Функція, що розраховує кількість днів до наступного дня нородження контакта
    def days_to_birthday(self):
        if self.Birthday.birthday:
            current_datetime = datetime.now()
            birthday = datetime.strptime(self.Birthday.birthday, '%d/%m/%Y')
            if int(current_datetime.month) > int(birthday.month) or (int(current_datetime.month) == int(birthday.month) and int(current_datetime.day) >= int(birthday.day)):
                next_birthday = datetime(
                    year=current_datetime.year+1, month=birthday.month, day=birthday.day)
                return f"In {(next_birthday - current_datetime).days} days"
            else:
                next_birthday = datetime(
                    year=current_datetime.year, month=birthday.month, day=birthday.day)
                return f"In {(next_birthday - current_datetime).days} days"
        else:
            return "The birthsay date is unknown."


#Після отримання введеної користувачем команди та відокремлення від неї слова-ключа, отримана інформація сортується за критеріями
class Field:
    def __init__(self, data):
        #Вілокремлюються всі слова
        self.name = ' '.join(re.findall('[a-z]+', data))
        #Відокремлюються всі номери
        self.phone = re.findall('\d+', data)
        #Відокремлення дати, що має формат дд/мм/рррр (маєця на увазі, що вона має бути введена тільки одна)
        self.birthday = ''.join(re.findall('\d{2}\/\d{2}\/\d{4}', data))


#Об'єкти класу "ім'я контакту"
class Name(Field):
    def __init__(self, name):
        super().__init__(name)


#Об'єкти класу "номер телефону"
class Phone(Field):
    def __init__(self, phone):
        self.__phone = None
        super().__init__(phone)

    @property
    def phone(self):
        return self.__phone
    
    #Перевірка на коректність вводу номерів телефону (мають містити від 10 до 12 чисел)
    @phone.setter
    def phone(self, phone):
        correct_numbers = []
        for number in phone:
            if 10 <= len(number) <= 12:
                correct_numbers.append(number)
        self.__phone = correct_numbers


#Обєкти класу "день народження"
class Birthday(Field):
    def __init__(self, birthday):
        self.__birthday = None
        super().__init__(birthday)

    @property
    def birthday(self):
        return self.__birthday

    #Перевірка на коректність вводу (має бути формат дд/мм/рррр)
    @birthday.setter
    def birthday(self, birthday):
        try:
            test = datetime.strptime(birthday, '%d/%m/%Y')
            current_datetime = datetime.now()
            if (current_datetime - test).days > 0:
                self.__birthday = birthday
        except:
            pass


#Наша адресна книга
CONTACTS = AddressBook()


#Функція привітання
def hello():
    return 'How can I help you?'


#Фунція виходу
def close():
    return "Good bye!"


#Уникання будь-яких помилок під час роботи програми
def input_error(func):
    def inner():
        flag = True
        while flag:
            try:
                result = func()
                flag = False
            except IndexError:
                print('Enter the name and numbers separated by a space.')
            except ValueError:
                print('I have no idea how you did it, try again.')
            except KeyError:
                print("The contact is missing.")
        return result
    return inner


#Головна функція, куди додаємо весь функціонал
@ input_error
def main():
    bot_status = True
    #Умава, що забеспечує безкінечний цикл запиту, поки не буде виходу
    while bot_status:
        #Введення команди з консолі
        command = input('Enter the command: ').lower()
        #Привітання з користувачем (сюди можна вставити правила вводу всіх можливих функцій)
        if command == 'hello':
            print(hello())
        #Додавання нового контакту
        elif 'add' in command:
            command = command.removeprefix('add ')
            if Name(command).name in CONTACTS.data:
                print(CONTACTS.data[Name(command).name].add_phone(
                    Phone(command)))
            #Додавання нової інформації до вже існуючого контакту
            else:
                print(CONTACTS.add_record(
                    Record(Name(command), Phone(command), Birthday(command))))
        #Зміна номеру телефону у вже існуючому контакті
        elif "change" in command:
            command = command.removeprefix('change ')
            print(CONTACTS.data[Name(command).name].change_phone(
                Phone(command)))
        #Видалення номеру телефону з вже існуючого контакту
        elif "delite" in command:
            command = command.removeprefix('delite ')
            print(CONTACTS.data[Name(command).name].delite_phone(
                Phone(command)))
        #Вивід всіх існуючих номерів телефону певного контакту (вказувати ім'я після пробілу)
        elif "phone" in command:
            command = command.removeprefix("phone ")
            print(CONTACTS.show_number(Name(command)))
        #Вивід всіх існуючих контактів у адресній книзі
        elif command == "show all":
            if CONTACTS:
                for contact in CONTACTS.show_all():
                    print(contact)
            else:
                print('The contact list is empty.')
        #Вивід кількості днів до наступного дня народження певного контакту із тих, що маються
        elif "birthday" in command:
            command = command.removeprefix("birthday ")
            print(CONTACTS.data[Name(command).name].days_to_birthday())
        #Пошук контакту за певною послідовністю літер або чисел
        elif "find" in command:
            command = command.removeprefix('find ')
            CONTACTS.find(command)
        #Вихід із програми (сюди треба додати автоматичне збереження наявної адресної книги)
        elif command in ("good bye", "bye", "close", "exit"):
            print(close())
            bot_status = False
        #Якщо користувач некоректно ввів команду (тут можна реалізувати додаткове завдання з підказкою можливих команд)
        else:
            print("Enter correct command, please.")


if __name__ == '__main__':
    main()
