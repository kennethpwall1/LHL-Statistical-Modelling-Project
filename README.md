# Final-Project-Statistical-Modelling-with-Python

## Project/Goals
1. Accessing data from APIs
    * CityBikes
    * Yelp
    * FourSquare
2. Cleaning and transforming data using Pandas
3. Creating and loading data into SQlite database
4. Exploratory data analysis using statistics and python visualizations
5. Building and interpreting statistical models

## Process
### Accessing data from APIs
During the project I used 3 APIs: citibikes, Yelp and Foursquare. I used python's requests library to access the citibkes API to obtain all of the ebikes station locations in Vancouver, BC, Canada (Latitude and Longitude) and created another get request sending the latitude and longitude for each ebike station into the Yelp and foursquare APIs to obtain the points of interest (POIs) in a 1,000 meter radius around the bike station. Which returns: restaurant name, address, rating, distance from station, etc.

```python
url = "http://api.citybik.es/"
href = "/v2/networks/"
response = requests.get(url + href)
# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON response into a Python dictionary
    data = response.json()
else:
    print("Request failed with status code:", response.status_code)
#It is necessary to obtain the network ID to get the ebike stations
networks = data['networks']
city = 'Vancouver'
filtered_network = [network for network in networks if network['location']['city'] == city]
network_id = filtered_network[0]['href']
response1 = requests.get(url + network_id)
if response1.status_code == 200:
    # Parse the JSON response into a Python dictionary
    data1 = response1.json()
else:
    print("Request failed with status code:", response.status_code)
```

### Cleaning and transforming data using Pandas
All API data was retrieved in JSON format. I used the json.normalize() method to transform the json response from the get request into a Pandas DataFrame or just added the JSON dictionary to a Pandas DataFrame. I then selected only the relevenant columns to be used in the joined dataframe. I used info() to check for null values and describe() and sort_values() to check for strange values. Only the yelp pricing data with its $$ scale was not fully poplulated fully, but that column was categorical and was not used in the linear regression model as noted below.

I used the Panda merge method to join the foursqaure dataframe with the ebikes dataframe using the station ID as the key. I then dropped the longitude and latitude columns as they were unecessary for the analysis.

```python
join_df = pd.merge(fsq_df, vancouver_network_stations,on='station_id', how='left')
join_df = join_df.drop(columns=['longitude', 'latitude'])
```



### Creating and loading data into SQlite database
I used the create_engine module from the sqlalchemy library to create an SQlite database using the following code:

```python 
from sqlalchemy import create_engine
sqlite_db = 'sqlite:///../data/ebikes.db'
engine = create_engine(sqlite_db)
join_df.to_sql('ebikes_POI', con=engine, index=False)
```

### Exploratory data analysis using statistics and python visualizations
First step in my EDA process is always to look at shape(), info() and describe(). Then I want to see the shape of the data and see if the distribution is normal so I run some histograms on the numerical data and see if there are any outliers. I also ran a scatter plot between free ebikes and POI distance as well as the correlation between the two variables. There was limited numerical data so analysis was limited.

I primary used Matplotlib as my EDA tool for visualization as I only needed simple charts.

```python
import matplotlib.pyplot as plt
```



```python
plt.hist(join_df['free_bikes'], bins=20)
plt.show()
```
A histogram of ebikes reveals skewed data with bike stations having a low number of free bikes. This makes sense as Vancouver is a city where bikes are used frequently and tourists often visit the city and like to explore via bike.

![Histogram ebikes](/data/hist_ebikes.png "ebikes")


A histogram of POI distance from bike stations reveals a normal distribution and that bike stations are placed an average of 300 meters between points of interest.

![Histogram poi distance](/data/hist_poi.png "POI distance")

I wanted to see if there was a relationship between two variables: free ebikes and distance from points of interest so I created a scatterplot.

```python
x= join_df['free_bikes']
y= join_df['POI_distance']
plt.figure(figsize=(8, 6))
plt.scatter(x,y)
plt.xlabel('free_bikes')
plt.ylabel('POI_distance')
plt.show()
```

![Scatter Plot](/data/scatter.png "scatter")

The distribution of dots didn't point to any meaningful relationship so I decided to calculate the correlation between the two variables:

```python
correlation = join_df['free_bikes'].corr(join_df['POI_distance'])
```
This resulted in a correlation of: 0.013077301726096491, which basically means no correlation.




### Building and interpreting statistical models
I want to identify relationships between variables, make predictions about future sets of data, and transform the data into visualizations so that non-analysts and stakeholders can consume and leverage it.

Foursquare joined dataframe only has free ebikes and POI distance as numerical variables:
- Independent variable: POI distance
- Dependent: free ebikes

H0: The points of interest distance has no significant effect on the number of ebikes available

H1: the points of interest distance has a significant effect on the number of ebikes available

**See model results below**




## Results

**FOURSQUARE**

Foursquare's Places API gives a $200 credit per month and deducts amounts based on requests. As of the conclusion of this project I used $12. The get request for the location based on a radius of 1,000 meters only allowed for 10 search results per request. The API only provided the basic place details like address, distance, latitude, longitude, name, category. Rating is including in the API documentation as a parameter, but was not included in the json response to the request. With the limited information provided it was challenging to do an indepth analysis.

**YELP**

Yelp's Fusion API allows for 300 requests per day and returns 20 results per get request for the places search for a radius of 1,000 meters. Yelp had the best coverage in terms of the amount of information provided. It had the same basic place information for the POIs as Foursquare like address, distance, latitude, longitude, name, category, but also included rating, pricing, review counts. In my opinion, Yelp provides the best coverage and more information per request.

### FOURSQUARE MODEL - OLS SIMPLE LINEAR REGRESSION
Dep. Variable: free_bikes

Ind. Varianvle: POI_distance

R-squared: 0.00

POI_distance p-value: 0.920

H0: The points of interest has no significant effect on the number of ebikes available

H1: the points of interest have a significant effect on the number of ebikes available

R squared: is zero so the independent variable (POI distance) doesn't explain the variability in the dependent variable (free ebikes)

P value: pvalue is 0.92, which is much greater that 0.05. A pvalue greater than 0.05 indicates that the obeserved data is consistent with the null hypothesis, which is the POI distance has no significant effect on the number of ebikes available

### YELP MODEL - OLS SIMPLE LINEAR REGRESSION
Dep. Variable: distance

Ind. Varianvle: rating

R-squared: 0.133

rating p-value: 0.021

H0: There is no significant relationship between POI rating and ebike station distance

H1: There is a significant relationship between POI rating and ebike station distance

R squared: is low at 0.133 so the independent variable (POI rating) doesn't explain the variability in the dependent variable (ebike station distance)

P value: pvalue is 0.021, which is much less than 0.05. A pvalue less than 0.05 indicates we reject the null hypothesis, which is the POI rating has no significant effect on the ebike station distanace


## Challenges 

I faced difficulties successfully running a get request for the Yelp API. I kept getting a 403 error. My code that I ran worked several days before and I was able to create a dataframe, but when I came back a few days later the code wouldn't run. The headers, parameters, url are all correct and work in Postman and on Yelp's API website, but will not work when I run my python code. I seeked out help from Larry AI and a Mentor and they were uanable to solve the issue after several hours. This seriously impacted my ability to complete the project sucessfully as I needed the rating information from Yelp to do the linear regression as well as other tasks.

I pulled two JSON files to mimick a get request to prove that I was able to complete the small tasks, but due to the limited size it wasn't enough to add to the database as there would be too many missing values.

## Future Goals
1. Explore additional APIs
2. Review python's visualizations in greater depth
3. Use existing datasets and practice developing statistical models

