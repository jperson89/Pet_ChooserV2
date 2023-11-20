# Jon Person
# Assignment: Upgrade Pet Chooser
# Details:

'''

Upgrade your Pet Chooser.  Clone your Pet Chooser program to a new PyCharm project.

At every menu, allow the user to use Q or q to quit your program nicely.

Initial View

When the program begins, list all of the pets like before, and ask the user to choose a pet.

Once a pet is chosen, print out the same information as before.

Options

When the pet's information has been displayed, ask the user if they would like to continue or edit the
pet's information.

Example

You have chosen Minnie, the chameleon. Minnie is 4 years old. Minnie's owner is Curtis.

Would you like to [C]ontinue, [Q]uit, or [E]dit this pet?

If the user chooses to quit (by typing Q + [ENTER]), quit the program nicely.

If the user chooses to continue (by typing C + [ENTER]), display the list of pets again from the Initial View.

If the user chooses to edit (by typing E + [ENTER]), display the Edit Process below.

Edit Process

Once the user chooses to edit a pet's information, ask the user which pet to edit (i.e., Which pet would you like to
edit?  The user will provide a number from the Initial View list), step through the pet's name and age to ask the user
to provide an update.

Example

You have chosen to edit Minnie.

New name: [ENTER == no change]

If the user presses [ENTER], the name is unchanged.  If the user types in a new name, update that pet's name in the
database.  Display a message indicating the pet's name has been updated.

New age: [ENTER == no change]

If the user presses [ENTER], the age is unchanged.  If the user types in a new age (check for valid input), update that
pet's age in the database.  Display a message indicating the pet's age has been updated.

When the updates are complete, display the list of pets again from the Initial View.

NOTE: We will only edit the pet's name and age.

NOTE: During the Edit Process, if the user answers QUIT (upper or lower case), quit the program nicely and do not save
the updates.

NOTE: I will log in and run your code to inspect the results.  I will also look at your code.

'''


# Let's import a Python package that reads SQL from MySQL. The package pymsql seems to be the most popular.
import pymysql

# This will hide our password. Nobody likes a shoulder surfer.
import pyautogui

from Pets import *

# This is an SQL Command that will pull our desired data from the SQL database, and also join the appropriate lists
# This took a little trial and error separately in MySQL, but this code works.
# Don't forget to go into MySQL and add the appropriate databases
petdbConnector = """
    select 
        pets.id,
        pets.name as petName,
        pets.age,
        owners.name as ownerName, 
        types.animal_type as petType
    from pets 
        join owners on pets.owner_id = owners.id 
        join types on pets.animal_type_id = types.id;
    """

# These are our entry options to exit the program.
quitOptions = {"q", "quit"}

editOptions = {"y"}

continueOptions = {"c"}

# This is the quit function
def quitPets():
    print("Thank you for using the Pet Chooser V2! Come back soon!")
    exit()


# This is the input function
def petInput():
    try:
        input("Press [ENTER] to continue.")
    # Error messages in case the user tries something odd with the pet Input message
    except EOFError:
        print("Whatever you're doing, I don't like it. If you come back, be on your best behavior.")
        quitPets()
    except Exception as e:
        print(f"Unhandled exception: {e}. Quitting Pet Chooser V2.")
        quitPets()

# This function will allow us to edit our list of pets.
def editPet(petNumber, connection, listOfPets):
    # Remember, we have to use petNumber - 1 because Python starts counting at 0
    indexID = petNumber - 1
    #Start with a 'try' function
    try:
        # Allow the user to input a new name
        newName = input("Please enter the new name:\n")
        # allow the user to quit by entering anything in quitOptions
        if newName in quitOptions:
            quitPets()
        else:
            print(listOfPets[indexID].petName + " is now " + newName)
        # Allow the user to input a new age
        newAge = input("What is the pet's new age? I wish I could change my age too, honestly.\n")
        # Allow the user to quit as before
        if newAge in quitOptions:
            quitPets()
        # Narrow the range of the age between 1-100 so this doesn't go off the rails. We can't have a
        # giraffe that's eons old
        elif int(newAge) not in range(0, 101):
            print("Their age must be an integer between 0 and 100. They're pets, not elves.")
            newAge = str(listOfPets[indexID].petAge)
            print("Their age is still: " + newAge)
        # Don't allow the user to simply leave this blank.
        elif newAge == "":
            raise ValueError
        else:
            print("This pet's age is " + newAge)
    except ValueError:
        print("That's not a valid input")
        newAge = str(listOfPets[indexID].petAge)
        print("Their age is still: " + newAge)
    except EOFError:
        print("Hmm...looks like something went wrong. Let's close up shop and talk to the pets later. Goodbye!")
        quitPets()
    except Exception as e:
        print(f"Unhandled exception: {e}. Quitting Pet Chooser V2.")
        print()
        exit()

    # A cursor in MySQL is used to retrieve rows from your SQL data set and then perform operations on that data.
    # This cursor allows us to update the data in MySQL.
    editCommand = "update pets set age = " + newAge + ", name = \"" + newName + "\" where id = " + str(indexID) + ";"
    with connection.cursor() as cursor:
        cursor.execute(editCommand)
    print("Updates saved to database. Name and age are changed.")
    print("You have changed this pet's information, the very fabric of its being. Neato.")
    petInput()


# This asks for your MySQL credentials to start the program.
try:
    # This asks for your MySQL password in a separate window, creates a connection to mySQL, and
    # hides your password from prying eyes using 'pyautogui'. In addition, you can still use any of the quit commands
    # from quitOptions. Incorrect passwords or invalid entries will exit.
    password = pyautogui.password(text='Please enter your MySQL password or type q to quit. Invalid entries will exit.',
                                  title='MySQL Password',
                                  default='',
                                  mask='*')
    if password.lower() in quitOptions:
        quitPets()
    # This defines connection so that we can automatically connect to MySQL database through a pymysql function
    connection = pymysql.connect(host="localhost",
                                 user="root",
                                 password=password,
                                 db="pets",
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
# You must define possible errors and exceptions and make the program quit nicely like we went over in class
except EOFError:
    print("Quitting. Come back soon!")
    quitPets()
except Exception as e:
    print(f"Error: {e}. Exiting Pet_Chooser.")
    exit()

# According to Ken and many wise men on YouTube, this executes the SQL command that we wrote above. Everything that
# we wrote will be put into a dictionary (petDict) that we can use to populate each list below.
# A cursor in MySQL is used to retrieve rows from your SQL data set and then perform operations on that data. The cursor
# enables you to iterate over returned rows from an SQL query.
# ^^^^ proof that I can read
with connection.cursor() as cursor:
    cursor.execute(petdbConnector)
    petDict = cursor.fetchall()

# make listOfPets an empty list
# name each row in the dictionary 'pet', and append your empty list with the contents of petDict
listOfPets = list()
for pet in petDict:
    listOfPets.append(Pet(pet["petName"],
                          pet["ownerName"],
                          pet["age"],
                          pet["petType"]))

# Now we give the statement to choose a pet. This gives the initial list. Begin with a 'while True' statement
while True:
    # Let's start with an initial greeting
    print("Please choose one of our lovely (if somewhat exotic in some cases) pets.")
    # This gives the list of the pets' names.
    # Essentially, you're printing each entry (pet) in the list as its own line
    # Use "i + 1" in the print function so that the objects are numbered starting at 1, and not 0
    for i in range(0, len(listOfPets)):
        print("[", i+1, "]", listOfPets[i].petName)
    # Remind the use of the option to enter a quit command at the end after your list
    print("[ Q ] Quit")

    # At this point, a list should be printed on screen and the user should choose from that list.

    # Let's get the user's input.
    try:
        print("Choose an integer corresponding to the pet in the list that you would like to display.")
        choice = input("You chose: ")
        # First check if the input is a quit command. using 'choice.lower' reads all the input as lower-case so even
        # if they enter 'Q' or 'Quit', it will still be interpreted as a viable input
        if choice.lower() in quitOptions:
            quitPets()
        # This will cover any input that might not be in the choices listed, and return a Value Error
        # Go through each one and make sure that each pet is properly linked with its owner, pet ID, age, etc.
        # I can't get Rex to work. I'm going insane.
        # NVM, all I had to do was add +1 to length. I can't believe that was all.
        choice = int(choice)
        if choice not in range(1, len(listOfPets) + 1):
            raise ValueError
    # Instead of a ValueError making the program quit, write an exception for it
    # Make sure to put petInput after the error message so that the loop starts over
    except ValueError:
        print("Invalid input. Remember, you have to enter the number next to the pet name, but not their actual name.")
        print()
        petInput()
    # This lets us use Ctrl-D to quit
    except EOFError:
        print("Oh shoot, you're using the ejector seat! Program better, Jon! ABANDON SHIP!")
        quitPets()
    # This should handle any other potential errors
    except Exception as e:
        print(f"Exception error: {e}. Quitting Pet Chooser.")
        quitPets()
    # This next portion covers everything that we want to happen if we get a proper input like we want.
    # According to a lot of sources I read, we're supposed to do all the exceptions we want first, then use 'else' to
    # cover the proper input. There's other ways to make the code work but this is supposedly proper syntax 'grammar'
    else:
        print("You have chosen " + listOfPets[choice - 1].petName + " the " + listOfPets[choice - 1].petType + ".",
              listOfPets[choice - 1].petName + " is " + str(listOfPets[choice - 1].petAge) + " years old.",
              listOfPets[choice - 1].petName + "'s owner is " + listOfPets[choice - 1].ownerName + ".")
        print()
        # This is where it diverges from V1; we allow the option to edit the data.
        print("Would you like to edit this pet's information? Input 'y' to edit, or 'c' to continue back to the list. "
              "'q' will exit Pet Chooser V2.")
        print()
        # Open another 'try' statement and let's allow the user to choose the option to edit the data
        try:
            editChoice = input("What say you?  ")
            # If 'y', then launch the editPet function
            if editChoice.lower() in editOptions:
                editPet(choice, connection, listOfPets)
            # If 'c', then bring them back to the list of pets to choose another.
            elif editChoice.lower() in continueOptions:
                print()
                continue
            # Every other input will cause them to quit.
                # If 'y', then launch the editPet function
            elif editChoice.lower() in quitOptions:
                print("Probably wise tbh. Who wants a pet with an identity crisis? Let's stop here.")
                quitPets()
        # This lets us use Ctrl-D to quit
        except EOFError:
            print("Oh shoot, you're using the ejector seat! Program better, Jon! ABANDON SHIP!")
            quitPets()
        # This should handle any other potential errors
        except Exception as e:
            print(f"Exception error: {e}. Quitting Pet Chooser V2.")
            quitPets()
