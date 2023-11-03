# Screening.py

##
# @file Screening.py
#
# @brief This file defines the class Screening and its methods.
#
# @section description_Screening Description
#
# The Screening class represents a movie screening at the cinema. It contains methods
# for managing seat bookings for a screening, checking available seats, and canceling bookings.

# Imports 
from datetime import datetime, date
from typing import List, Dict, Union
from Seat import Seat
from Hall import Hall


class Screening:
  
    """! The Screening Class 
    """
    nextID = 1
    def __init__(self, screeningDate: datetime, startTime: datetime, endTime: datetime, hall: Hall):
        """! The class initialiser
        """
        self.__screeningID = Screening.nextID
        self.__screeningDate = screeningDate
        self.__startTime = startTime
        self.__endTime = endTime
        self.__hall = hall
        self.__booked_seats = []  # List to track booked seats
        Screening.nextID += 1
    
    @property
    def screeningID(self):
        return self.__screeningID
    
    @property
    def screeningDate(self) -> str:
        return self.__screeningDate
    
    @property
    def startTime(self) -> str:
        return self.__startTime
    
    @property 
    def endTime(self) -> str:
        return self.__endTime
    
    @property 
    def hall(self) -> Hall:
        return self.__hall
    
    def bookSeats(self, seats_to_book: List[Seat]):
        """Books the specified seats for this screening."""
        for seat in seats_to_book:
            if not seat.isReserved:  # Check if the seat is not already booked
                seat.book()  # Assuming there's a 'book' method in the Seat class
                self.__booked_seats.append(seat)  # Add the seat to the list of booked seats
            
    
    def unbookSeats(self, seats_to_remove: List[Seat]) -> bool:
        """Unbooks (removes) the specified seats for this screening."""
        for seat in seats_to_remove:
            if seat in self.__booked_seats:
                seat.unbook()  # Assuming there's an 'unbook' method in the Seat class
                self.__booked_seats.remove(seat)  # Remove the seat from the list of booked seats
            else:
                # The seat was not booked for this screening; you can handle this case as needed.
                # For now, I'm returning False to indicate that the removal failed.
                return False

        # If all specified seats were successfully unbooked, return True
        return True

    def getBookedSeats(self):
        """Returns the list of seats that have been booked for this screening."""
        return self.__booked_seats 
    
    def getAvailableSeats(self):
    
        all_seats = self.hall.getSeats()  # Get all seats in the hall
        booked_seats = self.__booked_seats  # Get the booked seats

        available_seats = [seat for seat in all_seats if seat not in booked_seats and not seat.isReserved]
    
        return available_seats


    