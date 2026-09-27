import pickle
import os

FILE_NAME = "books.dat"

class Book:
    def __init__(self, book_id, name, author, quantity):
        self.id = book_id
        self.name = name
        self.author = author
        self.quantity = quantity

    def display(self):
        print("\nBook ID:", self.id)
        print("Book Name:", self.name)
        print("Book Author:", self.author)
        print("Book Quantity:", self.quantity)
        print("---------------------------")

def add_book():
    book_id = int(input("Enter book id: "))
    name = input("Enter book name: ")
    author = input("Enter book author: ")
    quantity = int(input("Enter book quantity: "))

    book = Book(book_id, name, author, quantity)

    with open(FILE_NAME, "ab") as file:
        pickle.dump(book, file)

    print("Book added successfully!")

def display_books():
    if not os.path.exists(FILE_NAME):
        print("No record found!")
        return

    with open(FILE_NAME, "rb") as file:
        try:
            while True:
                book = pickle.load(file)
                book.display()
        except EOFError:
            pass

def search_book():
    search_id = int(input("Enter book ID to search: "))
    found = False

    if not os.path.exists(FILE_NAME):
        print("No record found!")
        return

    with open(FILE_NAME, "rb") as file:
        try:
            while True:
                book = pickle.load(file)
                if book.id == search_id:
                    print("Book found:")
                    book.display()
                    found = True
                    break
        except EOFError:
            pass

    if not found:
        print("Book not found!")

def issue_book():
    issue_id = int(input("Enter book ID to issue: "))
    books = []
    issued = False

    with open(FILE_NAME, "rb") as file:
        try:
            while True:
                books.append(pickle.load(file))
        except EOFError:
            pass

    for book in books:
        if book.id == issue_id:
            if book.quantity > 0:
                book.quantity -= 1
                issued = True
                print("Book issued successfully!")
            else:
                print("Book out of stock!")
            break

    if not issued:
        print("Book not found!")

    with open(FILE_NAME, "wb") as file:
        for book in books:
            pickle.dump(book, file)

def return_book():
    return_id = int(input("Enter book ID to return: "))
    books = []
    returned = False

    with open(FILE_NAME, "rb") as file:
        try:
            while True:
                books.append(pickle.load(file))
        except EOFError:
            pass

    for book in books:
        if book.id == return_id:
            book.quantity += 1
            returned = True
            print("Book returned successfully!")
            break

    if not returned:
        print("Book not found!")

    with open(FILE_NAME, "wb") as file:
        for book in books:
            pickle.dump(book, file)

def delete_book():
    delete_id = int(input("Enter book ID to delete: "))
    books = []
    deleted = False

    with open(FILE_NAME, "rb") as file:
        try:
            while True:
                book = pickle.load(file)
                if book.id != delete_id:
                    books.append(book)
                else:
                    deleted = True
        except EOFError:
            pass

    with open(FILE_NAME, "wb") as file:
        for book in books:
            pickle.dump(book, file)

    if deleted:
        print("Book deleted successfully!")
    else:
        print("Book not found!")

def main():
    while True:
        print("\n====== Library Management System ======")
        print("1. Add Book")
        print("2. Display Books")
        print("3. Search Book")
        print("4. Issue Book")
        print("5. Return Book")
        print("6. Delete Book")
        print("7. Exit")

        choice = int(input("Enter choice: "))

        if choice == 1:
            add_book()
        elif choice == 2:
            display_books()
        elif choice == 3:
            search_book()
        elif choice == 4:
            issue_book()
        elif choice == 5:
            return_book()
        elif choice == 6:
            delete_book()
        elif choice == 7:
            print("Thank You!")
            break
        else:
            print("Invalid choice!")

main()