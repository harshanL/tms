# Tournament Management System

This was developed using Python 3.8.5. 

## Running the application

1. Clone the repo
2. Navigate to the clone repo directory and create a virtual env and activate it
3. Execute 'pip install -r requirements.txt' command to install dependencies
3. Execute 'python manage.py migrate' command to create database tables
5. Create a super user using 'python manage.py createsuperuser' command only 
if needs to login to the admin console
6. Execute 'python manage.py generate_data' command to populate 
database and users and groups (league_admin, coach, player)
7. Run the application using 'python manage.py runserver' command
8. It is possible to run integration tests using 'python manage.py test' command

## Users

- League Admin - eric_matific
- Coaches - 16 coach users corresponding to dummy data 
- Players - 244 player users corresponding to dummy data 

The default password is 'pwd'. 

## Exposed services and resources 

### Resources

1. Team - Represents a Basket-ball team with following properties.
    * id
    * name
    * average_score(read-only)

2. Coach - Represents a team coach with following properties.
    * id
    * name
    * team
    * team_name(read-only)

3. Player - Represents a Basket-ball player with following properties.
    * id
    * name
    * team
    * team_name(read-only) 
    * height
    * matches(read-only)
    * average_score(read-only)

4. Match - Represents a Basket-ball match with following properties.
    * id
    * scheduled_date
    * stadium
    * round - (Qualifying/Quarter-Final/Semi-Final/Final)
    * team1
    * team1_name(read-only)
    * team2
    * team2_name(read-only)
    * team1_score
    * team2_score
    
5. MatchPlayer - Represents a player of a Basket-ball match with following properties.
    * player - id of the player
    * name - name of the player
    * match - match id
    * score - individual player score

### Services

All of the services are protected and must provide basic authentication 
header when invoking exposed services. Please note that, resource authorization 
has not implemented. Thus, any user with valid credentials will be able to browse 
all the APIs. 

1. tms_web/coaches - Supports listing(GET) and creation(POST) of Coach entities.
2. tms_web/coaches/{coach-id} - Supports listing(GET), update(PUT), partial-update(PATCH) 
and deletion(DELETE HTTP) of Coach entities.
3. tms_web/players - Supports listing(GET) and creation(POST) of Player entities.
4. tms_web/players/{player-id} - Supports listing(GET), update(PUT), partial-update(PATCH) 
and deletion(DELETE HTTP) of Player entities.
5. tms_web/matches - Supports listing(GET) and creation(POST) of Match entities. 
Listing will provide the following details of each match.
    - Match venue and schedule
    - Participating teams and their scores
    - Round (Qualifying, Quarter-Final, Semi-Final, Final)
6. tms_web/matches/{match-id} - Supports deletion(DELETE) of Match entities.
7. tms_web/matches/{match-id}/players - Supports listing(GET) and creation(POST) of MatchPlayer 
entities. This API can be used to create and list participating players of a given match-id.
8. tms_web/teams - Supports listing(GET) and creation(POST) of Team entities.
9. tms_web/teams/{team-id} - Supports listing(GET), update(PUT), partial-update(PATCH) 
and deletion(DELETE HTTP) of Team entities.
10. tms_web/teams/{team-id}/top-players - Lists(GET) Top players of a given team id.
11. tms_web/teams/{team-id}/players - Lists(GET) players of a given team id.

## Further Improvements
1. Incorporate a resource authorization mechanism along with a proper permission model by 
assigning permissions to created roles and validating resource accesses against granted permissions
2. Track the stats
3. Additional business rule validations (ex: 10 players for a match from a team)
4. Module breakdown : However, in Django REST framework, views can act as the business layer as well and I was 
    unable to come up with a proper module breakdown for the business layer. Different people 
    suggest different things (ie. add business logic to serializers, add logic to view, 
    define separate service modules) and I couldn't figure out what's correct or wrong (probably 
    because I'm new to Python and I'm not mush familiar with python best practises).