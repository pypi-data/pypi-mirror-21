import os
from optparse import OptionParser

from SpiderKeeper.app import app, init_database


def main():
    opts, args = parse_opts()
    exitcode = 0
    app.config.update(dict(
        SERVER_TYPE=opts.server_type,
        SERVERS=opts.servers or ['http://localhost:6800'],
        SQLALCHEMY_DATABASE_URI=opts.database_url
    ))
    init_database()
    app.run(host=opts.host, port=opts.port, debug=True, threaded=True)


def parse_opts():
    parser = OptionParser(usage="%prog [options]",
                          description="Admin ui for spider service")
    parser.add_option("--type",
                      help="access spider server type, default:scrapyd",
                      dest='server_type',
                      default='scrapyd')
    parser.add_option("--host",
                      help="host, default:0.0.0.0",
                      dest='host',
                      default='0.0.0.0')
    parser.add_option("--port",
                      help="port, default:5000",
                      dest='port',
                      type="int",
                      default=5000)
    parser.add_option("--server",
                      help="servers, default:http://localhost:6800",
                      dest='servers',
                      action='append',
                      default=[])
    default_database_url = 'sqlite:///' + os.path.join(os.path.abspath('.'), 'SpiderKeeper.db')
    parser.add_option("--database_url",
                      help='SpiderKeeper metadata database default:' + default_database_url,
                      dest='database_url',
                      default=default_database_url)
    return parser.parse_args()


if __name__ == '__main__':
    main()
