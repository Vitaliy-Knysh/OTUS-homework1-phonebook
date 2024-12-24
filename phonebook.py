import json
import random
import re
from json import JSONDecodeError


class Contact:
    PUNCTUATION_MARKS = "/|\<>!?;%:?@#$%^&*()[]{}.,"
    PHONE_NUMBER_REGEX = "[()\d+-]{11,}"

    def __init__(self, name, phone_number, comment, id=""):
        self.name = name
        self.phone_number = phone_number
        self.comment = comment
        self.id = id if id else "".join([str(random.randint(0, 9)) for _ in range(20)])
        self.validate_input()

    def validate_input(self):
        if not isinstance(self.name, str):
            raise AttributeError(f"Имя {self.name} не является строкой")
        if not isinstance(self.phone_number, str):
            raise AttributeError(f"Номер телефона {self.phone_number} не является строкой")
        if not isinstance(self.comment, str):
            raise AttributeError(f"Комментарий {self.comment} не является строкой")

        elif any(char in self.name for char in self.PUNCTUATION_MARKS):
            raise AttributeError(f"В имени {self.name} присутствует специальный символ или знак препинания. "
                                 f"Имя должно включать только буквы и пробелы.")
        if not re.match(pattern=self.PHONE_NUMBER_REGEX, string=self.phone_number):
            raise AttributeError(f"{self.phone_number} не является валидным номером телефона."
                                 f" Номер телефона должен содержать 11 цифр, допустимы символы '()-+'")


class Phonebook:
    def __init__(self):
        open("./phonebook.json", "w").close()

    @staticmethod
    def __save_phonebook(contacts: list[Contact]):
        phonebook_dict = {}
        for contact in contacts:
            phonebook_dict.update({
                contact.id: {
                    "name": contact.name,
                    "phone_number": contact.phone_number,
                    "comment": contact.comment,
                }
            })
        with open("./phonebook.json", "w") as file:
            file.write(json.dumps(phonebook_dict))

    @staticmethod
    def get_contacts() -> list[Contact]:
        with open("./phonebook.json") as file:
            try:
                phonebook_dict = json.load(file)
            except JSONDecodeError:
                return []
        contacts = []
        for contact_id, contact_content in phonebook_dict.items():
            contacts.append(
                Contact(
                    name=contact_content["name"],
                    phone_number=contact_content["phone_number"],
                    comment=contact_content["comment"],
                    id=contact_id,
                )
            )
        return contacts

    @staticmethod
    def get_single_contact_by_id(id: str) -> Contact | None:
        with open("./phonebook.json") as file:
            try:
                phonebook_dict = json.load(file)
            except JSONDecodeError:
                return None
        return Contact(
                    name=phonebook_dict[id]["name"],
                    phone_number=phonebook_dict[id]["phone_number"],
                    comment=phonebook_dict[id]["comment"],
                    id=id,
                )

    def add_contact(self, new_contact: Contact):
        contacts = self.get_contacts()
        contact_exists = False
        for contact in contacts:
            if contact.name == new_contact.name and contact.phone_number == new_contact.phone_number:
                contact_exists = True
                print("Этот контакт уже существует!")
                break
        if not contact_exists:
            contacts.append(new_contact)
        self.__save_phonebook(contacts=contacts)

    def delete_contact(self, id: str):
        contacts = self.get_contacts()
        for contact in contacts:
            if contact.id == id:
                contacts.remove(contact)
                break
        self.__save_phonebook(contacts=contacts)

    def find_contacts(self, keyword: str, fields: tuple[str, ...]) -> list[Contact]:
        contacts = self.get_contacts()
        found_contacts = []
        for contact in contacts:
            if "Имя" in fields and keyword in contact.name:
                found_contacts.append(contact)
            elif "Номер телефона" in fields and keyword in contact.phone_number:
                found_contacts.append(contact)
            elif "Комментарий" in fields and keyword in contact.comment:
                found_contacts.append(contact)
        return found_contacts
