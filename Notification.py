# Notification.py

##
# @file Notification.py
#
# @brief This file defindes the class Notification and its method. 
#
# @section description_Notification Description 
# This class represents a notification message that can be used to notify users about various events or updates in the system. 
# Notifications are typically created with a message and can be converted to a string for display.

class Notification:
    def __init__(self,notificationID: int, content: str):
        self.__notificationID = notificationID
        self.__content = content

    def __str__(self):
        """! Converts the notification to a string.
        @return The notification message as a string.
        """
        return self.__content
    
    @property
    def notificationID(self) -> int:
        return self.__notificationID

    @notificationID.setter
    def notificationID(self, new_notificationID: int):
        self.__notificationID = new_notificationID

    @property
    def content(self) -> str:
        return self.__content

    @content.setter
    def content(self, new_content: str):
        self.__content = new_content

