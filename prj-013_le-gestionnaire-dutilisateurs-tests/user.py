"""
User class. Can store email, first and last name, phone number and address.
"""
import string


class User:
    def __init__(self, email: str, first_name: str, last_name: str = "", phone_number: str = "", address: str = ""):
        # -----CREATE EMAIL ADDRESS----- #
        self.email = email.lower()
        self.check_email(self.email)

        # -----CREATE NAMES----- #
        self.first_name = first_name.title().strip()
        self.check_first_name(first_name)

        self.last_name = last_name.title().strip()
        if self.last_name:
            self.check_last_name(self.last_name)

        # -----CREATE PHONE NUMBER----- #
        self.phone_number = phone_number
        if self.phone_number:
            self.check_phone_number(self.phone_number)

        # -----CREATE ADDRESS----- #
        self.address = address.strip()
        if self.address:
            self.address = self.check_and_reformat_address(self.address)

    def __str__(self):
        return (f"Email: {self.email}"
                f"\nFirst name: {self.first_name}"
                f"{f"\nLast name: {self.last_name}" if self.last_name else ""}"
                f"{f"\nPhone number: {self.phone_number}" if self.phone_number else ""}"
                f"{f"\nAddress: {self.address}" if self.address else ""}")

    def to_dict(self):
        dict_user = {
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "address": self.address
        }
        return dict_user

    # -----CHECKS----- #
    @staticmethod
    def check_email(email: str):
        # -----check '@' count----- #
        at_count = [letter for letter in email if letter == "@"]
        if len(at_count) < 1 or len(at_count) > 1:
            raise ValueError("Email must contain exactly 1 '@'")

        # -----check dot count after '@'----- #
        index = -1
        domain_chars = []
        while email[index] != '@':
            domain_chars.append(email[index])
            index -= 1

        dot_count = [char for char in domain_chars if char == "."]
        if len(dot_count) < 1:
            raise ValueError("Email domain name must have at least 1 dot (.)")

        # -----check for prohibited characters ----- #
        for char in email:
            if char not in string.ascii_letters + string.digits + ".@_+-":
                raise ValueError(
                    "Email must only contain letters, digits, dots (.), underscores (_), hyphens (-), plus (+) and an at (@)")

        # -----check if email starts/ends with valid character----- #
        if email.startswith(("@", ".", "-", "_")) or email.endswith(("@", ".")):
            raise ValueError("Email cannot start with a special character.")

        # -----check if TLD length > 1----- #
        index = -1
        tld_content = []
        while email[index] != '.':
            tld_content.append(email[index])
            index -= 1

        if len(tld_content) <= 1:
            raise ValueError("Top level domain must have 2 or more characters")

        # -----check if username length <=64----- #
        index = 0
        while email[index] != "@":
            index += 1

        if index + 1 > 64:
            raise ValueError("Username (part before the at (@)) must be 64 characters long or less.")

        # -----check if domain length <= 255----- #
        index = -1
        while email[index] != '@':
            index -= 1

        if index * -1 > 255:
            raise ValueError("Domain (part after the at (@)) must be 255 characters long or less")

    @staticmethod
    def check_first_name(first_name: str):
        # check length
        if not 2 <= len(first_name) <= 40:
            raise ValueError("First name length must be between 2-40 characters")

        # check prohibited characters
        allowed_characters = string.ascii_letters + " -'"
        for char in first_name:
            if char not in allowed_characters:
                raise ValueError("First name must only contain letters, hyphens (-), spaces and apostrophes (').")

    @staticmethod
    def check_last_name(last_name: str):
        # check length
        if not 2 <= len(last_name) <= 40:
            raise ValueError("Last name length must be between 2-40 characters")

        # check prohibited characters
        allowed_characters = string.ascii_letters + " -'"
        for char in last_name:
            if char not in allowed_characters:
                raise ValueError("Last name must only contain letters, hyphens (-), spaces and apostrophes (').")

    @staticmethod
    def check_phone_number(phone_number: str):
        if not phone_number.isdigit():
            raise ValueError("Phone number must only contain numbers")

        if len(phone_number) != 10:
            raise ValueError("Phone number must contain 10 digits.")

    @staticmethod
    def check_and_reformat_address(address: str) -> str:
        # check length
        if not 10 <= len(address) <= 100:
            raise ValueError("Address must only contain 10 - 100 characters")

        # check for prohibited characters
        allowed_characters = string.ascii_letters + string.digits + " .,-"
        for char in address:
            if char not in allowed_characters:
                raise ValueError(
                    "Address must only contain letters, spaces, numbers, hyphens (-), periods (.) and commas (,)")

        # check for double special characters (-,. )
        new_address_list = list(address)

        for index, char in enumerate(address):
            if index < len(address) - 1:  # if not the last character
                if char == address[index + 1] and char not in string.ascii_letters + string.digits:
                    new_address_list.remove(char)
        return "".join(new_address_list)