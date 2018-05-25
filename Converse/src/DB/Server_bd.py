
from .baseDBserver import Client, ClientContacts, ClientHistory
from .settingDB import DbBaseStorage
from .errors import NoneClientError


class Storage(DbBaseStorage):
    """Хранилище на стороне сервера."""

    def add_client(self, username, info=None):
        """Добавить клиента."""
        new_client = Client(username, info)
        print(new_client)
        self.session.add(new_client)


    def client_exists(self, username):
        """Проверить наличие пользователя."""
        result = self.session.query(Client).filter(Client.name == username).count() > 0
        return result


    def get_client_by_username(self, username):
        """Получить клиента по имени."""
        client = self.session.query(Client).filter(Client.name == username).first()
        return client


    def add_history(self, username, ip):
        """Добавить историю клиента."""
        client = self.get_client_by_username(username)
        if client:
            history = ClientHistory(client_id=client.ClientId, ip=ip)
            self.session.add(history)
        else:
            raise NoneClientError(username)


    def add_contact(self, client_username, contact_username):
        """Добавить контакт в список контактов клиента."""
        contact = self.get_client_by_username(contact_username)
        if contact:
            client = self.get_client_by_username(client_username)
            if client:
                cc = ClientContacts(client_id=client.ClientId, contact_id=contact.ClientId)
                self.session.add(cc)
            else:
                raise NoneClientError(client_username)
        else:
            raise NoneClientError(contact_username)


    def del_contact(self, client_username, contact_username):
        """Удалить контакт из списка контактов клиента."""
        contact = self.get_client_by_username(contact_username)
        if contact:
            client = self.get_client_by_username(client_username)
            if client:
                cc = self.session.query(ClientContacts).filter(
                    ClientContacts.ClientId == client.ClientId).filter(
                    ClientContacts.ContactId == contact.ClientId).first()
                self.session.delete(cc)
                self.session.commit()
            else:
                raise NoneClientError(contact_username)
        else:
            raise NoneClientError(client_username)


    def get_contacts(self, client_username):
        """Получить все контакты клиента."""
        client = self.get_client_by_username(client_username)
        if client:
            contacts_clients = self.session.query(ClientContacts).filter(ClientContacts.ClientId == client.ClientId)
            result = []
            for contact_client in contacts_clients:
                contact = self.session.query(Client).filter(Client.ClientId == contact_client.ContactId).first()
                result.append(contact.name)
            return result
        else:
            raise NoneClientError(client_username)


    def get_clients(self):
        """Получить всех клиентов."""
        return self.session.query(Client).all()




















