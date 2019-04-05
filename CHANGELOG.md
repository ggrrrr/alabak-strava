* Fixes 2019-04-05
  * updateAll fix
  * few changes in the folders
  * added updateSegment param during updateAll for fetch /segment/<id> and update the DB fields for strava_segment_name and strava_sport this also double the Strava API calls per segment
  * Added requirements.txt file and virtualenv in readme file.
* SQL udpate 2019-04-02
```
alter table strava_leaderboard
add column strava_segment_name character varying(255) NOT NULL

alter table strava_leaderboard
add column  strava_sport character varying(255) NOT NULL
```
