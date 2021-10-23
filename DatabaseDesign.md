
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

2.  Find the average popularity of the "short" and "long" trails for each Park where short Trails are in the bottom 50th percentile of all trail length and long trails are in the top 50th percentile of length. This query uses an aggregation function, join, and subquery.
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

1. For Query 1, the overall time was .17 seconds, the most significant source of time in this query is the filtering step (where statement). This is where many different entries need to be looked up in order to compare them. This is also the area where indexing helps the most to improve performance. This step took .93 seconds with the default indexing. The step that took the least amount of time was the single-row index lookup on Parks which is evidenced by the cost = 0.25 and time lapsed being 0.000 to 0.000 seconds.

<img width="1440" alt="Query2_defaultIndex" src="https://user-images.githubusercontent.com/35547998/138566889-fe0dcd40-085e-4ef7-b406-55540511a805.png">

2. For Query 2, the overall time was .02 seconds. The most significant source of time in this query is the step where the length of each trail needs to be compared to the average length for all trails. This occurs in the where clause, and with indexing, the performance can be improved. This total time elapsed during this step is .014 to (where the table scan on Trails occurs) to 2.645 seconds (during the filter step).

What 3 indexing designs did we analyze for each query? 

Query 1


1. Index on all columns in biodiversity table: Park, Biodiversity, Nativeness\
```create index bio_index on ParkBiodiversity (Park, Biodiversity, Nativeness);```
![q1](https://user-images.githubusercontent.com/37272048/138567218-755887a9-520e-4088-8e88-94b26e6da8c9.png)
This index design performed worse than the default design. It took .19 seconds overall and .103 seconds to do the filtering (which is the part affected by the new index system).  This index design puts an index on every column of the biodiversity table. We are filtering about 10,000 rows from over 100,000 rows. Extra indices are probably counter productive since we are mostly looking at the table  in general as opposed to just a few specific points.

2. Index on only Park and biodiversity\
```create index bio_index on ParkBiodiversity (Park, Biodiversity);```
![q2](https://user-images.githubusercontent.com/37272048/138567225-fd15db9c-08cc-4bb2-a94f-c3be38c04774.png)
This approach was only moderately better than the default approach. (.16 seconds overall as opposed to .17 seconds) This is probably because we unlimited a possibly unnecessary index on the nativeness. Also the reason it is only slightly better is because indices are less effective when querying large numbers of rows like we are aggregating in query 1. 

3. Index on only park and biodiversity, but a hash-based index\
``` create index bio_index on ParkBiodiversity (Park, Biodiversity) using hash;```
![q3](https://user-images.githubusercontent.com/37272048/138567234-d3344fa2-0ed3-4fd7-be6c-0903d78f2b16.png)
This is the exact same (.16 seconds) as the previous index design except that it uses a hash-based index as opposed to a btree. Btree is good for querying large amounts of data, especially ranged-based queries. A hash index is good because it generally will use less pointer arithmetic than the B-tree. It performs well when using an “equals” filter. In this base, our query is computing a “equals” filter which is probably one reason that the hash-index is fairly effective and on par with the b-tree performance. 

Query 2

1. Index on Trail Name and Popularity
<img width="1435" alt="Query2_Trails(TrailName, Popularity)" src="https://user-images.githubusercontent.com/35547998/138566527-eada7cb2-c9cc-438a-99e9-06f653137e61.png">

2. Index on Trail Length and Park Name
<img width="1439" alt="Query2_Trails(Length, ParkName)" src="https://user-images.githubusercontent.com/35547998/138566565-3f309d09-a920-42d5-b200-d2c7881fe201.png">

3. Index on Trail Length and Popularity
<img width="1440" alt="Query2_Trails(Length, Popularity)" src="https://user-images.githubusercontent.com/35547998/138566596-b7285455-5341-4e36-be63-b3061aeea11f.png"> 


What index design did we choose for each query? 
- Query 1: We settled on index design 2 which was fast and also uses a b-tree which we think will be a better overall implementation. It is more extensible for different types of filters or aggregations on this table. It also uses indices on the foreign keys in this table which will likely be accessed the most. Finally, unlike design 1, it doesn’t have any extra indices which might slow down the query by adding excess overhead. 
- Query 2: 
