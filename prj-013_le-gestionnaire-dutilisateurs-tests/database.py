"""
DB management happens here.
"""

import tinydb

from user import User

db = tinydb.TinyDB("db.json", indent=4)


def create_user(user: User):
    _check_user_duplicate(user)
    db.insert(user.to_dict())


def read_users():
    user_documents = db.all()
    return [document for document in user_documents]


def update_user(email: str, data_to_change: dict):
    doc = db.get(tinydb.where("email") == email)
    if not doc:
        raise ValueError("No user associated to this email.")
    doc_id = doc.doc_id

    # check the data to change
    keys = data_to_change.keys()

    if "email" in keys:
        data_to_change["email"] = data_to_change["email"].lower()
        User.check_email(data_to_change["email"])

    if "first_name" in keys:
        data_to_change["first_name"] = data_to_change["first_name"].title().strip()
        User.check_first_name(data_to_change["first_name"])

    if "last_name" in keys:
        data_to_change["last_name"] = data_to_change["last_name"].title().strip()
        User.check_last_name(data_to_change["last_name"])

    if "phone_number" in keys:
        User.check_phone_number(data_to_change["phone_number"])

    if "address" in keys:
        data_to_change["address"] = data_to_change["address"].strip()
        data_to_change["address"] = User.check_and_reformat_address(data_to_change["address"])

    for key in keys:
        if key not in ["email", "first_name", "last_name", "phone_number", "address"]:
            raise ValueError("The key does not exist for this user.")

    # update data in db
    db.update(fields=data_to_change, doc_ids=[doc_id])


def delete_user(email: str):
    _check_user_exists(email)
    document = db.get(tinydb.where("email") == email)

    db.remove(doc_ids=[document.doc_id])


# -----CHECKS----- #

def _check_user_duplicate(user: User):
    if db.search(tinydb.where("email") == user.email):
        raise ValueError("User associated to this email already exists in database")


def _check_user_exists(email: str):
    if not db.search(tinydb.where("email") == email):
        raise ValueError("User associated to this email does not exist in database")
