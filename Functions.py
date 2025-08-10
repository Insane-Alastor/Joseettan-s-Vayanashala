import pickle
import os
import random
from time import sleep

def sleeps(a,b):
  for i in a:
    print(i,end="")
    sleep(b)

def noinput(a,b):
  while True:
    sleeps(a,b)
    c=input()
    if c !="":
      return c
    print("Invalid Input")

def reg():
  print()
  user_input=noinput("Enter your Full Name/ID(Id preferred): ",0.01)
  try:
    with open("ResourcePacks/reg.dat", "rb") as f:
      while True:
        user_data = pickle.load(f)
        if user_input.title() in user_data:
          print(f"Are you {user_data[1]} (ID: {user_data[0]})?")
          if input("Y/n: ") in "Yy":
            print("Welcome Back", user_data[1].title())
            return user_data[0], user_data[1]
  except EOFError:
    print("Looks Like A New Customer!")
    return new_reg()

def new_reg():
  print()
  name=noinput("Enter Full Name: ",0.01)
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
      m= """
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
        sleeps(f"*Notice: A Book {data['Book']} is due by {data['Due_Date']}",0.01)
        print()
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
    sleeps("A Book Is Pending To Be Returned",0.01)
    print()
    return
  bookname = noinput("Enter Book Name:",0.01).title()
  try:
    with open("ResourcePacks/Book.dat", "rb+") as n:
      b=0
      while True:
        a = n.tell()
        book_data = pickle.load(n)
        if bookname in book_data[1]:
          sleeps(f"You Mean {book_data[1]} by {book_data[3]} Volume {book_data[2]} (Y/n): ",0.01)
          if input() in "Yy":
            if book_data[-1]:
              user_data["Book_No"] = book_data[0]
              user_data["Book"] = book_data[1]
              user_data["Rented_On"] = input("Today's Date (DD/MM/YYYY): ")
              user_data["Due_Date"] = input("Due Date (DD/MM/YYYY): ")
              user_data["Return_Status"] = False
              book_data[-1] = False
              sleeps(f"Rent Amount ₹{book_data[-2]} Paid (Y/n): ",0.01)
              if input() in "Yy":
                sleeps("Saving...",0.05)
                sleeps("Successfully Rented",0.01)
                print()
                with open(f"ResourcePacks/userdata/{user_id}.dat", "wb") as f_user:
                  pickle.dump(user_data, f_user)
                  n.seek(a)
                  pickle.dump(book_data, n)
                  b+=1
            else:
              sleeps("Book Not Available",0.01)
              print()
              break
  except EOFError:
    if not b:
      sleeps("Book Not Found",0.01)
      print()

def return_book(user_id, name):
  print()
  try:
    with open(f"ResourcePacks/userdata/{user_id}.dat", "rb") as f:
      user_data = pickle.load(f)
    if not user_data["Return_Status"]:
      sleeps(f"{name} needs to return {user_data['Book']}",0.01)
      print()
      sleeps("Returning it (Y/n): ",0.01)
      if input() in "Yy":
        sleeps(f"Due Date: {user_data['Due_Date']}",0.01)
        fine = input("Fine: ")
        if len(fine)<2:
          fine="0"+fine
        sleeps(f"""
+--------------------+
|                    |
| Status: RETURNED   |
| Fine  : ₹{fine}        |
|                    |
+--------------------+""",0.001)
        print()
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
              sleeps("Book Not Found",0.01)
              print()
              return
          user_data = {
            "Book_No": None, "Book": None,
            "Rented_On": None, "Due_Date": None,
            "Return_Status": True
            }
          with open(f"ResourcePacks/userdata/{user_id}.dat", "wb") as f:
            pickle.dump(user_data, f)
      else:
        sleeps("Returning Book Cancelled",0.01)
        print()
    else:
      sleeps("You Have No Books To Return",0.01)
      print()
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
        book_title = noinput("Enter Book Title:",0.01).title()
        volume = noinput("Enter Volume No: ",0.01)
        author = noinput("Enter Author:",0.01).title()
        rent_amount = noinput("Enter Rent Amount:",0.01)
        availability = True
        book_entry = [str(book_id), book_title.title(), volume, author.title(), rent_amount, availability]
        pickle.dump(book_entry, f)
        L.append(book_id)
        sleeps("Book Added",0.01)
        print()
        if noinput("Do you want to add more books? (Y/n): ",0.01) in "Nn":
          break

def remove():
  print()
  r_book=noinput("Enter Name or ID Book To Remove:",0.01)
  try:
    with open("ResourcePacks/Book.dat","rb") as f:
      A=[];L=[]
      while True:
        book = pickle.load(f)
        if r_book in book[1] or r_book==book[0]:
          book_display(book)
          if noinput("Is this the book(Y/n):",0.01) in "Yy":
            sleeps("Removing...",0.05)
            print()
            print("*****Book Removed*****")
            A+=[book]
            continue
        L.append(book)
  except EOFError:
    if A==[]:
      sleeps("Book Not Found",0.01)
      print()
    else:
      with open("ResourcePacks/Book.dat","wb") as f:
        for i in L:
          pickle.dump(i,f)

def edit():
  print()
  r_book=noinput("Name or ID or Author Book To Edit:",0.01)
  try:
    with open("ResourcePacks/Book.dat","rb") as f:
      L=[]
      while True:
        book = pickle.load(f)
        if r_book in book: 
          book_display(book)
          if noinput("Is this the book(Y/n):",0.01) in "Yy":
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
                book[1]=noinput("Enter New Book Title:",0.01)
              elif edit=="2":
                book[2]=noinput("Enter New Volume No:",0.01)
              elif edit=="3":
                book[3]=noinput("Enter New Author:",0.01)
              elif edit=="4":
                book[4]=noinput("Enter New Rent Amount:",0.01)
              elif edit=="5":
                while True:
                  sleeps("Availability(True/False):",0.01)
                  book[5]=input().title()
                  if book[5] == "True":
                    book[5] = True
                    break
                  elif book[5] == "False":
                    book[5] = False
                    break
                  sleeps("Invalid Input",0.01)
              book_display(book)
              if noinput("Is This Correct(Y/n):",0.01) in "Yy":
                sleeps("Saving...",0.05)
                print()
                print("*****Book Edited*****")
                break
        L.append(book)
  except EOFError:
    with open("ResourcePacks/Book.dat","wb") as f:
      for i in L:
        pickle.dump(i,f)

def feedback():
  feedback_text = noinput("Enter your feedback:",0.01)
  with open("ResourcePacks/feedback.dat", "ab") as f:
    pickle.dump(feedback_text, f)
    sleeps("Thank You For Your Feedback.",0.01)

def view():
  print()
  with open("ResourcePacks/Book.dat", "rb") as f:
    sleeps("Loading...",0.02)
    print()
    m="""
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
    return
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
