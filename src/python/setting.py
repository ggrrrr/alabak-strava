import argparse
import logging

import pgsql

class StravaSetting:
    def __init__(self, dbConn=None, args=None):
        self.log = logging.getLogger('alabak.strava.StravaSetting')
        self.dbConn = dbConn
        self.args = args
        self.log.debug("init")

    def readKey(self, key):
        return pgsql.SettingSql.get(self.dbConn, key)

    def saveKey(self, key, value):
        if value is None:
            return

        old = self.readKey(key)
        if old is None:
            pgsql.SettingSql.insert(self.dbConn, key=key, value = value)
        else:
            pgsql.SettingSql.update(self.dbConn, key=key, value = value)


    def readAll(self):
        """
        Read all settings for strava
        accessToken
        clientId
        clientSecret
        refreshToken
        """
        # SettingSql.insert(conn, key = 'key1', value='val1')
        # SettingSql.update(conn, key = 'key1', value='val1 1')
        self.clientId = self.readKey("clientId")
        self.clientSecret = self.readKey("clientSecret")
        self.refreshToken = self.readKey("refreshToken")
        self.accessToken = self.readKey("accessToken")
        # print("asd" , (accessToken))
        self.log.debug("clientId:%s: clientSecret:%s, refreshToken:%s, accessToken:%s" % (
            self.clientId
            , self.clientSecret
            , self.refreshToken
            , self.accessToken
            ))
        self.args.clientId = self.clientId
        self.args.clientSecret = self.clientSecret
        self.args.refreshToken = self.refreshToken
        self.args.accessToken = self.accessToken
       
    def saveAll(self):
        """
        Read all settings for strava
        """
        if self.args.clientId is not None:
            self.saveKey(key="clientId", value = self.args.clientId)
        if self.args.clientSecret is not None:
            self.saveKey(key="clientSecret", value = self.args.clientSecret)
        if self.args.refreshToken is not None:
            self.saveKey(key="refreshToken", value = self.args.refreshToken)
        if self.args.accessToken is not None:
            self.saveKey(key="accessToken", value = self.args.accessToken)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='alabak.strava PostgresSQL CLI.')
    parser.add_argument('--clientId', default=None, dest='clientId', help='pg Db', required=False)
    parser.add_argument('--clientSecret', default=None, dest='clientSecret', help='clientSecret', required=False)
    parser.add_argument('--grantType', default='refresh_token', dest='grantType', help='grantType', required=False)
    parser.add_argument('--refreshToken', default=None, dest='refreshToken', help='pg host', required=False)
    parser.add_argument('--accessToken', default=None, dest='accessToken', help='accessToken', required=False)
    parser.add_argument('--pgDb', default="alabak", dest='pgDb', help='pg Db default: alabak')
    parser.add_argument('--pgUser', default='postgres', dest='pgUser', help='pg user')
    parser.add_argument('--pgPassword', default='docker', dest='pgPassword', help='pg password')
    parser.add_argument('--pgHost', default='localhost', dest='pgHost', help='pg host')
    parser.add_argument('--pgPort', default=5432, dest='pgPort', type=int, help='pg port ')
    parser.add_argument('--test', default=None, dest='test', help='test call ')
    parser.add_argument('--level', default='debug', dest='level', help='level')
    parser.add_argument('--pgSchema', default='public', dest='pgSchema', help='pg schema')   


    args = parser.parse_args()

    if args.level == "debug":
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # logging.info("conn string: %s" % pgConnString(args) )

    if args.test is not None:

        conn = pgsql.pgConnect(args)
        setting = StravaSetting(dbConn = conn, args = args)
        if "readAll" in args.test: 
            # createSql(conn)
            setting.readAll()
            logging.info("read: %s" % args )
            # pass
        if "saveAll" in args.test: 
            # createSql(conn)
            setting.saveAll()
            # pass
        conn.close()
        print("done.")
