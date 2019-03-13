
#Import modules
import os
import time
import math
import random
#Define Functions
frame = []
#Add a line to the screen and refresh the screen
def display(string):
    frame.append(string)
    refresh()
    return
#Refresh the screen
def refresh():
    os.system("cls")
    for i in frame:
        print(i)
    return
#Clear the screen and empty the data file
def clear():
    global frame
    os.system("cls")
    frame = []
#Display a heading based off of location
def heading(location):
    display(location+": "+locations[location.lower()]+" \n")
    display("Money:"+str(money)+"\n")
#Capatalize a word
def cap(word):
    try:
        temp = capitals[word[0]]+word[1:len(word)]
    except KeyError:
        temp = word
    return temp
#Display what the shop sells
def stock():
    print("Here are the prices of our products (In order of popularity): ")
    for i in price:
        print(cap(i)+": "+"$"+str(price[i]))
    input()
#Display what raw ingredients you currently have
def inv():
    print("Here is your current stock levels (Go to the shop to buy more):")
    for i in inventory:
        if inventory[i] > 0:
            print(cap(i)+": "+str(inventory[i]))
    input()
#Display what is currently in the mixing bowl
def mixture():
    print("Here is your current mixing bowl:")
    for i in bowl:
        print(cap(i)+": "+str(bowl[i]))
    input()
#Display items of a list in a regular english format
def niceList(arg):
    string = ""
    for i in range(len(arg)-1):
        string += (cap(arg[i])+", ")
    string += cap(arg[len(arg)-1])
    return string
#Display what is currently in the shopping cart at the store
def order():
    global total
    total = 0
    print("Here is your current receipt: ")
    for i in receipt:
        print(cap(i)+": x"+str(receipt[i])+" ($"+str((price[i]*receipt[i]))+")")
        total += (price[i]*receipt[i])
    print("\nTotal: $"+str(total)+"\n")
    input()
#Determine the cost of a recipe
def cost(arg):
    temp = 0
    for i in arg:
        temp += (price[i]*arg[i])
    return temp
#Display all known recipes
def cookbook():
    print("\nThese are the recipes in your cookbook:")
    for i in recipes:
        print(cap(recipes[i]))
    input()
#Display recipe for specific item
def recipe(item):
    x = list(recipes.keys())[list(recipes.values()).index(item)]
    print(cap(item)+": ")
    for i in x:
        print(" "+str(i[1])+" "+cap(i[0]))
    input()
#Turn a dictionary into a set of tuples
def dictSet(arg):
    x = set()
    for i in arg:
        x.add((i,arg[i]))
    return x
#Turn a set of tuples into a dictionary
def setDict(arg):
    x = {}
    for i in arg:
        x[i[0]] = i[1]
    return x
#Show current finished products
def showProducts():
    print("Here are your current stock levels:")
    for i in products:
        print(i)
    input()
#Class containing main screens so that getattr() can be used
class Screens:
    #Main menu screen
    def menu():
        #Globalize screeb
        global frame
        #Clear screen and display menu heading
        clear()
        heading("Menu")
        #Show available locations
        display("The following locations are available: "+
              niceList(list(locations.keys())))
        #Recieve destination
        dest = input("Where would you like to go? ").lower()
        #Attempt to go to location, otherwise return error message
        try:
            if dest != "menu":
                getattr(Screens,dest)()
            else:
                pass
        except AttributeError:
            display("Sorry, that location is not available")
            input()
        return None
    #Shop screen, to buy raw ingredients
    def shop():
        #Globalize important variables
        global money
        global frame
        global receipt
        receipt = {}
        #Clear screen and display shop heading
        clear()
        heading("Shop")
        display("Welcome to our shop:")
        #Ask if they want to view stock
        entry = input("Would you like to look at our stock? ")
        if entry == "yes":
            stock()
        entry = ""
        #Recieve order
        display("Place your order:")
        while entry != "done":
            #Refresh the screen
            refresh()
            #Parse entry
            entry = input(": ").lower()
            entry = entry.split()
            try:
                amount = int(entry[1])
            except (IndexError,ValueError):
                amount = 1
            if entry == []:
                entry = "nothing (Please enter something)"
            else:
                entry = entry[0]
            #Try to find entry in price list
            try:
                price[entry]
                #Add purchase to receipt
                try:
                    receipt[entry] += amount
                except KeyError:
                    receipt[entry] = amount
                #Update money line of display
                frame[1] = "Money:"+str(money)+"\n"
                #Display information
                if frame[len(frame)-1] == "Place your order:":
                    display("Enjoy your "+entry)
                else:
                    frame[len(frame)-1] = "Enjoy your "+entry
            #If a product was not entered:
            except KeyError:
                #If command is not in other recognized, return error message
                if entry != "done" and entry != "stock" and entry != "receipt":
                    if frame[len(frame)-1] == "Place your order:":
                        display("Sorry, We dont sell "+entry)
                    else:
                        frame[len(frame)-1] = "Sorry, We dont sell "+entry
                #Show stock
                if entry == "stock":
                    stock()
                #Show receipt
                if entry == "receipt":
                    order()
        #Clear screen
        clear()
        #Make sure reciept exists
        try:
            receipt
        except NameError:
            receipt = {}
        #Display shop heading
        heading("Shop")
        #Show receipt
        order()
        #Allow cancelling of order
        display("Enter 'Cancel' to cancel your order, or enter anything else to complete the purchase")
        entry = input(": ").lower()
        if entry != "cancel":
            #Subtract money
            if money - total > 0:
                money -= total
                #Add purchase to inventory
                for i in receipt:
                    inventory[i] += receipt[i]
            else:
                #Inform that purchase is too expensive
                display("Sorry, you dont have enough money")
                time.sleep(1)
        else:
            pass
        #Display goodbye message
        clear()
        heading("Shop")
        display("Have a good day")
        time.sleep(1)
        return None
    def bakery():
        #Globalize important variables
        global money
        global frame
        global bowl
        #Clear and show bakery heading
        clear()
        heading("Bakery")
        #Display instructions
        display("Add something to the mixing bowl, look at the current contents, or bake the contents")
        #Declare bowl
        bowl = {}
        entry = ""
        while entry != "done":
            refresh()
            #Parse input
            entry = input(": ").lower()
            entry = entry.split()
            try:
                amount = int(entry[1])
            except (IndexError,ValueError):
                amount = 1
            if entry == []:
                entry = "nothing (Please enter something)"
            else:
                entry = entry[0]
            #Make sure that entry is valid, and they have enough
            try:
                1/(amount <= inventory[entry])
            except (KeyError,ZeroDivisionError):
                #Check for other recognized commands
                if entry == "inventory":
                    #Display inventory
                    inv()
                elif entry == "bowl":
                    #Display current mixing bowl
                    mixture()
                elif entry == "cookbook":
                    #Display recipes
                    cookbook()
                elif entry == "done":
                    #Display goodbye message
                    print("Goodbye")
                elif entry in list(recipes.values()):
                    #Show recipe
                    recipe(entry)
                elif entry == "bake":
                    #Check if recipe already exists
                    try:
                        recipes[frozenset(dictSet(bowl))]
                    except KeyError:
                        #If not then get user to name new recipe
                        entry = "cookie"
                        while entry in sellPrice:
                            refresh()
                            entry = input("Looks you've made a new recipe! Give it a name: ").lower()
                            if entry in sellPrice:
                                print("Sorry, there is already something with that name")
                                input()
                            else:
                                #Calculate price of recipe and add to cookbook
                                sellPrice[entry] = round(cost(bowl)*1.25)+1
                                recipes[frozenset(dictSet(bowl))] = entry
                                entry = 0
                    else:
                        pass
                    #Add recipe to products
                    entry = recipes[frozenset(dictSet(bowl))]
                    products.append(entry)
                    print("You baked a "+entry)
                    #Clear bowl
                    bowl = {}
                    input()
                else:
                    #Display error message if input for ingredient not recognized
                    print("Sorry, you dont have enough "+entry)
                    input()
            else:
                #Add ingredient to bowl
                try:
                    bowl[entry] += amount
                except KeyError:
                    bowl[entry] = amount
                #Take ingredient from inventory
                inventory[entry] -=amount
        input()
        return None
    def store():
        #Globalize important variables
        global money
        global frame
        global reputation
        #Clear and display store heading
        clear()
        heading("Store")
        display("Enter something to sell it, or view your stock, or enter done to finish")
        entry = ""
        while entry != "done":
            entry = input(": ").lower()
            try:
                products.index(entry)
            except ValueError:
                if entry == "stock":
                    showProducts()
                elif entry == "done":
                    print("Goodbye")
                    input()
                else:
                    print("Sorry, you dont have any of that to sell")
            else:
                print("You sold 1 "+entry+" for"+str(sellPrice[entry]))
                money += sellPrice[entry]
                reputation += round(sellPrice[entry]*0.1)
                products.pop(products.index(entry))
            refresh()
        return None
    def public():
        clear()
        heading("Public")
        display("Your current reputation: "+reputation)
        input()
        return None
#Declare variables
reputation = 0
money = 500
rawCapitals = ["abcdefghijklmnopqrstuvwxyz","ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
capitals = {}
for i in rawCapitals[0]:
    capitals[i] = rawCapitals[1][rawCapitals[0].find(i)]
bowl = {}
products = []
locations = {"shop":"Buy your ingredients here",
             "bakery":"Cook and bake here",
             "store":"Sell your products here",
             "public":"Manage public affairs here",
             "menu":"Manage your company"}
price = {"flour":1,"sugar":2,"shortening":1,"spice":2,"riser":1,"egg":1,
         "vanilla":3,"chocolate":4,"lard":1,"syrup":2,"fruit":3,"cocoa":4,
         "milk":1,"oatmeal":1,"cheese":6,"meat":4,"vegetable":2,"sauce":3,
         "cinnamon":2,"icing":2,"water":0,"salt":1}
inventory = {"flour":0,"sugar":0,"shortening":0,"spice":0,"riser":0,"egg":0,
             "vanilla":0,"chocolate":0,"lard":0,"syrup":0,"fruit":0,"cocoa":0,
             "milk":0,"oatmeal":0,"cheese":0,"meat":0,"vegetable":0,"sauce":0,
             "Cinnamon":0,"icing":0,"water":0,"salt":0}
recipes = {frozenset({("shortening",1),("sugar",1),("egg",1),("flour",3),("riser",1)}):"cookie",
           frozenset({("flour",4),("riser",1),("shortening",2)}):"biscuit",
           frozenset({("riser",3),("water",2),("flour",6)}):"bread",
           frozenset({("flour",3),("riser",1),("sugar",1),("water",3)}):"pancake",
           frozenset({("flour",4),("riser",2)}):"muffin",
           frozenset({("cocoa",1),("shortening",1),("egg",2),("sugar",2),("flour",3)}):"brownies",
           frozenset({("flour",2),("sugar",3),("egg",2),("icing",1)}):"cake",
           frozenset({("water",1),("riser",1),("flour",3)}):"pizza",
           frozenset({("flour",2),("water",1),("salt",1)}):"pretzel"}
sellPrice = {"cookie":15,"biscuit":14,"bread":16,"pancake":13,"muffin":13,
             "brownies":23,"cake":20,"pizza":10,"pretzel":9}
#Forever run script
while True:
    Screens.menu()
