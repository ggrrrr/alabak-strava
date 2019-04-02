# tests
import psycopg2
import psycopg2.extras

import argparse
import logging


class SettingSql:
    def createSql():
        out = [
            """CREATE SEQUENCE strava_setting_id_seq"""
            , """CREATE TABLE strava_setting
(
    "id" bigint DEFAULT NEXTVAL('strava_setting_id_seq') PRIMARY KEY,
    "row_ts" TIMESTAMP default now(),  
    "upd_ts" TIMESTAMP default now(),    
    "key1" character varying(255) NOT NULL,
    "value1" character varying(255) NOT NULL    
)"""
            , """CREATE INDEX strava_setting_id
    ON strava_setting USING btree
    (id )
    TABLESPACE pg_default;
"""]
        return out

    def dropSql():
        return [
            """DROP INDEX strava_setting_id"""
            , """DROP TABLE strava_setting"""
            , """DROP SEQUENCE strava_setting_id_seq """
            ]

    def insert( conn, key, value):
        sql = """
insert into strava_setting (key1, value1)
values('%s', '%s')
        """ % (key, value)
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            cur.execute(sql)
        except Exception as e:
            print(e)
            raise e
        finally:
            conn.commit()
            cur.close()

    def update( conn, key, value):
        sql = """
update strava_setting set 
value1 = '%s'
, upd_ts = now()
where 1=1
and key1 = '%s'
        """ % (value, key)
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            cur.execute(sql)
        except Exception as e:
            raise e
        finally:
            conn.commit()
            cur.close()

    def get(conn, key):
        sql = """
select * from strava_setting 
where 1=1
and key1 = '%s'
order by 1 desc
        """ % (key)
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            cur.execute(sql)
            out = list()
            for r in cur:
                # print()
                out.append(r['value1'])
            if len(out) == 0:
                return None
            return out[0]
        except Exception as e:
            print(e)
            raise e
        finally:
            conn.commit()
            cur.close()

class SegmentLeaderboardSql:
    def createSql():
        out = [
            """CREATE SEQUENCE strava_leaderboard_id_seq"""
            , """CREATE TABLE strava_leaderboard
(
    "id" bigint DEFAULT NEXTVAL('strava_leaderboard_id_seq') PRIMARY KEY,
    "row_ts" TIMESTAMP default now(),  
    "upd_ts" TIMESTAMP default now(),    
    "alabak_track_id" character varying(255) NOT NULL,
    "strava_segment_id" bigint NOT NULL,
    "strava_sport" character varying(255) NOT NULL,
    "strava_segment_name" character varying(255) NOT NULL,
    "strava_kom_type" character varying(255) NOT NULL,
    "strava_entry_count" character varying(255) NULL,
    "strava_effort_count" character varying(255) NULL,
    "entries_json" json NULL
    
)"""
            , """CREATE INDEX strava_leaderboard_strava_id
    ON strava_leaderboard USING btree
    (strava_segment_id )
    TABLESPACE pg_default;
"""]
        return out

    def dropSql():
        return [
            """DROP INDEX strava_leaderboard_strava_id"""
            , """DROP TABLE strava_leaderboard"""
            , """DROP SEQUENCE strava_leaderboard_id_seq """
            ]

    def insertSql(o):
        out = [
            """insert into strava_leaderboard (
            strava_segment_id
            , alabak_track_id
            , strava_sport
            , strava_segment_name
            , strava_kom_type
            , strava_entry_count
            , strava_effort_count
            , entries_json
            ) values ( %s, %s, '%s', '%s', '%s', '%s', '%s', '%s') """ % (
                o.strava_segment_id
                , ( 'Null' if o.alabak_track_id is None else "'%s'" % o.alabak_track_id)
                , o.strava_sport
                , o.strava_segment_name
                , o.strava_kom_type
                , o.strava_entry_count
                , o.strava_effort_count 
                , o.entriesJson()
                )
            ]
        return out

    def update(conn, id, leaderboard):
        up = [
            "" if leaderboard.strava_kom_type is None else ( "strava_kom_type = '%s'" % leaderboard.strava_kom_type)
            , "" if leaderboard.strava_entry_count is None else ( "strava_entry_count = '%s'" % leaderboard.strava_entry_count)
            , "" if leaderboard.entries is None else ( "entries_json = '%s'" % leaderboard.entriesJson())
        ]
        sql = """update  strava_leaderboard set 
            upd_ts = now(), 
            %s
            where id = %s """ % (
            ", \n\t".join(up)
            , id
            )
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            # print(sql)
            cur.execute(sql)
        except Exception as e:
            raise e
        finally:
            conn.commit()
            cur.close()


    def fetchData(conn, id = None, strava_segment_id = None, alabak_track_id = None):
        # cur = conn.cursor()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        whereId = "" if id is None else ( "and id = %s " % id )
        whereSegmentId = "" if strava_segment_id is None else ( "and strava_segment_id = '%s' " % strava_segment_id )
        whereTrackId = "" if alabak_track_id is None else ( "and alabak_track_id = '%s'" % alabak_track_id )
        where = "%s %s %s" % (whereId, whereSegmentId, whereTrackId) 
        try:
            cur.execute("select * from strava_leaderboard where 1=1 %s" % (where))
            for r in cur:
                # print(r['id'],r['row_ts'],  r['upd_ts'], )
                return r
        except Exception as e:
            print(e)
            raise e
        finally:
            cur.close()

    def fetchAll(conn, strava_segment_ids = None, alabak_track_ids = None):
        # cur = conn.cursor()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        whereSegmentId = "" if strava_segment_ids is None else ( "and strava_segment_id in (%s) " % strava_segment_ids )
        whereTrackId = "" if alabak_track_ids is None else ( "and alabak_track_id in ( %s) " % alabak_track_ids )
        where = "%s %s" % (whereSegmentId, whereTrackId) 
        try:
            cur.execute("select * from strava_leaderboard where 1=1 %s" % (where))
            out = list()
            for r in cur:
                # print(r['id'],r['row_ts'],  r['upd_ts'], )
                out .append(r)
            return out
        except Exception as e:
            print(e)
            raise e
        finally:
            cur.close()


    def fetchDataJson(conn, id = None, strava_segment_id = None, alabak_track_id = None):
        # cur = conn.cursor()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        whereId = "" if id is None else ( "and id = %s " % id )
        whereSegmentId = "" if strava_segment_id is None else ( "and strava_segment_id = '%s' " % strava_segment_id )
        whereTrackId = "" if alabak_track_id is None else ( "and alabak_track_id = '%s'" % alabak_track_id )
        where = "%s %s %s" % (whereId, whereSegmentId, whereTrackId) 
        try:
            sql = """select 
            json_array_elements( entries_json) -> 'rank' as "rank"  
            , json_array_elements( entries_json) -> 'name' as "name"  
            , json_array_elements( entries_json) -> 'time' as "time"  
            from strava_leaderboard where 1=1 %s""" % (where)
            logging.debug("sql: %s" % sql)
            cur.execute(sql)
            out = list()
            for r in cur:
                out.append(r)
            return out
        except Exception as e:
            print(e)
            raise e
        finally:
            cur.close()



    def insert(conn, leaderboard):
        cur = conn.cursor()
        for sql2 in SegmentLeaderboardSql.insertSql(leaderboard):
            sql = "%s" % sql2
            try:
                # print( "sql: %s" % ( sql ) )
                # print("%s:sql: %s..." % ( __class__, sql[0:20]) )
                cur.execute(sql2 )
                cur.execute('SELECT LASTVAL()')
                lastId = cur.fetchone()[0]
                if lastId is not None:
                    return leaderboard.setPK(lastId)
            except Exception as e:
                logging.error("%s:SQL: %s" % (  __class__, sql ) ) 
                logging.error("%s:ERROR: %s" % ( __class__, e ) )
                raise e
            finally:
                conn.commit()
                cur.close()


def pgConnect(args):
    try:
        connString = pgConnString(args)
        conn = psycopg2.connect(connString)
        logging.info(conn)
        cur = conn.cursor()
        cur.execute("SET search_path TO " + args.pgSchema)
        cur.close()

        return conn
    except Exception as e:
        logging.error("connString: %s" % connString)
        logging.error(e)
        raise e


def pgConnString(args):
    """
        connect_str = "dbname='testpython' user='matt' host='localhost' " + \
                  "password='myOwnPassword'"
    """
    port = ''
    db = ''
    out = "host='%s' user='%s' password='%s' " % ( 
        args.pgHost
        , args.pgUser
        , args.pgPassword
        )

    if args.pgPort:
        port = "port=%s" % args.pgPort

    if args.pgDb:
        db = "dbname=%s" % args.pgDb

    return "%s %s %s" % (out, port, db)


def executeSqls(conn, sqls):
    cur = conn.cursor()
    for sql in sqls:
        try:
            # print( "sql: %s" % ( sql ) )
            print("sql: %s..." % sql[0:40])
            cur.execute(sql)
            # cur.close()
        except Exception as e:
            logging.error("SQL: %s" % sql)
            logging.error("ERROR: %s" % e)
            print("error", e)
        finally:
            conn.commit()

    cur.close()


leaderboardData = {'effort_count': 121, 'entry_count': 121, 'kom_type': 'kom', 'entries': 
    [ {'rank': 1, 'athlete_name': 'Zlatislav I.', 'elapsed_time': 186, 'moving_time': 186, 'start_date': '2018-04-09T10:41:05Z', 'start_date_local': '2018-04-09T13:41:05Z'}
    , {'rank': 2, 'athlete_name': 'Румен Д.', 'elapsed_time': 279, 'moving_time': 225, 'start_date': '2018-08-19T15:09:25Z', 'start_date_local': '2018-08-19T18:09:25Z'}
    , {'rank': 3, 'athlete_name': 'Vihren M.', 'elapsed_time': 300, 'moving_time': 300, 'start_date': '2017-07-18T17:29:30Z', 'start_date_local': '2017-07-18T20:29:30Z'}
    , {'rank': 4, 'athlete_name': 'Alexander M.', 'elapsed_time': 327, 'moving_time': 327, 'start_date': '2017-12-30T11:11:53Z', 'start_date_local': '2017-12-30T13:11:53Z'}
    , {'rank': 5, 'athlete_name': 'Martin D.', 'elapsed_time': 341, 'moving_time': 341, 'start_date': '2018-04-09T12:03:04Z', 'start_date_local': '2018-04-09T15:03:04Z'}
    , {'rank': 6, 'athlete_name': 'Georgi N.', 'elapsed_time': 351, 'moving_time': 351, 'start_date': '2018-05-16T11:02:27Z', 'start_date_local': '2018-05-16T14:02:27Z'}
    , {'rank': 7, 'athlete_name': 'Vladislav G.', 'elapsed_time': 361, 'moving_time': 361, 'start_date': '2016-08-14T11:51:11Z', 'start_date_local': '2016-08-14T14:51:11Z'}
    , {'rank': 8, 'athlete_name': 'Boyko T.', 'elapsed_time': 361, 'moving_time': 361, 'start_date': '2017-08-27T10:24:51Z', 'start_date_local': '2017-08-27T13:24:51Z'}
    , {'rank': 9, 'athlete_name': 'Vladimir M.', 'elapsed_time': 393, 'moving_time': 393, 'start_date': '2018-09-02T14:46:24Z', 'start_date_local': '2018-09-02T17:46:24Z'}
    , {'rank': 10, 'athlete_name': 'Dimitar P.', 'elapsed_time': 395, 'moving_time': 395, 'start_date': '2018-06-03T10:10:09Z', 'start_date_local': '2018-06-03T13:10:09Z'}
    , {'rank': 11, 'athlete_name': 'Angel B.', 'elapsed_time': 687, 'moving_time': 609, 'start_date': '2018-07-01T09:06:42Z', 'start_date_local': '2018-07-01T12:06:42Z'}
    , {'rank': 12, 'athlete_name': 'Aleksandar P.', 'elapsed_time': 699, 'moving_time': 635, 'start_date': '2018-08-21T17:24:47Z', 'start_date_local': '2018-08-21T20:24:47Z'}
    , {'rank': 13, 'athlete_name': 'Varban K.', 'elapsed_time': 703, 'moving_time': 703, 'start_date': '2013-07-28T11:40:31Z', 'start_date_local': '2013-07-28T14:40:31Z'}
    , {'rank': 14, 'athlete_name': 'Stoyan C.', 'elapsed_time': 705, 'moving_time': 705, 'start_date': '2017-07-08T10:46:36Z', 'start_date_local': '2017-07-08T13:46:36Z'}
    , {'rank': 15, 'athlete_name': 'Dinko D.', 'elapsed_time': 713, 'moving_time': 664, 'start_date': '2016-06-04T15:03:07Z', 'start_date_local': '2016-06-04T18:03:07Z'}
    ]}

def insertTest(conn):
    from strava import objects
    leaderboard = objects.SegmentLeaderboard(strava_segment_id = 4920835, jsonData = leaderboardData)
    leaderboard.setAlabakTrackId(123213)
    SegmentLeaderboardSql.insert( conn, leaderboard)

def selectTest(conn):
    from strava import objects
    leaderboard = objects.SegmentLeaderboard(strava_segment_id = 4920835, jsonData = leaderboardData)
    leaderboard.setAlabakTrackId(123213)
    data = SegmentLeaderboardSql.fetchData(conn, id = 1)
    SegmentLeaderboardSql.update(conn, data['id'], leaderboard)
    data = SegmentLeaderboardSql.fetchDataJson(conn, id = 1)
    print(data)

def settingTest(conn):
    # SettingSql.insert(conn, key = 'key1', value='val1')
    SettingSql.update(conn, key = 'key1', value='val1 1')
    # print(data)

def createSql(conn):
    from strava import objects
    executeSqls( conn, SegmentLeaderboardSql.createSql())
    executeSqls( conn, SettingSql.createSql())
    # executeSqls( conn, SegmentLeaderboardEntrySql.createSql())

def dropSql(conn):
    from strava import objects
    executeSqls( conn, SegmentLeaderboardSql.dropSql())
    executeSqls( conn, SettingSql.dropSql())
    # executeSqls( conn, SegmentLeaderboardEntrySql.dropSql())



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='alabak.strava PostgresSQL CLI.')
    parser.add_argument('--pgDb', default="alabak", dest='pgDb', help='pg Db default: alabak')
    parser.add_argument('--pgUser', default='postgres', dest='pgUser', help='pg user')
    parser.add_argument('--pgSchema', default='public', dest='pgSchema', help='pg schema')   
    parser.add_argument('--pgPassword', default='docker', dest='pgPassword', help='pg password')
    parser.add_argument('--pgHost', default='localhost', dest='pgHost', help='pg host')
    parser.add_argument('--pgPort', default=5432, dest='pgPort', type=int, help='pg port ')
    parser.add_argument('--install', default=None, dest='install', help=' call createSql, dropSql')

    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    logging.info("conn string: %s" % pgConnString(args) )

    if args.install is not None:

        # conn = pgsql.pgConnect(args)
        conn = pgConnect(args)
        if "createSql" in args.install: 
            createSql(conn)
        if "dropSql" in args.install: 
            dropSql(conn)
        if "insertTest" in args.install: 
            insertTest(conn)
        if "selectTest" in args.install: 
            selectTest(conn)
        if "settingTest" in args.install: 
            settingTest(conn)
        
        conn.close()
        print("done.")
