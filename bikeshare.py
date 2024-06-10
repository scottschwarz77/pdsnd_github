import time
import pandas as pd
import numpy as np

CITY_DATA = { 'CHICAGO': 'chicago.csv',
              'NEW YORK CITY': 'new_york_city.csv',
              'WASHINGTON': 'washington.csv' }

# Custom exceptions to handle user input errors

class FilterError(Exception):
  pass

class DayofWeekError(Exception):
  pass
    
class CityError(Exception):
  pass
    
class MonthError(Exception):
  pass

class YesNoError(Exception):
  pass

def load_data(city, month, day):
  """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month from January to June to filter by, or "all" to apply no month filter
        (int) day - Digit corresponding to the the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
  
  df = pd.read_csv(CITY_DATA[city])

  # Convert the Start Time column to datetime
  df['Start Time'] = pd.to_datetime(df['Start Time'])

  # Extract month and day of week from Start Time to create new columns
  df['Month'] = df['Start Time'].dt.month
  df['Day of Week'] = df['Start Time'].dt.dayofweek

  # Filter by month if applicable
  if month != 'all':
      # Use the index of the months list to get the corresponding int
      months = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE']
      month = months.index(month) + 1
      df = df[df['Month'] == month]

  # Filter by day of week if applicable
  if day != 'all':
      df = df[df['Day of Week'] == day]

  return df

def get_day_of_week_input():
  """Ask the user for a day of the week for which to filter the data."""
  while True:
    try:
      number = int(input("\nEnter the day of the week. Use a digit between '0' and '6' , where '0' is for Monday and '6' is for Sunday: "))
      if (number < 0 or number > 6):
        raise DayofWeekError()
      return number
    except (ValueError, DayofWeekError):
      print("Invalid input. Try again")

def get_month_input():
  """Ask the user for a month for which to filter the data."""
  while True:
    try:
      month = input("Enter the name of the month from 'January' to 'June', such as 'February': ")
      month = month.upper()
      if month not in ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE']:
        raise MonthError("Invalid month entered. Try again.")
      return month
    except MonthError as m:
      print(m)
      
def get_yes_no_input(str):
  """Ask the user a yes/no question."""
  while True:
    try:
      yes_no = input(str)
      yes_no = yes_no.upper()
      if yes_no not in ('YES','NO'):
        raise YesNoError("Invalid input Try again.")
      return yes_no 
    except YesNoError as yn:
      print(yn)    

def get_city_input():
  """Ask the user for the city for which to filter the data."""
  while True:
    try:
      city = input("Which city would you like see data for? Enter 'Chicago', 'New York City', or 'Washington': ")
      city = city.upper()
      if (city not in ['CHICAGO', 'NEW YORK CITY', 'WASHINGTON']):
        raise CityError("\nInvalid city entered. Try again.\n")
      return city
    except CityError as c:
      print(c)
    
def get_month_day():
  """Ask the user how they want to filter the data by day and month."""
  while True:
    try:
      month_day_filter = input("\nWould you like to filter the data for month, day, both, or none at " \
                               "all? Enter 'month', 'day', 'both', or 'none': ")
      month_day_filter = month_day_filter.upper()         
      if (month_day_filter not in ['MONTH', 'DAY', 'BOTH', 'NONE']):
        raise FilterError("Invalid entry.")
      break
    except FilterError as f:
      print(f)
  month = 'all'
  day = 'all'
  if (month_day_filter in ('MONTH', 'BOTH')):
    month = get_month_input()
  if (month_day_filter in ('DAY', 'BOTH')):
    day = get_day_of_week_input()
  return month, day

def set_end_row(start_row, number_of_rows):
  """
  Set the end row, for use by the display_data function.
  
  Args:
  start_row: The starting row in the dataframe used in the display_data function.
  number_of_rows: The number of rows in the dataframe used in the display_data function.
  """
   
  end_row = start_row + 4
  if end_row > number_of_rows - 1:
      end_row = number_of_rows - 1
  return end_row
  
def display_data(df):
  """Display five rows of data at a time.

  Args:
  df: The dataframe containing the data to display
  """
  number_of_rows = len(df)
  start_row = 0
  end_row = set_end_row(start_row, number_of_rows)
  while True:
    for current_row in range(start_row, end_row + 1):
      print(df.iloc[current_row])
      print("\n")
    # If the last row has not been displayed, ask if want to see more rows
    if (end_row != number_of_rows - 1):
      yes_no_input = get_yes_no_input("\n\nWould you like to see more rows? Type 'yes' or 'no': ")
      if (yes_no_input == 'YES'):
        start_row = end_row + 1
        end_row = set_end_row(start_row, number_of_rows)
      else:
        return
    else:  
      return
    
def time_stats(df):
  """Displays statistics on the most common times of travel."""

  print('\n1. Calculating time stats...\n')
  
  print("\nMost common month:\n")
  print(df["Month"].mode())

  print("\nMost common day of week:\n")
  print(df['Day of Week'].mode())

  print("\nMost common start hour:\n")
  df["Hour"] = df['Start Time'].dt.hour
  print(df['Hour'].mode())
  
def station_stats(df):
  """Display statistics on the most popular stations and trip."""

  print('\n2. Calculating station stats...\n')

  print("\nMost commonly used start station:")
  print(df["Start Station"].mode())
   
  print("\nMost commonly used end station:")
  print(df["End Station"].mode())
  
  # Display most common combination of start station and end station trip
  start_and_end_station_df = df["Start Station"] + df["End Station"]  
  print(start_and_end_station_df.mode())

def trip_duration_stats(df):
  """Display statistics on the total and average trip duration."""

  print('\n3. Calculating trip duration stats...\n')

  print('\nTotal trip duration:\n')
  print(df['Trip Duration'].sum())

  print('\nMean trip duration:\n')
  print(df['Trip Duration'].mean())

def user_stats(df, city):
  """Displays statistics on bikeshare users."""

  print('\n4. Calculating user stats...\n')

  print("\nUser type counts:\n")
  print(df.groupby("User Type")["User Type"].count())

  if (city != 'WASHINGTON'):
    print("\nGender counts:\n")
    print(df.groupby("Gender")["Gender"].count())
    
    print("\nMost common birth year: \n")
    print(df["Birth Year"].mode())

    print("\nMaximum birth year: \n")
    print(df["Birth Year"].max())
    
    print("\nMinimum birth year: \n")
    print(df["Birth Year"].min())
  else:
    print("No user stats available for Washington.\n")
  
def main():
  while True:
    # Get user inputs to determine how to filter the data
    city = get_city_input()
    month, day = get_month_day()
    df = load_data(city, month, day)
    
    # Compute and display stats based on the filters
    time_stats(df)
    station_stats(df)
    trip_duration_stats(df)
    user_stats(df, city)

    # Display individual rows
    yes_no_input = get_yes_no_input("Would you like to see data for the first 5 rows \
                                    (or all rows if there less than 5)? Type 'yes' or 'no': ")
    if (yes_no_input == 'YES'):
      display_data(df)
    restart = get_yes_no_input("\nWould you like to restart? Enter 'yes' or 'no':")
    if restart == 'NO':
        break

if __name__ == "__main__":
	main()