
#Import

import Functions as fn
import pickle
import random

#User Interface

def UI():
  while True:
    choice=input("""


╔════════════════════════════════════════════════════════╗
║                 WELCOME TO OUR LIBRARY                 ║
║                                                        ║
║  Please select an option:                              ║
║                                                        ║
║    1. Register / Login                                 ║
║    2. Search Book                                      ║
║    3. Admin Portal                                     ║
║    4. View All Books                                   ║
║    5. Feedback                                         ║
║    0. Exit Program                                     ║
╚════════════════════════════════════════════════════════╝
Enter your choice: """)
    if choice=="1":
      user_portal()

    elif choice=="2":
      fn.search()

    elif choice=="3":
      if input("Enter the password:")=="lilboi@1":
        admin_portal()

    elif choice=="4":
      print("You have selected View All Books")
      fn.view()

    elif choice=="5":
      fn.feedback()

    elif choice=="0":
      print("Exiting Program")
      break

    else:
      print("Invalid Input")

#User Portal

def user_portal():
  user_id,name=fn.reg()
  while True:
    n=name
    if len(n)<31:
      n=n+" "*(29-len(n))
    choice=input(f"""


╔═════════════════════════════════════════════════════╗
║               WELCOME, {n.upper()}║
║                                                     ║
║   What would you like to do today?                  ║
║                                                     ║
║   1. Rent A Book                                    ║
║   2. Return Book                                    ║
║   3. Check Dues                                     ║
║   4. Remove Account                                 ║
║                                                     ║
║   Type 'Back' to return to the main menu            ║
╚═════════════════════════════════════════════════════╝
Enter your choice: """)
    if choice=="1":
      print("Proceeding to Renting")
      fn.rent(user_id,name)

    elif choice=="2":
      fn.return_book(user_id,name)

    elif choice=="3":
      print("Checking Due Status")
      fn.due(user_id,name)

    elif choice=="4":
      if input(f"""ID:{user_id} Name: {name}
      Are You Sure You Want to Remove Account(Y/n):""") in "Yy":
        print("Proceeding")
        fn.delete_account(user_id,name)
        UI()
        break

    elif choice.capitalize() == "Back":
      break

    else:
      print("Invalid Input")

#Admin

def admin_portal():
  while True:
    choice=input("""


╔════════════════════════════════════════════════════════╗
║                    ADMIN PORTAL                        ║
║                                                        ║
║   1. Add New Book                                      ║
║   2. Remove Books                                      ║
║   3. Edit Books                                        ║
║   4. View All Pending Returns                          ║
║   5. View All Registered Users                         ║
║   6. Remove a User Account                             ║
║   7. View Feedbacks                                    ║
║                                                        ║
║   Type 'Back' to return to the main menu               ║
╚════════════════════════════════════════════════════════╝
Enter your choice: """)

    if choice=="1":
      fn.add()
    elif choice=="2":
      fn.remove()
    elif choice=="3":
      fn.edit()
    elif choice=="4":
      print("\t\tAll Pending Returns")
      List=fn.users()
      for i in List:
        try:
          with open(f"ResourcePacks/userdata/{i[0]}.dat", "rb") as f:
            data = pickle.load(f)
            if not data["Return_Status"]:
              print("--------------------------------------------------------------")
              print(f"ID     : {i[0]}")
              print(f"Name   : {i[1]}")
              print(f"Report : A Book {data['Book']} is due by {data['Due_Date']}")
              print("--------------------------------------------------------------")
        except EOFError:
          if not b:
            print("No Users With Dues")

    elif choice=="5":
      print()
      print("|   ID   |  Name")
      print()
      List=fn.users()
      for i in List:
        print("| ",i[0]," |",i[1])

    elif choice=="6":
      userid=input("Enter ID:")
      n=input("Enter Name:")
      if [userid,n] in fn.users():
        if input(f"""ID:{userid} Name: {n}
        Are You Sure You Want to Remove Account(Y/n):""") in "Yy":
          print("Proceeding")
          fn.delete_account(userid,n)
      else:
        print("User Not Found")

    elif choice=="7":
      with open("ResourcePacks/feedback.dat","rb") as f:
        L=[]
        try:
          while True:
            feedback = pickle.load(f)
            print("\n----------------------")
            print("Feedback:", feedback)
            print("----------------------")
            if input("Next(Y/n):") in "Nn":
              while True:
                x=pickle.load(f)
                L.append(x)
        except EOFError:
          print("No Feedbacks left")
          with open("ResourcePacks/feedback.dat","wb") as f:
            for i in L:
              pickle.dump(i,f)

    elif choice.capitalize() == "Back":
      break

    else:
        print("Invalid Input")
UI()
