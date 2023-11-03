"""! @brief Lincoln Cinemas e-Ticketing System """

##
# @mainpage Lincoln Cinemas e-Ticketing Project 
#
# @section description_main Description 
# The management of Lincoln Cinemas is keen to develop an online movie ticket system 
# that can facilitate the purchase of movie tickets by its customers. 
# This e-ticketing system will allow customers to browse through the movies currently playing and book seats for screenings, anywhere and anytime.
#
# @section notes_main Notes
# This is just the design not the final codes.

##
# @file Cinema.py
#
# @brief This file defines the class Cinema and this is the controller of the application.
#
# @section description_Cinema Description
# The class Cinema will create the instance of the cinema. This class will create users and
# handles the interaction between users (Admin, Front Desk Staff, Customer, Guest) and the system. 
# It contains methods to facilitate the scenarios described in the requirements.
#
# @section notes_Cinema Notes 
# This is just the design not the final codes.
#
# @section author_Cinema Author 
# Created by Dora Wang on 24 September 2023 

# Imports 
from typing import List, Dict, Union, Optional
from datetime import date, datetime
from User import User,Customer, FrontDeskStaff, Admin
from Movie import Movie
from Screening import Screening
from Seat import Seat
from Booking import Booking
from Hall import Hall
from Notification import Notification 

class Cinema:
    """! The Cinema class 
    Defines all the methods for the controller
    """
    def __init__(self, cinema_name: str):
        """! The class initialiser
        """
        self.cinema_name = cinema_name
        # A dictionary to store user data (username -> User object)
        self.users = {} 
        self.customers = {}  # A dictionary to store customers
        self.notificationsList = {}  # A dictionary to store notifications for each customer
        # Create a dictionary to map screening numbers to movie titles
        self.screening_to_movie = {}
        # A list of movie objects 
        self.moviesList: List[Movie] = []  
        # A list of screening objects
        self.screeningsList: List[Screening] = []   
        # A list of booking objects 
        self.bookingList: List[Booking] = []
        # A list of hall objects 
        self.hallList: List[Hall] = []
        # Initialize a list to store Seat objects
        self.seatsList: List[Seat] = []

        self.customer_bookings = {}  # A dictionary to store bookings for each customer

    
    def create_customer(self,  name: str, username: str, password: str) -> None:
        """! Creates an instance of Customer """
        # Create a new Customer and add it to the users dictionary
        customer = Customer(name, username, password)
        self.users[username] = customer
        self.customers[username] = customer
       

    def get_all_customers(self):
        return list(self.customers.values())

    def create_seat(self,seatNumber, seatColumn, isReserved,seatPrice):
        seat = Seat(seatNumber, seatColumn, isReserved,seatPrice)
        self.seatsList.append(seat)
        return seat

    def create_hall(self, name, totalSeats,listOfSeats):
        hall = Hall(name, totalSeats, listOfSeats)
        #  Add the hall to the cinema
        self.hallList.append(hall)
        return hall
    
    def create_booking(self, customer: Customer, aScreening: Screening, seats: List[Seat], orderTotal: float, paymentDetail: str):
        booking = Booking(customer, aScreening, seats, orderTotal, paymentDetail)
    
        # Add the booking to the global booking list
        self.bookingList.append(booking)
    
        # Associate the booking with the customer
        if customer not in self.customer_bookings:
            self.customer_bookings[customer] = [booking]  # Create a new list for this customer
        else:
            self.customer_bookings[customer].append(booking)  # Append to the existing list
        return booking


    def find_customer_by_name(self, customer_name: str) -> Optional[Customer]:
        """Finds a customer by their name and returns the Customer object if found, or None if not found."""
        # print(customer_name)
        # print(self.customers.items())
        # print(self.customers)
        for name, customer in self.customers.items():
            if customer.name == customer_name:
                #print(customer.name)
                return customer
        return None
    
    def get_all_movies(self) -> List[Movie]:
        return self.moviesList
    
    def find_movie_by_title(self, selected_movie_title):
        for movie in self.moviesList:
            if movie.title == selected_movie_title:
                return movie
        return None  # Return None if the movie is not found
    
    def find_seat_by_id(self, seat_id):
        for seat in self.seatsList:
            if seat.seatID == seat_id:
                return seat
        return None
    
    def searchMovieTitle(self, title: str) -> List[Movie]:
        """Search for movies by title."""
        matching_movies = []
        for movie in self.get_all_movies():  # Implement get_all_movies() to retrieve all movies
            if title.lower() in movie.title.lower():
                matching_movies.append(movie)
        return matching_movies

    def searchMovieLang(self, lang: str) -> List[Movie]:
        """Search for movies by language."""
        matching_movies = []
        for movie in self.get_all_movies():
            if lang.lower() == movie.language.lower():
                matching_movies.append(movie)
        return matching_movies

    def searchMovieGenre(self, genre: str) -> List[Movie]:
        """Search for movies by genre."""
        matching_movies = []
        normalized_genre = genre.strip().lower()  # Remove leading/trailing spaces and convert to lowercase

        for movie in self.get_all_movies():
            normalized_movie_genre = movie.genre.strip().lower()  # Normalize movie genre

            if normalized_genre == normalized_movie_genre:
                matching_movies.append(movie)
        return matching_movies


    def view_movie(self, title):
        for movie in self.moviesList:
            if movie.title == title:
                return movie  # Return the Movie object
        return None  # Return None if the movie is not found

    def add_movie(self, title: str, description: str, durationMins: int, language: str, releaseDate: datetime, country: str, genre: str):

        # Create a new Movie and add it to the list of movies
        movie = Movie(title, description, durationMins, language, releaseDate, country, genre)
        self.moviesList.append(movie)
        #print(self.moviesList)

    def get_all_movies(self):
        return self.moviesList    
    
    def find_movie_by_screening_number(self, screening_number):
        # Lookup the associated movie title using the screening number
        return self.screening_to_movie.get(screening_number, None)
    
    def add_screening(self, screeningDate: datetime, startTime: datetime, endTime: datetime, hall: Hall) -> Screening:
        # Create a new Screening and add it to the list of screenings
        screening = Screening(screeningDate, startTime, endTime, hall)
        self.screeningsList.append(screening)
        return screening
    
    def find_screening_by_screening_number(self, screening_number):
        for screening in self.screeningsList:
            if screening.screeningID == screening_number:
                return screening
        return None
    
    def cancel_movie(self, movie: Movie) -> bool:
        """! Cancels a movie and all its screenings""" 
        # Cancel a movie and all its screenings
        if movie in self.moviesList:
            self.moviesList.remove(movie)
            for screening in movie.getScreenings:
                movie.cancelScreening(screening)
            return True
        return False

    def remove_screening(self, screening: Screening) -> bool:
        """! Cancels a screening """ 
        # Remove a screening if its in the screeningList 
        if screening in self.screeningsList:
            self.screeningsList.remove(screening)
            # Them remove all the movies in that screening 
            for movie in self.moviesList:
                if screening in movie.getScreenings:
                    movie.cancelScreening(screening)
            
            return True
        return False
    
    def get_movie_schedule(self, movie: Movie) -> List[Screening]:
        if movie in self.moviesList:
            movie.getScreenings

    def make_booking(self,customer, aScreening: Screening, seats: List[Seat], orderTotal: float, paymentDetail: str) -> Booking:
        booking = Booking(customer, aScreening, seats, orderTotal, paymentDetail)
        aScreening.bookSeats(seats)
        customer.addBooking(booking)
        self.bookingList.append(booking)
        # Associate the booking with the customer
        if customer not in self.customer_bookings:
            self.customer_bookings[customer] = [booking]  # Create a new list for this customer
        else:
            self.customer_bookings[customer].append(booking)  # Append to the existing list
        return booking
    
    def find_booking_by_id(self,booking_id):
        # Iterate through the list of bookings to find the one with the specified booking ID
        for booking in self.bookingList:
            if booking.bookingNum == booking_id:
                return booking
        # If the booking with the given ID is not found, return None
        return None

    def cancel_booking(self, booking: Booking) -> bool:
        """Cancels a booking and frees up the seats."""
        customer = booking.customer
    
        if customer is None:
            return False  # Handle cases where the booking has no associated customer

        # Remove the booking from the customer's bookings
        if customer in self.customer_bookings:
            self.customer_bookings[customer].remove(booking)
    
        # Remove the booking from the cinema's booking list
        if booking in self.bookingList:
            self.bookingList.remove(booking)
    
        screening = booking.screening

        if screening is not None:
            # Get the seats that were booked for this booking
            booked_seats = booking.getSeats
            # You can also remove the booked seat from the screening, if needed
            screening.unbookSeats(booked_seats)
    
        # Indicate that the booking is canceled successfully
        return True

    
    def send_notification(self, customer: Customer, notification: Notification) -> None:
        """Send a notification to a specific customer."""
        if customer in self.customers:
            self.customers[customer].append(notification)  # Add the new notification to the customer's list
        else:
            self.customers[customer] = [notification]  # Create a new list for the customer and add the notification
        customer.receiveNotification(notification)  # Add the notification to the customer's notification list

    def notify_new_movie(self, customer: Customer, movie: Movie, notificationID) -> None:
        """Notify a specific customer about a new movie."""
        notification_content = f"New movie '{movie.title}' is now available!"
        notification = Notification(notificationID, notification_content)  # Create a new Notification object
        self.send_notification(customer, notification)  # Send the notification to the customer

    def notify_booking(self, customer: Customer, booking: Booking, notificationID) -> None:
        """Notify a specific customer about a booking."""
        notification_content = f"Booking {booking.bookingNum} is confirmed!"
        notification = Notification(notificationID, notification_content)  # Create a new Notification object
        self.send_notification(customer, notification)  # Send the notification to the customer

    def notify_cancellation(self, customer: Customer, booking: Booking, notificationID) -> None:
        """Notify a specific customer about a booking cancellation."""
        notification_content = f"Booking {booking.bookingNum} has been canceled."
        notification = Notification(notificationID, notification_content)  # Create a new Notification object
        self.send_notification(customer, notification)  # Send the notification to the customer