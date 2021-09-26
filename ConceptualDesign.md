
# Project Conceptual Design 

### ER/UML Diagram 
***

<img src="images/UML diagram.JPG" alt="UML Diagram" width="600"/>

### Explanation of Entities and Relationships in ER/UML
***



### Relational Schema
***
Users(Username:VARCHAR(255) [PK], Password:VARCHAR(255))

Parks(ParkName:VARCHAR(255) [PK], Latitude:DECIMAL(15,2), Longitude: DECIMAL(15,2), Size:DECIMAL(15,2), TotalVisitors:INT))

Trails(TrailName:VARCHAR(255) [PK], ParkName:VARCHAR(255) [FK to Parks.ParkName], Elevation:DECIMAL(15,2), Length:DECIMAL(15,2), Popularity:DECIMAL(15,2))

Campsites(CampsiteName:VARCHAR(255) [PK], ParkName:VARCHAR(255) [FK to Parks.ParkName], Price:DECIMAL(15,2), Capacity:DECIMAL(15,2))

Species(ScientificName:VARCHAR(255), ParkName:VARCHAR(255) [FK to Parks.ParkName], CommonName:VARCHAR(255), Nativeness:VARCHAR(255), Category:VARCHAR(255))


