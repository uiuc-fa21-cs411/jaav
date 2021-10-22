
# Database Design

### To access database/project: 
* ssh awangoo2@20.88.14.242
* [Password](https://www.youtube.com/watch?v=dQw4w9WgXcQ) 


### DDL commands
***
```
Create table Parks(ParkName VARCHAR(255) primary key, Latitude DECIMAL(15,5), Longitude DECIMAL(15,5),Size DECIMAL(15,5), State VARCHAR(255));

Create table Trails(TrailName VARCHAR(255) primary key, ParkName VARCHAR(255) references Park(ParkName), Elevation DECIMAL(15,5), Length DECIMAL(15,5), Popularity DECIMAL(15,5));

Create table Species(ScientificName VARCHAR(255) primary key, CommonName VARCHAR(255), Category VARCHAR(255));

Create table VisitedParks(Username VARCHAR(255) references Users(Username), ParkName VARCHAR(255) references Parks(ParkName));

Create table Campsites(CampsiteName VARCHAR(255) primary key, ParkName VARCHAR(255) references Parks(ParkName), Price DECIMAL(15,5), Capacity DECIMAL(15,5))

Create table FavoriteTrails(Username VARCHAR(255) references Users(Username), TrailName VARCHAR(255) references Trails(TrailName), Visited INT);

Create table ParkBiodiversity(Park VARCHAR(255) references Parks(Parkname), Biodiversity VARCHAR(255) references Species (ScientificName), Nativeness VARCHAR(255));

Create table Users(Username VARCHAR(255) primary key, Password VARCHAR(255));
```

### Two Advanced Queries: 
1. Rank the parts by the number of native species. This uses a join and aggregation
```

SELECT Parks.ParkName, count(ParkBiodiversity.Biodiversity) AS NativeCount 
FROM Parks INNER JOIN ParkBiodiversity ON Parks.ParkName = ParkBiodiversity.Park 
WHERE ParkBiodiversity.Nativeness = 'Native' 
GROUP BY ParkName 
ORDER BY NativeCount desc;


```
![screenshot of first 15 rows of first advanced query](/img/Screen Shot 2021-10-21 at 9.51.35 PM.png)

2.  Find easy nearby trails. This computes the trails that are less than 5 miles and less than 500ft elevation. It also only looks in national parks that are within +/- 10 degrees longitude and latitude of Champaign. This uses a subquery and join
```

SELECT Parks.ParkName, Trails.TrailName, Trails.Length, Trails.Elevation 
FROM Parks INNER JOIN Trails on Parks.ParkName = Trails.ParkName 
WHERE Trails.Length > 5 AND Trails.Elevation > 700 and Parks.ParkName IN 
	(SELECT ParkName FROM Parks WHERE Latitude > 38 - 2 AND Latitude < 38+2 AND Longitude < -120+2 AND Longitude > -120-2) 
ORDER BY Trails.Popularity;

```
![screenshot of first 15 rows of second advanced query](/img/Screen Shot 2021-10-21 at 9.54.43 PM.png)

### Indexing: 
What 3 indexing designs did we analyze for each query? 

What index design did we choose for each query? 

Why did we choose these designs based on our analysis? 
