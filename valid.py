# ***************************************************************************
#
# Author: Paul Littrell
# Lab:    CIS-133Y Lab 9
# Date:   November 20, 2026
# Desc:   Utility module for validating GUI user inputs (first name and
#         gender selection) before querying the database.
#
# ***************************************************************************


def validate_name(raw_name):
    """
    Validates that the entered name is non-empty and contains only letters.
    Returns a tuple: (is_valid: bool, cleaned_name_or_error: str).
    """
    cleaned_name = raw_name.strip()

    if not cleaned_name:
        return False, "Please enter a first name to search (for example, Marc)."

    if not cleaned_name.isalpha():
        return False, "Please enter letters only (no numbers, spaces, or symbols)."

    # Normalize capitalization (e.g., 'marc' -> 'Marc')
    return True, cleaned_name.capitalize()


def validate_gender(raw_gender):
    """
    Validates that the selected gender code is 'M' or 'F'.
    Returns a tuple: (is_valid: bool, cleaned_gender_or_error: str).
    """
    cleaned_gender = raw_gender.strip().upper()

    if cleaned_gender in ("M", "F"):
        return True, cleaned_gender

    return False, "Please select a gender option (Male or Female)."