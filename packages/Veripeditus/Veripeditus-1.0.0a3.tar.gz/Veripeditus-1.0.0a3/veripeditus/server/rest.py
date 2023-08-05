"""
REST API definitions for the Veripeditus server.

This module contains everything to set up the API.
"""

# veripeditus-server - Server component for the Veripeditus game framework
# Copyright (C) 2016, 2017  Dominik George <nik@naturalnet.de>
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

import json
from socket import getfqdn

from flask import g, make_response, redirect, request
from flask_restless import APIManager, url_for
from werkzeug.wrappers import Response

from veripeditus.framework import VERSION
from veripeditus.framework.model import GameObject
from veripeditus.server.app import DB, OA
from veripeditus.server.control import needs_authentication, check_auth
from veripeditus.server.model import User, World, Game
from veripeditus.server.sources import get_sources, sources_to_tarball
from veripeditus.server.util import guess_mime_type

# Columns to include in all endpoints/models
_INCLUDE = ['id', 'created', 'updated']

def init_rest(app):
    # API manager from Flask-Restless
    manager = APIManager(app, flask_sqlalchemy_db=DB)

    # Create APIs for server models
    manager.create_api(User, page_size=0, max_page_size=0)
    manager.create_api(Game, page_size=0, max_page_size=0)
    manager.create_api(World, page_size=0, max_page_size=0)

    # Create APIs for all GameObjects
    for go in [GameObject] + GameObject.__subclasses__():
        # Find GameObjects in games tht derive the base objects
        for rgo in [go] + go.__subclasses__():
            # Dynamically create an API for everything we discovered
            manager.create_api(rgo,
                               additional_attributes=["gameobject_type"],
                               includes=rgo._api_includes,
                               exclude=["attributes"],
                               page_size=0, max_page_size=0)

    @app.route("/api/v2/<string:type_>/<int:id_>/<string:method>")
    @app.route("/api/v2/<string:type_>/<int:id_>/<string:method>/<arg>")
    def _get_gameobject_method_result(type_, id_, method, arg=None):
        """ Runs method on the object defined by the id and returns it verbatim
        if the object was found and has the method, or 404 if not.

        This is what the @api_method decorated methods in the modesl are for.
        """

        g.res = {}

        # Determine tpye of object and object
        types = {"gameobject": GameObject,
                 "world": World,
                 "game": Game}
        if type_ in types:
            obj = types[type_].query.get(id_)
        else:
            obj = None

        # Check for existence and method existence
        if obj is not None and getattr(obj, method):
            # Get method object
            method_impl = getattr(obj, method)

            # Check whether execution is allowed
            if method_impl.is_api_method:
                # Check authentication
                if method_impl.authenticated and g.user is None:
                    return needs_authentication()

                # Run method
                if arg is None:
                    ret = method_impl()
                else:
                    ret = method_impl(arg)

                if isinstance(ret, Response):
                    # We got a complete Response object
                    res = ret
                elif isinstance(ret, tuple):
                    # We got a tuple of type and data
                    res = make_response(ret[1])
                    res.headers["Content-Type"] = ret[0]
                elif ret is None:
                    res = make_response(json.dumps(g.res))
                    res.headers["Content-Type"] = "application/vnd.api+json"
                else:
                    # We need to guess the MIME type
                    res = make_response(ret)
                    res.headers["Content-Type"] = guess_mime_type(ret)
            else:
                # Return 403 Forbidden
                # FIXME more specific error
                res = ("", 403)
        else:
            # Return 404 Not Found
            # FIXME more specific error
            res = ("", 404)

        return res

    @app.route("/api/v2/gameobject_player/self")
    def _get_own_player():
        """ Return the GameObject Player of the user that is currently logged in. """

        # Check if a user is logged in, in the first place
        if g.user is None:
            # Return an error causing the lcient to ask for login
            # FIXME more specific error
            return ("", 401)

        # Check if a player is associated to the user currently
        if g.user.current_player is None:
            # Check if the user has any player objects
            if g.user.players.count() > 0:
                # Set current player to the first available player of the current user
                g.user.current_player = g.user.players[0]
            else:
                # Create a new player in the first world found
                World.query.filter_by(enabled=True).first().player_join()

        # Redirect to the current player object
        return redirect(url_for(g.user.current_player.__class__, resource_id=g.user.current_player.id))

    @app.route("/api/v2/user/register")
    def _register_user():
        """ Create the User defined in the Authorization header """

        # Get credentials from HTTP basic auth
        username = request.authorization.username
        password = request.authorization.password

        # Try to find a user with that name
        user = DB.session.query(User).filter_by(username=username).scalar()

        if user is None:
            # Create a new User object with these credentials
            user = User()
            user.username = username
            user.password = password

            # Store in database
            DB.session.add(user)
            DB.session.commit()

            # Re-check auth to get newly created user
            check_auth()

            # Pass on to login routine
            return _get_own_player()
        else:
            # If a user with this name already exists, return an error
            # FIXME proper error
            return ("", 409)

    @app.route("/api/v2/source_tarball")
    def _get_source_tarball():
        """ Returns a dynamically generated source tarball to the client. """

        # Assemble filename
        filename = "veripeditus-server_%s_%s.tar.xz" % (VERSION, getfqdn())

        # Get source tarball contents
        contents = sources_to_tarball(get_sources())

        # Build response for download
        res = make_response(contents)
        res.headers["Content-Type"] = "application/x-xz"
        res.headers["Content-Disposition"] = "attachment; filename=\"%s\"" % filename

        # Return HTTP response
        return res

    return manager
