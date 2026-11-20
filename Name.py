# ***************************************************************************
#
# Author: Paul Littrell
# Lab:    CIS-133Y Lab 9
# Date:   November 20, 2026
# Desc:   Business logic layer module containing the Name class. Encapsulates
#         yearly census name popularity records, total births, and popularity
#         percentage calculations.
#
# ***************************************************************************

import Database as db


class Name:
    """Represents a single year's census popularity record for a given name."""

    def __init__(self, name, year, gender, count, total):
        self.__name = name
        self.__year = year
        self.__gender = gender
        self.__count = count
        self.__total = total

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_year(self):
        return self.__year

    def set_year(self, year):
        self.__year = year

    def get_gender(self):
        return self.__gender

    def set_gender(self, gender):
        self.__gender = gender

    def get_count(self):
        return self.__count

    def set_count(self, count):
        self.__count = count

    def get_total(self):
        return self.__total

    def set_total(self, total):
        self.__total = total

    def get_popularity_percentage(self):
        """Calculates the percentage of total births for this name and year."""
        if self.__total and self.__total > 0:
            return round((self.__count / self.__total) * 100, 2)
        return 0.0

    @staticmethod
    def get_name_popularity(target_name, gender):
        """Queries the database layer and returns a list of Name objects."""
        raw_records = db.Database.fetch_name_popularity(target_name, gender)

        popularity_history = []
        for row in raw_records:
            record = Name(
                name=row["Name"],
                year=row["Year"],
                gender=row["Gender"],
                count=row["NameCount"],
                total=row["Total"],
            )
            popularity_history.append(record)

        return popularity_history