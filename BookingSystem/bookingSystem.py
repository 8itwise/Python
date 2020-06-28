rooms=["Voyager","Sputnik","Python","Endevaour","Beta","Clarion","Pioneer","Swift","Elixir","Galileo","Genasis","Ace","Racket", "Openspace","Vega"]
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
periodNumber = ["1", "2", "3", "4", "5", "6"]

bookingList = []

#saves booking
def saveBooking(data):
    with open('bookingDatabase.txt', 'w') as f: #opens the text file with aim to write to it
        f.write(" ".join(data)) #writes booking information into the text file
        f.write('\n')
        f.close() #closes the text file
        print("Booking has been saved!!")

#deletes booking
def deleteBooking(bookingId):
    f = open('bookingDatabase.txt', 'r') #opens the text file with thr aim to read to it
    fileData = f.readlines() #text file information is stored in fileDta
    f.close()

    f = open('bookingDatabase.txt', 'w')
    for line in fileData: #loops through data in fileData
        print(line)
        if line[0] != bookingId:
            f.write("".join(line)) #rewrites booking information to the text file except for the ones in whih the booking id matches the user input
            print("Booking deleted")
    f.close() #closes the text file

def showAllBookings():
    f = open('bookingDatabase.txt', 'r')
    for line in f.readlines(): #reads booking information from the text file line by line
        print(line.strip()) #prints out booking information
    f.close()

#checks if the room is availability
def checkAvailableRoom(date, room, period):
    available = ""
    f = open('bookingDatabase.txt', 'r')
    for line in f.readlines(): #reads booking information from the text file line by line
    #if three of the user input is found in one of the line it will return false which means the room has been booked for that date and period
        if date in line:
            if room in line:
                if period in line:
                    print("You cannot make a booking for this specific period")
                    available = "unavailable"
    f.close()
    return available

def editBooking(bookingId, action, newInfo):
    num = int(action)

    if action == "1":
        num = 1
    if action == "2":
        num = 2
    elif action == "3":
        num = 3
    elif action == "4":
        num = 4

    f = open('bookingDatabase.txt', 'r') #opens the text file with thr aim to read to it
    fileData = f.readlines() #text file information is stored in fileDta
    f.close()

    f = open('bookingDatabase.txt', 'w')
    for line in fileData:
        line = line.split() #converts line into a list
        line[num]= newInfo  #replaces information in the index with newInfo
        line = " ".join(line)#converts line back to a string
        f.write(line) #write line back to the text file
    f.close()
    print("Change was sucessful")


#main function
def makeBooking():
    bookingId = 0
    while True:
        print("""
            [+]Choose 1 to make a book
            [+]Choose 2 to delete booking
            [+]Choose 3 to show all bookings
            [+]Choose 4 to edit bookings

                """)

        option = input("Enter what function you want to be carried out today? ")

        if option == "1":
            while True:
                global name
                name = input("Input your name ")
                if name.isdigit():#check if user input is an integer
                    print("You cannot enter an integer")
                elif name == "":
                        print("Please enter your full name")
                else:
                    break

            while True:
                global bookingDate
                bookingDate = input("what day do you want this booking for? ")
                bookingDate = bookingDate.title()
                if bookingDate == "":
                    print("You cannot leave this empty")
                elif bookingDate.isdigit():
                    print("You cannot enter an integer")
                elif bookingDate not in days:
                    print("That is not a valid day")
                else:
                    break

            while True:
                global room
                room = input("what room do you want to book? ")
                room = room.title()#capitalises user input
                if room == "": # check if the user has left the field empty
                    print("You cannot leave this empty")
                elif bookingDate.isdigit():
                    print("You cannot enter an integer")
                elif room not in rooms:#checks if the room exists in the array rooms
                    print("This room does not exists")
                else:
                    break

            while True:
                global period
                period = input("what period do you want this booking for? ")
                if period == "":
                    print("You cannot leave this empty")
                elif period not in periodNumber:
                    print("That is not a valid period")
                else:
                    break

            availability = checkAvailableRoom(bookingDate, room, period)
            if availability == "unavailable":
                pass
            else:
                if bookingId > 0:
                    bookingList.extend(["\n" + str(bookingId), name, bookingDate, room, period])#converts booking information into a list
                    saveBooking(bookingList)# saves the list in the text file using the save booking function
                else:
                    bookingList.extend([str(bookingId), name, bookingDate, room, period])#converts booking information into a list
                    saveBooking(bookingList)# saves the list in the text file using the save booking function

                print("\n Booking ID: " + str(bookingId) +"(Please remember your booking id!!!)" + "\n", "Name: " + name + "\n", "Booking Date " + bookingDate + "\n", "Room: " + room + "\n", "Period: " + period, "\n")
                bookingId += 1 #increments booking id by 1 everytime a booking is maid

        elif option == "2":
            id1 = input("Input booking id you want to be deleted ")
            result = deleteBooking(id1)

        elif option == "3":
            showAllBookings()

        elif option == "4":
                print("""
Action Guide

    [+]choose 1 to make changes to the name
    [+]Choose 2 to make changes to the bookingDate
    [+]choose 3 to make changes to the room
    [+]choose 4 to make changes to the period
                    """)

                bookingId = input("Input booking id ")

                while True:
                    action = input("Input action you want to be taken ")
                    if action != "1" or action != "2" or action != "3" or action != "4":
                        print("This is not a valid action")
                    else:
                        break
                newInfo = input("Input new information which will replace the old one ")
                editBooking(bookingId, action, newInfo)

makeBooking()

