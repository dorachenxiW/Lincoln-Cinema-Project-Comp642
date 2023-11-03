
from datetime import datetime, date
from typing import List, Dict, Union
from Screening import Screening


class Movie:
    """! The Movie class
    """
    def __init__(self, title: str, description: str, durationMins: int, language: str, releaseDate: datetime, country: str, genre:str):

        self.__title = title
        self.__description = description
        self.__durationMins = durationMins
        self.__language = language
        self.__releaseDate = releaseDate
        self.__country = country
        self.__genre = genre
        self.__screeningsList: List[Screening] = []
    
    @property 
    def title(self) -> str:
        return self.__title
    
    @property
    def description(self) -> str:
        return self.__description
    
    @property
    def durationMins(self) -> int:
        return self.__durationMins
    
    @property
    def language(self) -> str:
        return self.__language
    
    @property
    def releaseDate(self) -> datetime:
        return self.__releaseDate
    
    @property
    def country(self) -> str:
        return self.__country
    
    @property
    def genre(self) -> str:
        return self.__genre
    
    def getScreenings(self) -> List[Screening]:
        return self.__screeningsList
    
    def addScreening(self, aSreening: Screening):
        self.__screeningsList.append(aSreening)
       

    def cancelScreening(self, aScreening: Screening):
        if aScreening in self.__screeningsList:
                self.__screeningsList.remove(aScreening)
     

    def view_movie(self) -> str:
        details = [
                    f"Title: {self.title}",
                    f"Description: {self.description}",
                    f"Duration: {self.durationMins} minutes",
                    f"Language: {self.language}",
                    f"Release Date: {self.releaseDate.strftime('%m-%d-%Y')}",
                    f"Country: {self.country}",
                    f"Genre: {self.genre}"
                ]
        return details
