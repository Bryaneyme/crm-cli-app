import pytest
import tinydb

import database
from user import User

database.db = tinydb.TinyDB(storage=tinydb.storages.MemoryStorage)


@pytest.fixture
def user():
    return User("example@gmail.com", "John", "Doe", "0123456789", "123 main street")


class TestCreateUser:

    def test_document_added_to_db(self, user):
        database.db.truncate()

        database.create_user(user)
        assert {"email": "example@gmail.com",
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "0123456789",
                "address": "123 main street"
                } in database.db.all()

    def test_no_duplicates_in_db(self, user):
        database.db.truncate()

        database.create_user(user)
        with pytest.raises(ValueError):
            database.create_user(user)


class TestReadUsers:
    def test_read_function(self, user):
        database.db.truncate()
        user_1 = user
        user_2 = User("joseph.lighthead@gmail.com", "Joseph", "Lighthead")
        database.create_user(user_1)
        database.create_user(user_2)

        assert database.read_users() == [user_1.to_dict(), user_2.to_dict()]


class TestUpdateUsers:
    def test_user_not_exists(self, user):
        database.db.truncate()

        # doesnt exist
        database.create_user(user)

        with pytest.raises(ValueError):
            database.update_user("nonexistantemail@gmail.com", {"first_name": "John changed"})

    def test_user_exists(self, user):
        database.db.truncate()

        database.create_user(user)
        # exists
        database.update_user(user.email,
                             {"email": "example@gmail.com", "first_name": "John peTer", "last_name": "sUntHon",
                              "phone_number": "0192837465", "address": "321 main street"})

        assert {
                   "email": "example@gmail.com",
                   "first_name": "John Peter",
                   "last_name": "Sunthon",
                   "phone_number": "0192837465",
                   "address": "321 main street"
               } in database.db.all()

    def test_key_not_exists(self, user):
        database.db.truncate()

        database.create_user(user)

        with pytest.raises(ValueError):
            database.update_user("example@gmail.com", {"non_existant_key": "fail"})


class TestDeleteUser:

    def test_document_deleted_from_db(self, user):
        database.db.truncate()

        user_wo_address = User("example@gmail.com", "John", "Doe", "0123456789")
        database.create_user(user_wo_address)
        assert {"email": "example@gmail.com",
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "0123456789",
                "address": ""
                } in database.db.all()

        database.delete_user(email="example@gmail.com")

        assert {"email": "example@gmail.com",
                "first_name": "John",
                "last_name": "Doe",
                "phone_number": "0123456789",
                "address": ""
                } not in database.db.all()

    def test_document_exists_in_db(self, user):
        with pytest.raises(ValueError):
            database.delete_user("example@gmail.com")
