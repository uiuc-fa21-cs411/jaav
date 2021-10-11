
# Database Design

### To access database/project: 
* ssh awangoo2@20.88.14.242
* [Password](https://www.youtube.com/watch?v=dQw4w9WgXcQ) 

### DDL for creating table: 
```
CREATE TABLE parks (value type);
```

### Two Advanced Queries: 
1. Compute a ratio to estimate how crowded a park is. This ratio is the total visitors to a park divided by the total capacity of the parks campsites.
```
/*This is untested*/

SELECT ParkName,  Parks.TotalVisitors/ParkCapacity AS CrowdRatio
FROM (SELECT Campsites.ParkName, Parks.TotalVisitors, SUM(Campsites.Capacity) AS ParkCapacity
FROM Campsites INNER JOIN Parks ON Parks.ParkName = Campsites.ParkName
GROUP BY ParkName)
GROUP BY ParkName
ORDER BY CrowdRatio

```
![screenshot of first 15 rows of first advanced query](/img/file_path)

2.  Find easy nearby trails. This computes the trails that are less than 5 miles and less than 500ft elevation. It also only looks in national parks that are within +/- 10 degrees longitude and latitude of Champaign. 
```
/*This is untested, also, the subquery is slightly unecessary, but I think it is okay??? let me know thoughts or corrections -Alan*/

DECLARE CUR_LAT = 40
DECLARE CUR_LONG = -88

SELECT Parks.ParkName, Trails.TrailName, Trails.Length, Trails.Elevation
FROM Parks INNER JOIN Trials on Parks.ParkName = Trails.ParkName
WHERE Trails.Length < 5 AND Trails.Elevation < 500 and Parks.ParkName IN 
	(SELECT ParkName FROM Parks WHERE Latitude > CUR_LAT-10 AND Latitude < 	CUR_LAT+10 AND Longitude < CUR_LONG+10 AND Longitude > CUR_LONG-10)
ORDER BY Trails.Popularity

```
![screenshot of first 15 rows of second advanced query](/img/file_path)

### Indexing: 
What 3 indexing designs did we analyze for each query? 

What index design did we choose for each query? 

Why did we choose these designs based on our analysis? 
