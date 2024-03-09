import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

# Drop 'workingday' column
hour_df.drop(['workingday'], axis=1, inplace=True)
day_df.drop(['workingday'], axis=1, inplace=True)

# Convert categorical columns
columns = ['season', 'mnth', 'holiday', 'weekday', 'weathersit']
for column in columns:
    day_df[column] = day_df[column].astype("category")
    hour_df[column] = hour_df[column].astype("category")

# Convert 'dteday' column to datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Renamed columns for readability
day_df.rename(columns={'yr': 'year', 'mnth': 'month', 'weekday': 'one_of_week', 'weathersit': 'weather_situation',
                       'windspeed': 'wind_speed', 'cnt': 'count_cr', 'hum': 'humidity'}, inplace=True)
hour_df.rename(columns={'yr': 'year', 'hr': 'hours', 'mnth': 'month', 'weekday': 'one_of_week',
                        'weathersit': 'weather_situation', 'windspeed': 'wind_speed', 'cnt': 'count_cr',
                        'hum': 'humidity'}, inplace=True)

# 1. Convert column contents for easy understanding
# Season conversion to: 1:Spring, 2:Summer, 3:Fall, 4:Winter
day_df.season.replace((1,2,3,4), ('Spring','Summer','Fall','Winter'), inplace=True)
hour_df.season.replace((1,2,3,4), ('Spring','Summer','Fall','Winter'), inplace=True)

# convert month to: 1:Jan, 2:Feb, 3:Mar, 4:Apr, 5:May, 6:Jun, 7:Jul, 8:Aug, 9:Sep, 10:Oct, 11:Nov, 12:Dec
day_df.month.replace((1,2,3,4,5,6,7,8,9,10,11,12),('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'), inplace=True)
hour_df.month.replace((1,2,3,4,5,6,7,8,9,10,11,12),('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'), inplace=True)

# convert weather situation to: 1:Clear, 2:Misty, 3:Light_RainSnow 4:Heavy_RainSnow
day_df.weather_situation.replace((1,2,3,4), ('Clear','Misty','Light_rainsnow','Heavy_rainsnow'), inplace=True)
hour_df.weather_situation.replace((1,2,3,4), ('Clear','Misty','Light_rainsnow','Heavy_rainsnow'), inplace=True)

# convert one_of_week to: 0:Sun, 1:Mon, 2:Tue, 3:Wed, 4:Thu, 5:Fri, 6:Sat
day_df.one_of_week.replace((0,1,2,3,4,5,6), ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'), inplace=True)
hour_df.one_of_week.replace((0,1,2,3,4,5,6), ('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'), inplace=True)

# convert year to: 0:2011, 1:2012
day_df.year.replace((0,1), ('2011','2012'), inplace=True)
hour_df.year.replace((0,1), ('2011','2012'), inplace=True)

# Calculating Humidity
day_df['humidity'] = day_df['humidity']*100
hour_df['humidity'] = hour_df['humidity']*100

# Create a new column called category_days which shows the contents of the column as weekend or weekdays
def get_category_days(one_of_week):
    if one_of_week in ["Saturday", "Sunday"]:
        return "weekend"
    else:
        return "weekdays"

hour_df["category_days"] = hour_df["one_of_week"].apply(get_category_days)
day_df["category_days"] = day_df["one_of_week"].apply(get_category_days)

def classify_humidity(humidity):
    if humidity < 45:
        return "Terlalu kering"
    elif 45 <= humidity < 65:
        return "Ideal"
    else:
        return "Terlalu Lembab"

hour_df["humidity_category"] = hour_df["humidity"].apply(classify_humidity)
day_df["humidity_category"] = day_df["humidity"].apply(classify_humidity)

# Sidebar for date range selection
st.sidebar.header("Select Date Range")
min_date = day_df['dteday'].min().date()
max_date = day_df['dteday'].max().date()
start_date = st.sidebar.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)
end_date = st.sidebar.date_input("End Date", min_value=min_date, max_value=max_date, value=max_date)

# Filter data based on selected date range
filtered_hour_df = hour_df[(hour_df['dteday'] >= pd.Timestamp(start_date)) & (hour_df['dteday'] <= pd.Timestamp(end_date))]
filtered_day_df = day_df[(day_df['dteday'] >= pd.Timestamp(start_date)) & (day_df['dteday'] <= pd.Timestamp(end_date))]

# Show summary statistics and visualizations based on the filtered data

# 1. Summary statistics and visualizations for accidents based on weather situation

st.header("Accidents Based on Weather Situation")

# Hourly data
st.subheader("Hourly Data")
hourly_weather_counts = filtered_hour_df['weather_situation'].value_counts()
st.write("Counts of Accidents by Weather Situation (Hourly)")
st.write(hourly_weather_counts)

# Visualize
fig, ax = plt.subplots()
sns.countplot(data=filtered_hour_df, x='weather_situation', order=hourly_weather_counts.index, ax=ax)
ax.set_title('Accidents by Weather Situation (Hourly)')
ax.set_xlabel('Weather Situation')
ax.set_ylabel('Count')
st.pyplot(fig)

# Daily data
st.subheader("Daily Data")
daily_weather_counts = filtered_day_df['weather_situation'].value_counts()
st.write("Counts of Accidents by Weather Situation (Daily)")
st.write(daily_weather_counts)

# Visualize
fig, ax = plt.subplots()
sns.countplot(data=filtered_day_df, x='weather_situation', order=daily_weather_counts.index, ax=ax)
ax.set_title('Accidents by Weather Situation (Daily)')
ax.set_xlabel('Weather Situation')
ax.set_ylabel('Count')
st.pyplot(fig)

# 2. Summary statistics and visualizations for accidents based on humidity category

st.header("Accidents Based on Humidity Category")

# Hourly data
st.subheader("Hourly Data")
hourly_humidity_counts = filtered_hour_df['humidity_category'].value_counts()
st.write("Counts of Accidents by Humidity Category (Hourly)")
st.write(hourly_humidity_counts)

# Visualize
fig, ax = plt.subplots()
sns.countplot(data=filtered_hour_df, x='humidity_category', order=hourly_humidity_counts.index, ax=ax)
ax.set_title('Accidents by Humidity Category (Hourly)')
ax.set_xlabel('Humidity Category')
ax.set_ylabel('Count')
st.pyplot(fig)

# Daily data
st.subheader("Daily Data")
daily_humidity_counts = filtered_day_df['humidity_category'].value_counts()
st.write("Counts of Accidents by Humidity Category (Daily)")
st.write(daily_humidity_counts)

# Visualize
fig, ax = plt.subplots()
sns.countplot(data=filtered_day_df, x='humidity_category', order=daily_humidity_counts.index, ax=ax)
ax.set_title('Accidents by Humidity Category (Daily)')
ax.set_xlabel('Humidity Category')
ax.set_ylabel('Count')
st.pyplot(fig)

# 2. Bicycle rentals by season

st.header("Bicycle Rentals by Season")

# Daily data
st.subheader("Daily Data")
season_counts_daily = filtered_day_df['season'].value_counts()
st.write("Counts of Bicycle Rentals by Season (Daily)")
st.write(season_counts_daily)

# Visualize
fig, ax = plt.subplots()
sns.countplot(x='season', data=filtered_day_df, order=filtered_day_df['season'].value_counts().index, ax=ax)
ax.set_xlabel("Season")
ax.set_ylabel("Number of Bicycle Rentals")
ax.set_title("Bicycle Rentals by Season (Daily)")
st.pyplot(fig)


# 3. Summary statistics and visualizations for accidents based on temperature

st.header("Accidents Based on Temperature")

# Hourly data
st.subheader("Hourly Data")
hourly_temp_mean = filtered_hour_df.groupby('weather_situation')['temp'].mean()
st.write("Average Temperature by Weather Situation (Hourly)")
st.write(hourly_temp_mean)

# Visualize
fig, ax = plt.subplots()
hourly_temp_mean.plot(kind='bar', ax=ax)
ax.set_title('Average Temperature by Weather Situation (Hourly)')
ax.set_xlabel('Weather Situation')
ax.set_ylabel('Temperature (Celsius)')
st.pyplot(fig)

# Daily data
st.subheader("Daily Data")
daily_temp_mean = filtered_day_df.groupby('weather_situation')['temp'].mean()
st.write("Average Temperature by Weather Situation (Daily)")
st.write(daily_temp_mean)

# Visualize
fig, ax = plt.subplots()
daily_temp_mean.plot(kind='bar', ax=ax)
ax.set_title('Average Temperature by Weather Situation (Daily)')
ax.set_xlabel('Weather Situation')
ax.set_ylabel('Temperature (Celsius)')
st.pyplot(fig)
