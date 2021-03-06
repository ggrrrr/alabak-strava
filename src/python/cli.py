import argparse
import logging
import sys

from strava import api, objects
from sql import pgsql
import  setting as pgSetting

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

    leaderboard = objects.SegmentLeaderboard(strava_segment_id = strava_segment_id
        , jsonData = strava.callLeaderboard(strava_segment_id) )
    leaderboard.setAlabakTrackId(trackId)
    leaderboard.strava_segment_name = segment.strava_segment_name
    leaderboard.strava_sport = segment.strava_sport

    conn = pgsql.pgConnect(args)
    logging.debug(leaderboard)
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
        if args.updateSegment:
            segment = objects.Segment(jsonData = strava.callSegment(strava_segment_id))
            leaderboard.strava_segment_name = segment.strava_segment_name
            leaderboard.strava_sport = segment.strava_sport

        logging.debug("data:%s" % (leaderboard))

        "save new leaderboard to DB"
        pgsql.SegmentLeaderboardSql.update(conn, id, leaderboard)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='alabak.strava CLI.')
    pgsql.setArgparse(parser)
    api.setArgparse(parser)

    parser.add_argument('--updateSegment', action='store_true', dest='updateSegment', help='fetch segment name and update it')
    parser.add_argument('--trackId', default=None, dest='trackId', help='alabak track id')
    parser.add_argument('--stravaSegmentId', default=None, dest='stravaSegmentId', help='strava Segment Id')
    parser.add_argument('--segmentId', default=None, dest='segmentId', help='db id')

    _cmds = ['fetchLeaderboard', 'addSegment', 'updateTrack', 'refreshToken', 'updateAll']

    parser.add_argument('--cmd', default=None,dest='cmd'
                        , choices=_cmds, help='what to do')

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

