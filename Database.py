# ***************************************************************************
#
# Author: Paul Littrell
# Lab:    CIS-133Y Lab 9
# Date:   November 20, 2026
# Desc:   Data layer module containing the Database class. Connects to
#         the MSSQL database and queries yearly popularity data for a
#         given name and gender using parameterized SQL.
#
# ***************************************************************************

import pymssql


class Database:
    """Handles database connectivity and queries for the NAMES database."""

    __connection = None

    @classmethod
    def connect(cls):
        """Establishes and shares a single connection to the MSSQL server."""
        if cls.__connection is None:
            cls.__connection = pymssql.connect(
                server="cisdbss.pcc.edu",
                user="275student",
                password="275student",
                database="NAMES",
            )

    @classmethod
    def fetch_name_popularity(cls, target_name, gender):
        """Fetches yearly popularity records for a specific name and gender."""
        cls.connect()

        # Return rows as dictionaries keyed by column name
        cursor = cls.__connection.cursor(as_dict=True)

        # Parameterized query against the all_data view/table
        query = """
                SELECT Name, Year, Gender, NameCount, Total
                FROM all_data
                WHERE Name = %s
                  AND Gender = %s
                ORDER BY Year;
                """

        cursor.execute(query, (target_name, gender))
        results = cursor.fetchall()
        cursor.close()
        return results