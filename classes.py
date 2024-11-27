class Action:
    def speaks(self):
        print(f"{self.name} speaks {self.language}")

    def sleep(self):
        print(f"{self.name} sleeps")
# update
#uppppppp


class Person(Action):
    language = "English, Uzbek"

    def __init__(self, name, age, balance):
        self.name = name
        self.age = age
        self.__balance = balance
        self.friends = []

    def __str__(self):
        return f"{self.name} is {self.age} years old. And has {self.balance} dollars"

    def __repr__(self):
        return self.name

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, amount):
        if amount < 0:
            print("Amount can't be negative")
            return
        self.__balance = amount

    @balance.deleter
    def balance(self):
        del self.__balance
        print("Balance deleted")

    def earn(self, amount):
        self.__balance += amount

    def spend(self, amount):
        if self.__balance - amount < 0:
            print("Not enough money")
            return
        self.__balance -= amount

    def add_friend(self, friend):
        self.friends.append(friend)


class Baby(Person):
    language = None

    def __init__(self, name, age, gender):
        # super().__init__(name, age, 0)

        self.name = name
        self.age = age
        self.__balance = 0

        self.gender = gender

    def speaks(self):
        print(f"{self.name} laughs")

    def add_friend(self, friend):
        print("Baby can't have friends")


# Person  # -> class
# Person()

shamsiddin = Person(name="Shamsiddin", age=24, balance=1000)
# shamsiddin.speaks()

sardor = Baby("sardor", 1, "boy")
# sardor.speaks()

shamsiddin.add_friend(sardor)
print(shamsiddin.friends)
# print(shamsiddin.gender)
# print(sardor.gender)

# print(shamsiddin.balance)
# shamsiddin.earn(999)
# print(shamsiddin.balance)
# shamsiddin.spend(1800)
# print(shamsiddin.balance)

# shoxrux = Person("Shoxrux", 24)
# axror = Person("Akhror", 24)

# @property
# def balance(self):
#     return self.__balance

# @staticmethod
# def get_current_time():
#     return datetime.datetime.now()

# @classmethod
# def create_person(cls, name, age, balance):
#     return cls(name, age, balance)

# def add_friend(self, friend):
#     self.friends.append(friend)

# def __str__(self):
#     return f"{self.name} is {self.age} years old"
