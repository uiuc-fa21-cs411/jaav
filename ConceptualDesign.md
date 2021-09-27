
# Project Conceptual Design 

### ER/UML Diagram 
***

<img width="570" alt="Screen Shot 2021-09-26 at 8 32 30 PM" src="https://user-images.githubusercontent.com/37272048/134832897-8ec0f0ab-d283-44a2-b878-b50f9383070a.png">


### Explanation of Entities and Relationships in ER/UML
***
#### Entity Descriptions and Assumptions 
1. Users: each user consists of a username which uniquely identifies users, and a password that allows them to access the application and store their favorite parks and trails. Both of these values are strings. 
2. Parks: Each park is uniquely identified by its name, which is the primary key. This entity contains data related to that park including the decimal longitude and latitude of the centroid of the park, the size in acres of the park and the total number of visitors to the park since the park opened which must be an integer. 
3. Campsites: Each campsite is uniquely identified by its name as a primary key. This works because every campsite name is prefixed with the name of the park and no park has two campsites with the same name. The campsite name will be a string. Each campsite also includes a foreign key which is the park where the campsite is located, which is a string and a foregin key connecting it to the parks table. Finally, each campsite has a decimal price, which is a typical overnight fee for one site. There is also the decimal capacity of the campground. 
4. Trials: Each trail's primary key is the name of the trail which is a unique string for US national parks. Trails also contain a foreign key which references the name of the park where the trail  is found. Finally, each trail includes three decimal values that describe the trail: the elevation gain, the length (in miles), and the popularity which is a measure calculated and published by alltrails.com. 
5. Species: The species table provides biodiversity information to the user about each park. Each species is uniquely identified by a string which is its scientific name. It has a string for the species common name. The name of the park where this species was sighted (foreign key to parks). It also includes information about whether or not the species is native (a string) and a string which is the category of species (bird, vascular plant, ect.)

#### Relationship Descriptions and Assumptions 

1. Favorite trails: A many to many relationship between the users and the trails. Each user can have selected zero to any number of trails to be their favorite. Zero to any number of users can select the same trail to be a favorite. This relationship also contains a int atrribute (which will always be 0 for false or 1 for true) which shows whether or not the user has visited the trail.
2. Visited parks: A many to many relationship between the users and the parks. Each user can select zero to any number of parks to be their favorite. A park can be visited by zero to any number of users. 
3. Park’s trails: A many to one relationship between parks and trails. Every trail must belong to a park and only one park. A park must have at least 1 trail. 
4. Park biodiversity: A many to many relationship between parks and species that represents which species have been seen in each park. Each species must be in at least one park, but can also be seen in any number of parks. Additionally, each park must have at least one species associated with it, but there is no limit to the number of species in a park.  
5. Park’s campsites: A many to one relationship between parks and campsites. Each campsite must be in one and only one park. A park must have at least one campsite, but there is no limit to the number of campsites. 


### Relational Schema
***
```Users(Username:VARCHAR(255) [PK], Password:VARCHAR(255))

Parks(ParkName:VARCHAR(255) [PK], Latitude:DECIMAL(15,5), Longitude: DECIMAL(15,5), Size:DECIMAL(15,5), TotalVisitors:INT))

Trails(TrailName:VARCHAR(255) [PK], ParkName:VARCHAR(255) [FK to Parks.ParkName], Elevation:DECIMAL(15,5), Length:DECIMAL(15,5), Popularity:DECIMAL(15,5))

Campsites(CampsiteName:VARCHAR(255) [PK], ParkName:VARCHAR(255) [FK to Parks.ParkName], Price:DECIMAL(15,5), Capacity:DECIMAL(15,5))

Species(ScientificName:VARCHAR(255), ParkName:VARCHAR(255) [FK to Parks.ParkName], CommonName:VARCHAR(255), Nativeness:VARCHAR(255), Category:VARCHAR(255))

VisitedParks(Username:VARCHAR(255)[FK to Users.Username], ParkName:VARCHAR(255) [FK to Parks.ParkName])

FavoriteTrails(Username:VARCHAR(255)[FK to Users.Username], TrailName:VARCHAR(255) [FK to Trails.TrailName], Visited:INT)
```


