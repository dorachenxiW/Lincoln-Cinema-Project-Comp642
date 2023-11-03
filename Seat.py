# Seat.py

##
# @file Seat.py
#
# @brief This file defines the class Seat.
#
# @section description_Seat Description
# The Seat class represents an individual seat in a cinema hall. 
# Each seat has a unique seat number to distinguish it from other seats.

class Seat:
    nextID = 1000
    def __init__(self, seatNumber: int, seatColumn: str, isReserved: bool, seatPrice: float):
        self.__seatID = Seat.nextID
        self.__seatNumber = seatNumber
        self.__seatColumn = seatColumn
        self.__isReserved = isReserved
        self.__seatPrice = seatPrice
        Seat.nextID += 1 
    
    @property
    def seatID(self):
        return self.__seatID
    
    @property
    def seatNumber(self):
        return self.__seatNumber
    
    @property
    def seatColumn(self):
        return self.__seatColumn
    
    @property
    def isReserved(self):
        return self.__isReserved
    
    @property
    def seatPrice(self):
        return self.__seatPrice
    
    def book(self):
        """Marks the seat as booked."""
        if not self.__isReserved:
            self.__isReserved = True
            print(f"Seat {self.__seatNumber} in column {self.__seatColumn} is now booked.")
        else:
            print(f"Seat {self.__seatNumber} in column {self.__seatColumn} is already booked.")

    def unbook(self):
        """Marks the seat as unbooked (not reserved)."""
        if self.__isReserved:
            self.__isReserved = False
            print(f"Seat {self.__seatNumber} in column {self.__seatColumn} is now unbooked.")
        else:
            print(f"Seat {self.__seatNumber} in column {self.__seatColumn} is not booked.")
   