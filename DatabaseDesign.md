
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

Tables with 1000+ rows: Trails, Species, Campsites, ParkBiodiversity

### Two Advanced Queries: 
1. Rank the parks by the number of native species. This uses a join and aggregation
```

SELECT Parks.ParkName, count(ParkBiodiversity.Biodiversity) AS NativeCount 
FROM Parks INNER JOIN ParkBiodiversity ON Parks.ParkName = ParkBiodiversity.Park 
WHERE ParkBiodiversity.Nativeness = 'Native' 
GROUP BY ParkName 
ORDER BY NativeCount desc;


```
![screenshot of first 15 rows of first advanced query](https://github.com/uiuc-fa21-cs411/jaav/blob/main/img/Screen%20Shot%202021-10-21%20at%2010.06.49%20PM.png?raw=true)

2.  Find easy nearby trails. This computes the trails that are greater than 5 miles and greater than 700ft elevation. It also only looks in national parks that are within +/- 2 degrees longitude and latitude of Yosemite National Park (38 degrees north, 120 degrees west). This uses a subquery and join.(VINEET UPDATE THIS)
```

SELECT * FROM (SELECT AVG(Trails.Popularity) as longTrailPopularity, Trails.ParkName 
FROM Trails WHERE Trails.Length >= (select avg(Trails.Length) as avgLength from Trails) group by Trails.ParkName)  as q1 
NATURAL JOIN 
(SELECT AVG(Trails.Popularity) as ShortTrailPopularity, Trails.ParkName from Trails where Trails.Length < (select avg(Trails.Length) as avgLength from Trails) group by Trails.ParkName) as q2;

```
<img width="1440" alt="query2" src="https://user-images.githubusercontent.com/37272048/138566262-f4e0ec2f-1227-407e-8d77-e9da781e1ed9.png">
### Indexing: 
What was the baseline perfomace for each query? 





![query1index1](https://user-images.githubusercontent.com/37272048/138566798-116f528b-c519-4cec-a07c-3e63b650d917.png)

1. For Query 1, the overall time was .17 seconds, the most significant source of time in this query is the filtering step (where statement). This is where many different entries need to be looked up in order to compare them. This is also the area where indexing helps the most to improve performance. This step took .93 seconds with the default indexing. 
2. For Query 2, without creating an index, this query takes 2ms to run. The majority of that time is spent filtering the trails (1.5ms) and a small amount of time (.063)ms is spent filtering the parks. This is because the trails dataset has several thousand rows and the parks table only has around 50. For this query it is already very fast, so it might be hard to significantly improve the performance. 

What 3 indexing designs did we analyze for each query? 

Query 1




1. Index on all columns in biodiversity table: Park, Biodiversity, Nativeness \
This index design performed worse than the default design. It took .19 seconds overall and .103 seconds to do the filtering (which is the part affected by the new index system).  This index design puts an index on every column of the biodiversity table. We are filtering about 10,000 rows from over 100,000 rows. Extra indices are probably counter productive since we are mostly looking at the table  in general as opposed to just a few specific points.
2. Index on only Park and biodiversity \
This approach was only moderately better than the default approach. (.16 seconds overall as opposed to .17 seconds) This is probably because we unlimited a possibly unnecessary index on the nativeness. Also the reason it is only slightly better is because indices are less effective when querying large numbers of rows like we are aggregating in query 1. 
3. Index on only park and biodiversity, but a hash-based index \
This is the exact same (.16 seconds) as the previous index design except that it uses a hash-based index as opposed to a btree. Btree is good for querying large amounts of data, especially ranged-based queries. A hash index is good because it generally will use less pointer arithmetic than the B-tree. It performs well when using an “equals” filter. In this base, our query is computing a “equals” filter which is probably one reason that the hash-index is fairly effective and on par with the b-tree performance. 

Query 2

<img width="1435" alt="Query2_Trails(TrailName, Popularity)" src="https://user-images.githubusercontent.com/35547998/138566527-eada7cb2-c9cc-438a-99e9-06f653137e61.png">

<img width="1439" alt="Query2_Trails(Length, ParkName)" src="https://user-images.githubusercontent.com/35547998/138566565-3f309d09-a920-42d5-b200-d2c7881fe201.png">

<img width="1440" alt="Query2_Trails(Length, Popularity)" src="https://user-images.githubusercontent.com/35547998/138566596-b7285455-5341-4e36-be63-b3061aeea11f.png">


What index design did we choose for each query? 
- Query 1: We settled on index design 2 which was fast and also uses a b-tree which we think will be a better overall implementation. It is more extensible for different types of filters or aggregations on this table. It also uses indices on the foreign keys in this table which will likely be accessed the most. Finally, unlike design 1, it doesn’t have any extra indices which might slow down the query by adding excess overhead. 
- Query 2: 
