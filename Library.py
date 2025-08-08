#Import

import Functions as fn
import pickle
import random

#User Interface

print()
fn.sleeps("            WELCOME TO JOSETTAN'S VAYANASHALA",0.01)
def UI():
  while True:
    fn.sleeps("""

╔════════════════════════════════════════════════════════╗
║                      MAIN MENU                         ║
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
Enter your choice:""",0.0007)
    choice=input()
    if choice=="1":
      user_portal()

    elif choice=="2":
      fn.search()

    elif choice=="3":
      fn.sleeps("Enter the password:",0.01)
      if input()=="lilboi@1":
        admin_portal()

    elif choice=="4":
      fn.view()

    elif choice=="5":
      fn.feedback()

    elif choice=="0":
      fn.sleeps("Exiting...",0.01)
      print()
      print("Thank You For Using Our Library")
      break

    else:
      fn.sleeps("Invalid Input",0.01)

#User Portal

def user_portal():
  user_id,name=fn.reg()
  while True:
    n=name
    if len(n)<31:
      n=n+" "*(29-len(n))
    fn.sleeps(f"""

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
Enter your choice:""",0.0007)
    choice=input()
    if choice=="1":
      fn.sleeps("Proceeding to Renting...",0.01)
      fn.rent(user_id,name)

    elif choice=="2":
      fn.sleeps("Proceeding to Returning Menu...",0.01)
      fn.return_book(user_id,name)

    elif choice=="3":
      fn.sleeps("Checking Dues...",0.01)
      fn.due(user_id,name)

    elif choice=="4":
      fn.sleeps("Are You Sure You Want to Remove Your Account(Y/n):",0.01)
      if input() in "Yy":
        fn.sleeps("Proceeding...",0.02)
        fn.delete_account(user_id,name)
        UI()
        break

    elif choice.capitalize() == "Back":
      break

    else:
      fn.sleeps("Invalid Input",0.01)

#Admin

def admin_portal():
  while True:
    fn.sleeps("""

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
Enter your choice:""",0.0007)
    choice=input()

    if choice=="1":
      fn.add()
    elif choice=="2":
      fn.remove()
    elif choice=="3":
      fn.edit()
    elif choice=="4":
      fn.sleeps("Loading...",0.01)
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
      fn.sleeps("""
+-----------------------------------
|   ID   |         NAME
+-----------------------------------""",0.001)
      print()
      List=fn.users()
      for i in List:
        fn.sleeps(f"|  {i[0]}  | {i[1]} ",0.01)
      fn.sleeps("+-----------------------------------",0.001)

    elif choice=="6":
      fn.sleeps("Enter the ID of the user you want to remove:",0.01)
      if [userid,n] in fn.users():
        fn.sleeps(f"""ID: {userid}     Name: {n}
              Are You Sure You Want to Remove Account(Y/n):""",0.01)
        if input() in "Yy":
          fn.sleeps("Proceeding...",0.01)
          fn.delete_account(userid,n)
      else:
        fn.sleeps("User Not Found",0.01)

    elif choice=="7":
      with open("ResourcePacks/feedback.dat","rb") as f:
        L=[]
        try:
          while True:
            feedback = pickle.load(f)
            fn.sleeps(f"""
----------------------------------------
Feedback: {feedback}
----------------------------------------
            Next(Y/n):""",0.01)
            if input() in "Nn":
              while True:
                x=pickle.load(f)
                L.append(x)
        except EOFError:
          fn.sleeps("\nNo Feedbacks left",0.01)
          print()
          with open("ResourcePacks/feedback.dat","wb") as f:
            for i in L:
              pickle.dump(i,f)

    elif choice.capitalize() == "Back":
      break

    else:
      fn.sleeps("Invalid Input",0.01)
UI()
