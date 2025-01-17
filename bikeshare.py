import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs.
    while True:
        try:
            city = str(input("Would you like to see data for Chicago, New York City or Washington?\n")).lower()
            if city not in ['chicago', 'new york city', 'washington']:
                print("Please input a valid city")
            else:
                break
        except:
         print("Please enter a valid city ")

    # Give some feedback to user
    print("Great choice! You will be shown data from {}".format(city.title()))
    # Get user input for month (all, january, february, ... , june).
    while True:
        try:
            month = str(input("What month would you like to see data for?\n")).title()
            if month not in ['January','February','March','April','May','June','All']:
                print("Please input a valid month")
            else:
                break
        except:
            print("Please enter a valid month")
    # Get user input for day of week (all, monday, tuesday, ... sunday).
    while True:
        try:
            day = str(input("What day would you like to see data for?\n")).title()
            if day not in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','All']:
                print("Please input a valid day")
            else:
                break
        except:
            print("Please input a valid day of the week")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Loads data file into a dataframe.
    df = pd.read_csv(CITY_DATA[city])

    # Converts the Start Time column to datetime.
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extracts month and day of week from Start Time to create new columns.
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    
    # Filters by month if applicable.
    if month != 'All':
        # Use the index of the months list to get the corresponding int.
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
    
        # Filters by month to create the new dataframe.
        df = df[df['month'] == month]
        
    # Filters by day of week if applicable.
    if day != 'All':
        # Filters by day of week to create the new dataframe.
        df = df[df['day_of_week'] == day.title()]    

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Displays the most common month.
    print("Most commom month: {}".format(df['month'].mode()[0]))

    # Displays the most common day of week.
    print('Most common day: {}'.format(df['day_of_week'].mode()[0]))

    # Displays the most common start hour.
    df['hour'] = df['Start Time'].dt.hour
    print('Most common start hour: {}'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Displays most commonly used start station.
    print('Most common start station: {}'.format(df['Start Station'].mode()[0]))

    # Displays most commonly used end station.
    print('Most common end station: {}'.format(df['End Station'].mode()[0]))

    # Displays most frequent combination of start station and end station trip.
    most_common_combination = df['Start Station'].map(str) + ' to ' + df['End Station']
    print('Most popular combination: {}'.format(most_common_combination.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time.
    total_m, total_s = divmod(df['Trip Duration'].sum(), 60)
    total_h, total_m = divmod(total_m, 60)
    print ('Total travel time: ',total_h,' hours, ', total_m,' minutes, and ', total_s,' seconds.')

    # Displays mean travel time.
    mean_m, mean_s = divmod(df['Trip Duration'].mean(), 60)
    mean_h, mean_m = divmod(mean_m, 60)
    print ('Mean travel time: ',mean_h,' hours, ', mean_m,' minutes, and ', mean_s,' seconds.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types.
    print('Users can be broken down into \n{}'.format(df['User Type'].value_counts()))

    # Displays counts of gender.
    if('Gender' not in df):
        print('Sorry! Gender data unavailable for Washington')
    else:
        print('The genders are \n{}'.format(df['Gender'].value_counts()))

    # Displays earliest, most recent, and most common year of birth.
    if ('Birth Year' not in df):
        print('Sorry! Birth year data unavailable for Washington')
    else:
        print('The Earliest birth year is: {}'.format(df['Birth Year'].min()))
        print('The most recent birth year is: {}'.format(df['Birth Year'].max()))
        print('The most common birth year is: {}'.format(df['Birth Year'].mode()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    '''Displays rows of data, 5 lines each time'''
    # Ask user if they would like to see individual trip data
    view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no \n")
    start_loc = 0
    while view_data == "yes":
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower
        if view_data == "no":
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
