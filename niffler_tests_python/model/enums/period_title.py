from enum import Enum

class PeriodTitle(str, Enum):
    ALL_TIME = "ALL TIME"
    MONTH = "MONTH"
    WEEK = "WEEK"
    TODAY = "TODAY"
