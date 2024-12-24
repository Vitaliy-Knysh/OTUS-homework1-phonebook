from prettytable import PrettyTable
from simple_term_menu import TerminalMenu

from phonebook import Contact
import os


class Display:
    def __init__(self):
        self.table = PrettyTable()
        self.main_menu = TerminalMenu(["Добавить контакт", "Удалить контакт", "Изменить контакт", "Поиск", "Выйти"])

    def make_table(self, contacts: list[Contact]):
        self.table.clear()
        self.table.field_names = ["Имя", "Номер телефона", "Комментарий"]
        self.table.add_rows([
            [contact.name, contact.phone_number, contact.comment] for contact in contacts
        ])

    def make_contact_compare_table(self, contacts: list[Contact, Contact]):
        self.table.clear()
        self.table.field_names = [" ", "Имя", "Номер телефона", "Комментарий"]
        self.table.add_rows([["Старый контакт", contacts[0].name, contacts[0].phone_number, contacts[0].comment],
                             ["Новый контакт", contacts[1].name, contacts[1].phone_number, contacts[1].comment]])

    def display_table(self, pre_text=None, show_main_menu=True):
        os.system("cls||clear")
        if pre_text:
            print(pre_text)
        print(f"{self.table}")
        if show_main_menu:
            self.main_menu.show()

    @staticmethod
    def add_contact_form() -> Contact | None:
        name = input("Введите имя: ")
        phone = input("Введите номер телефона: ")
        comment = input("Введите комментарий (не обязательно): ")
        try:
            new_contact = Contact(name=name, phone_number=phone, comment=comment)
            return new_contact
        except AttributeError as e:
            menu = TerminalMenu(title=str(e),
                                menu_entries=["Ввести контакт заново", "Назад к телефонной книге"])
            menu.show()
            if menu.chosen_menu_entry == "Ввести контакт заново":
                Display.add_contact_form()
            else:
                return None

    @staticmethod
    def choose_contact_form(contacts: list[Contact]) -> str:
        options = [f"Имя: {contact.name}, Номер: {contact.phone_number}, Комментарий: {contact.comment}"
                   for contact in contacts]
        delete_contact_menu = TerminalMenu(options)
        delete_contact_menu.show()
        contact_id_to_delete = contacts[delete_contact_menu.chosen_menu_index].id
        return contact_id_to_delete

    @staticmethod
    def search_again_form() -> bool:
        menu = TerminalMenu(title="Искать ещё раз?",
                            menu_entries=["Поиск", "Вернуться на главную"])
        menu.show()
        return True if menu.chosen_menu_entry == "Поиск" else False

    @staticmethod
    def yes_or_no_form() -> bool:
        menu = TerminalMenu(["Да", "Нет"])
        menu.show()
        return True if menu.chosen_menu_entry == "Да" else False

    @staticmethod
    def search_fields_form() -> tuple[str, ...] | None:
        menu = TerminalMenu(title="По каким категориям вести поиск?"
                                  " Если нужно, выберите несколько при помощи клавиши 'Пробел'.",
                            menu_entries=["Имя", "Номер телефона", "Комментарий", "Назад"],
                            multi_select=True)
        menu.show()
        return menu.chosen_menu_entries

    @staticmethod
    def return_to_main_page_form():
        menu = TerminalMenu(menu_entries=["Вернуться на главную страницу"])
        menu.show()
