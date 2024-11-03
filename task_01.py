from collections import UserDict
import re
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    # Клас для зберігання імені контакту. Обов'язкове поле.
    def __init__(self, value):
        super().__init__(value)

class Phone(Field):
    # Клас для зберігання номера телефону з валідацією
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Номер телефону має бути 10 цифр.")
        super().__init__(value)

    @staticmethod
    def validate(value):
        # Валідація формату телефону (10 цифр)
        return bool(re.match(r'^\d{10}$', value))

class Birthday(Field):
    def __init__(self, value):
        try:
            # Перевірка формату дати та перетворення рядка на об'єкт datetime
            self.value = datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return False

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return True
        return False

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, birthday: {self.birthday.value.strftime('%d.%m.%Y') if self.birthday else 'None'}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        return False

    def get_upcoming_birthdays(self):
        upcoming_birthdays = []
        today = datetime.now()
        next_week = today + timedelta(days=7)
        for record in self.data.values():
            if record.birthday:
                # Визначаємо день народження цього року
                birthday_this_year = record.birthday.value.replace(year=today.year)
                if today <= birthday_this_year < next_week:
                    upcoming_birthdays.append(record.name.value)
        return upcoming_birthdays

# Приклад використання
if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("15.11.1990")  # Додаємо день народження

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    jane_record.add_birthday("07.11.1995")  # Додаємо день народження
    book.add_record(jane_record)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555, birthday: 15.11.1990

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    # Отримання майбутніх днів народження
    upcoming_birthdays = book.get_upcoming_birthdays()
    print(f"Upcoming birthdays: {upcoming_birthdays}")  # Виведе список контактів з днями народження на наступному тижні
