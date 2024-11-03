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

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError) as e:
            return str(e)
    return wrapper

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def add_birthday(args, book):
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday for {name} added."
    else:
        return "Contact not found."

@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday is on {record.birthday.value.strftime('%d.%m.%Y')}."
    elif record:
        return f"{name} does not have a birthday recorded."
    return "Contact not found."

@input_error
def birthdays(args, book):
    upcoming_birthdays = book.get_upcoming_birthdays()
    if upcoming_birthdays:
        return "Upcoming birthdays: " + ", ".join(upcoming_birthdays)
    return "No upcoming birthdays."

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = user_input.split()

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            name, old_phone, new_phone = args
            record = book.find(name)
            if record and record.edit_phone(old_phone, new_phone):
                print(f"Phone number for {name} changed to {new_phone}.")
            else:
                print("Failed to change phone number.")

        elif command == "phone":
            name = args[0]
            record = book.find(name)
            if record:
                print(f"Phone numbers for {name}: {', '.join(p.value for p in record.phones)}")
            else:
                print("Contact not found.")

        elif command == "all":
            if book.data:
                for name, record in book.data.items():
                    print(record)
            else:
                print("Address book is empty.")

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
