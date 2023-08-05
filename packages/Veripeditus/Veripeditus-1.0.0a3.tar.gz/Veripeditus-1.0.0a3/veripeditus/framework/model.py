# veripeditus-server - Server component for the Veripeditus game framework
# Copyright (C) 2016, 2017  Dominik George <nik@naturalnet.de>
# Copyright (C) 2016, 2017  Eike Tim Jesinghaus <eike@naturalnet.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version, with the Game Cartridge Exception.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from collections import Sequence
from glob import glob
from numbers import Real
import json
import os
import random

from flask import redirect
from flask_restless import url_for
from sqlalchemy import and_ as sa_and
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm.collections import attribute_mapped_collection
from sqlalchemy.sql import and_

from veripeditus.framework.util import current_player, get_image_path, get_gameobject_distance, random_point_in_polygon, send_action
from veripeditus.server.app import DB, OA
from veripeditus.server.model import Base, World
from veripeditus.server.util import api_method, get_data_path

class _GameObjectMeta(type(Base)):
    """ Meta-class to allow generation of dynamic mapper args.

    Necessary because SQLAlchemy traverses __dict__ to find configuration
    attributes, and our inherited classes in games obviously don't get
    inherited __mapper_args__ in their __dict__. This method injects
    the dictionary to the __dict__ upon instantiation as meta-class.
    """

    def __new__(cls, *args, **kwargs):
        """ Called upon deriving from GameObject, which uses this meta-class. """

        # Create a new instance by calling __new__ on our parent class,
        # which is the meta-class of the used SQLAlchemy declarative base
        obj = super().__new__(cls, *args, **kwargs)

        # Later filled with the relevant mapper args
        mapperargs = {}

        if obj.__module__ == "veripeditus.framework.model":
            # We are a parent class in the framework, so we need to configure
            # the polymorphism to use
            mapperargs["polymorphic_on"] = obj.type
            mapperargs["with_polymorphic"] = "*"
            mapperargs["polymorphic_identity"] = obj.__name__
        elif obj.__module__.startswith("veripeditus.game"):
            # We are an implementation in a game, so we only need to set the identity
            # It is the game module and the class name defined there prefixed with game
            mapperargs["polymorphic_identity"] = \
                "game_%s_%s" % (obj.__module__.split(".")[2], obj.__name__)
        else:
            # We are somwhere else, which is a bug
            raise RuntimeError("GameObject can only be derived in game modules.")

        # Inject into class and return the new instance
        setattr(obj, "__mapper_args__", mapperargs)
        return obj

class Attribute(Base):
    # Key/value pair
    key = DB.Column(DB.Unicode(256))
    value = DB.Column(DB.Unicode(256))

class GameObject(Base, metaclass=_GameObjectMeta):
    __tablename__ = "gameobject"

    _api_includes = ["world"]

    id = DB.Column(DB.Integer(), primary_key=True)

    # Columns and relationships

    name = DB.Column(DB.String(32))
    image = DB.Column(DB.String(32), default="dummy", nullable=False)

    world_id = DB.Column(DB.Integer(), DB.ForeignKey("world.id"))
    world = DB.relationship("World", backref=DB.backref("gameobjects",
                                                        lazy="dynamic"),
                            foreign_keys=[world_id])

    longitude = DB.Column(DB.Float(), default=0.0, nullable=False)
    latitude = DB.Column(DB.Float(), default=0.0, nullable=False)

    osm_element_id = DB.Column(DB.Integer(), DB.ForeignKey("osm_elements.id"))
    osm_element = DB.relationship(OA.element, backref=DB.backref("osm_elements",
                                                                 lazy="dynamic"),
                                  foreign_keys=[osm_element_id])

    type = DB.Column(DB.Unicode(256))

    attributes = DB.relationship("Attribute", secondary="gameobjects_to_attributes")
    def attribute(self, key, value=None):
        """ Set or get an attribute on this game object.

        Attributes can be used to store state information about the
        game or this game object.

        Gotcha: Attributes can only be strings, and you are responsible
        for casting.

        Returns the value of the attribute.

        :param key: key for the attribute
        :param value: value of the attribute if it shall be set
        :type key: str
        :type value: str
        :rtype: str
        """

        attributes = [attribute for attribute in self.attributes if attribute.key == key]
        attribute = attributes[0] if attributes else None

        if value is not None:
            if not attribute:
                attribute = Attribute()
                self.attributes.append(attribute)
            attribute.key = key
            attribute.value = value
            self.commit()

        return attribute.value if attribute else None

    distance_max = None

    available_images_pattern = ["*.svg", "*.png"]

    @property
    def latlon(self):
        return (self.latitude, self.longitude)

    @latlon.setter
    def latlon(self, latlon):
        self.latitude, self.longitude = latlon

    @property
    def gameobject_type(self):
        # Return type of gameobject
        return self.__tablename__

    def distance_to(self, obj):
        """ Return distance to another gamobject.

        :param obj: Object to determine the distance to
        :type obj: :class:`veripeditus.framework.model.GameObject`
        :rtype: float
        """

        return get_gameobject_distance(self, obj)

    @property
    def image_path(self):
        # Return path of image file
        return get_image_path(self.world.game.module, self.image)

    @hybrid_property
    def isonmap(self):
        return True

    @property
    def distance_to_current_player(self):
        # Return distance to current player
        if current_player() is None:
            return None
        return self.distance_to(current_player())

    @api_method(authenticated=False)
    def image_raw(self, name=None):
        # Take path of current image if name is not given
        # If name is given take its path instead
        if name is None:
            image_path = self.image_path
        elif name in self.available_images():
            image_path = get_image_path(self.world.game.module, name)
        else:
            # FIXME correct error
            return None

        with open(image_path, "rb") as file:
            return file.read()

    @api_method(authenticated=True)
    def set_image(self, name):
        # Check if image is available
        if name in self.available_images():
            # Update image
            self.image = name
            self.commit()
        else:
            # FIXME correct error
            return None

        # Redirect to new image
        return redirect("/api/v2/gameobject/%d/image_raw" % self.id)

    @api_method(authenticated=False)
    def available_images(self):
        res = []

        if self.available_images_pattern is not None:
            # Make patterns a list
            if isinstance(self.available_images_pattern, list):
                patterns = self.available_images_pattern
            else:
                patterns = [self.available_images_pattern]

            # Get data path of this object's module
            data_path_game = get_data_path(self.world.game.module)
            # Get data path of the framework module
            data_path_framework = get_data_path()

            for data_path in (data_path_game, data_path_framework):
                for pattern in patterns:
                    # Get images in data path matching the pattern
                    res += glob(os.path.join(data_path, pattern))

        # Get basenames of every file without extension
        basenames = [os.path.extsep.join(os.path.basename(r).split(os.path.extsep)[:-1])
                     for r in res]

        # Return files in json format
        return json.dumps(basenames)

    @classmethod
    def spawn(cls, world=None):
        if world is None:
            # Iterate over all defined GameObject classes
            for go in cls.__subclasses__():
                # Iterate over all worlds using the game
                worlds = World.query.filter(World.game.has(package=go.__module__.split(".")[2])).all()
                for world in worlds:
                    if "spawn" in vars(go):
                        # Call spawn for each world
                        go.spawn(world)
                    else:
                        # Call parameterised default spawn code
                        go.spawn_default(world)

    @classmethod
    def spawn_default(cls, world):
        # Determine existing number of objects on map
        existing = cls.query.filter_by(world=world, isonmap=True).count()
        if "spawn_max" in vars(cls) and existing < cls.spawn_max:
            to_spawn = cls.spawn_max - existing
        elif existing == 0 or "spawn_osm" in vars(cls):
            to_spawn = 1
        else:
            to_spawn = 0

        # Determine spawn locations
        spawn_points = {}
        for _ in range(0, to_spawn):
            if "spawn_latlon" in vars(cls):
                latlon = cls.spawn_latlon

                if isinstance(latlon, Sequence):
                    # We got one of:
                    #  (lat, lon)
                    #  ((lat, lon), (lat, lon),…)
                    #  ((lat, lon), radius)
                    if isinstance(latlon[0], Sequence) and isinstance(latlon[1], Sequence):
                        if len(latlon) == 2:
                            # We got a rect like ((lat, lon), (lat, lon))
                            # Randomise coordinates within that rect
                            spawn_points[(random.uniform(latlon[0][0], latlon[1][0]), random.uniform(latlon[0][1], latlon[1][1]))] = None
                        else:
                            # We got a polygon, randomise coordinates within it
                            spawn_points[random_point_in_polygon(latlon)] = None
                    elif isinstance(latlon[0], Sequence) and isinstance(latlon[1], Real):
                        # We got a circle like ((lat, lon), radius)
                        # FIXME implement
                        raise RuntimeError("Not implemented.")
                    elif isinstance(latlon[0], Real) and isinstance(latlon[1], Real):
                        # We got a single point like (lat, lon)
                        # Nothing to do, we can use that as is
                        spawn_points[latlon] = None
                    else:
                        raise TypeError("Unknown value for spawn_latlon.")
            elif "spawn_osm" in vars(cls):
                # Skip if no current player or current player not in this world
                if current_player() is None or current_player().world is not world:
                    return

                # Define bounding box around current player
                # FIXME do something more intelligent here
                lat_min = current_player().latitude - 0.001
                lat_max = current_player().latitude + 0.001
                lon_min = current_player().longitude - 0.001
                lon_max = current_player().longitude + 0.001
                bbox_queries = [OA.node.latitude>lat_min, OA.node.latitude<lat_max,
                                OA.node.longitude>lon_min, OA.node.longitude<lon_max]

                # Build list of tag values using OSMAlchemy
                has_queries = [OA.node.tags.any(key=k, value=v) for k, v in cls.spawn_osm.items()]
                and_query = sa_and(*bbox_queries, *has_queries)

                # Do query
                # FIXME support more than plain nodes
                nodes = DB.session.query(OA.node).filter(and_query).all()

                # Extract latitude and longitude information and build spawn_points
                spawn_points = {(node.latitude, node.longitude): node for node in nodes}
            else:
                # Do nothing if we cannot determine a location
                return

        for latlon, osm_element in spawn_points.items():
            # Check existing object on OSM element
            if osm_element is not None:
                existing = cls.query.filter_by(world=world, isonmap=True, osm_element=osm_element).count()
                if existing > 0:
                    # Skip this spawn point if a visible object is bound to it
                    continue

            # Create a new object
            obj = cls()
            obj.world = world
            obj.latitude = latlon[0]
            obj.longitude = latlon[1]
            obj.osm_element = osm_element

            # Determine any defaults
            for k in vars(cls):
                if k.startswith("default_"):
                    setattr(obj, k[8:], getattr(cls, k))

            # Derive missing defaults from class name
            if obj.image is None:
                obj.image = cls.__name__.lower()
            if obj.name is None:
                obj.name = cls.__name__.lower()

            # Add to session
            obj.commit()

    def say(self, message):
        """ Let the GameObject provide a message for the player, probably
        displayed as a text box or similar by the client.

        :param message: the message to be sent to the player
        :type message: str
        :rtype: None
        """

        send_action("say", self, message)
        return

    def commit(self):
        """ Commit this object to the database. """

        DB.session.add(self)
        DB.session.commit()

class GameObjectsToAttributes(Base):
    __tablename__ = "gameobjects_to_attributes"

    gameobject_id = DB.Column(DB.Integer(),
                              DB.ForeignKey('gameobject.id'))
    attribute_id = DB.Column(DB.Integer(),
                             DB.ForeignKey('attribute.id'))

class Player(GameObject):
    __tablename__ = "gameobject_player"

    _api_includes = GameObject._api_includes + ["inventory"]

    id = DB.Column(DB.Integer(), DB.ForeignKey("gameobject.id"), primary_key=True)

    # Relationship to the user which the player belongs to
    user_id = DB.Column(DB.Integer(), DB.ForeignKey("user.id"))
    user = DB.relationship("User", backref=DB.backref("players",
                                                      lazy="dynamic"),
                           foreign_keys=[user_id])

    available_images_pattern = "avatar_*"

    def __init__(self, **kwargs):
        GameObject.__init__(self, **kwargs)
        if "image" not in kwargs:
            self.image = "avatar_default"

    def new_item(self, itemclass):
        """ Add a new item to the player's inventory.

        The new item will be a new instance of the item class.
        Most often this will be a sub-class you defined in your
        game.

        :param itemclass: class of the Item to create
        :type itemclass: :class:`veripeditus.framework.model.Item`
        :rtype: None
        """

        item = itemclass()
        item.world = self.world
        item.owner = self

        # Determine any defaults
        for k in vars(itemclass):
            if k.startswith("default_"):
                setattr(item, k[8:], getattr(itemclass, k))

        # Derive missing defaults from class name
        if item.image is None:
            item.image = itemclass.__name__.lower()
        if item.name is None:
            item.name = itemclass.__name__.lower()

        item.commit()
        self.commit()

    def has_item(self, itemclass):
        """Get the amount the player has of a specific item.

        :param itemclass: the class of which the checked items are
        :type itemclass: :class:`veripeditus.framework.model.Item`
        :rtype: int
        """
        count = 0
        for item in self.inventory:
            if isinstance(item, itemclass):
                count += 1
        return count

    def has_items(self, *itemclasses):
        """Check whether the player has at least one of each item queried for.

        :param itemclasses: All item types to check for
        :type itemclasses: :class:`veripeditus.framework.model.Item`
        :rtype: bool
        """

        # Return whether the player has every given item at least one time
        for itemclass in itemclasses:
            if not self.has_item(itemclass):
                return False

        return True

    def drop_item(self, itemclass):
        """Drop every item of a class from the player's inventory

        :param itemclass: the class of which the items shall be removed
        :type itemclasses: :class:`veripeditus.framework.model.Item`
        :rtype: None
        """

        # Remove every item on a class from the players inventory
        for item in self.inventory:
            if isinstance(item, itemclass):
                DB.session.delete(item)
                DB.session.commit()

    def drop_items(self, *itemclasses):
        """Srop every item of the classes from the player's inventory.

        :param itemclasses: All item types to drop
        :type itemclasses: :class:`veripeditus.framework.model.Item`
        :rtype: None
        """

        # Remove every item of every given class from the players inventory
        for itemclass in itemclasses:
            self.drop_item(itemclass)

    def may_accept_handover(self, item):
        """Determine whether the player can accept a handover of a specific item.

        This method defaults to always returning True and is designed to be
        overridden in games.

        :param item: item that is about to be handed over
        :type item: :class:`veripeditus.framework.model.Item`
        :rtype: bool
        """

        return True

    @api_method(authenticated=True)
    def update_position(self, latlon):
        if current_player() is None:
            # FIXME proper error
            return None

        if current_player() != self:
            # FIXME proper error
            return None

        # Update position
        self.latitude, self.longitude = [float(x) for x in latlon.split(",")]

        # FIXME remove slow iteration
        for item in Item.query.filter_by(world=current_player().world).all():
            if item.auto_collect_radius > 0 and item.distance_to_current_player <= item.auto_collect_radius:
                item.collect()

        for loc in Location.query.filter_by(world=current_player().world).all():
            if hasattr(loc, "distance_max") and loc.distance_max is not None and loc.distance_to(self) < loc.distance_max:
                loc.pass_()

        self.commit()

        # Redirect to own object
        return redirect(url_for(self.__class__, resource_id=self.id))

    @classmethod
    def spawn_default(cls, world):
        pass

    @hybrid_property
    def isonmap(self):
        # Check if isonmap is called by the class or by an instance
        if isinstance(self, type):
            cls = self
        else:
            cls = self.__class__

        if current_player() is not None:
            # Check if specific constants are set and apply their effects
            mod = current_player().world.game.module
            if hasattr(mod, "VISIBLE_RAD_PLAYERS"):
                # Check if the player is in the visible range
                if self is not cls and self.distance_to_current_player > mod.VISIBLE_RAD_PLAYERS:
                    return False
            if hasattr(mod, "HIDE_SELF"):
                # Hide the player if it is the current player
                if self is not cls and self == current_player() and mod.HIDE_SELF:
                    return False
        return True

class Item(GameObject):
    __tablename__ = "gameobject_item"

    # Columns

    id = DB.Column(DB.Integer(), DB.ForeignKey("gameobject.id"), primary_key=True)

    owner_id = DB.Column(DB.Integer(), DB.ForeignKey("gameobject_player.id"))
    owner = DB.relationship("veripeditus.framework.model.Player", backref=DB.backref("inventory", lazy="dynamic"),
                            foreign_keys=[owner_id])

    # Class attributes

    collectible = True
    handoverable = True
    placeable = True
    owned_max = None
    auto_collect_radius = 0
    show_if_owned_max = None

    @api_method(authenticated=True)
    def collect(self):
        if current_player() is None:
            # FIXME throw proper error
            return None

        # Check if the player is in range
        if self.distance_max is not None:
            if self.distance_max < self.distance_to(current_player()):
                send_action("notice", self, "You are too far away!")
                return

        # Check if the player already has the maximum amount of items of a class
        if self.owned_max is not None:
            if current_player().has_item(self.__class__) >= self.owned_max:
                send_action("notice", self, "You have already collected enough of this!")
                return

        # Check if the collection is allowed
        if self.collectible and self.isonmap and self.may_collect(current_player()):
            # Change owner
            self.owner = current_player()
            self.on_collected(player=current_player())
            self.commit()
            return redirect(url_for(self.__class__, resource_id=self.id))
        else:
            send_action("notice", self, "You cannot collect this!")
            return

    @api_method(authenticated=True)
    def place(self):
        if current_player() is not None and self.owner == current_player() and self.may_place(self.owner) and self.placeable:
            self.latlon = self.owner.latlon
            self.owner = None
            self.on_placed(player=current_player())

            for loc in Location.query.filter_by(world=current_player().world).all():
                if self.distance_to(loc) <= loc.distance_max:
                    loc.on_item_placed(player=current_player(), item=self)

            self.commit()
            return redirect(url_for(self.__class__, resource_id=self.id))
        else:
            send_action("notice", self, "You cannot place this!")
            return

    @api_method(authenticated=True)
    def handover(self, target_player):
        # Check if the handover is allowed
        if self.owner is not None and self.handoverable and self.may_handover(target_player) and target_player.may_accept_handover(self):
            # Change owner
            self.owner = target_player
            self.on_handedover(player=current_player(), receiver=target_player)
            self.commit()
            return redirect(url_for(self.__class__, resource_id=self.id))
        else:
            send_action("notice", self, "You cannot hand this over.")
            return

    @hybrid_property
    def isonmap(self):
        # Check whether we were called as class or instance method
        if isinstance(self, type):
            # Class method
            cls = self
        else:
            cls = self.__class__

        # Seed expression
        expr = True

        # Check if item is owned by someone
        if self is cls:
            # For class method, and_() existing expression with check for ownership
            expr = and_(expr, self.owner==None)
        elif self.owner is not None:
            # For instance method, return a terminal False if owned by someone
            return False

        # Check for owned_max functionality
        # Independent of class or instance method
        if current_player() is not None:
            if self.owned_max is not None and current_player().has_item(cls) >= self.owned_max:
                if self.show_if_owned_max is None or not self.show_if_owned_max:
                    # Return a terminal false
                    return False
            mod = current_player().world.game.module
            if hasattr(mod, "VISIBLE_RAD_ITEMS"):
                if self is not cls and self.distance_to_current_player > mod.VISIBLE_RAD_ITEMS:
                    return False

        # Verify conditional attributes for spawning
        # Independent of class or instance method
        if hasattr(self, "spawn_player_attributes"):
            for key, value in self.spawn_player_attributes.items():
                if key in current_player().attributes:
                    attribute = current_player().attributes[key]
                else:
                    return False

                if value is not None and attribute != value:
                    return False

        # Find out final return value
        if self is cls:
            # For class method, return boolean SQL expression
            return expr
        else:
            # For instance method, return terminal True
            return True

    def may_collect(self, player):
        """Determine whether this item can be collected by a specific player.

        This method defaults to always returning True and is designed to be
        overridden in games.

        :param player: the player trying to collect the item
        :type player: :class:`veripeditus.framework.model.Player`
        :rtype: bool
        """

        return True

    def may_handover(self, player):
        """Determine whether this item can be handed over by a specific player.

        This method defaults to always returning True and is designed to be
        overridden in games.

        :param player: the player trying to hand the item over
        :type player: :class:`veripeditus.framework.model.Player`
        :rtype: bool
        """

        return True

    def may_place(self, player):
        """Determine whether this item can be placed on the map by a specific player.

        This method defaults to always returning True and is designed to be
        overridden in games.

        :param player: the player trying to collect the item
        :type player: :class:`veripeditus.framework.model.Player`
        :rtype: bool
        """

        return True

    def on_collected(self, **kwargs):
        """ Run as soon as a Player collects an item. This method can trigger
        complex game logic.

        :param player: the current player that collected the item
        :type player: :class:`veripeditus.framework.model.Player`
        :rtype: None
        """

        pass

    def on_handedover(self, **kwargs):
        """ Run after a player handed over an item. This method can trigger
        complex game logic.

        :param player: the current player that held the item before
        :param receiver: the other player that now holds the item
        :type player: :class:`veripeditus.framework.model.Player`
        :type recceiver: :class:`veripeditus.framework.model.Player`
        :rtype: None
        """

        pass

    def on_placed(self, **kwargs):
        """ Run as soon as a Player places an item on the map. This method can trigger
        complex game logic.

        :param player: the current player that placed the item
        :type player: :class:`veripeditus.framework.model.Player`
        :rtype: None
        """

        pass

class NPC(GameObject):
    __tablename__ = "gameobject_npc"

    # Columns

    id = DB.Column(DB.Integer(), DB.ForeignKey("gameobject.id"), primary_key=True)

    # Attribute for determining if a player can talk to the NPC
    talkable = True

    def on_talk(self, **kwargs):
        """ Run as soon as a Player talks to an NPC. This method can trigger
        complex game logic.

        :param player: the current player that talked to the NPC
        :type player: :class:`veripeditus.framework.model.Player`
        :rtype: None
        """

        pass

    @api_method(authenticated=True)
    def talk(self):
        if current_player() is None:
            # FIXME throw proper error
            return None

        # Check if the player is in range for talking to the NPC
        if self.distance_max is not None:
            if self.distance_max < self.distance_to(current_player()):
                send_action("notice", self, "You are too far away!")
                return

        # Check if talking to the NPC is allowed
        if self.talkable and self.isonmap and self.may_talk(current_player()):
            # Run talk logic
            return self.on_talk(player=current_player())
        else:
            send_action("notice", self, "You cannot talk to this character!")
            return

    def may_talk(self, player):
        """Check whether a player is allowed to talk to this NPC

        :param player: The player that is about to talk to this NPC
        :type player: :class:`veripeditus.framework.model.Player`
        """
        return True

    @hybrid_property
    def isonmap(self):
        if isinstance(self, type):
            cls = self
        else:
            cls = self.__class__

        if current_player() is not None:
            mod = current_player().world.game.module
            if hasattr(mod, "VISIBLE_RAD_NPCS"):
                if self is not cls and self.distance_to_current_player > mod.VISIBLE_RAD_NPCS:
                    return False

        return True

class Location(GameObject):
    __tablename__ = "gameobject_location"

    # Columns

    id = DB.Column(DB.Integer(), DB.ForeignKey("gameobject.id"), primary_key=True)

    # Attribute for determining if a player can trigger the location 
    passable = True

    def on_passed(self, **kwargs):
        """ Run as soon as a Player passes a Location. This method can trigger
        complex game logic.

        :param player: the current player that passed the location
        :type player: :class:`veripeditus.framework.model.Player`
        :rtype: None
        """

        pass

    def on_item_placed(self, **kwargs):
        """ Run as soon as a Player places an Item in a Location.
        This method can trigger complex game logic.

        :param player: the current player that passed the location
        :type player: :class:`veripeditus.framework.model.Player`
        :param item: the item that is placed within the Location
        :type item: :class:`veripeditus.framework.model.Item`
        :rtype: None
        """

        pass

    def pass_(self):
        if current_player() is None:
            # FIXME throw proper error
            return None

        if self.passable and self.may_pass(current_player()):
            return self.on_passed(player=current_player())

    def may_pass(self, player):
        """Determine whether this location may be passed by a specific player.

        This method defaults to always returning True and is designed to be
        overridden in games.

        :param player: the player trying to collect the item
        :type player: :class:`veripeditus.framework.model.Player`
        :rtype: bool
        """

        return True

    @hybrid_property  
    def isonmap(self):
        return True
