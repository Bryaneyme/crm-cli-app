import pytest

from user import User


class TestEmailAddress:
    def test_contains_1_at(self):
        with pytest.raises(ValueError):
            User("examplegmail.com", "Joseph")

        with pytest.raises(ValueError):
            User("example@@gmail.com", "Joseph")

    def test_contains_min_1_dot_after_at(self):
        with pytest.raises(ValueError):
            User("example@gmailcom", "Joseph")

    def test_contains_only_allowed_characters(self):
        with pytest.raises(ValueError):
            User(email="!#$%())example@gmail.com[]{}|;./`~<>?", first_name="Joseph")

        assert User(email="exam-ple@gmail.com", first_name="Joseph").email == "exam-ple@gmail.com"

    def test_start_with_allowed_character(self):
        with pytest.raises(ValueError):
            User(".example@gmail.com", "Joseph")

        with pytest.raises(ValueError):
            User("example@gmail.com@", "Joseph")

    def test_domain_extension_min_2_chars_long(self):
        with pytest.raises(ValueError):
            User("example@gmail.c", "Joseph")

    def test_username_length(self):
        with pytest.raises(ValueError):
            User("qwertyuiopasdfghjklzxcvbnmqwertyuiopasdfghjklzxcvbnmqwertyuiopas@gmail.com", "Joseph")

    def test_email_length(self):
        with pytest.raises(ValueError):
            User(
                "exampleeee@ppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppppp.com",
                "Joseph")

    def test_converted_to_lowercase(self):
        assert User("eXAmPle@gmail.com", "Joseph").email == "example@gmail.com"


class TestName:
    def test_first_name_length(self):
        with pytest.raises(ValueError):
            assert User("example@gmail.com", "", "Campbell")

        with pytest.raises(ValueError):
            assert User("example@gmail.com", "qwertyuiopasdfghjklzxcvbnmqwertyuiopasdfghjklzxcvbnm", "Campbell")

    def test_first_name_titled(self):
        assert User("example@gmail.com", "james", "campbell").first_name.istitle()

    def test_first_name_stripped(self):
        assert User("example@gmail.com", "    James          ", "Campbell").first_name == "James"

    def test_first_name_prohibited_characters(self):
        with pytest.raises(ValueError):
            User("example@gmail.com", "!@#$%())12345James67890[]{}|;./`~<>?", "Campbell")

    def test_last_name_length(self):
        with pytest.raises(ValueError):
            assert User("example@gmail.com", "James", "p")

        with pytest.raises(ValueError):
            assert User("example@gmail.com", "James", "qwertyuiopasdfghjklzxcvbnmqwertyuiopasdfghjklzxcvbnm")

    def test_last_name_titled(self):
        user = User("example@gmail.com", "james richard", "campbell")
        assert user.last_name.istitle()

    def test_last_name_stripped(self):
        assert User("example@gmail.com", "James", "       Campbell        ").last_name == "Campbell"

    def test_last_name_prohibited_characters(self):
        with pytest.raises(ValueError):
            User("example@gmail.com", "James", "!@#$%())12345James67890[]{}|;./`~<>?")

    # def test_full_name_no_double_special_characters(self):
    #     assert User("example@gmail.com", "James   Richard O''''Connor  ",
    #                 " Jean-----Claude  ").full_name == "James Richard O'Connor Jean-Claude"


class TestPhone:
    def test_only_digits(self):
        with pytest.raises(ValueError):
            User("example@gmail.com", "James", "Campbell", "012p4son56")

    def test_length(self):
        with pytest.raises(ValueError):
            User("example@gmail.com", "James", "Campbell", "1234567893245678987654")

        with pytest.raises(ValueError):
            User("example@gmail.com", "James", "Campbell", "1234")


class TestAddress:
    def test_length(self):
        with pytest.raises(ValueError):
            assert User("example@gmail.com", "James", "Campbell", "1234567890", "123 main")

        with pytest.raises(ValueError):
            assert User("example@gmail.com", "James", "Campbell", "1234567890",
                        "123 main street234567890-0987654 sdjhasvdjahsvdjahsvdasjhdvdjhavdhjavdasjhdvajda  djhasgdjd khkusahdjhasjdah")

    def test_stripped(self):
        assert User("example@gmail.com", "James", "Campbell", "1234567890",
                    "  123 main street    ").address == "123 main street"

    def test_prohibited_characters(self):
        with pytest.raises(ValueError):
            User("example@gmail.com", "James", "Campbell", "1234567890",
                 "!@#$%())12345James67890[]{}|;./`~<>? street")

    def test_double_special_characters(self):
        assert User(
            "example@gmail.com",
            "James",
            "Campbell",
            "1234567890",
            "1223   main-Street... of O,,,Connor"
        ).address == "1223 main-Street. of O,Connor"


def test_str():
    assert User("example@gmail.com", "Joseph").__str__() == ("Email: example@gmail.com"
                f"\nFirst name: Joseph")



def test_to_dict():
    u = User("example@gmail.com", "John", "Doe")
    assert u.to_dict() == {"email": "example@gmail.com", "first_name": "John", "last_name": "Doe",
                               "phone_number": "", "address": ""}

    u.phone_number = "0123456789"
    assert u.to_dict() == {"email": "example@gmail.com", "first_name": "John", "last_name": "Doe",
                           "phone_number": "0123456789", "address": ""}

    u.address = "123 main street"
    assert u.to_dict() == {"email": "example@gmail.com", "first_name": "John", "last_name": "Doe",
                               "phone_number": "0123456789",
                               "address": "123 main street"}

