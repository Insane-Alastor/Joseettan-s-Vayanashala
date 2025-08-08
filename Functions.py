import pickle
import os
import random
from time import sleep

def sleeps(a,b):
  for i in a:
    print(i,end="")
    sleep(b)

def reg():
  print()
  while True:
    sleeps("Enter your Full Name/ID(Id preferred)",0.01)
    user_input = input(": ")
    if user_input !="":
      break
    print("Please enter a valid name")
  try:
    with open("ResourcePacks/reg.dat", "rb") as f:
      while True:
        user_data = pickle.load(f)
        if user_input.title() in user_data:
          print("Are You", user_data[0], user_data[1])
          if input("Y/n: ") in "Yy":
            print("Welcome Back", user_data[1].title())
            return user_data[0], user_data[1]
  except EOFError:
    print("Looks Like A New Customer!")
    return new_reg()

def new_reg():
  print()
  while True:
    sleeps("Enter Full Name",0.01)
    name = input(": ")
    if name !="":
      break
  ids = []
  try:
    with open("ResourcePacks/reg.dat", "rb") as f:
      while True:
        x = pickle.load(f)
        ids.append(x[0])
  except EOFError:
    pass
  while True:
    new_id = str(random.randint(1000, 9999))
    if new_id not in ids:
      sleeps(f"ID: {new_id}",0.01)
      with open("ResourcePacks/reg.dat", "ab") as f:
        pickle.dump([new_id, name.title()], f)
        with open(f"ResourcePacks/userdata/{new_id}.dat", "wb") as n:
          default_data = {
                  "Book_No": None, "Book": None,
                  "Rented_On": None, "Due_Date": None,
                  "Return_Status": True
                  }
          pickle.dump(default_data, n)
          return new_id, name.title()

def search():
  print()
  c=0
  try:
    with open("ResourcePacks/Book.dat", "rb") as f:
      a = input("Enter Book/Author Name: ").title()
      sleeps("Searching...",0.01)
      b=104
      m = """
+------------------------------------------------------------------------------------------------------+
| ID   |           Book Title           | Volume |        Author        | Rent Amount |  Availability  |
+------------------------------------------------------------------------------------------------------+"""
      sleeps(m,0.005)
      print()
      while True:
        x = pickle.load(f)
        if a in x[1] or a in x[3]:
          book_display(x)
          c+=1
  except EOFError:
    if not c:
      m="|"+" "*(((len(b)-len("Book Not Found"))//2)-1)+"BOOK NOT FOUND"+" "*(((len(b)-len("Book Not Found"))//2)-1)+"|"
      sleeps(m,0.01)
    sleeps("+------------------------------------------------------------------------------------------------------+",0.005)

def due(user_id, name):
  print()
  try:
    with open(f"ResourcePacks/userdata/{user_id}.dat", "rb") as f:
      data = pickle.load(f)
      if not data["Return_Status"]:
        print(f"*Notice: A Book {data['Book']} is due by {data['Due_Date']}")
        return data["Return_Status"]
      else:
        print("No Books Due")
  except EOFError:
    pass

def rent(user_id, name):
  print()
  with open(f"ResourcePacks/userdata/{user_id}.dat", "rb") as f:
    user_data = pickle.load(f)
  if not user_data["Return_Status"]:
    print("A Book Is Pending To Be Returned")
    return
  bookname = input("Enter Book Name: ").title()
  try:
    with open("ResourcePacks/Book.dat", "rb+") as n:
      b=0
      while True:
        a = n.tell()
        book_data = pickle.load(n)
        if bookname in book_data[1]:
          if input(f"You Mean {book_data[1]} by {book_data[3]} Volume {book_data[2]} (Y/n): ") in "Yy":
            if book_data[-1]:
              user_data["Book_No"] = book_data[0]
              user_data["Book"] = book_data[1]
              user_data["Rented_On"] = input("Today's Date (DD/MM/YYYY): ")
              user_data["Due_Date"] = input("Due Date (DD/MM/YYYY): ")
              user_data["Return_Status"] = False
              book_data[-1] = False
              if input(f"Rent Amount ₹{book_data[-2]} Paid (Y/n): ") in "Yy":
                print("Successfully Rented")
                with open(f"ResourcePacks/userdata/{user_id}.dat", "wb") as f_user:
                  pickle.dump(user_data, f_user)
                  n.seek(a)
                  pickle.dump(book_data, n)
                  b+=1
            else:
              print("Book Not Available")
              break
  except EOFError:
    if not b:
      print("Book Not Found")

def return_book(user_id, name):
  print()
  try:
    with open(f"ResourcePacks/userdata/{user_id}.dat", "rb") as f:
      user_data = pickle.load(f)
    if not user_data["Return_Status"]:
      print(f"{name} needs to return {user_data['Book']}")
      if input("Returning it (Y/n): ") in "Yy":
        print(f"Due Date: {user_data['Due_Date']}")
        fine = input("Fine: ")
        if len(fine)<2:
          fine="0"+fine
        print(f"""
+--------------------+
|                    |
| Status: RETURNED   |
| Fine  : ₹{fine}        |
|                    |
+--------------------+""")
        with open("ResourcePacks/Book.dat", "rb+") as p:
          while True:
            try:
              a = p.tell()
              book = pickle.load(p)
              if user_data["Book_No"] == book[0]:
                book[-1] = True
                p.seek(a)
                pickle.dump(book, p)
                break
            except EOFError:
              print("Book record not found.")
              return
          user_data = {
            "Book_No": None, "Book": None,
            "Rented_On": None, "Due_Date": None,
            "Return_Status": True
            }
          with open(f"ResourcePacks/userdata/{user_id}.dat", "wb") as f:
            pickle.dump(user_data, f)
      else:
        print(f"Return by {user_data['Due_Date']}")
    else:
      print("You Have No Books In Due")
  except:
    pass

def add():
  print()
  L = []
  with open("ResourcePacks/Book.dat", "ab+") as f:
    f.seek(0)
    try:
      while True:
        x = pickle.load(f)
        L.append(x[0])
    except EOFError:
      while True:
        while True:
          book_id =random.randint(1000,9999)
          if book_id not in L:
            print(f"Book ID: {book_id}")
            break
        book_title = input("Enter the Book Title: ").title()
        volume = input("Enter the Volume No: ")
        author = input("Enter the Author: ").title()
        rent_amount = input("Enter the Rent Amount: ")
        availability = True
        book_entry = [book_id, book_title.title(), volume, author.title(), rent_amount, availability]
        pickle.dump(book_entry, f)
        L.append(book_id)
        if input("Do you wish to add more books? (Y/n): ") in "Nn":
          break

def remove():
  print()
  sleeps("Enter Name or ID Book To Remove:",0.01)
  r_book=input()
  try:
    with open("ResourcePacks/Book.dat","rb") as f:
      A=[];L=[]
      while True:
        book = pickle.load(f)
        if r_book in book[1] or r_book==book[0]:
          book_display(book)
          sleeps("Is this the book(Y/n):",0.01)
          if input() in "Yy":
            sleeps("Removing...",0.05)
            print("*****Book Removed*****")
            A+=[book]
            continue
        L.append(book)
  except EOFError:
    if A==[]:
      sleeps("Book Not Found",0.01)
    else:
      with open("ResourcePacks/Book.dat","wb") as f:
        for i in L:
          pickle.dump(i,f)

def edit():
  print()
  sleeps("Name or ID Book To Edit:",0.01)
  r_book=input()
  try:
    with open("ResourcePacks/Book.dat","rb") as f:
      L=[]
      while True:
        book = pickle.load(f)
        if r_book in book[1] or r_book==book[0]:
          book_display(book)
          sleeps("Is this the book(Y/n):",0.01)
          if input() in "Yy":
            while True:
              sleeps(("""
  Do You Want To Edit

  [1] Book Title
  [2] Volume No
  [3] Author
  [4] Rent Amount
  [5] Availability

  Choice[1-5]:"""),0.001)
              edit=input()
              if edit=="1":
                sleeps("Enter New Book Title:",0.01)
                book[1]=input()
              elif edit=="2":
                sleeps("Enter New Volume No:",0.01)
                book[2]=input()
              elif edit=="3":
                sleeps("Enter New Author:",0.01)
                book[3]=input()
              elif edit=="4":
                sleeps("Enter New Rent Amount:",0.01)
                book[4]=input()
              elif edit=="5":
                sleeps("Availability(True/False):",0.01)
                book[5]=input().title()
              else:
                sleeps("Invalid Choice",0.01)
              book_display(book)
              if input("Is This Correct(Y/n):") in "Yy":
                sleeps("Saving...",0.05)
                print("*****Book Edited*****")
                break
        L.append(book)
        break
  except EOFError:
    with open("ResourcePacks/Book.dat","wb") as f:
      for i in L:
        pickle.dump(i,f)

def feedback():
  sleeps("Enter your feedback:",0.01)
  feedback_text = input()
  with open("ResourcePacks/feedback.dat", "ab") as f:
    pickle.dump(feedback_text, f)
    sleeps("Thank You For Your Feedback.",0.01)

def view():
  print()
  with open("ResourcePacks/Book.dat", "rb") as f:
    sleeps("Loading...",0.02)
    m = """
+------------------------------------------------------------------------------------------------------+
| ID   |           Book Title           | Volume |        Author        | Rent Amount |  Availability  |
+------------------------------------------------------------------------------------------------------+"""
    sleeps(m,0.005)
    print()
    while True:
      try:
        book = pickle.load(f)
        book_display(book)
      except EOFError:
        sleeps("+------------------------------------------------------------------------------------------------------+",0.005)
        break

def delete_account(user_id,name):
  if due(user_id,name):
    print()
    sleeps("Due left, Cant Delete",0.01)
  with open("ResourcePacks/reg.dat", "rb") as f:
    L=[]
    while True:
      try:
        x = pickle.load(f)
        if x == [user_id, name.title()]:
          os.remove(f"ResourcePacks/userdata/{user_id}.dat")
          sleeps("Removing...",0.05)
          print("Account Removed",0.01)
          continue
        L.append(x)
      except EOFError:
        print("Account Not Found")
        break
  with open("ResourcePacks/reg.dat", "wb") as f:
    for i in L:
      pickle.dump(i,f)

def users():
  UserIds=[]
  with open("ResourcePacks/reg.dat", "rb") as f:
    try:
      while True:
        x=pickle.load(f)
        UserIds.append(x)
    except EOFError:
      return UserIds

def book_display(book):
  book_id = book[0]
  title = book[1]
  volume = book[2]
  author = book[3]
  rent = str(book[4])
  if len(title) > 30:
    title = title[:27] + "..."
  else:
    title = title + " " * (30 - len(title))
  if len(volume) == 1:
    volume = "0" + volume
  elif len(volume) > 2:
    volume = volume[:2]
  if len(author) > 20:
    author = author[:17] + "..."
  else:
    author = author + " " * (20 - len(author))
  rent = " " * (10 - len(rent)) + "₹" + rent
  availability = str(book[5])
  availability += " " * (13 - len(availability))
  sleeps(f"| {book_id} | {title} |   {volume}   | {author} | {rent} | {availability}  |",0.003)
  print()
