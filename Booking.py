# Booking.py

##
# @file Booking.py
#
# @brief This file defines the class Booking.
#
# @section description_Booking Description
# The Booking class represents a booking made by a customer for a movie screening at Lincoln Cinemas. 
# It stores information about the customer, the screening, the booked seats, any applied discount coupon, and the payment method.

# Imports
from datetime import datetime, date
from typing import List, Dict, Union
from Screening import Screening
from Seat import Seat
#from Payment import Payment

class Booking:
    """! The Booking class
    """
    nextID = 100
    def __init__(self, customer, aScreening: Screening, seats: List[Seat], orderTotal: float, paymentDetail: str):
        self.__bookingNum = Booking.nextID
        self.__customer = customer
        self.__screening = aScreening
        self.__seats = seats
        self.__orderTotal = orderTotal
        self.__paymentDetail = paymentDetail
        Booking.nextID += 1 
    

    @property
    def bookingNum(self):
        return self.__bookingNum
    
    @bookingNum.setter
    def bookingNum(self, new_bookinNum):
        self.__bookingNum = new_bookinNum


    @property
    def customer(self):
        return self.__customer

    @customer.setter
    def customer(self, new_customer):
        self.__customer = new_customer

    @property
    def screening(self) -> Screening:
        return self.__screening

    @screening.setter
    def screening(self, new_screening: Screening):
        self.__screening = new_screening

    @property
    def getSeats(self) -> List[Seat]:
        return self.__seats

    @getSeats.setter
    def seats(self, new_seats: List[Seat]):
        self.__seats = new_seats

    @property
    def orderTotal(self) -> float:
        return self.__orderTotal

    @orderTotal.setter
    def orderTotal(self, new_orderTotal: float):
        self.__orderTotal = new_orderTotal

    @property
    def paymentDetail(self):
        return self.__paymentDetail

    @paymentDetail.setter
    def paymentDetail(self, new_paymentDetail: str):
        self.__paymentDetail = new_paymentDetail
