# Installation instructions

### Dockerized
1. Git clone:
```
git clone https://github.com/mikeliou/workable_movies_app
```
2. Change directory
```
cd workable_movies_app
```
3. Build docker image
```
docker build --no-cache -t workable_app:0.1.0 .
```
4. Run command to erase data from previous executions (optional)
```
rm -rf mysql-volume/data
```
5. Docker compose
```
docker-compose up
```
6. Create database tables
```
docker exec -it <container_id> python -m app.database.main
```
7. Open browser and type URL (or click below)
[Workable movies app](http://localhost:8070/)

# API documentation

|Endpoint|Description|Parameters|
|--------|:---------:|----------|
|/|Gets all movies from database|-|
|/actions/like/<int:movie_id>|Creates a positive action (like) in database|movie_id: int|
|/actions/dislike/<int:movie_id>|Creates a negative action (dislike) in database|movie_id: int|
|/actions/remove/<int:action_id>|Deletes an action from database|action_id: int|
|/movies/all|Gets all movies from database|
|/movies/<int:user_id>|Gets all movies from database based on user id|user_id: int|
|/movies/create|Creates a movie in database|title: string, description: string|
|/users/create|Creates a user in database|first_name: string, last_name: string, email: string, password: string|
|/users/auth|Authenticates a user from database|email: string, password: string|
|/sort_by|Changes the sorting field for movies|field: string|
|/add_movie|Redirects to add_movie_form|-|
|/sign_up|Redirects to sign_up_form|-|
|/login|Redirects to login_form|-|

# Class diagram

![Class diagram](class_diagram/img.jpg)
