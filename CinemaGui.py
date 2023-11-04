import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from tkcalendar import Calendar
from PIL import Image, ImageTk
from CinemaController import Cinema
from datetime import date, datetime


class FirstPage(tk.Frame):
    def __init__(self, parent, app, cinema):
        tk.Frame.__init__(self, parent)
        self.app = app
        self.cinema = cinema

        # Create a frame for the top section (welcome label)
        top_frame = tk.Frame(self)
        top_frame.pack(side="top", fill="x")

        # Create a label for the "Welcome" message
        welcome_label = tk.Label(top_frame, text="Welcome to Lincoln Cinemas", font=("Arial Bold", 30))
        welcome_label.pack()

        # Create a paragraph label with additional information
        welcome_paragraph = tk.Label(top_frame, text="Please click on the movie title to view the details and schedules. Please log in or register for booking.", font=("Arial", 14))
        welcome_paragraph.pack()

        # Create a frame for the middle section (list boxes)
        middle_frame = tk.Frame(self)
        middle_frame.pack(pady=10)

        # Label for "Current Movies"
        current_movies_label = tk.Label(middle_frame, text="Current Movies", font=("Arial Bold", 20))
        current_movies_label.grid(row=0, column=0, padx=10)

        # Create a list box for current movies
        self.movie_listbox = tk.Listbox(middle_frame, width=30, height=10)
        self.movie_listbox.grid(row=1, column=0, padx=10)

        # Create a button for "View Selected Movie"
        view_button = tk.Button(middle_frame, text="View Selected Movie", font=("Arial", 15), command=self.view_movie)
        view_button.grid(row=2, column=0, padx=10)

        # Label for "Movie Details"
        movie_details_label = tk.Label(middle_frame, text="Movie Details", font=("Arial Bold", 20))
        movie_details_label.grid(row=0, column=1, padx=10)

        # Create a list box for movie details
        self.details_listbox = tk.Listbox(middle_frame, width=30, height=10)
        self.details_listbox.grid(row=1, column=1, padx=10)

        # Label for "Movie Schedules"
        schedules_label = tk.Label(middle_frame, text="Movie Schedules", font=("Arial Bold", 20))
        schedules_label.grid(row=0, column=2, padx=10)

        # Create a list box for movie schedules
        self.schedules_listbox = tk.Listbox(middle_frame, width=30, height=10)
        self.schedules_listbox.grid(row=1, column=2, padx=10)

        # Create a frame for the search input, paragraph, and button
        search_frame = tk.Frame(self)
        search_frame.pack(pady=10)

        # Create a label for the search paragraph
        search_paragraph = tk.Label(search_frame, text="Search by Title, Language, or Genre:", font=("Arial", 14))
        search_paragraph.grid(row=0, column=0, padx=10)

        # Create an entry for user input
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.grid(row=1, column=0, padx=10)

        # Create a button for "Search Movies" under the input bar
        search_button = tk.Button(search_frame, text="Search Movies", font=("Arial", 15), command=self.search_movies)
        search_button.grid(row=1, column=1, padx=10)

        # Create a frame for the bottom section (log in and register buttons)
        bottom_frame = tk.Frame(self)
        bottom_frame.pack()

        # Create login and register buttons in the bottom section
        login_button = tk.Button(bottom_frame, text="Log In", font=("Arial", 15), command=self.log_in)
        login_button.pack(side="left", padx=10)

        register_button = tk.Button(bottom_frame, text="Register as a New Customer", font=("Arial", 15), command=self.register_member)
        register_button.pack(side="left", padx=10)

        # Read movie information file
        self.read_movie_info_file("movie_info.txt")

        # Read movie information file and populate the movie listbox with titles
        self.populate_movie_list()

        # Read hall information file 
        self.read_hall_file("hall.txt")
        
        # Read screening information file 
        self.read_screening_file("screening.txt")

        # Create customer by reading the credential file
        self.read_credential_file()

        # Create booking by reading the booking file 
        self.read_booking_file("booking.txt")

    def read_movie_info_file(self, file_name):
        try:
            with open(file_name, "r") as file:
                # Read all lines from the file
                lines = file.readlines()

                # Initialize an empty list to store movie titles
                titles = []
                result = ""

                # Process each line to extract movie details
                for line in lines:
                    movie_info = line.strip().split(',')
                    if len(movie_info) == 7:
                        title, description, durationMins, language, releaseDateStr, country, genre = movie_info
                        releaseDate = datetime.strptime(releaseDateStr, "%Y-%m-%d")

                        self.cinema.add_movie(title, description, int(durationMins), language, releaseDate, country, genre)
                        #titles.append(title)  # Append the title to the titles list    

        except FileNotFoundError:
            messagebox.showinfo("File Read Unsuccesfull!")
    
    def read_hall_file(self, file_name):
        try:
            with open(file_name, "r") as file:
                lines = file.readlines()

                for line in lines:
                    hall_info = line.strip().split(',')
                    if len(hall_info) == 3:
                        name, totalSeats, seats_str = hall_info
                        totalSeats = int(totalSeats)
                    
                        # Parse the seats information from the string
                        seats_list = seats_str.split(';')
                        listOfSeats = []

                        for seat_info in seats_list:
                        
                            seat_data = seat_info.split(':')
                
                            if len(seat_data) == 4:
                                seatNumber, seatColumn, isReserved_str, seatPrice = seat_data
                                
                                # Convert isReserved_str to a boolean
                                isReserved = isReserved_str.lower() == "true"
                                
                                seat = self.cinema.create_seat(int(seatNumber), seatColumn, isReserved, float(seatPrice))
                                #print('seat created')
                                listOfSeats.append(seat)

                        # Create a Hall object with the parsed information
                        self.cinema.create_hall(name, totalSeats, listOfSeats)

        except FileNotFoundError:
            messagebox.showinfo("Error", "Hall file not found.")

        except Exception as e:
            messagebox.showinfo("Error", f"An error occurred while reading the hall file: {str(e)}")

    def read_screening_file(self, file_name):
        try:
            with open(file_name, "r") as file:
                lines = file.readlines()

                for line in lines:
                    screening_info = line.strip().split(',')
                    if len(screening_info) == 5:
                        title, screeningDateStr, startTimeStr, endTimeStr, hall_name = screening_info

                        screeningDate = datetime.strptime(screeningDateStr, "%Y-%m-%d")
                        startTime = datetime.strptime(startTimeStr, "%H:%M")
                        endTime = datetime.strptime(endTimeStr, "%H:%M")

                        # Find the corresponding Hall object based on the hall_name
                        hall = None
                        for h in self.cinema.hallList:
                            if h.name == hall_name:
                                hall = h
                                break
                        
                        screening = self.cinema.add_screening(screeningDate, startTime, endTime, hall)
                        # Map the screening number to the movie title
                        self.cinema.screening_to_movie[screening.screeningID] = title

                        # You can add the screening to the corresponding movie by matching the movie's title
                        movies = self.cinema.get_all_movies()
                        for movie in movies:
                            if movie.title == title:
                                movie.addScreening(screening)

        except FileNotFoundError:
            messagebox.showinfo("Screening file not found.")

        except Exception as e:
            messagebox.showinfo("An error occurred while reading the screening file:", str(e))
    
    def read_credential_file(self): 
        try:
            with open("credential.txt", "r") as f:
                info = f.readlines()
                i = 0
                for e in info:
                    username, password, name, role = e.strip().split(",")
                    if role == "customer":
                        self.cinema.create_customer(name, username, password)        
        except:
            messagebox.showinfo("Error", "Credential file not found.")
    
    def read_booking_file(self, file_name):
        try:
            with open(file_name, "r") as file:
                lines = file.readlines()

                for line in lines:
                    booking_info = line.strip().split(',')
                    if len(booking_info) == 5:
                        customer_name, screening_number_str, seats_str, order_total_str,payment_method = booking_info

                        customer = self.cinema.find_customer_by_name(customer_name)
                        screening = self.cinema.find_screening_by_screening_number(int(screening_number_str))
                        order_total = float(order_total_str)

                        # Parse the seats information from the string
                        seats = []
                        seat_ids = [int(seat_id) for seat_id in seats_str.split(':')]
                        #print(seat_ids)
                        for seatID in seat_ids:
                            seat = self.cinema.find_seat_by_id(seatID)
                            #print(seat)
                            if seat is not None:
                                seats.append(seat)
                                
                        screening.bookSeats(seats)

                        # Create a Booking object with the parsed information
                        booking = self.cinema.create_booking(customer, screening, seats, order_total, payment_method)

        except FileNotFoundError:
            messagebox.showinfo("Booking file not found.")

        except Exception as e:
            messagebox.showinfo("An error occurred while reading the booking file:", str(e))
    
    def populate_movie_list(self):
        # Get a list of movie objects from the Cinema class
        movies = self.cinema.get_all_movies()

        # Clear the previous list box entries
        self.movie_listbox.delete(0, tk.END)

        # Populate the movie listbox with titles
        for movie in movies:
            self.movie_listbox.insert(tk.END, movie.title)

    def view_movie(self):
        #print("View Movie button clicked")  # Add this line
        # Get the selected item(s) from the movie_listbox
        selected_indices = self.movie_listbox.curselection()
        #print("Selected indices:", selected_indices) 
        if selected_indices:
            # Get the selected movie's title (using the first selected index)
            selected_index = selected_indices[0]
            selected_title = self.movie_listbox.get(selected_index)

            # Search for the selected movie using the title and the Cinema class
            movie = self.cinema.view_movie(selected_title)

            if movie is not None:
                # Clear the details_listbox and schedules_listbox
                self.details_listbox.delete(0, tk.END)
                self.schedules_listbox.delete(0, tk.END)

                # Populate the details_listbox with the selected movie's details
                details = movie.view_movie()
                
                # Insert the movie details into details_listbox
                for line in details:
                    self.details_listbox.insert(tk.END, line)
                
                # Get the list of screenings for the selected movie
                screenings = movie.getScreenings()    
                if screenings:
                # Populate the schedules_listbox with screening details
                    for screening in screenings:
                        
                        schedule_info = [
                            f"Screening Number: {screening.screeningID}",
                            f"Screening Date: {screening.screeningDate.strftime('%d-%m-%Y')}",
                            f"Start Time: {screening.startTime.strftime('%H:%M')}",
                            f"End Time: {screening.endTime.strftime('%H:%M')}",
                            f"Hall: {screening.hall.name}",
                            f" "
                        ]
                        for line in schedule_info:
                            self.schedules_listbox.insert(tk.END, line)
                else:
                    # If no screening, for example, a newly added movie.
                    schedule_info = "No available screening for this movie."
                    self.schedules_listbox.insert(tk.END, schedule_info)            
            else:
                # If the movie is not found, clear the details_listbox
                self.details_listbox.delete(0, tk.END)
        else:
            # If no movie is selected, clear the details_listbox and schedules
            self.details_listbox.delete(0, tk.END)
            self.schedules_listbox.delete(0, tk.END)
      
    def search_movies(self):
        # Get the search query from the entry
        search_query = self.search_entry.get()
    
        if search_query:
            matching_movies = []
            # Try searching by title
            matching_movies.extend(self.cinema.searchMovieTitle(search_query))

            # Try searching by language
            matching_movies.extend(self.cinema.searchMovieLang(search_query))
            
            # Try searching by genre
            matching_movies.extend(self.cinema.searchMovieGenre(search_query))

            # Clear the details_listbox
            self.details_listbox.delete(0, tk.END)
            # Clear the schedules_listbox
            self.schedules_listbox.delete(0, tk.END)

            # Display the matching movies in the details_listbox
            if matching_movies:
                for movie in matching_movies:
                    details = movie.view_movie()
                    #self.details_listbox.insert(tk.END, f"Title: {movie.title}")
                    for line in details:
                        self.details_listbox.insert(tk.END, line)
                    self.details_listbox.insert(tk.END, "\n")

                    # Get the list of screenings for the selected movie
                    screenings = movie.getScreenings()
                    if screenings:
                        for screening in screenings:
                            schedule_info = [
                                f"Movie Title: {movie.title}",
                                f"Screening Number: {screening.screeningID}",
                                f"Screening Date: {screening.screeningDate.strftime('%d-%m-%Y')}",
                                f"Start Time: {screening.startTime.strftime('%H:%M')}",
                                f"End Time: {screening.endTime.strftime('%H:%M')}",
                                f"Hall: {screening.hall.name}",
                                f" "
                            ]
                            for line in schedule_info:
                                self.schedules_listbox.insert(tk.END, line)
            else:  
                # If no matching movies were found, display a message
                self.details_listbox.insert(tk.END, "No matching movies found.")       
        else:
            messagebox.showinfo("Error", "Please input a valid title, langague or genre.")

    def register_member(self):
        self.app.show_frame(SecondPage)

    def log_in(self):
        self.app.show_frame(SecondPage)

class SecondPage(tk.Frame):
    def __init__(self,parent, app, cinema):
        tk.Frame.__init__(self, parent)
        self.app = app
        self.cinema = cinema

        border = tk.LabelFrame(self, text="Login", bg='ivory', bd=10, font=('Arial, 20'))
        border.pack(fill="both", expand="yes", padx= 100, pady=150)

        L1 = tk.Label(border, text="Username", font=("Arial Bold", 15), bg='ivory')
        L1.place(x=50, y=20)
        T1 = tk.Entry(border, width=30, bd=5)
        T1.place(x=180, y=20)

        L2 = tk.Label(border, text="Password", font=("Arial Bold", 15), bg='ivory')
        L2.place(x=50, y=80)
        T2 = tk.Entry(border, width=30, show='*', bd=5)
        T2.place(x=180, y=80)

        def verify():
            uname = T1.get()
            pswd = T2.get()
            try:
                with open("credential.txt", "r") as f:
                    info = f.readlines()
                    i = 0
                    for e in info:
                        u, p, name, role = e.strip().split(",")  # Role is stored in the credential file
                        if u == uname and p == pswd:
                            if role == "customer":
                                #print(name)
                                # Inside SecondPage when login is successful
                                self.app.set_customer_name(name)
                                self.app.show_frame(ThirdPage)  # Show ThirdPage for customers
                                # Call a method or callback to update booking list in ThirdPage
                                self.app.frames[ThirdPage].update_booking_list()

                            elif role == "frontDesk":
                                self.app.show_frame(FourthPage)  # Show FourthPage for frontDeskStaff
                            else:
                                self.app.show_frame(FifthPage)   # Show FifthPage for admins 
                            i = 1
                            break
                    if i == 0:
                        messagebox.showinfo("Error", "Incorrect Username and Password")
            except:
                messagebox.showinfo("Error", "Incorrect Username and Password")

        B1 = tk.Button(border, text="Submit", font=("Arial",15), command = verify)
        B1.place(x=320, y=115)

        def register():
            window = tk.Tk()
            window.resizable(0, 0)
            window.configure(bg="deep sky blue")
            window.title("Register")

            l1 = tk.Label(window, text="Username:", font=("Arial", 15), bg="deep sky blue")
            l1.place(x=10, y=10)
            t1 = tk.Entry(window, width=30, bd=5)
            t1.place(x=200, y=10)

            l2 = tk.Label(window, text="Password:", font=("Arial", 15), bg="deep sky blue")
            l2.place(x=10, y=60)
            t2 = tk.Entry(window, width=30, bd=5, show="*")
            t2.place(x=200, y=60)

            l3 = tk.Label(window, text="Confirm Password:", font=("Arial", 15), bg="deep sky blue")
            l3.place(x=10, y=110)
            t3 = tk.Entry(window, width=30, bd=5, show="*")
            t3.place(x=200, y=110)

            l4 = tk.Label(window, text="Name:", font=("Arial", 15), bg="deep sky blue")
            l4.place(x=10, y=160)
            t4 = tk.Entry(window, width=30, bd=5)
            t4.place(x=200, y=160)

            def check():
                if t1.get() != "" and t2.get() != "" and t3.get() != "" and t4.get() != "":
                    if t2.get() == t3.get():
                        with open("credential.txt", "a") as f:
                            f.write(t1.get() + "," + t2.get() + "," + t4.get() +","+"customer"+"\n")
                            
                            # when registering, create a customer object in CinemaController
                            name = t4.get()
                            username = t1.get()
                            password = t2.get()
                            self.cinema.create_customer(name, username, password)
                            
                            messagebox.showinfo("Welcome", "Successfully Registered")
                    else:
                        messagebox.showinfo("Error", "Password did not match")
                else:
                    messagebox.showinfo("Error", "Please complete all fields")

            b1 = tk.Button(window, text="Sign In", font=("Arial", 15), bg="yellow", command=check)
            b1.place(x=170, y=210)  # Adjusted the placement of the "Sign In" button

            window.geometry("550x250")  # Adjusted the window size to accommodate the new input field
            window.mainloop()

        B2 = tk.Button(self, text="Register", bg='dark orange', font=("Arial",15), command = register)
        B2.place(x=650, y=20)
        
        # Create a button to go back to the first page
        back_to_first_button = tk.Button(self, text="Back to First Page", font=("Arial", 15), command=self.back_to_first)
        back_to_first_button.place(x=10, y=10)
        
    def back_to_first(self):
        # Switch back to the first page when the "Back to First Page" button is clicked
        self.app.show_frame(FirstPage)  # Use controller to access the show_frame method

class ThirdPage(tk.Frame):
    def __init__(self, parent, app, cinema):
        tk.Frame.__init__(self, parent)
        self.app = app
        self.cinema = cinema

        # Create a label for "Welcome Customer" at the top
        welcome_label = tk.Label(self, text="Welcome Customer", font=("Arial Bold", 20))
        welcome_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Create a welcome paragraph label with additional information
        welcome_paragraph = tk.Label(self, text="We're glad to have you at Lincoln Cinemas. "
                                                "Click on the screening number for booking, then press button 'Book Selected Screening'.", font=("Arial", 14))
        welcome_paragraph.grid(row=1, column=0, columnspan=3, pady=10)

        # Create a frame for the middle section (list boxes)
        middle_frame = tk.Frame(self)
        middle_frame.grid(row=2, column=0, columnspan=3, pady=10)

        # Create a list box for current movies
        current_movies_label = tk.Label(middle_frame, text="Current Movies", font=("Arial Bold", 20))
        current_movies_label.grid(row=0, column=0, padx=10)

        self.movie_listbox = tk.Listbox(middle_frame, width=30, height=10, selectmode=tk.SINGLE)
        self.movie_listbox.grid(row=1, column=0, padx=10)

        # Create a list box for movie details
        movie_details_label = tk.Label(middle_frame, text="Movie Details", font=("Arial Bold", 20))
        movie_details_label.grid(row=0, column=1, padx=10)

        self.details_listbox = tk.Listbox(middle_frame, width=30, height=10)
        self.details_listbox.grid(row=1, column=1, padx=10)

        # Create a list box for movie schedules
        schedules_label = tk.Label(middle_frame, text="Movie Schedules", font=("Arial Bold", 20))
        schedules_label.grid(row=0, column=2, padx=10)

        self.schedules_listbox = tk.Listbox(middle_frame, width=30, height=10, selectmode=tk.SINGLE)
        self.schedules_listbox.grid(row=1, column=2, padx=10)

        # Create a frame for the customer's actions
        actions_frame = tk.Frame(self)
        actions_frame.grid(row=3, column=0, columnspan=3, pady=10)

        # Place the "View Movie," "Book Selected Screening," and "Cancel Booking" buttons under the list boxes
        view_button = tk.Button(actions_frame, text="View Selected Movie", font=("Arial", 15), command=self.view_movie)
        view_button.grid(row=0, column=0, padx=10)

        make_booking_button = tk.Button(actions_frame, text="Book Selected Screening", font=("Arial", 15), command=self.book_screening)
        make_booking_button.grid(row=0, column=1, padx=10)

        cancel_booking_button = tk.Button(actions_frame, text="Cancel Booking", font=("Arial", 15), command=self.cancel_booking)
        cancel_booking_button.grid(row=0, column=2, padx=10)
        
        # Create a list box for customer's bookings
        bookings_label = tk.Label(self, text="Your Bookings", font=("Arial Bold", 20))
        bookings_label.grid(row=4, column=0, columnspan=3, pady=10)

        self.bookings_listbox = tk.Listbox(self, width=90, height=5)
        self.bookings_listbox.grid(row=5, column=0, columnspan=3, pady=10)

        # Create a button to log out
        log_out_button = tk.Button(self, text="Log Out", font=("Arial", 15), command=self.log_out)
        log_out_button.grid(row=6, column=0, columnspan=3, pady=10)

        # Read movie information file and populate the movie listbox with titles
        self.populate_movie_list()
       
    def update_booking_list(self):
        # Clear the previous list box entries
        self.bookings_listbox.delete(0, tk.END)

        # Get a list of booking objects from the Cinema class
        customer_name = self.app.customer_name
        if customer_name is not None:
            customer = self.cinema.find_customer_by_name(customer_name) 

            if customer in self.cinema.customer_bookings:
                customer_bookings = self.cinema.customer_bookings[customer]
                booking_texts = []  # Accumulate booking information here

                for booking in customer_bookings:
                    # Extract the relevant booking information
                    movie_title = self.cinema.find_movie_by_screening_number(booking.screening.screeningID)
                    hall_name = booking.screening.hall.name
                    screening_date = booking.screening.screeningDate.strftime('%d-%m-%Y')
                    start_time = booking.screening.startTime.strftime('%H:%M')
                    end_time = booking.screening.endTime.strftime('%H:%M')
                    booked_seat_numbers = ", ".join([f"{seat.seatNumber}{seat.seatColumn}" for seat in booking.seats])
                    order_total = booking.orderTotal

                    # Create a string with booked seat numbers and other booking details
                    booking_text = (
                        f"Booking ID: {booking.bookingNum}, Customer: {booking.customer.name}, Movie: {movie_title}, "
                        f"Hall: {hall_name}, Seats: {booked_seat_numbers}, "
                        f"Date: {screening_date}, Time: {start_time}-{end_time}, Fee: ${order_total}"
                    )
                
                    booking_texts.append(booking_text)  # Add the booking text to the list

                # Insert the accumulated booking details into the bookings_listbox
                for text in booking_texts:
                    self.bookings_listbox.insert(tk.END, text)
    
    def populate_movie_list(self):
        # Get a list of movie objects from the Cinema class
        movies = self.cinema.get_all_movies()
        # Clear the previous list box entries
        self.movie_listbox.delete(0, tk.END)
        # Populate the movie listbox with titles
        for movie in movies:
            self.movie_listbox.insert(tk.END, movie.title)
    
    def view_movie(self):
        #print("View Movie button clicked")  # Add this line
        # Get the selected item(s) from the movie_listbox
        selected_indices = self.movie_listbox.curselection()
        #print("Selected indices:", selected_indices) 
        if selected_indices:
            # Get the selected movie's title (using the first selected index)
            selected_index = selected_indices[0]
            selected_title = self.movie_listbox.get(selected_index)

            # Search for the selected movie using the title and the Cinema class
            movie = self.cinema.view_movie(selected_title)

            if movie is not None:
                # Clear the details_listbox and schedules_listbox
                self.details_listbox.delete(0, tk.END)
                self.schedules_listbox.delete(0, tk.END)

                # Populate the details_listbox with the selected movie's details
                details = movie.view_movie()
                
                # Insert the movie details into details_listbox
                for line in details:
                    self.details_listbox.insert(tk.END, line)

                # Get the list of screenings for the selected movie
                screenings = movie.getScreenings()    
                if screenings:
                
                # Populate the schedules_listbox with screening details
                    for screening in screenings:
                        schedule_info = [
                            f"Screening Number: {screening.screeningID} (Click me to BOOK)",
                            f"Screening Date: {screening.screeningDate.strftime('%d-%m-%Y')}",
                            f"Start Time: {screening.startTime.strftime('%H:%M')}",
                            f"End Time: {screening.endTime.strftime('%H:%M')}",
                            f"Hall: {screening.hall.name}",
                            f" "
                        ]

                        for line in schedule_info:
                            self.schedules_listbox.insert(tk.END, line)
                else:
                    # If no screening, for example, a newly added movie.
                    schedule_info = "No available screening for this movie."
                    self.schedules_listbox.insert(tk.END, schedule_info)   
            else:
                # If the movie is not found, clear the details_listbox
                self.details_listbox.delete(0, tk.END)
        else:
            # If no movie is selected, clear the details_listbox and schedules
            self.details_listbox.delete(0, tk.END)
            self.schedules_listbox.delete(0, tk.END)

    def book_screening(self):
        selected_indices_screening = self.schedules_listbox.curselection()
        if not selected_indices_screening:
            messagebox.showinfo("Error", "Please select a screening.")
            return

        # Get the selected screening details
        selected_screening_index = selected_indices_screening[0]
        selected_screening = self.schedules_listbox.get(selected_screening_index)

        # Extract the "Screening Number" from the selected screening details
        screening_number_line = selected_screening.split('\n')[0]
        screening_number_str = screening_number_line.split(": ")[1].split()[0]

        try:
            screening_number = int(screening_number_str)
        except ValueError:
            messagebox.showinfo("Invalid screening number:", screening_number_str)
            return

        # Retrieve the selected screening
        screening = self.cinema.find_screening_by_screening_number(screening_number)

        if screening is None:
            messagebox.showinfo("Error", "Selected screening not found.")
            return
        # Create a pop-up window for booking with customer name input
        booking_window = tk.Toplevel(self)
        booking_window.title("Booking")

        # Create entry field for the customer's name
        customer_name_label = tk.Label(booking_window, text="Confirm Customer Name:")
        customer_name_entry = tk.Entry(booking_window)
        customer_name_label.pack()
        customer_name_entry.pack()

        # Create entry field for the number of seats
        num_seats_label = tk.Label(booking_window, text="Available Seats:")
        num_seats_label.pack()

        # Get the available seats for the selected screening
        #print(screening)
        available_seats = screening.getAvailableSeats()
        #print(available_seats)

        # Create IntVar for seat selection
        selected_seats_vars = []
        seat_checkboxes = []
        for seat in available_seats:
            selected_seat_var = tk.IntVar()
            seat_checkbox = tk.Checkbutton(
                booking_window,
                text=f"Seat {seat.seatNumber}, Column {seat.seatColumn}, Price: ${seat.seatPrice}",
                variable=selected_seat_var,
            )
            selected_seats_vars.append(selected_seat_var)
            seat_checkboxes.append(seat_checkbox)
            seat_checkbox.pack()
        
        # Create a Combobox for payment method selection
        payment_method_var = tk.StringVar()
        payment_method_label = tk.Label(booking_window, text="Payment Method:")
        payment_method_combobox = ttk.Combobox(booking_window, textvariable=payment_method_var, values=["Credit Card", "Debit Card","Cash"])
        payment_method_label.pack()
        payment_method_combobox.pack()

        def confirm_booking():
            # Retrieve the user input from the entry fields
            customer_name = customer_name_entry.get()

            # Find the Customer object based on the customer name
            customer = self.cinema.find_customer_by_name(customer_name)
            if customer is None:
                messagebox.showinfo("Error", "Customer not found.")
                return
            
            # Retrieve the selected payment method from the dropdown
            selected_payment_method = payment_method_var.get()
            
            # Retrieve the selected seats based on the IntVars
            selected_seats = [available_seats[i] for i, seat_var in enumerate(selected_seats_vars) if seat_var.get()]

            if not selected_seats:
                messagebox.showinfo("Error", "Please select at least one seat.")
                return
            
            # Calculate the order total based on selected seats
            order_total = sum(seat.seatPrice for seat in selected_seats)
            
            # Create a Booking object with the retrieved information
            booking = self.cinema.make_booking(customer, screening, selected_seats, order_total, selected_payment_method)

            messagebox.showinfo("Success", "A booking has been made.")
            print(booking)
            print(self.cinema.customer_bookings)
            self.update_booking_list()  # Update the booking list

            # Close the pop-up window
            booking_window.destroy()


        confirm_button = tk.Button(booking_window, text="Confirm Booking", command=confirm_booking)
        confirm_button.pack()

    def cancel_booking(self):
         # Get the selected item(s) from the bookings_listbox
        selected_indices = self.bookings_listbox.curselection()

        if not selected_indices:
            messagebox.showinfo("Error", "Please select a booking to cancel.")
            return

        # Get the selected booking's index (using the first selected index)
        selected_index = selected_indices[0]

        # Get the text of the selected booking
        selected_booking_text = self.bookings_listbox.get(selected_index)

        # Extract the booking ID from the selected booking text
        booking_id = None
        try:
            booking_id = int(selected_booking_text.split("Booking ID: ")[1].split(",")[0])
        except ValueError:
            messagebox.showinfo("Error", "Unable to determine the Booking ID for cancellation.")
            return

        # Find the Booking object to cancel based on the Booking ID
        booking_to_cancel = self.cinema.find_booking_by_id(booking_id)  # Implement this method in your Cinema class

        if booking_to_cancel is not None:
            # Remove the booking from the Cinema class
            self.cinema.cancel_booking(booking_to_cancel)  # Implement this method in your Cinema class

            # Remove the booking from the bookings_listbox
            self.bookings_listbox.delete(selected_index)

            messagebox.showinfo("Success", "Booking has been canceled.")
            
        else:
            messagebox.showinfo("Error", "Selected booking not found.")

    def receive_notifications(self):
        # Implement this method to allow customers to receive and view notifications
        # You can use the Cinema class to retrieve and display notifications for the customer
        pass

    def log_out(self):
        # Callback to log out and update the central Cinema instance
        self.app.frames[FourthPage].update_booking_list()
        self.app.frames[FifthPage].update_booking_list()
        self.app.log_out_from_third_page()

class FourthPage(tk.Frame):
    def __init__(self, parent, app, cinema):
        tk.Frame.__init__(self, parent)
        self.app = app
        self.cinema = cinema
        self.selected_screening = None
        self.selected_customer = None

        # Create a label for "Welcome Front Desk Staff" at the top
        welcome_label = tk.Label(self, text="Welcome Front Desk Staff", font=("Arial Bold", 22))
        welcome_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Create a label for "Select a Screening" and its Combobox in the same line
        screening_label = tk.Label(self, text="Select a Screening:", font=("Arial", 15))
        screening_label.grid(row=1, column=0, padx=20, pady=10, sticky='w')
        self.screening_combobox = ttk.Combobox(self, width=50)
        self.screening_combobox.grid(row=1,column=1, padx=0, pady=0)
        self.screening_combobox.set("Select a screening")  # Initial text

        # Create a label for "Select a Customer" and its Combobox in the same line
        customer_label = tk.Label(self, text="Select a Customer:", font=("Arial", 15))
        customer_label.grid(row=2, column=0, padx=20, pady=10, sticky='w')
        self.customer_combobox = ttk.Combobox(self, width=30)
        self.customer_combobox.grid(row=2, column=0, columnspan=2, padx=(10, 20), pady=10)

        # Create a button to confirm the choice and open the seat and payment selection window
        confirm_button = tk.Button(self, text="Book This Screening", font=("Arial", 15), command=self.open_seat_payment_window)
        confirm_button.grid(row=3, column=0, columnspan=2, padx=(10, 20), pady=10)

        # Create a list box for customer's bookings
        bookings_label = tk.Label(self, text="All Bookings", font=("Arial Bold", 20))
        bookings_label.grid(row=4,  column=0, columnspan=2, padx=(10, 20), pady=10)

        self.bookings_listbox = tk.Listbox(self, width=95, height=10)
        self.bookings_listbox.grid(row=5, column=0, columnspan=3, pady=10, padx=20)

        # Create a button to cancel selected booking
        cancel_booking_button = tk.Button(self, text="Cancel Selected Booking", font=("Arial", 15), command=self.cancel_selected_booking)
        cancel_booking_button.grid(row=6, column=0, columnspan=2, padx=(10, 20), pady=10)
        
        # Create a button to log out at the very bottom
        log_out_button = tk.Button(self, text="Log Out", font=("Arial", 15), command=self.log_out)
        log_out_button.grid(row=8, column=0, columnspan=2, padx=(10, 20), pady=10)

        self.populate_customer_combobox()
        self.populate_screening_combobox()
        self.update_booking_list()  # Initial update

    def populate_screening_combobox(self):
        # Get a list of all screenings from the Cinema class
        screenings = self.cinema.screeningsList

        # Clear previous values
        self.screening_combobox.set("Select a screening")

        # Populate the screening Combobox with screening details
        screening_values = []
        for screening in screenings:
            screening_text = (
                f"Screening {screening.screeningID}, "
                f"{self.cinema.screening_to_movie[screening.screeningID]}, "
                f"{screening.screeningDate.strftime('%d-%m-%Y')} {screening.startTime.strftime('%H:%M')}-{screening.endTime.strftime('%H:%M')}, "
                f"{screening.hall.name}"
            )
            screening_values.append(screening_text)

        # Set the values of the Combobox
        self.screening_combobox["values"] = tuple(screening_values)

    def populate_customer_combobox(self):
        # Get a list of customer names from the Cinema class
        customers = self.cinema.get_all_customers()

        # Populate the customer Combobox with customer names
        self.customer_combobox["values"] = [customer.name for customer in customers]
    
    def open_seat_payment_window(self):
        # Retrieve the selected screening and customer
        selected_screening_text = self.screening_combobox.get()
        selected_customer_name = self.customer_combobox.get()

        if (
            selected_screening_text == "Select a screening"
            or selected_customer_name == "Select a customer"
        ):
            # Show an error message if a selection is not made
            tk.messagebox.showerror("Error", "Please select a customer and a screening.")
        else:
            # Split the selected screening text to extract the screening ID
            screening_id_str = selected_screening_text.split(" ")[1].strip(",")  # Remove the comma
            selected_screening = self.cinema.find_screening_by_screening_number(int(screening_id_str))
            # Find the corresponding customer object
            selected_customer = self.cinema.find_customer_by_name(selected_customer_name)

            if selected_screening and selected_customer:
                
                self.selected_screening = selected_screening
                self.selected_customer = selected_customer
                messagebox.showinfo("Success", "Customer and Screening Chosen")
                # Populate the seat Combobox based on the selected screening
                #self.populate_seat_combobox()
            else:
                tk.messagebox.showerror("Error", "Failed to find the selected customer or screening.")

        # Create a pop-up window for booking with customer name input
        booking_window = tk.Toplevel(self)
        booking_window.title("Seat and Payment")    

        # Create entry field for the number of seats
        num_seats_label = tk.Label(booking_window, text="Available Seats:")
        num_seats_label.pack()
        available_seats = selected_screening.getAvailableSeats()
        # Create IntVar for seat selection
        selected_seats_vars = []
        seat_checkboxes = []
        for seat in available_seats:
            selected_seat_var = tk.IntVar()
            seat_checkbox = tk.Checkbutton(
                booking_window,
                text=f"Seat {seat.seatNumber}, Column {seat.seatColumn}, Price: ${seat.seatPrice}",
                variable=selected_seat_var,
            )
            selected_seats_vars.append(selected_seat_var)
            seat_checkboxes.append(seat_checkbox)
            seat_checkbox.pack()
        # Create a Combobox for payment method selection
        payment_method_var = tk.StringVar()
        payment_method_label = tk.Label(booking_window, text="Payment Method:")
        payment_method_combobox = ttk.Combobox(booking_window, textvariable=payment_method_var, values=["Credit Card", "Debit Card","Cash"])
        payment_method_label.pack()
        payment_method_combobox.pack()    

        def confirm_booking():
            # Retrieve the selected payment method from the dropdown
            selected_payment_method = payment_method_var.get()
            # Retrieve the selected seats based on the IntVars
            selected_seats = [available_seats[i] for i, seat_var in enumerate(selected_seats_vars) if seat_var.get()]
            if not selected_seats:
                messagebox.showinfo("Error", "Please select at least one seat.")
                return
            
            # Calculate the order total based on selected seats
            order_total = sum(seat.seatPrice for seat in selected_seats)
            order_total_str = format(order_total, '.0f')
            # Create a Booking object with the retrieved information
            booking = self.cinema.make_booking(selected_customer, selected_screening, selected_seats, order_total, selected_payment_method)
            # Add the booking to the bookings_listbox
            # Get movie tile 
            movie_title = self.cinema.find_movie_by_screening_number(screening_id_str)
            
            # Get hall name 
            hall_name = selected_screening.hall.name
            # Get date datetime 
            d = selected_screening.screeningDate.strftime('%d-%m-%Y')
            start = selected_screening.startTime.strftime('%H:%M')
            end = selected_screening.endTime.strftime('%H:%M')
            
            # Create a string with booked seat numbers
            booked_seat_numbers = ", ".join([f"{seat.seatNumber}{seat.seatColumn}" for seat in selected_seats])

            booking_text = (
                f"Booking ID: {booking.bookingNum}, Customer: {booking.customer.name}, Movie: {movie_title}, "
                f"Hall: {hall_name}, Seats: {booked_seat_numbers}, "
                f"Date: {d}, Time: {start}-{end}, Fee: ${order_total}"
                )

            self.bookings_listbox.insert(tk.END, booking_text)
            # Write the new booking in the booking.txt
            selected_seat_ID = []
            for selected_seat in selected_seats:
                seatID = selected_seat.seatID
                selected_seat_ID.append(seatID)
            if len(selected_seat_ID) >= 1:
                try:
                    with open("booking.txt", "a") as file:
                      # Join the selected seat IDs with colons if there are multiple seats
                        seats_str = ":".join(map(str, selected_seat_ID))
                        file.write(
                            f"{selected_customer_name},{screening_id_str},{seats_str},"
                            f"{order_total_str},{selected_payment_method}\n"
                        )
                    messagebox.showinfo("Success", "A new booking has been added.")
                except Exception as e:
                    messagebox.showerror("Error writing booking details to file:", str(e))
            
            # Close the pop-up window
            booking_window.destroy()
        confirm_button = tk.Button(booking_window, text="Confirm Booking", command=confirm_booking)
        confirm_button.pack()    
    
    def cancel_selected_booking(self):
         # Get the selected item(s) from the bookings_listbox
        selected_indices = self.bookings_listbox.curselection()

        if not selected_indices:
            messagebox.showinfo("Error", "Please select a booking to cancel.")
            return

        # Get the selected booking's index (using the first selected index)
        selected_index = selected_indices[0]

        # Get the text of the selected booking
        selected_booking_text = self.bookings_listbox.get(selected_index)

        # Extract the booking ID from the selected booking text
        booking_id = None
        try:
            booking_id = int(selected_booking_text.split("Booking ID: ")[1].split(",")[0])
        except ValueError:
            messagebox.showinfo("Error", "Unable to determine the Booking ID for cancellation.")
            return

        # Find the Booking object to cancel based on the Booking ID
        booking_to_cancel = self.cinema.find_booking_by_id(booking_id)  # Implement this method in your Cinema class

        if booking_to_cancel is not None:
            # Remove the booking from the Cinema class
            self.cinema.cancel_booking(booking_to_cancel)  # Implement this method in your Cinema class
            # Read the content of "booking.txt" into a list of lines
            with open("booking.txt", "r") as file:
                lines = file.readlines()

            # Find the index of the line to be deleted
            line_index = None
            for i, line in enumerate(lines):
        
                if str(booking_id) in line:
                    line_index = i
                    print(line_index)
                    break

            if line_index is not None:
                # Remove the line from the list of lines
                del lines[line_index]

                # Write the updated list of lines back to "booking.txt"
                with open("booking.txt", "w") as file:
                    file.writelines(lines)

            # Remove the booking from the bookings_listbox
            self.bookings_listbox.delete(selected_index)

            messagebox.showinfo("Success", "Booking has been canceled.")
        else:
            messagebox.showinfo("Error", "Selected booking not found.")
    
    def log_out(self):
        self.app.show_frame(SecondPage)

    def update_booking_list(self):
        # Clear the previous list box entries
        self.bookings_listbox.delete(0, tk.END)

        # Get a list of booking objects from the Cinema class
        bookings = self.cinema.bookingList

        # Populate the bookings_listbox with booking details
        for booking in bookings:
            # Extract the relevant booking information
            movie_title = self.cinema.find_movie_by_screening_number(booking.screening.screeningID)
            #print("movie title")
            #print(movie_title)
            hall_name = booking.screening.hall.name
            screening_date = booking.screening.screeningDate.strftime('%d-%m-%Y')
            start_time = booking.screening.startTime.strftime('%H:%M')
            end_time = booking.screening.endTime.strftime('%H:%M')
            booked_seat_numbers = ", ".join([f"{seat.seatNumber}{seat.seatColumn}" for seat in booking.seats])
            order_total = booking.orderTotal

            # Create a string with booked seat numbers and other booking details
            booking_text = (
                f"Booking ID: {booking.bookingNum}, Customer: {booking.customer.name}, Movie: {movie_title}, "
                f"Hall: {hall_name}, Seats: {booked_seat_numbers}, "
                f"Date: {screening_date}, Time: {start_time}-{end_time}, Fee: ${order_total}"
            )

            # Insert the updated booking details into the bookings_listbox
            self.bookings_listbox.insert(tk.END, booking_text)
    

class FifthPage(tk.Frame):
    def __init__(self, parent, app, cinema):
        tk.Frame.__init__(self, parent)
        self.app = app
        self.cinema = cinema
        self.selected_screening = None
        self.selected_customer = None

        # Create a label for "Welcome Front Desk Staff" at the top
        welcome_label = tk.Label(self, text="Welcome Admin", font=("Arial Bold", 22))
        welcome_label.grid(row=0, column=0, columnspan=3, pady=10)

        # Create a label for "Select a Screening" and its Combobox in the same line
        screening_label = tk.Label(self, text="Select a Screening:", font=("Arial", 15))
        screening_label.grid(row=1, column=0, padx=20, pady=10, sticky='w')
        self.screening_combobox = ttk.Combobox(self, width=50)
        self.screening_combobox.grid(row=1,column=1, padx=0, pady=0)
        self.screening_combobox.set("Select a screening")  # Initial text

        # Create a label for "Select a Customer" and its Combobox in the same line
        customer_label = tk.Label(self, text="Select a Customer:", font=("Arial", 15))
        customer_label.grid(row=2, column=0, padx=20, pady=10, sticky='w')
        self.customer_combobox = ttk.Combobox(self, width=30)
        self.customer_combobox.grid(row=2, column=0, columnspan=2, padx=(10, 20), pady=10)

        # Create a button to confirm the choice and open the seat and payment selection window
        confirm_button = tk.Button(self, text="Book This Screening", font=("Arial", 15), command=self.open_seat_payment_window)
        confirm_button.grid(row=3, column=0, columnspan=2, padx=(10, 20), pady=10)

        # Create a list box for customer's bookings
        bookings_label = tk.Label(self, text="All Bookings", font=("Arial Bold", 20))
        bookings_label.grid(row=4,  column=0, columnspan=2, padx=(10, 20), pady=10)

        self.bookings_listbox = tk.Listbox(self, width=95, height=10)
        self.bookings_listbox.grid(row=5, column=0, columnspan=3, pady=10, padx=20)

        # Create a button to cancel selected booking
        cancel_booking_button = tk.Button(self, text="Cancel Selected Booking", font=("Arial", 15), command=self.cancel_selected_booking)
        cancel_booking_button.grid(row=6, column=0, columnspan=2, padx=(10, 20), pady=10)
        
        # Create buttons to perform administrative actions
        #button_padding = (10, 20)
        add_movie_button = tk.Button(self, text="Add a Movie", font=("Arial", 15), command=self.add_movie)
        add_movie_button.grid(row=7, column=0, columnspan=1, padx=0, pady=10)

        cancel_movie_button = tk.Button(self, text="Cancel a Movie", font=("Arial", 15), command=self.cancel_movie)
        cancel_movie_button.grid(row=7, column=1, columnspan=1, padx=0, pady=10)

        add_screening_button = tk.Button(self, text="Add a Screening", font=("Arial", 15), command=self.add_screening)
        add_screening_button.grid(row=8, column=0, columnspan=1, padx=0, pady=10)

        cancel_screening_button = tk.Button(self, text="Cancel a Screening", font=("Arial", 15), command=self.cancel_screening)
        cancel_screening_button.grid(row=8, column=1, columnspan=1, padx=0, pady=10)
        
        
        # Create a button to log out at the very bottom
        log_out_button = tk.Button(self, text="Log Out", font=("Arial", 15), command=self.log_out)
        log_out_button.grid(row=9, column=0, columnspan=2, padx=(10, 20), pady=10)

        self.populate_customer_combobox()
        self.populate_screening_combobox()
        
        self.update_booking_list()  # Initial update
    
    def add_movie(self):
        # Create a pop-up window for adding a movie
        add_movie_window = tk.Toplevel(self)
        add_movie_window.title("Add a Movie")

        # Create input fields for movie details
        title_label = tk.Label(add_movie_window, text="Title:")
        title_label.grid(row=0, column=0, padx=10, pady=5)
        title_entry = tk.Entry(add_movie_window)
        title_entry.grid(row=0, column=1, padx=10, pady=5)

        description_label = tk.Label(add_movie_window, text="Description:")
        description_label.grid(row=1, column=0, padx=10, pady=5)
        description_entry = tk.Entry(add_movie_window)
        description_entry.grid(row=1, column=1, padx=10, pady=5)

        duration_label = tk.Label(add_movie_window, text="Duration (Mins):")
        duration_label.grid(row=2, column=0, padx=10, pady=5)
        duration_entry = tk.Entry(add_movie_window)
        duration_entry.grid(row=2, column=1, padx=10, pady=5)

        language_label = tk.Label(add_movie_window, text="Language:")
        language_label.grid(row=3, column=0, padx=10, pady=5)
        language_entry = tk.Entry(add_movie_window)
        language_entry.grid(row=3, column=1, padx=10, pady=5)

        release_date_label = tk.Label(add_movie_window, text="Release Date:")
        release_date_label.grid(row=4, column=0, padx=10, pady=5)
        release_date_calendar = Calendar(add_movie_window, date_pattern="yyyy-mm-dd")
        release_date_calendar.grid(row=4, column=1, padx=10, pady=5)

        country_label = tk.Label(add_movie_window, text="Country:")
        country_label.grid(row=5, column=0, padx=10, pady=5)
        country_entry = tk.Entry(add_movie_window)
        country_entry.grid(row=5, column=1, padx=10, pady=5)

        genre_label = tk.Label(add_movie_window, text="Genre:")
        genre_label.grid(row=6, column=0, padx=10, pady=5)
        genre_entry = tk.Entry(add_movie_window)
        genre_entry.grid(row=6, column=1, padx=10, pady=5)

        # Create a function to save the movie details
        def save_movie_details():
            
            title = title_entry.get()
            description = description_entry.get()
            durationMins = int(duration_entry.get()) 
            language = language_entry.get()
            releaseDate_str = release_date_calendar.get_date()
            releaseDate = datetime.strptime(releaseDate_str, "%Y-%m-%d").date()
            country = country_entry.get()
            genre = genre_entry.get()
            
            try:
                durationMins = int(durationMins)  # Convert input to an integer
            except ValueError:
                messagebox.showinfo("Error", "DurationMins must be a number.")
                return  # Exit the function if 'durationMins' is not a number

            # Call a function in your Cinema class to add the movie
            movie = self.cinema.add_movie(title,description,int(durationMins),language,releaseDate,country,genre)

            # Write it in the movie_info.txt
            try:
                with open("movie_info.txt", "a") as file:
                    file.write(
                        f"{title},{description},{durationMins},{language},"
                        f"{releaseDate},{country},{genre}\n"
                    )
                    messagebox.showinfo("success","A new movie has been added.")
            except Exception as e:
                messagebox.showerror("Error writing movie details to file:", str(e))

            # Close the pop-up window
            add_movie_window.destroy()

        # Create a button to save the movie details
        save_button = tk.Button(add_movie_window, text="Save Movie", command=save_movie_details)
        save_button.grid(row=7, column=0, columnspan=2, pady=10)
    
    def cancel_movie(self):
        # Create a pop-up window for movie cancellation
        cancel_movie_window = tk.Toplevel(self)
        cancel_movie_window.title("Cancel Movie")

        # Retrieve the list of available movies from your cinema
        available_movies = self.cinema.get_all_movies()

        # Create a Listbox to display the scheduled movies
        movie_listbox = tk.Listbox(cancel_movie_window, width=30, height=10)
        for movie in available_movies:
            movie_listbox.insert(tk.END, movie.title)  # Display movie titles
        movie_listbox.pack(pady=20)

        # Create a button to confirm the cancellation
        def confirm_cancellation():
            selected_movie_index = movie_listbox.curselection()
            if not selected_movie_index:
                messagebox.showinfo("Error", "Please select a movie to cancel.")
                return

            # Get the selected movie's title
            selected_movie_index = selected_movie_index[0]  # Get the first selected index
            selected_movie_title = movie_listbox.get(selected_movie_index)

            # Implement the cancellation logic here, e.g., remove the movie from your data
            movie = self.cinema.find_movie_by_title(selected_movie_title)
            self.cinema.cancel_movie(movie)

            if movie.getScreenings():
                print(movie.getScreenings())
                # Delete the lines in the screening.txt file for this movie
                try:
                    with open("screening.txt", "r") as file:
                        lines = file.readlines()
                    with open("screening.txt", "w") as file:
                        for line in lines:
                            if selected_movie_title not in line:
                                file.write(line)
                except Exception as e:
                    messagebox.showerror("Error deleting screenings:", str(e))

            # Delete the line from the movie_info.txt file
            try:
                with open("movie_info.txt", "r") as file:
                    lines = file.readlines()
                with open("movie_info.txt", "w") as file:
                    for line in lines:
                        if selected_movie_title not in line:
                            file.write(line)

                messagebox.showinfo("Success", f"The movie: {selected_movie_title} and its screenigns have been canceled.")
            except Exception as e:
                messagebox.showerror("Error deleting the movie:", str(e))

            # Update the listbox to reflect the changes
            #self.populate_screening_combobox()
            movie_listbox.delete(selected_movie_index)
            cancel_movie_window.destroy()

        cancel_button = tk.Button(cancel_movie_window, text="Cancel Movie", command=confirm_cancellation)
        cancel_button.pack()
 
    def add_screening(self):
        # Create a pop-up window for adding a screening
        add_screening_window = tk.Toplevel(self)
        add_screening_window.title("Add a Screening")

         # Create input fields for screening details
        screening_date_label = tk.Label(add_screening_window, text="Screening Date:")
        screening_date_label.grid(row=0, column=0, padx=10, pady=5)
        screening_date_calendar = Calendar(add_screening_window, date_pattern="yyyy-mm-dd")
        screening_date_calendar.grid(row=0, column=1, padx=10, pady=5)

        start_time_label = tk.Label(add_screening_window, text="Start Time (HH:MM):")
        start_time_label.grid(row=1, column=0, padx=10, pady=5)
        start_time_entry = tk.Entry(add_screening_window)
        start_time_entry.grid(row=1, column=1, padx=10, pady=5)

        end_time_label = tk.Label(add_screening_window, text="End Time (HH:MM):")
        end_time_label.grid(row=2, column=0, padx=10, pady=5)
        end_time_entry = tk.Entry(add_screening_window)
        end_time_entry.grid(row=2, column=1, padx=10, pady=5)

        hall_label = tk.Label(add_screening_window, text="Hall:")
        hall_label.grid(row=3, column=0, padx=10, pady=5)

        # Create a combo box for selecting a hall and populate it with available halls
        hall_combobox = ttk.Combobox(add_screening_window, values=["Hall 1", "Hall 2", "Hall 3", "Hall 4"])
        hall_combobox.grid(row=3, column=1, padx=10, pady=5)

        def create_screening():
            # Retrieve the selected screening details
            screening_date_str = screening_date_calendar.get_date()
            start_time_str = start_time_entry.get()
            end_time_str = end_time_entry.get()
            selected_hall_name = hall_combobox.get()

            # Define the time format expected from the user (24-hour format)
            time_format = "%H:%M"  # HH:MM format

            try:
                screening_date = datetime.strptime(screening_date_str, "%Y-%m-%d").date()
                start_time = datetime.strptime(start_time_str, time_format)
                end_time = datetime.strptime(end_time_str, time_format)
            except ValueError:
                messagebox.showinfo("Error", "Invalid time format. Please use HH:MM 24-hour format.")

            # Find the hall object from the selected hall name
            hall = self.cinema.find_hall_by_name(selected_hall_name)

            # Create the screening object with the selected details, hall, and movie (if applicable)
            screening = self.cinema.add_screening(screening_date, start_time, end_time, hall)

            # You can handle movie association here if needed
            # Retrieve the list of available movies from your cinema
            available_movies = self.cinema.get_all_movies()

            # Create a pop-up window for movie selection
            movie_selection_window = tk.Toplevel(self)
            movie_selection_window.title("Select a Movie for Screening")

            # Create a Combobox for selecting a movie
            selected_movie_var = tk.StringVar()
            selected_movie_var.set("Select a movie")
            movie_combobox = ttk.Combobox(movie_selection_window, textvariable=selected_movie_var)
            movie_combobox['values'] = ["None"] + [movie.title for movie in available_movies]
            movie_combobox.grid(row=0, column=0, padx=10, pady=5)

            def confirm_movie_selection():
                # Retrieve the selected movie name
                selected_movie_name = selected_movie_var.get()
                #screening_date_str = screening_date.strftime("%Y-%m-%d")

                if selected_movie_name == "None":
                    messagebox.showinfo("Info", "No movie selected.")
                else:
                    movie = self.cinema.find_movie_by_title(selected_movie_name)
                    # add this movie to screening
                    self.cinema.add_movie_to_screening(screening,movie)
                    try:
                        with open("screening.txt", "a") as file:
                            file.write(
                                f"\n"
                                f"{selected_movie_name},{screening_date_str},{start_time_str},{end_time_str},{selected_hall_name}"
                            )
                        messagebox.showinfo("Sucess","A new screening has been added.")    
                        messagebox.showinfo("Success", "A movie has been associated with the a screening.")
                        self.populate_screening_combobox()
                    except Exception as e:
                        messagebox.showerror("Error writing movie details to file:", str(e))

                movie_selection_window.destroy()
                add_screening_window.destroy()

            confirm_button = tk.Button(movie_selection_window, text="Confirm Selection", command=confirm_movie_selection)
            confirm_button.grid(row=1, column=0, padx=10, pady=5)

        create_button = tk.Button(add_screening_window, text="Create Screening", command=create_screening)
        create_button.grid(row=4, column=0, columnspan=2, pady=10)

    def cancel_screening(self):
        pass

    def populate_screening_combobox(self):
        # Get a list of all screenings from the Cinema class
        screenings = self.cinema.screeningsList

        # Clear previous values
        self.screening_combobox.set("Select a screening")

        # Populate the screening Combobox with screening details
        screening_values = []
        for screening in screenings:
            screening_text = (
                f"Screening {screening.screeningID}, "
                f"{self.cinema.screening_to_movie[screening.screeningID]}, "
                f"{screening.screeningDate.strftime('%d-%m-%Y')} {screening.startTime.strftime('%H:%M')}-{screening.endTime.strftime('%H:%M')}, "
                f"{screening.hall.name}"
            )
            screening_values.append(screening_text)

        # Set the values of the Combobox
        self.screening_combobox["values"] = tuple(screening_values)

    def populate_customer_combobox(self):
        # Get a list of customer names from the Cinema class
        customers = self.cinema.get_all_customers()

        # Populate the customer Combobox with customer names
        self.customer_combobox["values"] = [customer.name for customer in customers]  

    def open_seat_payment_window(self):
        # Retrieve the selected screening and customer
        selected_screening_text = self.screening_combobox.get()
        selected_customer_name = self.customer_combobox.get()

        if (
            selected_screening_text == "Select a screening"
            or selected_customer_name == "Select a customer"
        ):
            # Show an error message if a selection is not made
            tk.messagebox.showerror("Error", "Please select a customer and a screening.")
        else:
            # Split the selected screening text to extract the screening ID
            screening_id_str = selected_screening_text.split(" ")[1].strip(",")  # Remove the comma
            selected_screening = self.cinema.find_screening_by_screening_number(int(screening_id_str))
            # Find the corresponding customer object
            selected_customer = self.cinema.find_customer_by_name(selected_customer_name)

            if selected_screening and selected_customer:
                
                self.selected_screening = selected_screening
                self.selected_customer = selected_customer
                messagebox.showinfo("Success", "Customer and Screening Chosen")
                # Populate the seat Combobox based on the selected screening
                #self.populate_seat_combobox()
            else:
                tk.messagebox.showerror("Error", "Failed to find the selected customer or screening.")

        # Create a pop-up window for booking with customer name input
        booking_window = tk.Toplevel(self)
        booking_window.title("Seat and Payment")    

        # Create entry field for the number of seats
        num_seats_label = tk.Label(booking_window, text="Available Seats:")
        num_seats_label.pack()
        available_seats = selected_screening.getAvailableSeats()
        # Create IntVar for seat selection
        selected_seats_vars = []
        seat_checkboxes = []
        for seat in available_seats:
            selected_seat_var = tk.IntVar()
            seat_checkbox = tk.Checkbutton(
                booking_window,
                text=f"Seat {seat.seatNumber}, Column {seat.seatColumn}, Price: ${seat.seatPrice}",
                variable=selected_seat_var,
            )
            selected_seats_vars.append(selected_seat_var)
            seat_checkboxes.append(seat_checkbox)
            seat_checkbox.pack()
        # Create a Combobox for payment method selection
        payment_method_var = tk.StringVar()
        payment_method_label = tk.Label(booking_window, text="Payment Method:")
        payment_method_combobox = ttk.Combobox(booking_window, textvariable=payment_method_var, values=["Credit Card", "Debit Card","Cash"])
        payment_method_label.pack()
        payment_method_combobox.pack()    

        def confirm_booking():
            # Retrieve the selected payment method from the dropdown
            selected_payment_method = payment_method_var.get()
            # Retrieve the selected seats based on the IntVars
            selected_seats = [available_seats[i] for i, seat_var in enumerate(selected_seats_vars) if seat_var.get()]
            if not selected_seats:
                messagebox.showinfo("Error", "Please select at least one seat.")
                return
            
            # Calculate the order total based on selected seats
            order_total = sum(seat.seatPrice for seat in selected_seats)
            order_total_str = format(order_total, '.0f')

            # Create a Booking object with the retrieved information
            booking = self.cinema.make_booking(selected_customer, selected_screening, selected_seats, order_total, selected_payment_method)
            #print("booking made")
            # Add the booking to the bookings_listbox
            # Get movie tile 
            movie_title = self.cinema.find_movie_by_screening_number(int(screening_id_str))
            
            # Get hall name 
            hall_name = selected_screening.hall.name
            # Get date datetime 
            d = selected_screening.screeningDate.strftime('%d-%m-%Y')
            start = selected_screening.startTime.strftime('%H:%M')
            end = selected_screening.endTime.strftime('%H:%M')
            
            # Create a string with booked seat numbers
            booked_seat_numbers = ", ".join([f"{seat.seatNumber}{seat.seatColumn}" for seat in selected_seats])

            booking_text = (
                f"Booking ID: {booking.bookingNum}, Customer: {booking.customer.name}, Movie: {movie_title}, "
                f"Hall: {hall_name}, Seats: {booked_seat_numbers}, "
                f"Date: {d}, Time: {start}-{end}, Fee: ${order_total}"
                )

            self.bookings_listbox.insert(tk.END, booking_text)
            # Write the new booking in the booking.txt
            selected_seat_ID = []
            for selected_seat in selected_seats:
                seatID = selected_seat.seatID
                selected_seat_ID.append(seatID)
            if len(selected_seat_ID) >= 1:
                try:
                    with open("booking.txt", "a") as file:
                      # Join the selected seat IDs with colons if there are multiple seats
                        seats_str = ":".join(map(str, selected_seat_ID))
                        file.write(
                            f"{selected_customer_name},{screening_id_str},{seats_str},"
                            f"{order_total_str},{selected_payment_method}\n"
                        )

                    messagebox.showinfo("Success", "A new booking has been added.")
                except Exception as e:
                    messagebox.showerror("Error writing booking details to file:", str(e))
                    
            # Close the pop-up window
            booking_window.destroy()

        confirm_button = tk.Button(booking_window, text="Confirm Booking", command=confirm_booking)
        confirm_button.pack()    
    
    def cancel_selected_booking(self):
         # Get the selected item(s) from the bookings_listbox
        selected_indices = self.bookings_listbox.curselection()

        if not selected_indices:
            messagebox.showinfo("Error", "Please select a booking to cancel.")
            return

        # Get the selected booking's index (using the first selected index)
        selected_index = selected_indices[0]

        # Get the text of the selected booking
        selected_booking_text = self.bookings_listbox.get(selected_index)

        # Extract the booking ID from the selected booking text
        booking_id = None
        try:
            booking_id = int(selected_booking_text.split("Booking ID: ")[1].split(",")[0])
        except ValueError:
            messagebox.showinfo("Error", "Unable to determine the Booking ID for cancellation.")
            return

        # Find the Booking object to cancel based on the Booking ID
        booking_to_cancel = self.cinema.find_booking_by_id(booking_id)  # Implement this method in your Cinema class

        if booking_to_cancel is not None:
            # Remove the booking from the Cinema class
            self.cinema.cancel_booking(booking_to_cancel)  # Implement this method in your Cinema class

            # Read the content of "booking.txt" into a list of lines
            with open("booking.txt", "r") as file:
                lines = file.readlines()

            # Find the index of the line to be deleted
            line_index = None
            for i, line in enumerate(lines):
        
                if str(booking_id) in line:
                    line_index = i
                    print(line_index)
                    break

            if line_index is not None:
                # Remove the line from the list of lines
                del lines[line_index]

                # Write the updated list of lines back to "booking.txt"
                with open("booking.txt", "w") as file:
                    file.writelines(lines)

            # Remove the booking from the bookings_listbox
            self.bookings_listbox.delete(selected_index)

            messagebox.showinfo("Success", "Booking has been canceled.")
        else:
            messagebox.showinfo("Error", "Selected booking not found.")
    
    def log_out(self):
        # Notify the FourthPage to update its booking list
        self.app.frames[FourthPage].update_booking_list()
        # Notify the First and Third Page to update movie list
        self.app.frames[FirstPage].populate_movie_list()
        self.app.frames[ThirdPage].populate_movie_list()
        # Switch back to the login page when the Front Desk Staff logs out
        self.app.show_frame(SecondPage)

    def update_booking_list(self):
        # Clear the previous list box entries
        self.bookings_listbox.delete(0, tk.END)

        # Get a list of booking objects from the Cinema class
        bookings = self.cinema.bookingList

        # Populate the bookings_listbox with booking details
        for booking in bookings:
            # Extract the relevant booking information
            movie_title = self.cinema.find_movie_by_screening_number(booking.screening.screeningID)
            #print("movie title")
            #print(movie_title)
            hall_name = booking.screening.hall.name
            screening_date = booking.screening.screeningDate.strftime('%d-%m-%Y')
            start_time = booking.screening.startTime.strftime('%H:%M')
            end_time = booking.screening.endTime.strftime('%H:%M')
            booked_seat_numbers = ", ".join([f"{seat.seatNumber}{seat.seatColumn}" for seat in booking.seats])
            order_total = booking.orderTotal

            # Create a string with booked seat numbers and other booking details
            booking_text = (
                f"Booking ID: {booking.bookingNum}, Customer: {booking.customer.name}, Movie: {movie_title}, "
                f"Hall: {hall_name}, Seats: {booked_seat_numbers}, "
                f"Date: {screening_date}, Time: {start_time}-{end_time}, Fee: ${order_total}"
            )

            # Insert the updated booking details into the bookings_listbox
            self.bookings_listbox.insert(tk.END, booking_text)

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Container to hold all the pages
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Create an instance of the Cinema class
        self.cinema = Cinema("Lincoln Cinemas")

        self.customer_name = None  # Initialize customer_name as None

        for F in (FirstPage, SecondPage, ThirdPage, FourthPage, FifthPage):
            frame = F(container, self, self.cinema)  # Pass the cinema instance and the app instance to the frames
            
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(FirstPage)
    
    def set_customer_name(self, customer_name):
        self.customer_name = customer_name
        
    def log_out_from_third_page(self):
        # This callback is called when logging out from ThirdPage
        # Ensure the central Cinema instance is updated with the latest booking information
        self.cinema = self.frames[ThirdPage].cinema
        self.show_frame(SecondPage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        self.title("Lincoln Cinemas")
    

if __name__ == "__main__":
    app = Application()
    app.geometry("900x620")
    app.title("Lincoln Cinemas")
    app.mainloop()
