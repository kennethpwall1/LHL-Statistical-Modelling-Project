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

I used the Pandas concat method to create a union with the foursqaure dataframe with the yelp dataframe. I then dropped all duplicate values that had the same name which reduced the data set from 5000 to 800 as many of the stations have POIs that are close together. I then joined the union of foursquare and yelp on the station id to obtain the free bikes for each station from the ebikes dataframe. I dropped longitude and latitude columns as they were unecessary for the analysis.

```python
poi_join = pd.concat([foursquare_df,yelp_df], ignore_index= True)
poi_join = poi_join.drop_duplicates(subset=['name'], ignore_index=True)

join_df = pd.merge(fsq_df, vancouver_network_stations,on='station_id', how='left')
join_df = join_df.drop(columns=['longitude', 'latitude'])
```

### Creating and loading data into SQlite database
I used the create_engine module from the sqlalchemy library to create an SQlite database using the following code:

```python 
from sqlalchemy import create_engine
sqlite_db = 'sqlite:///../data/ebikes.db'
engine = create_engine(sqlite_db)
join_df.to_sql('points_of_interest' con=engine, index=False)
```

### Exploratory data analysis using statistics and python visualizations
First step in my EDA process is always to look at shape(), info() and describe(). Then I want to see the shape of the data and see if the distribution is normal so I run some histograms on the numerical data and see if there are any outliers. I also ran a scatter plot between free ebikes, POI distance and POI rating as well as the correlation between the variables. 

I primary used Matplotlib as my EDA tool for visualization as I only needed simple charts.

```python
import matplotlib.pyplot as plt
```

```python
plt.hist(full_join'free_bikes'], bins=20)
plt.show()
```
A histogram of ebikes reveals skewed data with bike stations having a low number of free bikes. This makes sense as Vancouver is a city where bikes are used frequently and tourists often visit the city and like to explore via bike.

![Histogram ebikes](/images/hist_ebikes.png "ebikes")


A histogram of POI distance from bike stations reveals skewed data and that more bike stations are placed closer to the POI interest at an average of 360 meters between points of interest.

![Histogram poi distance](/images/hist_poi.png "POI distance")

I wanted to see if there was a relationship between two variables: free ebikes and distance from points of interest so I created a scatterplot.

```python
x= full_join['free_bikes']
y= full_join['distance']
plt.figure(figsize=(8, 6))
plt.scatter(x,y)
plt.xlabel('free_bikes')
plt.ylabel('distance')
plt.show()
```

![Scatter Plot](/images/scatter.png "scatter")

The distribution of dots didn't point to any meaningful relationship so I decided to calculate the correlation between the two variables:

```python
correlation = full_join['free_bikes'].corr(full_join['distance'])
```
This resulted in a correlation of: 0.1633244524848804, which means very minimal correlation.

I wanted to see if there was a relationship between two variables: free ebikes and the rating of the points of interest so I created a scatterplot.

```python
x= full_join['free_bikes']
y= full_join['rating']
plt.figure(figsize=(8, 6))
plt.scatter(x,y)
plt.xlabel('free_bikes')
plt.ylabel('rating')
plt.show()
```

![Scatter Plot](/images/scatter_rating_freebikes.png "ratings scatter")

The distribution of dots didn't point to any meaningful relationship so I decided to calculate the correlation between the two variables:

```python
correlation = full_join['free_bikes'].corr(full_join['rating'])
```
This resulted in a correlation of: 0.016574207980216353 which means almost no correlation.


### Building and interpreting statistical models
I want to identify relationships between variables, make predictions about future sets of data, and transform the data into visualizations so that non-analysts and stakeholders can consume and leverage it.

The joined dataframe only has three characteristics free ebikes, POI distance, and POI rating as numerical variables:
- Independent variable: POI distance
- Independent variable: POI rating
- Dependent: free ebikes

I chose to do first do simple linear regression on each independent variable and its potential effect on the dependent variable, the number of free ebikes.

1. POI Distance

    H0: The points of interest distance has no significant effect on the number of ebikes available

    H1: the points of interest distance has a significant effect on the number of ebikes available

    **See model results below**

2. POI rating

    H0: The points of interest rating has no significant effect on the number of ebikes available

    H1: the points of interest rating has a significant effect on the number of ebikes available

    **See model results below**


## Results

### POI DISTANCE - OLS SIMPLE LINEAR REGRESSION
Dep. Variable: free_bikes

Ind. Varianvle: POI_distance

R-squared: 0.007

POI_distance p-value: 0.301

H0: The points of interest distance has no significant effect on the number of ebikes available

H1: the points of interest distance have a significant effect on the number of ebikes available

R squared: is 0.007 so the independent variable (POI distance) doesn't explain the variability in the dependent variable (free ebikes)

P value: pvalue is 0.301, which is much greater that 0.05. A pvalue greater than 0.05 indicates that the obeserved data is consistent with the null hypothesis, which is the POI distance has no significant effect on the number of ebikes available

### POI RATING - OLS SIMPLE LINEAR REGRESSION
Dep. Variable: free_bikes

Ind. Varianvle: rating

R-squared: 0.000

rating p-value: 0.628

H0: There is no significant relationship between POI rating and ebike station distance

H1: There is a significant relationship between POI rating and ebike station distance

R squared: is low at 0.000 so the independent variable (POI rating) doesn't explain the variability in the dependent variable (ebike station distance)

P value: pvalue is 0.628, which is much greater that 0.05. A pvalue greater than 0.05 indicates that the obeserved data is consistent with the null hypothesis, which is the POI rating has no significant effect on the number of ebikes available


## Challenges 

I faced difficulties successfully running a get request for the Yelp API. I kept getting a 403 error. My code that I ran worked several days before and I was able to create a dataframe, but when I came back a few days later the code wouldn't run. The headers, parameters, url are all correct and work in Postman and on Yelp's API website, but will not work when I run my python code. I seeked out help from Larry AI and a Mentor and they were uanable to solve the issue after several hours. This seriously impacted my ability to complete the project sucessfully as I needed the rating information from Yelp to do the linear regression as well as other tasks. A Mentor Lead was not able to solve the problem directly but found a solution using the urllib with the following partial code snippet.

```python
import urllib.request
import urllib.parse
import json

query_string = urllib.parse.urlencode(params)
url_with_params = f"{url}?{query_string}"
req = urllib.request.Request(url_with_params, headers=headers)

try:
    with urllib.request.urlopen(req) as response:
        response_body = response.read()
        data = json.loads(response_body.decode("utf-8"))
        df = pd.DataFrame(data['businesses'])
        df['station_id'] = row['id']
        yelp_df = pd.concat([yelp_df, df], ignore_index=True) 
except urllib.error.HTTPError as e:
    print(f"HTTP error occurred: {e.code} - {e.reason}")
except urllib.error.URLError as e:
    print(f"URL error occurred: {e.reason}")
```


## Future Goals
1. Explore additional APIs
2. Review python's visualizations in greater depth
3. Use existing datasets and practice developing statistical models

