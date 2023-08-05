"""
Veripeditus game server main package

This package contains the code necessary to run the game server
as a Flask application, either stand-alone or as a WSGI application.
"""

# veripeditus-server - Server component for the Veripeditus game framework
# Copyright (C) 2016  Dominik George <nik@naturalnet.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version, with the Game Cartridge Exception.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
from os.path import realpath

from flask import send_from_directory

def server_main(): # pragma: no cover
    """ Entry point for the veripeditus-standalone command.

    Used to run the stand-alone webserver with different options.
    """

    from veripeditus.server.app import create_app
    app = create_app()

    # parse arguments
    aparser = argparse.ArgumentParser()
    aparser.add_argument("-w", "--webapp", help="path to the webapp files")
    aparser.add_argument("-d", "--debug", help="enable debug in Flask app",
                         action="store_true")
    aparser.add_argument("-H", "--host", help="the host address to listen on",
                         default="127.0.0.1")
    aparser.add_argument("-P", "--port", help="the port to listen on",
                         default="5000")
    aparser.add_argument("-z", "--gzip", help="enable GZip compression for HTTP",
                         action="store_true")
    aparser.add_argument("-s", "--single", help="run webserver single-threaded",
                         action="store_true")
    args = aparser.parse_args()

    # Enable debugging in Flask application if debug option was set
    if args.debug:
        app.debug = True

    # Enable serving of static files at / if it was enabled
    if args.webapp:
        app.config['PATH_WEBAPP'] = realpath(args.webapp)
        @app.route('/')
        @app.route('/<path:path>')
        def _serve_webapp(path='index.html'): # pylint: disable=unused-variable
            """ Called for all static resources. """

            return send_from_directory(app.config['PATH_WEBAPP'], path)

    # Enable compression if option was enabled
    if args.gzip:
        from flask_compress import Compress
        Compress(app)

    # Run Flask application
    app.run(host=args.host, port=int(args.port), threaded=not args.single)

# Allow direct calling of this script
if __name__ == '__main__': # pragma: no cover
    # Jump to veripeditus-standalone entry point
    server_main()
