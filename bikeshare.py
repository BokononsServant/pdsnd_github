import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    while True:
        city = input('\nWhat city to you want to analyze data from? Chicago, New York City or Washington?').lower()
        if city in CITY_DATA.keys():
            print ('\nYou selected {}.'.format(city))
            break
        else:
            print('\nPlease try again.\n')

    while True:
        month = input('\nWhat month do you want to analyze? Answer \'all\' for no filter.\n').lower()
        if month in months or month=='all':
            print('\nYou selected {}'.format(month))
            break
        else:
            print('\nPlease try again.\n')
            
    while True:
        day = input('\nWhat day do you want to analyze? Answer \'all\' for no filter.\n').lower()
        if day in days or day=='all':
            print('\nYou selected {}'.format(day))
            break
        else:
            print('\nPlease try again.\n')

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

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time']  = pd.to_datetime(df['Start Time'])
    df['month']       = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour']        = df['Start Time'].dt.hour

    if month != 'all':
        month = months.index(month)+1
        df    = df[df['month']==month]

    if day != 'all':
        day = days.index(day)
        df  = df[df['day_of_week']==day]
    

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...')
    start_time = time.time()  

    print ('\nThe most common month(s) is(are): ', end='')
    for most_common_month in df['month'].mode():
        print(months[most_common_month-1].capitalize()+'',end='')

    print ('\nThe most common day(s) is(are): ', end='')
    for most_common_day in df['day_of_week'].mode():
        print(days[most_common_day].capitalize()+' ', end='')

    print ('\nThe most common hour(s) is(are): ', end='')
    for most_common_hour in df['hour'].mode():
        print(str(most_common_hour)+':00 ', end='')

    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...')
    start_time = time.time()

    print('\nThe most common start station(s) is(are):',end='')
    for most_common_start_station in df['Start Station'].mode():
        print (most_common_start_station+' ',end='')
    
    print('\nThe most common end station(s) is(are):',end='')
    for most_common_end_station in df['End Station'].mode():
        print (most_common_end_station+' ',end='')

    df['Trip']='From ' + df['Start Station'] + ' to ' + df['End Station']
    print('\nThe most common trip(s) is(are): ')
    for most_common_trip in df['Trip'].mode():
        print (most_common_trip+' ')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total=int(df['Trip Duration'].sum())
    print('Total travel time is {} seconds.'.format(total))

    mean=int(df['Trip Duration'].mean())
    print('Mean travel time is {} seconds.'.format(mean))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('What is the breakdown of users?')
    print(df['User Type'].value_counts())

    try:        
        print('\nWhat is the breakdown by gender?')
        print(df['Gender'].value_counts())
    except:
        print('Data for gender not available.')

    try:
        print('\nEarliest year of birth: ',int(df['Birth Year'].min()))
        ind=df['Start Time'].idxmax()
        print('Date of birth of most recent trip: ',int(df['Birth Year'][ind]))
    except:
        print('Data for Date of Birth not available.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def see_raw_data(df):
    i=0
    while True:
        if i==0:
            yes_no = input('\nDo you want to see the first 5 rows of raw data? y/n: ').lower()
        else:
            yes_no = input('\nDo you want to see the next 5 rows of raw data? y/n: ').lower()
        if yes_no == 'y':
            print (df.iloc[i:i+5])
            i+=5
        elif yes_no == 'n':
            break
        else:
            print('\nPlease try again')

def main():
    while True:
        city, month, day = get_filters()
        #city, month, day = 'washington', 'all', 'all'
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)  
        trip_duration_stats(df)
        user_stats(df)
        see_raw_data(df)

        restart = input('\nWould you like to restart? y/n.\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
