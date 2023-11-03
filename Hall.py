# Hall.py

##
# @file Hall.py
#
# @brief This file defines the class Hall and its method. 
#
# @section description_Hall Description
# The Hall class represents a movie hall in the Lincoln Cinemas. 
# Each hall has a unique hall number and a specific seating capacity. 
# It contains information about the available seats within the hall. 
# The Hall class is used to manage the seating arrangements for movie screenings.

# Imports 
from typing import List, Dict, Union
from Seat import Seat

class Hall:
    """! The Hall class
    """
    def __init__(self, name: str, totalSeats: int, listOfSeats: List[Seat]):
        
        self.__name = name
        self.__totalSeats = totalSeats
        self.__listOfSeats = listOfSeats
    
    @property
    def name(self):
        return self.__name
    
    @property
    def totalSeats(self):
        return self.__totalSeats

    def getSeats(self) -> List[Seat]:
        """Retrieves a list of seats available in the hall."""
        return self.__listOfSeats