* SQL udpate 2019-04-02
```
alter table strava_leaderboard
add column strava_segment_name character varying(255) NOT NULL

alter table strava_leaderboard
add column  strava_sport character varying(255) NOT NULL
```