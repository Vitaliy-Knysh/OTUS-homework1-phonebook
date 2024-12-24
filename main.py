from phonebook import Phonebook, Contact
from display import Display


def starter_page():
    display.make_table(contacts=phonebook.get_contacts())
    display.display_table()


def search_contacts(return_result=False) -> tuple[list[Contact], str] | None:
    search_fields = display.search_fields_form()
    if not search_fields or "Назад" in search_fields:
        print("Не выбрана ни одна категория для поиска.")
        return None
    keyword = input("Введите любой текст для поиска: ")
    found_contacts = phonebook.find_contacts(keyword=keyword, fields=search_fields)
    if found_contacts:
        display.make_table(contacts=found_contacts)
        display.display_table(pre_text=f"Поиск по ключевому слову {keyword}:", show_main_menu=False)
        if return_result:
            return found_contacts, keyword
        else:
            display.return_to_main_page_form()
    else:
        print(f"Поиск по ключевому слову {keyword} не дал результатов.")
        search_again = display.search_again_form()
        if search_again:
            search_contacts()


def add_contact():
    new_contact = display.add_contact_form()
    if new_contact:
        phonebook.add_contact(new_contact)


def delete_contact():
    contacts = phonebook.get_contacts()
    contact_id_to_delete = display.choose_contact_form(contacts=contacts)
    phonebook.delete_contact(contact_id_to_delete)


def change_contact():
    found_contacts, _ = search_contacts(return_result=True)
    contact_to_change_id = display.choose_contact_form(found_contacts)
    old_contact = phonebook.get_single_contact_by_id(contact_to_change_id)
    print("Введите изменённые данные для контакта:")
    new_contact = display.add_contact_form()
    if not new_contact:
        return None
    display.make_contact_compare_table(contacts=[old_contact, new_contact])
    display.display_table(pre_text="Вы уверены, что хотите изменить контакт?", show_main_menu=False)
    confirm_contact_change = display.yes_or_no_form()
    if confirm_contact_change:
        phonebook.delete_contact(contact_to_change_id)
        phonebook.add_contact(new_contact)


def fill_phonebook_with_test_data(pb: Phonebook):
    pb.add_contact(new_contact=Contact(name="name1", phone_number="11111111111", comment="comment1"))
    pb.add_contact(new_contact=Contact(name="name2", phone_number="+2(222)222-22-22", comment="comment2"))
    pb.add_contact(new_contact=Contact(name="name3", phone_number="3-333-333-33-33", comment="comment3"))


if __name__ == "__main__":
    phonebook = Phonebook()
    fill_phonebook_with_test_data(pb=phonebook)
    display = Display()
    starter_page()
    while True:
        if display.main_menu.chosen_menu_entry == "Добавить контакт":
            add_contact()
        elif display.main_menu.chosen_menu_entry == "Удалить контакт":
            delete_contact()
        elif display.main_menu.chosen_menu_entry == "Изменить контакт":
            change_contact()
        elif display.main_menu.chosen_menu_entry == "Поиск":
            search_contacts(return_result=False)
        elif display.main_menu.chosen_menu_entry == "Выйти":
            raise SystemExit
        starter_page()
