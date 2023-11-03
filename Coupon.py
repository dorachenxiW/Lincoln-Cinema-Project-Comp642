from datetime import datetime, date

class Coupon:
    def __init__(self, couponID: str, discountRate: float):
        self.__couponID = couponID
        self.__discountRate = discountRate

    @property
    def couponID(self) -> int:
        return self.__couponID

    @couponID.setter
    def couponID(self, new_couponID: int):
        self.__couponID = new_couponID

    @property
    def discountRate(self) -> float:
        return self.__discountRate

    @discountRate.setter
    def discountRate(self, new_discountRate: float):
        self.__discountRate = new_discountRate