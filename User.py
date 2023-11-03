from abc import ABC
from datetime import datetime, date
from typing import List, Dict, Union
from Movie import Movie
from Screening import Screening
from Booking import Booking
from Notification import Notification


class Person(ABC):
    def __init__(self, name: str):
       
        self._name = name

    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, new_name: str) -> None:
        self._name = new_name
    

class User(Person):
   
    def __init__(self, name: str, username: str, password: str):
        super().__init__(name)
        self._username = username
        self._password = password

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, new_username: str):
        self._username = new_username

    @property
    def password(self) -> str:
        return self._password
    
    @password.setter
    def password(self, new_password: str):
        self._password = new_password

class Customer(User):
    def __init__(self, name: str, username: str, password: str):
        super().__init__(name, username, password)
        self.__bookingList: List[Booking] = [] 
        self.__notificationList: List[Notification] =[]
    
    @property
    def bookingList(self) -> List[Booking]:
        return self.__bookingList
    
    @property 
    def notificationList(self) -> List[Notification]:
        return self.__notificationList
    
    def addBooking(self, aBooking: Booking) -> bool:
        self.__bookingList.append(aBooking)
        return True

    def removeBooking(self, aBooking: Booking) -> bool:
        if aBooking in self.__bookingList:
            self.__bookingList.remove(aBooking)
            return True
        else:
            return False   
    
    def getBookingList(self) -> List[Booking]:
        return self.__bookingList
    
    def receiveNotification(self, notification: Notification) -> None:
        """Receive and store a notification in the customer's notification list."""
        self.__notificationList.append(notification)

class FrontDeskStaff(User):
    def __init__(self, name: str, username: str, password: str):

        super().__init__(name, username, password)
    

class Admin(User):
    def __init__(self, name: str, username: str, password: str):
        super().__init__(name, username, password)


