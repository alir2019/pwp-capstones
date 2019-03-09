class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        return "{user}'s email address has been updated!".format(user=self.name)

    def __repr__(self):
        return "User {user}, email: {email}, books read: {books}".format(user=self.name, email=self.email, books=len(self.books))

    def __eq__(self, other_user):
        if self.name == other_user.name and self.email == other_user.email:
            return True
        else:
            return False

    def read_book(self, book, rating='None'):
        if rating == 'None':
            self.books[book] = rating
        elif rating != 'None':
            self.books[book] = int(rating)

    def get_average_rating(self):
        value_total = 0
        for rating in self.books.values():
            if rating != 'None':
                value_total += rating
        if value_total != 0:
            return value_total/len(self.books)
        else:
            return 0
            

class Book(object):
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []

    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        return "The ISBN for {book} has been updated!".format(book=self.title)

    def add_rating(self, rating):
        if rating in range(0, 5):
            self.ratings.append(rating)
        else:
            return "Invalid Rating"

    def __eq__(self, other_book):
        if self.title == other_book.title and self.isbn == other_book.isbn:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.title, self.isbn))

    def get_average_rating(self):
        rating_total = 0
        for rating in self.ratings:
            rating_total += rating
        return rating_total/len(self.ratings)

    def __repr__(self):
        return "{book} with ISBN No. {isbn}".format(book=self.title, isbn=self.isbn)


class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author
    
    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author}".format(title=self.title, author=self.author)

class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format(title=self.title, level=self.level, subject=self.subject)

class TomeRater():
    def __init__(self):
        self.users = {}
        self.books = {}
        self.isbn = []

     def __repr__(self):
        print('\n')
        print("List of all the users in TomeRater:\n")
        for user in self.users.values():
            print(user)
        print("\n")
        
        print("List of all the books in TomeRater:\n")
        for book in self.books.keys():
            print(book)
        print('\n')
        
        return "Please use the following TomeRater functions:\nadd_user\ncreate_book\ncreate_novel\ncreate_non_fiction\nadd_book_to_user\nprint_catalog\nprint_users\nmost_read_book\nhighest_rated_book\nmost_positive_user\n"
   
    def __eq__(self, other):
        return self.users == other.users and self.books == other.books

    def isbn_check(self, isbn):
        bool = False
        for existing_isbn in self.isbn:
            if isbn == existing_isbn:
                bool = True
                break
        return bool

    def create_book(self, title, isbn):
        if not self.isbn_check(isbn):
            new_book = Book(title, isbn)
            self.isbn.append(isbn)
            return new_book
        else:
            return "There is already an existing book with this ISBN number!  Please ensure that the ISBN number is uique!"

    def create_novel(self, title, author, isbn):
        new_fiction = Fiction(title, author, isbn)
        return new_fiction

    def create_non_fiction(self, title, subject, level, isbn):
        new_non_fiction = Non_Fiction(title, subject, level, isbn)
        return new_non_fiction
    
    def add_book_to_user(self, book, email, rating = "None"):
        user_occurrence = 0
        for user_email, user in self.users.items():
            if user_email == email and rating != "None":
                user.read_book(book, rating)
                book.add_rating(rating)
                user_occurrence += 1
            elif user_email == email and rating == "None":
                user.read_book(book)
                user_occurrence += 1

            book_occurrence = 0
            for book_item in self.books.keys():
                if book == book_item:
                    self.books[book_item] += 1
                    book_occurrence += 1
            if book_occurrence == 0:
                self.books[book] = 1
        
        if user_occurrence == 0:
            return "No user with email {email}!".format(email=email)

    def email_check(self, email):
        domain_check = False
        atsign_check = False
        if email.find('.com') > 0 or email.find('.edu') > 0 or email.find('.org') > 0:
            domain_check = True
        else:
            domain_check = False

        for char in email:
            if char == '@':
                atsign_check = True
                break
        if domain_check == True and atsign_check == True:
            return True
        else:
            return False
        
    def user_check(self, email):
        bool = False
        for user_email in self.users.keys():
            if email == user_email:
                bool = True
                break
        return bool

    def add_user(self, name, email, user_books = 'None'):
        if not self.email_check(email):
            return "Please provide a valid email address!"
        if not self.user_check(email):
            new_user = User(name, email)
            self.users[new_user.email] = new_user
            if user_books != 'None':
                for book in user_books:
                    self.add_book_to_user(book, new_user.email)
        else:
            return "User already exists!"

    def print_catalog(self):
        for book in self.books.keys():
            print(book)

    def print_users(self):
        for user in self.users.values():
            print(user)

    def most_read_book(self):
        highest_read = 0
        most_read_book = ''
        for book, read_value in self.books.items():
            if read_value > highest_read:
                highest_read = read_value
                most_read_book = book
        return most_read_book

    def highest_rated_book(self):
        highest_rating = 0
        highest_rated = []
        for book in self.books.keys():
            if book.get_average_rating() > highest_rating:
                highest_rating = book.get_average_rating()
        for book in self.books.keys():
            if book.get_average_rating() == highest_rating:
                highest_rated.append(book)
        for book in highest_rated:
            print(book)            
        
    def most_positive_user(self):
        highest_user_rating = 0
        most_positive = []
        for user in self.users.values():
            if user.get_average_rating() > highest_user_rating:
                highest_user_rating = user.get_average_rating()
        for user in self.users.values():
            if user.get_average_rating() == highest_user_rating:
                most_positive.append(user)
        for user in most_positive:
            print(user)
