
# Project Conceptual Design 

### ER/UML Diagram 
***

### Explanation of Relationships in ER/UML
***

### Relational Schema  TODO: Update this after adding the diagram to make sure that the information is consistenet between the two 
***
Users(username:VARCHAR(255) [PK],password:VARCHAR(255))

Parks(park_name:VARCHAR(255), [PK], state:VARCHAR(255), acres:INT, longitude: INT, latitude:INT)

Trails(name:VARCHAR(255) [PK], park_name:VARCHAR(255) [FK to Parks.park_name],state:VARCHAR(255), longitude: Decimal, latitude:Decimal, popularity: Decimal, length: Decimal, elevation_gain: INT, difficulty_rating: INT, route_type:VARCHAR(255), avg_rating: Decimal, num_reviews:INT, features:VARCHAR(255), activities:VARCHAR(255),units:VARCHAR(1))

Attendance(state:VARCHAR(255), park_name:VARCHAR(255)[PK][FK to Parks.park_name], park_type:VARCHAR(255),visitors:INT,year: INT[PK])

Campsites(camp_name:VARCHAR(255)[PK], park_name:VARCHAR(255)[FK to Parks.park_name], capacity:INT, price:INT)

Species(park_name:VARCHAR(255) [PK, FK to Parks.park_name], scientific_name:VARCHAR(255) [PK], category:VARCHAR(255), order:VARCHAR(255), family:VARCHAR(255), common_name:VARCHAR(255), occurrence:VARCHAR(255), nativeness:VARCHAR(255), abundance:VARCHAR(255), conservation_status:VARCHAR(255))


