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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    months = ['January', 'February', 'March', 'April', 'May', 'June'] 
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                        'Friday', 'Saturday', 'Sunday']
    correct_city = True
    while correct_city:
        city = input('Would you like to see data for Chicago, New York City or Washington?\n')
        city = city.lower()
        #get user input for month & day
        if city in CITY_DATA:
            correct_city = False
            time_filter = input('Would you like to filter data by month, '+
            'day, both, or not at all? Type "none" for no time filter.\n')
            #handling incorrect month input if month filter is chosen
            if time_filter == 'month': 
                month = input('Which month? January, February, March, April, May or June?\n').title()
                if month in months:
                    day = 'none'
                else:
                    print("There is no such month in the data. Please try again.")  
            #handling incorrect day input if day filter is chosen  
            elif time_filter == 'day':
                day = input('Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday?\n').title()
                if day in days:
                    month = 'none'
            #handling incorrect month and day inputs when both filters are chosen
            elif time_filter == 'both':
                month = input('Which month? January, February, March, April, May or June?\n').title()
                if month in months:
                    day = input('Which day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday?\n').title()
                    if day not in days:
                        print('The day entered is incorrect please try again.')  
                else:
                    print('There is no such month.')
            #handling 
            elif time_filter == 'none':
                month = 'none'
                day = 'none'
            else:
                print('Your input is not valid. Please try again.')
        else:
            print('Your input is not valid. Please try again.')
            exit(0)

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
    df = pd.read_csv(CITY_DATA[city]).rename(columns={'Unnamed: 0': 'ID'})
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    df['month'] = df['Start Time'].dt.month
    df['day']= df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'none':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by weekday if applicable
    if day != 'none':
        # use the index of the days list to get the corresponding weekday
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
        'Friday', 'Saturday', 'Sunday']
        day = days.index(day)
        # filter by day of week to create the new dataframe
        df = df[df['day'] == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    month_int = int(df['month'].mode().to_string(index=False))
    # display the most common day of week
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
            'Friday', 'Saturday', 'Sunday']
    day_int = int(df['day'].mode().to_string(index=False))
    # display the most common start hour
    common_hour = int(df['hour'].mode())
    print('Most Popular Month is {}'.format(months[month_int-1].title()))
    print('Most Popular Day is {}'.format(days[day_int-1].title()))
    print('Most Popular Hour is {}'.format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
   
    start_station_count = df['Start Station'].value_counts()
    print('Most Common Start Station: {} Count: {}'.format(start_station_count.keys()[0], start_station_count[0]))
    # display most commonly used end station
    
    end_station_count = df['End Station'].value_counts()
    print('Most Common End Station: {} Count: {}'.format(end_station_count.keys()[0], end_station_count[0]))
    # display most frequent combination of start station and end station trip
    print('\nPopular Trip for Travellers: ')
    start_end_count = df.groupby(['Start Station', 'End Station']).size().nlargest(1)
    for i, value in start_end_count.iteritems():
        print('Start Station: ' + str(i[0]) + '\nEnd Station: ' + str(i[1]) + '\nCount: ' + str(value))
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = round(df['Trip Duration'].sum(),4)
    # display mean travel time
    average_travel_time = round(np.mean(df['Trip Duration']),4)
    trip_count = df['Trip Duration'].count()
    print('Total Trip Duration: {} Average Trip Duration: {:4f} Count: {}'
            .format(total_travel_time, average_travel_time,trip_count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("User Types Breakdown:")
    user_types = df['User Type'].value_counts()
    print('Subscribers: {} \nCustomers: {}\n'.format(user_types['Subscriber'], user_types['Customer']))
    

    # Display counts of gender; does not provide output if Washington is selected
    if city != 'washington':
        print("\nGender Breakdown:")
        gender_count = df['Gender'].value_counts()
        print("Male: "+ str(gender_count['Male'])+ 
        "\nFemale: "+str(gender_count['Female']))

        # Display earliest, most recent, and most common year of birth
        print("\nBirth Year Breakdown:")
        oldest_dob = int(df['Birth Year'].min())
        youngest_dob = int(df['Birth Year'].max())
        common_dob = int(df['Birth Year'].mode())

        print("Earliest Birth Year: {}\nMost Recent Birth Year: {}\nMost Common Birth Year: {}"
                .format(oldest_dob,youngest_dob,common_dob))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_records(df):
    
    i = 0
    

    #changing df back to original form
    original_df = df.drop(['month', 'day', 'hour'], axis = 1)
    df_head = original_df.loc[i:i+4]

    print(df_head)
    more_records = input('Would you like to see more records? Y or N\n').upper()

    while more_records == 'Y':
        i = i + 5
        df_5rec = original_df.loc[i:i+4]
        print(df_5rec)
        more_records = input('Would you like to see more records? Y or N\n').upper()




def main():
    
    while True:
        
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_records(df)

        restart = input('\nWould you like to restart? Y or N.\n')
        if restart.lower() != 'y':
            break

    

if __name__ == "__main__":
    main()
