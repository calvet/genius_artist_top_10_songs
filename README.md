# genius_artist_top_10_songs
Genius API to fetch top 10 songs by artist. Built with Flask, DynamoDB and Redis.

### Requirements:
• Python 3+;
• Redis Server 3.0;
• DynamoDB Server (or running on AWS instance);
• Genius API Account;

### How to run:
• Configure ".env" file in the root folder of the project with the following information:
```
FLASK_ENV=production
DEBUG=False

GENIUS_ACCESS_TOKEN= ** GENIUS API ACCES TOKEN **

REDIS_HOST=** REDIS HOST ADDRESS **
REDIS_PORT=** REDIS PORT NUMBER **
REDIS_DAYS_EXPIRE=7

AWS_ACCESS_KEY_ID=** AWS ACCESS KEY **
AWS_SECRET_ACCESS_KEY=** AWS SECRET ACCESS KEY **
```

• After configuring env file, you may need to install the project requirements.
```pip install -r requirements.txt```

• Now you just have to run the flask application.
```flask run```
or just simply run:
```python -m app.py```

### How to fetch data from the API:
- You can make a GET request to the following URL:
```http://127.0.0.1:5050/api/v1/get_artist_top_songs/ARTIST_NAME```
(replace ARTIST_NAME with your favorite artist name)

~ optional: you can pass ?cache=False in the URL to avoid fetching cached data ~


