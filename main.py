from __future__ import annotations
from enum import Enum

CURRENT_YEAR = 2026

all_people = {} #fullname : Person pairs. fullname = person._name + ' ' + person._surname
class Gender(Enum):
    MALE = "M"
    FEMALE = "F"
class Person:
    def __init__(self, gender:Gender, name:str, surname:str, birth:int, death=(-1), father:Person=None, mother:Person=None):
        if (father is None and mother is not None) or (father is not None and mother is None):
            print('Error: You must initialize either both parents (for a regular entry) or neither of them (for root entries).')
            return
        self._gender = gender
        self._name = name
        self._surname = surname
        self._father = father
        self._mother = mother
        self._birth = birth
        self._death = death
        self._married_to = None
        self._children = {}
        full_name = name + ' ' + surname
        if full_name not in all_people:
            all_people[full_name] = self
            print(full_name, ' added.')
        else:
            return
        if father is None:
            self._level = 0
        else:
            self._level = max(father.level, mother.level) + 1
            father.children[full_name] = self
            mother.children[full_name] = self

    def set_marriage(self, spouse:Person):
        if is_valid_marriage(self, spouse):
            self._married_to = spouse
            spouse._married_to = self
    def add_child(self, child:Person):
        child_fullname = child._name + ' ' + child._surname
        if child_fullname not in self._children:
            self._children[child_fullname] = child
        else:
            print('Child with fullname ', child_fullname, ' already exists') # this line should never run according to the assumptions
    def update_person(self, birth=None, death=None):
        if birth is not None: self._birth = birth
        if death is not None: self._death = death
    def dump_person_info(self):
        print(f'Name and Surname: {self._name} {self._surname}')
        if self._death != -1:
            print('Age: ', (CURRENT_YEAR - self._birth))
        else:
            print('Age of Death: ', (self._death - self._birth))
        print(f'Level: {self._level}')
        print('Total Children: ', len(self._children))
        if self._death == -1:
            print('Status: Alive')
        else:
            print('Status: Died')
    @property
    def gender(self):
        return self._gender

    @property
    def name(self):
        return self._name

    @property
    def surname(self):
        return self._surname

    @property
    def father(self):
        return self._father

    @property
    def mother(self):
        return self._mother

    @property
    def birth(self):
        return self._birth

    @property
    def death(self):
        return self._death

    @property
    def married_to(self) -> Person:
        return self._married_to

    @property
    def children(self):
        return self._children

    @property
    def level(self):
        return self._level

def is_valid_marriage(spouse1:Person, spouse2:Person) -> bool:
    return True

def _get_name_surname_input() -> (str, str):
    while True:
        full_name = input("Enter Name and Surname: ")
        parts = full_name.strip().split()
        if len(parts) >= 2:
            break  # guaranteed name-surname
        print('Please enter name and surname.')
    return " ".join(parts[:-1]), parts[-1]

def _get_birth_year_input() -> int:
    while True:
        try:
            birth = int(input("Enter Birthdate: "))
            break
        except ValueError:
            print('Please enter an Integer value as the birth year. e.g. 1881')
    return birth
def _get_death_year_input() -> int:
    while True:
        death = input("Enter Death date ('none' if alive): ")
        if death == 'none':
            return -1
        try:
            death = int(death)
            break
        except ValueError:
            print('Please enter an Integer value as the death year. e.g. 1950')
    return death
def _get_gender_input() -> Gender:
    while True:
        gender_input = input('Enter gender (m/f): ')
        if gender_input == 'm':
            return Gender.MALE
        elif gender_input == 'f':
            return Gender.FEMALE
        print('Please enter (m)ale or (f)emale')


def _add_root_marriage():
    root = []
    for i in range(2):
        if i == 0:
            print('--- Father ---')
            gender = Gender.MALE
        else:
            print('--- Mother ---')
            gender = Gender.FEMALE
        name, surname = _get_name_surname_input()
        full_name = name + ' ' + surname
        birth = _get_birth_year_input()
        if full_name in all_people: #so root mother and root father cannot have the same names
            all_people.clear()
            print('Father and mother cannot have the same names.')
            return
        root_father_or_mother = Person(gender, name, surname, birth)
        root.append(root_father_or_mother)
        print('')
    if is_valid_marriage(root[0], root[1]):
        print(f"success: {root[0].name} {root[0].surname} and {root[1].name} {root[1].surname} married.")
        root[0].set_marriage(root[1])
def print_menu() -> int:
    print("=" * 58)
    print("1-) Ask relation        | 2-) Add/Update person")
    print("3-) Get info of person  | 4-) Print the family tree")
    print("5-) Add marriage        | 6-) Terminate program")
    print("=" * 58)

    while True:
        choice = input("Please choose an operation: ")

        if not choice.isdigit():
            print("Invalid input! Please enter a number.")
            continue

        choice = int(choice)

        if 1 <= choice <= 6:
            print('')
            return choice

        print("Invalid operation! Choose between 1 and 6.")
    return -1 #never happens

def add_person():
    father:Person
    mother:Person
    if len(all_people) == 0:
        print('')
        print('Empty Family tree. Adding root members')
        print('')
        _add_root_marriage()
        return
    print('--- Adding a new family member ---')
    father_name = input('Please type the father name and surname: ')
    mother_name = input('Please type the mother name and surname: ')
    if father_name not in all_people or mother_name not in all_people:
        print('Parent(s) not found')
        return
    father = all_people[father_name]
    mother = all_people[mother_name]
    if father.married_to is not mother:
        print(f'{father_name} and {mother_name} are not married!')
        return

    new_child_name, new_child_surname = _get_name_surname_input()
    birth = _get_birth_year_input()

    if birth < father.birth or birth < mother.birth:
        print('Child cannot be born before either of his/her parents')
        return

    if father.death != -1 and birth > father.death:
        print(f'Error: Father ({father.name} {father.surname}) died before the birth of the child.')
        return

    if mother.death != -1 and birth > mother.death:
        print(f'Error: Mother ({mother.name} {mother.surname}) died before the birth of the child.')
        return
    death = _get_death_year_input()
    gender = _get_gender_input()
    Person(gender, new_child_name, new_child_surname, birth, death, father, mother)

def find_relation():
    pass


def get_person_info():
    name, surname = _get_name_surname_input()
    key = name + ' ' + surname
    person:Person
    if key not in all_people:
        print('Person ', key, ' is not found')
    else:
        person = all_people[key]
        person.dump_person_info()


def print_family_tree():
    if not all_people:
        print("Empty Family Tree.")
        return

    visited = set()
    lvl = 0
    while len(visited) < len(all_people):
        output_lines = []

        for full_name, person in all_people.items():
            if person not in visited:
                if person.married_to is not None:
                    couple_level = max(person.level, person.married_to.level)
                    if couple_level == lvl:
                        output_lines.append(
                            f"{person.name} {person.surname}-{person.married_to.name} {person.married_to.surname}")
                        visited.add(person)
                        visited.add(person.married_to)
                else:
                    if person.level == lvl:
                        output_lines.append(f"{person.name} {person.surname}")
                        visited.add(person)

        if output_lines:
            print(f"---LEVEL {lvl}---")
            for line in output_lines:
                print(line)
        lvl += 1


def add_marriage():
    pass


if __name__ == '__main__':
    flag = True
    while flag:
        op = print_menu()
        match op:
            case 1:
                find_relation()
            case 2:
                add_person()
            case 3:
                get_person_info()
            case 4:
                print_family_tree()
            case 5:
                add_marriage()
            case 6:
                flag = False
            case _:
                print("Invalid operation! Choose between 1 and 6.")


    print('Terminating!')






