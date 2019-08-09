# Restaurant Recommender

A restaurant recommender service based on data crawled from Google Maps Places with Selenium.


## Development
```
docker build -t gcr.io/khuongav-recsys/recommender-app:dev .
docker run -p 5003:5003 gcr.io/khuongav-recsys/recommender-app:dev
```

+ Test
```
curl -H "Content-Type: application/json" -X POST -d '{"place_id": "ChIJEyLo-zE92jERXFAj_RC82Kk"}' http://localhost:5003/restaurant-recommender
curl -H "Content-Type: application/json" -X POST -d '[{"place_id": "ChIJEyLo-zE92jERXFAj_RC82Kk"}, {"place_id": "ChIJ4SgyUwsZ2jERPRgInXK4lfk"}]' http://localhost:5003/restaurant-recommender
```
