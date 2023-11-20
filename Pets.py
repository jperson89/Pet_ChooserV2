# This defines our pets as a class

# This works like it did before when we made the bike class, but let's make it a little easier on ourselves by
# making sure everything is either a string or integer where needed.
class Pet:
    def __init__(self, petName, ownerName, petAge, petType):
        self.petName = str(petName)
        self.ownerName = str(ownerName)
        self.petAge = int(petAge)
        self.petType = str(petType)

    def getPetType(self) -> str:
        return self.__petType

    def getPetAge(self) -> int:
        return self.__petAge

    def getPetName(self) -> str:
        return self.__petName

    def getPetType(self) -> str:
        return self.__type

    def getOwnerName(self) -> str:
        return self.__owner


    def setPetName(self, name: str) -> None:
        try:
            self.__petName = name
        except ValueError as e:
            print("Invalid input.")

    def setPetAge(self, age: int) -> None:
        try:
            self.__petAge = age
        except ValueError as e:
            print("Invalid input.")

    def setPetType(self, petType: str) -> None:
        try:
            self.__petType = petType
        except ValueError as e:
            print("Invalid input.")

    def setOwnerName(self, ownerName: str) -> None:
        try:
            self.__ownerName = ownerName
        except ValueError as e:
            print("Invalid input.")