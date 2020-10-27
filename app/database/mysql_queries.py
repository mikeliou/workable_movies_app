
GET_MOVIE_DATA = """
    SELECT A.id,A.title,A.description,A.created,A.updated,A.posted_by,A.full_name,A.likes,B.dislikes FROM (
    SELECT movies.id, movies.title, movies.description, movies.created, movies.posted_by,movies.updated,
    CONCAT(users.first_name,' ',users.last_name) as full_name, COALESCE(cnt,0) as likes
    FROM movies 
    INNER JOIN users ON movies.posted_by=users.id
    LEFT OUTER JOIN (SELECT movie_id, count(*) cnt 
    FROM actions WHERE action_type=1 GROUP BY movie_id) x ON movies.id = movie_id) as A

    INNER JOIN(
    SELECT movies.id, movies.title, movies.description, movies.created, movies.posted_by,movies.updated,
    CONCAT(users.first_name,' ',users.last_name) as full_name, COALESCE(cnt,0) as dislikes
    FROM movies 
    INNER JOIN users ON movies.posted_by=users.id
    LEFT OUTER JOIN (SELECT movie_id, count(*) cnt 
    FROM actions WHERE action_type=0 GROUP BY movie_id) x ON movies.id = movie_id) as B

    ON A.id = B.id
"""

GET_MOVIE_DATA_BY_ID = """
    SELECT A.id,A.title,A.description,A.created,A.updated,A.posted_by,A.full_name,A.likes,B.dislikes FROM (
    SELECT movies.id, movies.title, movies.description, movies.created, movies.posted_by,movies.updated,
    CONCAT(users.first_name,' ',users.last_name) as full_name, COALESCE(cnt,0) as likes
    FROM movies 
    INNER JOIN users ON movies.posted_by=users.id
    LEFT OUTER JOIN (SELECT movie_id, count(*) cnt 
    FROM actions WHERE action_type=1 GROUP BY movie_id) x ON movies.id = movie_id
    WHERE movies.posted_by = %s) as A

    INNER JOIN(
    SELECT movies.id, movies.title, movies.description, movies.created, movies.posted_by,movies.updated,
    CONCAT(users.first_name,' ',users.last_name) as full_name, COALESCE(cnt,0) as dislikes
    FROM movies 
    INNER JOIN users ON movies.posted_by=users.id
    LEFT OUTER JOIN (SELECT movie_id, count(*) cnt 
    FROM actions WHERE action_type=0 GROUP BY movie_id) x ON movies.id = movie_id
    WHERE movies.posted_by = %s) as B

    ON A.id = B.id
"""
