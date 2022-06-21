from collections import UserDict
from typing import List
from datetime import datetime, timedelta
import re


# The parent class for all fields is the general logic for all fields
class Field:

    def __init__(self, value) -> None:
        self._value = None  # zaglushka
        self.value = value  # pseudonym

    @property
    def value(self):  # Getter
        return self._value

    @value.setter  # Setter
    def value(self, value):
        self._value = value


# inheritance of field

class Name(Field):
    @Field.value.setter
    def value(self, value: str):
        if not isinstance(value, str):  # check name is string
            raise ValueError("Name is not a string!")
        self._value = value


# new class, inheritance of field
class Birthday(Field):
    @Field.value.setter
    def value(self, value: str):
        try:
            self._value = datetime.strptime(value, "%Y-%m-%d").date()  # conversion str to datatime
        except ValueError:
            print("Enter HB in format 1990-10-03")


# inheritance of field
class Phone(Field):
    @Field.value.setter
    def value(self, value: str) -> None:  # check phone number
        if (len(value) == 13 or len(value) == 10 or len(value) == 12 or len(value) == 9) and (
                value.startswith("380")
                or value.startswith("+380") or value.startswith("0") or value.startswith("+0")):
            self._value = value
        else:
            raise ValueError('Phone number is incorrect!')


"""
Class that is responsible for the logic of adding / removing / editing optional fields and storing the required field Name
"""


class Record:
    # Initialization
    def __init__(self, name: Name, birthday: Birthday = None, phone=None, other_phone=None) -> None:
        self.name = name
        self.birthday = birthday
        self.other_phone = other_phone
        self.phones = []
        if phone:
            self.phones.append(phone)

    # editing phones
    def edit_phone(self, phone: Phone, other_phone: Phone):
        for p in self.phones:
            if phone.value == p.value:
                self.phones.remove(p)
            if other_phone != p.value:
                self.phones.append(other_phone)
                return f'Phone {phone.value} edited on {other_phone.value}'

    # adding phones
    def add_phone(self, phone: Phone):
        for p in self.phones:
            if phone.value == p.value:
                return f'Phone {p} in record'
            else:
                self.phones.append(phone)
                return f'Phone {phone.value} add successful'

    # removing phones
    def del_phone(self, phone: Phone):
        for p in self.phones:
            if phone.value == p.value:
                self.phones.remove(p)
                return f'Phone {phone.value} removed successful'

    # returns the number of days until the contact's next birthday, if a birthday is given.
    def days_to_birthday(self):
        day_now = datetime.now().date()
        if self.birthday.value:
            day_to_birth = self.birthday.value - day_now
            day_to_birth = day_to_birth.days
            return f' {day_to_birth} days to birthday'

    def __repr__(self) -> str:
        if self.birthday:
            return f'{self.name.value} : {[p.value for p in self.phones]}, Birthday: {self.birthday}'
        return f'{self.name.value} : {[p.value for p in self.phones]}'

    # def __repr__(self) -> str:
    #     return f'{[p.value for p in self.phones]}'


# Search logic for records of this class
class AddressBook(UserDict):

    def add_record(self, rec):  # make dict
        self.data[rec.name.value] = rec

    def iterator(self, max_count):  # make iterator
        count = 0
        for k in self.data:
            if count < max_count:
                count += 1
                yield self.data[k]
        else:
            raise StopIteration


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return """If you write command 'add' please write 'add' 'name' 'number'
If you write command 'change' please write 'change' 'name' 'number'
If you write command 'phone' please write 'phone' 'name'
If you write command 'remove' please write 'remove' 'name' 'number'"""
        except KeyError:
            return "This key not found try again"
        except TypeError:
            return "Type not supported try again"
        except ValueError:
            return "Incorrect value try again"
        except AttributeError:
            return "Incorrect attribute try again"
        except StopIteration:
            return "That's oll"
        except RuntimeError:
            return "That's oll"

    return wrapper
def input_help():
    return """help - output command, that help find command
hello - output command 'How can I help you?' 
add - add contact, use 'add' 'name' 'number'
change - change your contact, use 'change' 'name' 'number'
phone - use 'phone' 'name' that see number this contact
show all - show all your contacts
"""


@input_error
def input_bye(*args):
    return "Good bye"


@input_error
def input_hello(*args):
    return "How can I help you?"


ab = AddressBook()


@input_error
def input_add(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    other_phone = Phone(args[2])
    try:
        birthday = Birthday(args[2])
    except IndexError:
        birthday = None
    rec = Record(name=name, phone=[phone], other_phone= =[phone], birthday=birthday) #error
    ab.add_record(rec)
    return f"Contact {rec.name.value.title()} add in system successful"


@input_error
def input_change(*args):
    phone = Phone(args[1])
    new_phone = Phone(args[2])
    rec = ab.data[args[0]]
    result = rec.change_phone(phone, new_phone)
    if result:
        return f"Contact {rec.name.value.title()} change successful"


@input_error
def input_phone(*args):
    return ab.get(args[0])


@input_error
def input_show(*args):
    return "\n".join([f"{v} " for v in ab.values()])


@input_error
def input_remove(*args):
    phone = Phone(args[1])
    rec = ab.data[args[0]]
    result = rec.remove_record(phone)
    if result:
        return f"Phone {phone.value} delete successful"


@input_error
def input_day_to_hb(*args):
    rec = ab[args[0]]
    result = (repr(rec))
    result1 = re.search(r"\d{4}-\d{2}-\d{2}", result)
    birt = Birthday(result1.group())
    rec_func = rec.days_to_birthday(birt)
    return rec_func


@input_error
def input_show_n(*args):
    for i in ab.iterator(int(args[0])):
        print(i)


commands = {
    input_hello: "hello",
    input_add: "add",
    input_phone: "phone",
    input_show: "show all",
    input_change: "change",
    input_bye: "good bye",
    input_help: "help",
    input_remove: "remove",
    input_day_to_hb: "birthday",
    input_show_n: "display"
}


def command_parser(user_input1):
    data = []
    command = ""
    for k, v in commands.items():
        if user_input1.startswith(v):
            command = k
            data = user_input1.replace(v, "").split()
        if user_input1 == "":
            main()
    return command, data


@input_error
def main():
    while True:
        user_input = input(">>>")
        user_input1 = user_input.lower()
        command, data = command_parser(user_input1)
        if command == "display":
            command(*data)
        else:
            print(command(*data))
        if command == input_bye:
            break


if __name__ == "__main__":
    main()

if __name__ == '__main__':
    # fulling class
    name_new = Name("Bob")
    # print(name_new.value)
    name_new1 = Name("Anastasiia")
    name_new2 = Name("Vova")
    name_new3 = Name("Mirra")

    # phone_first = Phone("+380678996765")
    # print(phone_first.value)

    try:
        phone_first = Phone("+380678996765")
    except ValueError as e:
        print(e)
        phone_first = None

    try:
        phone_first1 = Phone("+380677654321")
    except ValueError as e:
        print(e)
        phone_first = None

    try:
        phone_first2 = Phone("+380678991111")
    except ValueError as e:
        print(e)
        phone_first2 = None

    try:
        phone_first3 = Phone("+380678922222")
    except ValueError as e:
        print(e)
        phone_first3 = None

    new_birthday = Birthday("2011-09-05")
    # print(new_birthday.value)

    rec = Record(name_new, phone_first)
    rec1 = Record(name_new1, phone_first1)
    # print(rec)
    rec2 = Record(name_new2, phone_first2)
    rec3 = Record(name_new3, phone_first3)

    # phone_second = Phone("+380678996765")
    # print(phone_second.value)

    try:
        phone_second = Phone("+380965035661")
    except ValueError as e:
        print(e)
        phone_second = None

    rec.add_phone(phone_second)
    # rec.del_phone(phone_first)
    # rec.edit_phone(phone_first, phone_second)

    ab = AddressBook()
    ab.add_record(rec)
    ab.add_record(rec1)
    # print(ab)

    ab.add_record(rec2)
    ab.add_record(rec3)


    it = ab.iterator(2)
    for i in it:
        print(i)



