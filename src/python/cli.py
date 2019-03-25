import argparse
import logging
import sys

from strava import api, objects
import pgsql
import setting as pgSetting



def loadSetting(conn, args):
    setting = pgSetting.StravaSetting(dbConn = conn, args = args)
    setting.readAll()
    return setting

def updateTrack(conn, args):
    trackId = args.trackId
    id = args.segmentId

    data = pgsql.SegmentLeaderboardSql.fetchData( conn, id = id, alabak_track_id = trackId)
    strava_segment_id = data['strava_segment_id']
    id = data['id']

    strava = api.StravaApi(args)

    leaderboard = objects.SegmentLeaderboard(strava_segment_id
        , strava.callLeaderboard(strava_segment_id) )


    pgsql.SegmentLeaderboardSql.update(conn, id, leaderboard)

    print ( leaderboard)

def addSegment(conn, args):
    if args.trackId is None:
        raise Exception("trackId is None")
    if args.stravaSegmentId is None:
        raise Exception("stravaSegmentId is None")
    strava_segment_id = args.stravaSegmentId
    trackId = args.trackId

    conn = pgsql.pgConnect(args)
    strava = api.StravaApi(args)

    segment = objects.Segment(jsonData = strava.callSegment(strava_segment_id))

    leaderboard = objects.SegmentLeaderboard(strava_segment_id
        , strava.callLeaderboard(strava_segment_id) )
    leaderboard.setAlabakTrackId(trackId)

    conn = pgsql.pgConnect(args)

    conn = pgsql.pgConnect(args)
    pgsql.SegmentLeaderboardSql.insert( conn, leaderboard)
    conn.close()

    print ( leaderboard)

def fetchLeaderboard(conn, args):
    id = args.segmentId
    alabak_track_id = args.trackId
    strava_segment_id = args.stravaSegmentId
    conn = pgsql.pgConnect(args)
    data = pgsql.SegmentLeaderboardSql.fetchDataJson(conn
        , id = id
        , strava_segment_id = strava_segment_id
        , alabak_track_id = args.trackId
        )
    print(data)
    conn.close()

def refreshToken(setting, conn, args):
    strava = api.StravaApi(args)
    strava.callRefreshToken()
    print(strava.accessToken)
    args.accessToken = strava.accessToken
    setting.saveAll()

def updateAll(conn, args):
    """
    TODO add filter by segment and/or alabak id
    """

    strava = api.StravaApi(args)

    "fetch tracks from DB"
    segments = pgsql.SegmentLeaderboardSql.fetchAll(conn)
    for data in segments:
        # print ( data)
        strava_segment_id = data['strava_segment_id']
        id = data['id']
        logging.debug("fetchData for: id:%s, strava_segment_id:%s" % (id, strava_segment_id))

        "fetch segment leaderboard from strava API"
        leaderboard = objects.SegmentLeaderboard(strava_segment_id, strava.callLeaderboard(strava_segment_id) )

        logging.debug("data:%s" % (leaderboard))

        "save new leaderboard to DB"
        pgsql.SegmentLeaderboardSql.update(conn, id, leaderboard)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='alabak.strava CLI.')
    parser.add_argument('--pgDb', default="alabak", dest='pgDb', help='pg Db default: alabak')
    parser.add_argument('--pgUser', default='postgres', dest='pgUser', help='pg user')
    parser.add_argument('--pgPassword', default='docker', dest='pgPassword', help='pg password')
    parser.add_argument('--pgHost', default='localhost', dest='pgHost', help='pg host')
    parser.add_argument('--pgPort', default=5432, dest='pgPort', type=int, help='pg port ')

    parser.add_argument('--clientId', default=None, dest='clientId', help='strava user Id', required=False)
    parser.add_argument('--clientSecret', default=None, dest='clientSecret', help='strava user Id', required=False)
    parser.add_argument('--grantType', default='refresh_token', dest='grantType', help='strava grant type for refresh token', required=False)
    parser.add_argument('--refreshToken', default=None, dest='refreshToken', help='strava refresh token', required=False)
    parser.add_argument('--accessToken', default=None, dest='accessToken', help='strava access token', required=False)
    parser.add_argument('--stravaCall', default=None, dest='stravaCall', help='strava API call refresh', required=False)

    parser.add_argument('--trackId', default=None, dest='trackId', help='alabak track id')
    parser.add_argument('--stravaSegmentId', default=None, dest='stravaSegmentId', help='strava Segment Id')
    parser.add_argument('--segmentId', default=None, dest='segmentId', help='db id')

    cmds = ['fetchLeaderboard', 'addSegment', 'updateTrack', 'refreshToken', 'updateAll']

    parser.add_argument('--cmd', default=None,dest='cmd'
                        , choices=cmds, help='what to do')

    parser.add_argument('--level', default='error', dest='level', help='level')

    args = parser.parse_args()
    if args.level == "debug":
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    conn = pgsql.pgConnect(args)

    if conn is None:
        raise Exception("unable to connect to DB!")

    setting = loadSetting(conn, args)

    if args.cmd in "fetchLeaderboard":
        fetchLeaderboard(conn, args)
        sys.exit(0)

    if args.cmd in "addSegment":
        addSegment(conn, args)
        sys.exit(0)

    if args.cmd in "updateTrack":
        updateTrack(conn, args)
        sys.exit(0)

    if args.cmd in "updateAll":
        updateAll(conn, args)
        sys.exit(0)

    if args.cmd in "refreshToken":
        refreshToken(setting, conn, args)
        sys.exit(0)
    
    raise Exception("not implemented cmd: %s" % args.cmd)

