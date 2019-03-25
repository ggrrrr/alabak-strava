Някъде долу в ляво на sidebar-a поле "страва класация" примерно. 
Тази класация да включва топ 10 като списъка трябва да е нещо от рода:

снимка, име, време

снимката и името да са линк към профила на потребителя, а времето към конкретната активност (каране)

Предполагам последното, за да се визуализира ще трябва да се парсне някак резултата от заявката. 
Принципно се чудя дали трябва да е live това нещо един вид всяко отваряне на маршрут да прави заявка и към страва или да има някакъв регулярен интервал при който всички описани сегменти да бъдат проверявани и кеширани резултатите. 
Как мислиш? 
Или другия вариант е при разпъване на полето strava класация да изпраща тогава заявка (пост).

Привет, 
Ето на кратко какво разбрах и по долу какво бих предложил, разбирасе ти решаваш ако те кефи.
Може и друго да измислим на по бира ;-)

From API doc:
https://developers.strava.com/docs/reference/#api-Segments
https://developers.strava.com/docs/reference/#api-models-DetailedSegment
HTTP GET: /segments/{id}
path params: id: segment ID from site


https://developers.strava.com/docs/reference/#api-Segments-getLeaderboardBySegmentId
https://developers.strava.com/docs/reference/#api-models-SegmentLeaderboard
HTTP GET: /segments/{id}/leaderboard
path params: id: segment ID from site
query params:
	gender: default M
	age_group:
	weight_class:
	following: 
	club_id: 
	date_range: this_year ...
	context_entries: No info
	page: start from 1 
	per_page: ?

Returns: entry_count, effort_count, kom_type, entries: [
		athlete_name, 
		elapsed_time, 
		moving_time, 
		start_date, 
		start_date_local, 
		rank
	]

Липсват данни за потребителя (athlete_id) и снимка.

Задна врата:
може да се ползва "https://www.strava.com/segments/{id}" и да се парсва HTML-a и от там може да се открадне
URL=effort и efforId - което ще доведе до данни за Athlete_id и т.н. каквото ни трябва.
но аз не съм много за такиа решения, ти си прецени.

Имам следното предложение:
Backend:
1. От http://developers.strava.com/docs/authentication "Refresh expired access tokens" може да се напраи refresh на token.
Това да става в някакъв cron job. ( това трябва да го проверя 100% дали съм разбрал правилно)
http://developers.strava.com/docs/authentication/#refresh-expired-access-tokens

UI:
1. При click na "страва класация" "backend" да GET-ва и записва в локална база данните с "last_update_timestamp".
2. Aко "last_update_timestamp” > "update_time_X" пак да ги "GET"-ва, ( пример: refresh on 24 hours on request)
	По този начин да правим малко API calls и така ще си пазим трафика. (Strava API rate limit: 600 requests every 15 minutes, 30000 daily)
	Ако преценим може да измилим и друг начин за "refresh"
	Също можем да напраим някакъв "internal rate limit" за да пазим API-a.
3.  UI-a да дава:
	list: <segment_name> (link to https://www.strava.com/segments/{id} )
		list: <rank, elapsed_time, athlete_name>
t.e.
	Няма да има снимка и линк към профил на потребителя, но ше има линк към "strava segment page".


https://hackernoon.com/dont-install-postgres-docker-pull-postgres-bee20e200198

docker pull postgres
mkdir -p $HOME/docker/volumes/postgres
docker run --rm   --name pg-docker -e POSTGRES_PASSWORD=docker -d -p 5432:5432 -v $HOME/docker/volumes/postgres:/var/lib/postgresql/data  postgres

docker pull dpage/pgadmin4
docker run -p 8080:80 \
        -e "PGADMIN_DEFAULT_EMAIL=user@domain.com" \
        -e "PGADMIN_DEFAULT_PASSWORD=SuperSecret" \
        -d dpage/pgadmin4



docker pull dockage/phppgadmin:latest
docker run --name='phppgadmin' -d \
  --publish=8080:80 \
  -e PHP_PG_ADMIN_SERVER_PORT=5431 \
  -e PHP_PG_ADMIN_SERVER_HOST=172.17.0.1 \
  -e PHP_PG_ADMIN_SERVER_DESC=kur \
dockage/phppgadmin:latest

export STRAVA_CLIENT_ID="123123"
export STRAVA_CLIENT_SECRET="secret"
export STRAVA_REFRESH_TOKEN="refresh"
export STRAVA_ACCESS_TOKEN="token"


# save strava setting
python3 src/python/setting.py --test saveAll --pgHost 192.168.88.254 \
	 --clientId ${STRAVA_CLIENT_ID} \
	 --clientSecret ${STRAVA_CLIENT_SECRET} \
	 --refreshToken ${STRAVA_REFRESH_TOKEN} \
	 --accessToken ${STRAVA_ACCESS_TOKEN}

# refresh strava API token
python3 src/python/cli.py --pgHost 192.168.88.254 \
--cmd refreshToken

# add  strava segment 4992444 to db with alabakTrackId asdasd
python3 src/python/cli.py  --pgHost 192.168.88.254 \
--cmd addSegment \
--trackId asdasd \
--stravaSegmentId 4992444

# fetch data from dababase
python3 src/python/cli.py --pgHost 192.168.88.254 \
--cmd fetchLeaderboard \
--trackId asdasd \
--stravaSegmentId "4992444"

# update data in database with db primary id 6
python3 src/python/cli.py  --pgHost 192.168.88.254 \
--cmd updateTrack \
--segmentId 6


