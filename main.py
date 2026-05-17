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

    @property
    def siblings(self):
        if self.mother is None:
            return {}
        # exclude self
        return {
            fullname: child
            for fullname, child in self.mother.children.items()
            if child is not self
        }


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

# For the following kinship functions, the kinship relations are calculated from the person1's perspective
# e.g. _is_uncle(person1, person2) returns true if person2 is person1's uncle
# e.g. _is_child(person1, person2) returns true if person1 is person2's mother or father
# e.g. _is_mother(person1, person2) returns true if person2 is person1's mother
# e.g. _is_big_brother(person1, person2) returns true if person2 is person1's brother and person2 is older
def _is_mother(person1:Person, person2:Person) -> bool:
    if person1 is None or person2 is None: return False
    return person1.mother is person2

def _is_father(person1:Person, person2:Person) -> bool:
    if person1 is None or person2 is None: return False
    return person1.father is person2

def _is_child(person1:Person, person2:Person) -> bool:
    if person1 is None or person2 is None: return False
    children = person1.children
    if children is None: return False
    key = person2.name + ' ' + person2.surname
    return key in children

def _is_son(person1:Person, person2:Person) -> bool:
    if person1 is None or person2 is None or person2.gender is not Gender.MALE: return False
    return _is_child(person1, person2)

def _is_daughter(person1:Person, person2:Person) -> bool:
    if person1 is None or person2 is None or person2.gender is not Gender.FEMALE: return False
    return _is_child(person1, person2)

def _is_sibling(person1:Person, person2:Person) -> bool:
    if person1 is None or person2 is None: return False
    mother = person1.mother
    if mother is None: return False
    return _is_child(mother, person2)

def _is_brother(person1:Person, person2:Person) -> bool:
    if person1 is None or person2 is None or person2.gender is not Gender.MALE: return False
    return _is_sibling(person1, person2)

def _is_sister(person1:Person, person2:Person) -> bool:
    if person1 is None or person2 is None or person2.gender is not Gender.FEMALE: return False
    return _is_sibling(person1, person2)

def _is_big_brother(person1:Person, person2:Person) -> bool:
    if not _is_brother(person1, person2): return False
    return person2.birth < person1.birth

def _is_little_brother(person1:Person, person2:Person) -> bool:
    if not _is_brother(person1, person2): return False
    return person2.birth > person1.birth

def _is_big_sister(person1:Person, person2:Person) -> bool:
    if not _is_sister(person1, person2): return False
    return person2.birth < person1.birth

def _is_little_sister(person1:Person, person2:Person) -> bool:
    if not _is_sister(person1, person2): return False
    return person2.birth > person1.birth

def _is_grandmother(person1:Person, person2:Person) -> bool:
    if person1 is None or person2 is None: return False
    mother = person1.mother
    if mother is not None:
        grandmother = mother.mother
        if grandmother is not None and person2 is grandmother:
            return True
    father = person1.father
    if father is not None:
        grandmother = father.mother
        if grandmother is not None and person2 is grandmother:
            return True
    return False

def _is_grandfather(person1:Person, person2:Person) -> bool:
    if person1 is None or person2 is None: return False
    mother = person1.mother
    if mother is not None:
        grandfather = mother.father
        if grandfather is not None and person2 is grandfather:
            return True
    father = person1.father
    if father is not None:
        grandfather = father.father
        if grandfather is not None and person2 is grandfather:
            return True
    return False

def _is_grandchild(person1:Person, person2:Person) -> bool:
    return _is_grandmother(person2, person1) or _is_grandfather(person2, person1)

def _is_uncle_father(person1:Person, person2:Person) -> bool:
    # AMCA
    if person1 is None or person2 is None or person2.gender is not Gender.MALE: return False
    father = person1.father
    if father is None: return False
    fathers_siblings = father.siblings
    uncle_key = person2.name + ' ' + person2.surname
    return uncle_key in fathers_siblings

def _is_uncle_mother(person1:Person, person2:Person) -> bool:
    # DAYI
    if person1 is None or person2 is None or person2.gender is not Gender.MALE: return False
    mother = person1.mother
    if mother is None: return False
    mothers_siblings = mother.siblings
    uncle_key = person2.name + ' ' + person2.surname
    return uncle_key in mothers_siblings

def _is_aunt_father(person1:Person, person2:Person) -> bool:
    # HALA
    if person1 is None or person2 is None or person2.gender is not Gender.FEMALE: return False
    father = person1.father
    if father is None: return False
    fathers_siblings = father.siblings
    aunt_key = person2.name + ' ' + person2.surname
    return aunt_key in fathers_siblings

def _is_aunt_mother(person1:Person, person2:Person) -> bool:
    # TEYZE
    if person1 is None or person2 is None or person2.gender is not Gender.FEMALE: return False
    mother = person1.mother
    if mother is None: return False
    mothers_siblings = mother.siblings
    aunt_key = person2.name + ' ' + person2.surname
    return aunt_key in mothers_siblings

def _is_nephew_or_niece(person1:Person, person2:Person) -> bool:
    if person1 is None or person2 is None: return False
    siblings = person1.siblings
    key = person2.name + ' ' + person2.surname
    for fullname, person_ptr in siblings.items():
        nephews_and_nieces = person_ptr.children
        if key in nephews_and_nieces: return True
    return False

def _is_cousin(person1:Person, person2:Person) -> bool:
    if person1 is None or person2 is None: return False
    father = person1.father
    key = person2.name + ' ' + person2.surname
    if father is not None:
        fathers_siblings = father.siblings
        for _, fathers_siblings_ptr in fathers_siblings.items():
            cousins = fathers_siblings_ptr.children
            if key in cousins: return True
    mother = person1.mother
    if mother is not None:
        mothers_siblings = mother.siblings
        for _, mothers_siblings_ptr in mothers_siblings.items():
            cousins = mothers_siblings_ptr.children
            if key in cousins: return True
    return False

def _is_sibling_in_law(person1:Person, person2:Person) -> bool:
    if person1 is None or person2 is None: return False
    spouse = person1.married_to
    if spouse is None: return False
    key = person2.name + ' ' + person2.surname
    return key in spouse.siblings

def _is_brother_in_law_sisters_husband(person1:Person, person2:Person) -> bool:
    # ENİŞTE
    return _is_sibling_in_law(person2, person1) and person2.gender is Gender.MALE

def _is_sister_in_law_brothers_wife(person1:Person, person2:Person) -> bool:
    # YENGE
    return _is_sibling_in_law(person2, person1) and person2.gender is Gender.FEMALE

def _is_mother_in_law(person1:Person, person2:Person) -> bool:
    if person1 is None or person2 is None: return False
    spouse = person1.married_to
    if spouse is None: return False
    mother_in_law = spouse.mother
    return mother_in_law is person2

def _is_father_in_law(person1:Person, person2:Person) -> bool:
    if person1 is None or person2 is None: return False
    spouse = person1.married_to
    if spouse is None: return False
    father_in_law = spouse.father
    return father_in_law is person2

def _is_daughter_in_law(person1:Person, person2:Person) -> bool:
    return (_is_mother_in_law(person2, person1) or _is_father_in_law(person2, person1)) and person2.gender is Gender.FEMALE

def _is_son_in_law(person1:Person, person2:Person) -> bool:
    return (_is_mother_in_law(person2, person1) or _is_father_in_law(person2, person1)) and person2.gender is Gender.MALE


def _is_brother_in_law_wifes_sisters_husband(person1: Person, person2: Person) -> bool:
    # BACANAK
    if person1 is None or person1.gender is not Gender.MALE or person2 is None or person2.gender is not Gender.MALE: return False
    wife1 = person1.married_to
    wife2 = person2.married_to
    if wife1 is None or wife2 is None: return False
    wife2_key = wife2.name + ' ' + wife2.surname
    return wife2_key in wife1.siblings

def _is_sister_in_law_wifes_sister(person1:Person, person2:Person) -> bool:
    # BALDIZ
    if person1 is None or person2 is None or person2.gender is not Gender.FEMALE: return False
    spouse = person1.married_to
    if spouse is None: return False
    key = person2.name + ' ' + person2.surname
    return key in spouse.siblings

def _is_sister_in_law_husbands_brothers_wife(person1:Person, person2:Person) -> bool:
    # ELTİ
    if person1 is None or person1.gender is not Gender.FEMALE or person2 is None or person2.gender is not Gender.FEMALE: return False
    husband1, husband2 = person1.married_to, person2.married_to
    if husband1 is None or husband2 is None: return False
    h1_key = husband1.name + ' ' + husband1.surname
    return h1_key in husband2.siblings

def _is_brother_in_law_spouses_brother(person1:Person, person2:Person) -> bool:
    # KAYINBİRADER
    if person1 is None or person2 is None or person2.gender is not Gender.MALE: return False
    spouse = person1.married_to
    if spouse is None: return False
    key = person2.name + ' ' + person2.surname
    return key in spouse.siblings


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






