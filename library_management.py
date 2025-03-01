import tkinter as tk
from tkinter import messagebox, simpledialog
import json

class Book:
    def __init__(self, title, author, ISBN):
        self.title = title
        self.author = author
        self.ISBN = ISBN
        self.status = "available"  # "available" or "borrowed"

    def __str__(self):
        return f"Title: {self.title}, Author: {self.author}, ISBN: {self.ISBN}, Status: {self.status}"

class Library:
    def __init__(self):
        self.books = []
        self.load_books()  # Load books from the JSON file when initializing

    def add_book(self, book):
        self.books.append(book)
        self.save_books()  # Save books to file after adding

    def remove_book(self, ISBN):
        for book in self.books:
            if book.ISBN == ISBN:
                self.books.remove(book)
                self.save_books()  # Save books to file after removal
                return True
        return False

    def search_book(self, title):
        low, high = 0, len(self.books) - 1
        while low <= high:
            mid = (low + high) // 2
            if self.books[mid].title.lower() == title.lower():
                return self.books[mid]
            elif self.books[mid].title.lower() < title.lower():
                low = mid + 1
            else:
                high = mid - 1
        return None

    def borrow_book(self, ISBN):
        book = self.search_book_by_ISBN(ISBN)
        if book and book.status == "available":
            book.status = "borrowed"
            self.save_books()  # Save books to file after borrowing
            return f"You've borrowed {book.title}"
        else:
            return "Sorry, this book is either not available or already borrowed."

    def return_book(self, ISBN):
        book = self.search_book_by_ISBN(ISBN)
        if book and book.status == "borrowed":
            book.status = "available"
            self.save_books()  # Save books to file after returning
            return f"Thank you for returning {book.title}"
        else:
            return "This book is not borrowed or doesn't exist."

    def search_book_by_ISBN(self, ISBN):
        for book in self.books:
            if book.ISBN == ISBN:
                return book
        return None

    def list_books(self):
        return [str(book) for book in self.books]

    # Save the books list to a JSON file
    def save_books(self):
        with open('books.json', 'w') as f:
            books_data = [{'title': book.title, 'author': book.author, 'ISBN': book.ISBN, 'status': book.status} for book in self.books]
            json.dump(books_data, f, indent=4)

    # Load books from the JSON file
    def load_books(self):
        try:
            with open('books.json', 'r') as f:
                books_data = json.load(f)
                for book_data in books_data:
                    book = Book(book_data['title'], book_data['author'], book_data['ISBN'])
                    book.status = book_data['status']
                    self.books.append(book)
        except FileNotFoundError:
            self.books = []  # If no file exists, start with an empty list

class LibraryInterface(tk.Tk):
    def __init__(self):
        super().__init__()

        self.library = Library()
        self.title("Library Management System")
        self.geometry("600x500")

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Library Management System", font=("Arial", 16))
        self.label.pack(pady=10)

        self.add_button = tk.Button(self, text="Add Book", command=self.add_book)
        self.add_button.pack(pady=10)

        self.remove_button = tk.Button(self, text="Remove Book", command=self.remove_book)
        self.remove_button.pack(pady=10)

        self.search_button = tk.Button(self, text="Search Book by Title", command=self.search_book)
        self.search_button.pack(pady=10)

        self.borrow_button = tk.Button(self, text="Borrow Book", command=self.borrow_book)
        self.borrow_button.pack(pady=10)

        self.return_button = tk.Button(self, text="Return Book", command=self.return_book)
        self.return_button.pack(pady=10)

        self.list_button = tk.Button(self, text="List All Books", command=self.list_books)
        self.list_button.pack(pady=10)

        # Adding Exit button
        self.exit_button = tk.Button(self, text="Exit", command=self.exit_program)
        self.exit_button.pack(pady=10)

    def add_book(self):
        title = self.prompt_input("Enter book title:")
        author = self.prompt_input("Enter book author:")
        ISBN = self.prompt_input("Enter book ISBN:")
        if title and author and ISBN:
            new_book = Book(title, author, ISBN)
            self.library.add_book(new_book)
            messagebox.showinfo("Success", f"Book '{title}' added successfully.")
        else:
            messagebox.showerror("Error", "All fields are required.")

    def remove_book(self):
        ISBN = self.prompt_input("Enter ISBN of the book to remove:")
        if ISBN:
            if self.library.remove_book(ISBN):
                messagebox.showinfo("Success", f"Book with ISBN {ISBN} removed.")
            else:
                messagebox.showerror("Error", "Book not found.")

    def search_book(self):
        title = self.prompt_input("Enter the title of the book to search:")
        if title:
            book = self.library.search_book(title)
            if book:
                messagebox.showinfo("Found", str(book))
            else:
                messagebox.showerror("Error", "Book not found.")

    def borrow_book(self):
        ISBN = self.prompt_input("Enter ISBN of the book to borrow:")
        if ISBN:
            message = self.library.borrow_book(ISBN)
            messagebox.showinfo("Borrow Book", message)

    def return_book(self):
        ISBN = self.prompt_input("Enter ISBN of the book to return:")
        if ISBN:
            message = self.library.return_book(ISBN)
            messagebox.showinfo("Return Book", message)

    def list_books(self):
        books = self.library.list_books()
        if books:
            book_list = "\n".join(books)
            messagebox.showinfo("List of Books", book_list)
        else:
            messagebox.showinfo("List of Books", "No books available.")

    def exit_program(self):
        self.destroy()  # Close the window and exit the program

    def prompt_input(self, prompt):
        return simpledialog.askstring("Input", prompt, parent=self)

if __name__ == "__main__":
    app = LibraryInterface()
    app.mainloop()
