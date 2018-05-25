"""Хранилище на стороне клиента."""

from .baseDBclient import Contact, Message
from .settingDB import DbBaseStorage
from .errors import NoneContactError


class Storage(DbBaseStorage):
    """Клиентское хранилище"""

    def add_contact(self, username):
        """Добавить контакт по имени"""
        new_item = Contact(username)
        self.session.add(new_item)

    def get_contact_by_username(self, username):
        """Получить контакт по имени"""
        contact = self.session.query(Contact).filter(Contact.Name == username).first()
        return contact

    def del_contact(self, username):
        """Удалить контакт по имени"""
        contact = self.get_contact_by_username(username)
        self.session.delete(contact)

    def get_contacts(self):
        """Получить всех контакты."""
        contacts = self.session.query(Contact)
        return contacts

    def add_message(self, username, text):
        """Добавить сообщения."""
        contact = self.get_contact_by_username(username)
        print(contact)
        if contact:
            new_item = Message(text=text, contact_id=contact.ContactId)
            self.session.add(new_item)
        else:
            raise NoneContactError(username)

    def clear_contacts(self):
        """Удалить всех контакты."""
        self.session.query(Contact).delete()

