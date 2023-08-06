"""TBApi - Python Library for The Blue Alliance API v3"""

import os
import sys
import json
import datetime
import requests
from SQLiteHelper import SQLiteHelper as sq # SQLite3 Wrapper for easier reading and programming
import numpy as np
from numpy import array as np_array


# EXCEPTION: Data Class is EMPTY
class EmptyError(Exception):
    """EXCEPTION: Data Class is EMPTY."""
    def __init__(self):
        Exception.__init__(self, 'Data Class is EMPTY.')


# EXCEPTION: Data Class errored during data parsing
class ParseError(Exception):
    """EXCEPTION: Data Class errored during data parsing."""
    def __init__(self):
        Exception.__init__(self, 'Data Class errored during data parsing.')


# EXCEPTION: Impropper Key passed during data parsing
class KeyInputError(Exception):
    """EXCEPTION: Impropper Key passed during data parsing."""
    def __init__(self):
        Exception.__init__(self, 'Impropper Key passed during data parsing.')


# EXCEPTION: Network Connection to The Blue Alliance is Offline
class OfflineError(Exception):
    """EXCEPTION: Network Conenction to The Blue Alliance is Offline."""
    def __init__(self):
        Exception.__init__(self, 'Network Connection to The Blue Alliance is Offline.')


# EXCEPTION: Fluid Key not available
class FluidKeyError(Exception):
    """EXCEPTION: Fluid Key not available"""
    def __init__(self):
        Exception.__init__(self, 'Fluid Key not availble.  Key may not be available for the represented Season, if applicable.')


# List-Extension Class:  Adds extra functionality to lists used for data-returns
class DataList(list):
    """List-Extension used for storing data objects with extra information."""
    def __init__(self, data_list, json_array, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.extend(data_list)
        self.raw = json_array

        self.is_error = False

        if 'error' in json_array:
            if json_array['error'] is True:
                self.is_error = True

    # A method allowing for end-users to filter data-points by specific attributes, ex: team number.
    def filter(self, attr_name, attr_value):
        """Filter the stored objects by a given attribute.  Returns a new DataList."""

        return_list = self.__class__([], [])

        for data_object in self:
            actual_attribute = getattr(data_object, str(attr_name), None)

            if str(attr_value).lower() in str(actual_attribute).lower():
                return_list.append(data_object)
                return_list.raw.append(data_object.raw)

        return return_list

    # Customize Object Description Output to identify the given list as a DataList
    def __repr__(self):
        """Return a customized object description identifying the list as a DataList."""
        list_return = super().__repr__()
        return '<tbapi.DataList> {}'.format(list_return)

    # A method to return the standard Object Description Output if needed by the user
    @property
    def list_representation(self):
        """Return a JSON-like representation of the data in the list."""
        return super().__repr__()


# Basic Data Class:  Stores information about data returned by TBA by the parser.
class Data(dict):
    """Base Data Class:  Meant for extension by base data models."""
    def __init__(self, json_array, identifier='Generic Data Object'):
        self.update(json_array)
        self.identifier = identifier

    # When referenced in terminal without called attribute, identify as a Data object
    def __repr__(self):
        """Return the Team Key Nickname as the Object Description"""
        return '<tbapi.Data: {}>'.format(self.identifier)


# App Data Class: Represents TBA Mobile App Information.
class App(Data):
    """App Data Class: Represents TBA Mobile App Information."""

    @property
    def latest_app_version(self):
        """The Latest Available App Version on the represented Platform."""
        return self['latest_app_version']

    @property
    def latest(self):
        """The Latest Available App Version on the represented Platform."""
        return self['latest_app_version']

    @property
    def min_app_version(self):
        """The Minimum Supported  App Version on the represented Platform."""
        return self['min_app_version']

    @property
    def minimum(self):
        """The Minimum Supported App Version on the represented Platform."""
        return self['min_app_version']

    @property
    def min(self):
        """The Minimum Supported App Version on the represented Platform."""
        return self['min_app_version']

    # When referenced in terminal without called attribute, identify as a Data object
    def __repr__(self):
        """Return the Team Key Nickname as the Object Description"""
        return '<tbapi.App: {} Platform>'.format(self['platform'])


# Status Data Class: Represents the Status of The Blue Alliance API v3.
class Status(Data):
    """Status Data Class: Represents the Status of The Blue Alliance API v3"""

    @property
    def android(self):
        """Android App Status Information"""
        modified_dict = self['android']
        modified_dict['platform'] = 'Android'
        return App(modified_dict)

    @property
    def ios(self):
        """iOS App Status Information"""
        modified_dict = self['ios']
        modified_dict['platform'] = 'iOS'
        return App(modified_dict)

    @property
    def current_season(self):
        """The Current FRC Season"""
        return self['current_season']

    @property
    def max_season(self):
        """The Max FRC Season"""
        return self['max_season']

    @property
    def is_datafeed_down(self):
        """A Boolean representing whether or not the datafeed is down"""
        return bool(self['is_datafeed_down'])

    @property
    def down_events(self):
        """A raw JSON array representing events that are currently down"""
        return self['down_events']

    def __repr__(self):
        """Modified Reference Return"""
        return '<tbapi.Status: API Status Keys>'


# Team Data Class: Provides team information returned by TBA by the parser.
class Team(Data):
    """Team Data Class: Provides information regarding a given team."""

    @property
    def key(self):
        """Team Key of the represented team"""
        return self['key']

    @property
    def team_number(self):
        """Team Number of the represented team"""
        return self['team_number']

    @property
    def number(self):
        """Team Number of the represented team"""
        return self['team_number']

    @property
    def nickname(self):
        """Nickname of the represented team"""
        return self['nickname']

    @property
    def nick(self):
        """Nickname of the represented team"""
        return self['nickname']

    @property
    def name(self):
        """Full Name of the represented team"""
        return self['name']

    @property
    def rookie_year(self):
        """Rookie Year of the represented team"""
        return self['rookie_year']

    @property
    def motto(self):
        """Motto of the represented team"""
        return self['motto']

    @property
    def website(self):
        """Website URL for the represented team"""
        return self['website']

    @property
    def address(self):
        """Address of the represented team"""
        return self['address']

    @property
    def city(self):
        """Home City of the represented team"""
        return self['city']

    @property
    def state(self):
        """State or Province of the represented team"""
        return self['state_prov']

    @property
    def state_prov(self):
        """State or Province of the represented team"""
        return self['state_prov']

    @property
    def province(self):
        """State or Province of the represented team"""
        return self['state_prov']

    @property
    def country(self):
        """Home Country of the represented team"""
        return self['country']

    @property
    def postal_code(self):
        """Postal Code of the represented team"""
        return self['postal_code']

    @property
    def location_name(self):
        """Name of the location of the represented team"""
        return self['location_name']

    @property
    def lat(self):
        """Latitude of the represented team"""
        return self['lat']

    @property
    def latitude(self):
        """Latitude of the represented team"""
        return self['lat']

    @property
    def lng(self):
        """Longitude of the represented team"""
        return self['lng']

    @property
    def longitude(self):
        """Longitude of the represented team"""
        return self['lng']

    @property
    def home_championship(self):
        """Dictionary sorted by year containing the home championship of the represented team"""
        return self['home_championship']

    @property
    def gmaps_place_id(self):
        """Place ID of the represented team as registered in Google Maps"""
        return self['gmaps_place_id']

    @property
    def gmaps_url(self):
        """A URL representing the location of the represented team in Google Maps"""
        return self['gmaps_url']

    # When referenced in terminal without called attribute, output team_number & nick (readability)
    def __repr__(self):
        """Return the Team Key Nickname as the Object Description"""
        return '<tbapi.Team: {} - {}>'.format(self.team_number, self.nickname)

    # When converted to a string, return the team key
    def __str__(self):
        """Return the Team Key when converted to a String."""
        return self.key

    # When converted to an integer, return the team_number
    def __int__(self):
        """Return the Team Number when converted to an integer."""
        return int(self.team_number) # Convert to an integer, in case of errors in JSON parsing.


# District Data Class: Provides information about a given district.
class District(Data):
    """District Data Class: Provides information regarding a given district."""

    @property
    def key(self):
        """The key of the represented district."""
        return self['key']

    @property
    def year(self):
        """The year of operation of the represented district."""
        return self['year']

    @property
    def display_name(self):
        """A string representing a human readable name for the represented district."""
        return self['display_name']

    @property
    def abbreviation(self):
        """A string representing a simple abbreviation of the represented district's name."""
        return self['abbreviation']

    # When referenced in terminal without called attribute, output display_name, year, and key (readability).
    def __repr__(self):
        """Return the Team Key and Team Name as the Object Description."""
        return '<tbapi.District: {} {} District ({})>'.format(self.year, self.display_name, self.key)

    # When converted to a string, return the district key
    def __str__(self):
        """Return the District Key when converted to a String."""
        return self.key

    # When converted to an integer, return the district year
    def __int__(self):
        """Return the district year when converted to an Integer."""
        return int(self.year) # Convert to an integer, in case of errors in JSON parsing.


# Robot Data Class: Provides information about an individual robot beloging to a team in a given year.
class Robot(Data):
    """Robot Data Class: Provides information about a robot belonging to a team in a given year."""

    @property
    def key(self):
        """The key of the represented robot."""
        return self['key']

    @property
    def robot_name(self):
        """The name of the represented robot."""
        return self['robot_name']

    @property
    def name(self):
        """The name of the represented robot."""
        return self['robot_name']

    @property
    def team_key(self):
        """The team_key of the team that owns the represented robot."""
        return self['team_key']

    @property
    def team(self):
        """The team_key of the team that owns the represented robot."""
        return self['team_key']

    @property
    def team_number(self):
        """The team_number of the team that owns the represented robot."""
        return self['team_key'][3:]

    @property
    def year(self):
        """The year in which the represented robot was built and competed."""
        return self['year']

    # When referenced in terminal without called attribute, output robot_name and key (readability).
    def __repr__(self):
        """Return the Robot Name and Key when referenced."""
        return '<tbapi.Robot: {} ({})>'.format(self.robot_name, self.key)

    # When converted to a string, return the robot's key.
    def __str__(self):
        """Return the Robot Key when converted to a String."""
        return self.key

    # When converted to an integer, return the year in which the robot was built.
    def __int__(self):
        """Return the robot build year when converted to an Integer."""
        return int(self.year) # Convert to an integer, in case of errors in JSON parsing.


# Social Media Data Class: Represents a team's presense on a social media platform.
class Social(Data):
    """Social Media Data Class: Represents a team's presense on a social media platform."""

    @property
    def details(self):
        """Details about the represented Social Media Presense."""
        return self['details']

    @property
    def foreign_key(self):
        """Foreign Key for the represented Social Media Presense."""
        return self['foreign_key']

    @property
    def key(self):
        """Foreign Key for the represented Social Media Presense."""
        return self['foreign_key']

    @property
    def preferred(self):
        """Whether or not the given Social Media Presense is preferred by it's team."""
        return self['preferred']

    @property
    def type(self):
        """The type of Social Media Presense represented."""
        return self['type']

    # When referenced in terminal without called attribute, output Robot Name and Key.
    def __repr__(self):
        """Return the Robot Name and Key when referenced."""
        return '<tbapi.Social: {}>'.format(self.type)


# Event Data Class: Represents a given event and it's corresponding data.
class Event(Data):
    """Event Data Class:  Represents a given Event and it's corresponding data."""

    @property
    def key(self):
        """The key for the represented event."""
        return self['key']

    @property
    def event_code(self):
        """The event code for the represented event."""
        return self['event_code']

    @property
    def code(self):
        """The event code for the represented event."""
        return self['event_code']

    @property
    def year(self):
        """The year in which the represented event takes place."""
        return self['year']

    @property
    def week(self):
        """The event week in which the represented event takes place."""
        return self['week']

    @property
    def name(self):
        """The name of the represented event."""
        return self['name']

    @property
    def short_name(self):
        """The short name of the represented event."""
        return self['short_name']

    @property
    def event_type(self):
        """The type of the represented event."""
        return self['event_type']

    @property
    def event_type_string(self):
        """A string representing the type of the represented event."""
        return self['event_type_string']

    @property
    def start_date(self):
        """The starting date of the represented event."""
        return self['start_date']

    @property
    def start(self):
        """The starting date of the represented event."""
        return self['start_date']

    @property
    def end_date(self):
        """The ending date of the represented event."""
        return self['end_date']

    @property
    def end(self):
        """The ending date of the represented event."""
        return self['end_date']

    @property
    def webcasts(self):
        """A list of Webcast Objects for the represented event."""
        modified_return = self['webcasts']
        modified_return['event'] = '{} ({})'.format(self.name, self.key)
        return DataList([Webcast(webcast_item) for webcast_item in modified_return], self['webcasts'])

    @property
    def website(self):
        """The Website for the represented event."""
        return self['website']

    @property
    def district(self):
        """The District in which the represented event takes place, if available."""
        return self['district']

    @property
    def location_name(self):
        """The name of the location at which the represented event takes place."""
        return self['location_name']

    @property
    def lat(self):
        """A float representing the latitude of the represented event's venue."""
        return self['lat']

    @property
    def latitude(self):
        """A float representing the latitude of the represented event's venue."""
        return self['lat']

    @property
    def lng(self):
        """A float representing the latitude of the represented event's venue."""
        return self['lng']

    @property
    def longitude(self):
        """A float representing the longitude of the represented event's venue."""
        return self['lng']

    @property
    def address(self):
        """The address of the venue of the represented event."""
        return self['address']

    @property
    def city(self):
        """The city of the venue of the represented event."""
        return self['city']

    @property
    def state_prov(self):
        """The state or province of the venue of the represented event."""
        return self['state_prov']

    @property
    def state(self):
        """The state or province of the venue of the represented event."""
        return self['state_prov']

    @property
    def province(self):
        """The state or province of the venue of the represented event."""
        return self['state_prov']

    @property
    def country(self):
        """The country of the venue of the represented event."""
        return self['country']

    @property
    def postal_code(self):
        """The postal code of the venue of the represented event."""
        return self['postal_code']

    @property
    def timezone(self):
        """The timezone of the venue of the represented event."""
        return self['timezone']

    @property
    def gmaps_place_id(self):
        """The google maps place id of the venue of the represented event."""
        return self['gmaps_place_id']

    @property
    def gmaps_url(self):
        """The google maps url of the venue of the represented event."""
        return self['gmaps_url']

    @property
    def first_event_id(self):
        """I have no idea what this does."""
        return self['first_event_id']

    # When referenced in terminal without called attribute, output event name and key.
    def __repr__(self):
        """Return the Event Name and Key when referenced."""
        return '<tbapi.Event: {} ({})>'.format(self.name, self.key)


# Webcast Data Class: Represents a webcast for a given event and its corresponding data.
class Webcast(Data):
    """Webcast Data Class: Represents a webcast for a given event and its corresponding data."""

    @property
    def channel(self):
        """The Channel of the represented Webcast."""
        if 'channel' in self:
            return self['channel']
        else:
            return None

    @property
    def type(self):
        """The Type of the represented Webcast."""
        if 'type' in self:
            return self['type']
        else:
            return None

    @property
    def date(self):
        """The Date of the represented Webcast."""
        if 'date' in self:
            return self['date']
        else:
            return None

    @property
    def file(self):
        """The File of the represented Webcast."""
        if 'file' in self:
            return self['file']
        else:
            return None

    # When referenced in terminal without called attribute, output webcast information.
    def __repr__(self):
        """Return webcast information when referenced."""
        return '<tbapi.Webcast: Webcast for {}>'.format(self['event'])


# Video Data Class: Represents a video as posted on The Blue Alliance.
class Video(Data):
    """Video Data Class: Represents a video as posted on The Blue Alliance."""

    @property
    def key(self):
        """The key of the represented video."""
        return self['key']

    @property
    def type(self):
        """The type of represented video."""
        return self['type']

    # When referenced in terminal without called attribute, output video information.
    def __repr__(self):
        """Return video information when referenced."""
        return '<tbapi.Video: Video for {}>'.format(self['match'])


# Alliance Data Class:  Represents an Alliance that participated in a given Match.
class Alliance(Data):
    """Alliance Data Class:  Represents an Alliance that participated in a given Match."""

    @property
    def score(self):
        """The score earned by the represented Alliance in a given Match."""
        return self['score']

    @property
    def team_keys(self):
        """A list of team keys representing the teams that participated on the represented Alliance."""
        return self['team_keys']

    @property
    def teams(self):
        """A list of team keys representing the teams that participated on the represented Alliance."""
        return self['team_keys']

    @property
    def surrogate_team_keys(self):
        """A list of team keys representing teams that acted as surrogates on the represented Allliance."""
        return self['surrogate_team_keys']

    @property
    def surrogate_teams(self):
        """A list of team keys representing teams that acted as surrogates on the represented Allliance."""
        return self['surrogate_team_keys']

    @property
    def surrogates(self):
        """A list of team keys representing teams that acted as surrogates on the represented Allliance."""
        return self['surrogate_team_keys']

    # When referenced in terminal without called attribute, output alliance information.
    def __repr__(self):
        """Return alliance information when referenced."""
        alliance_members = ''

        for key in self['team_keys']:
            alliance_members += key[3:] + ' '

        return '<tbapi.Alliance: {}>'.format(alliance_members[:-1])


# AllianceSet Data Class:  Wrapper for both Alliances that competed in a given Match.
class AllianceSet(Data):
    """AllianceSet Data Class:  Wrapper for both Alliances that competed in a given Match."""

    @property
    def red(self):
        """The red Alliance for a given Match."""
        return Alliance(self['red'])

    @property
    def r(self):
        """The red Alliance for a given Match."""
        return Alliance(self['red'])

    @property
    def blue(self):
        """The blue Alliance for a given Match."""
        return Alliance(self['blue'])

    @property
    def b(self):
        """The blue Alliance for a given Match."""
        return Alliance(self['blue'])

    # When referenced in terminal without called attribute, output alliance set information.
    def __repr__(self):
        """Return set information when referenced."""
        red_alliance = ''
        blue_alliance = ''

        for key in self['red']['team_keys']:
            red_alliance += key[3:] + ', '

        for key in self['blue']['team_keys']:
            blue_alliance += key[3:] + ', '

        return '<tbapi.AllianceSet: RED[{}], BLUE[{}]>'.format(red_alliance[:-2], blue_alliance[:-2])


# Breakdown Class: Fluid Match Statistics for a given Alliance in a given Match.
class Breakdown(Data):
    """Breakdown Class: Fluid Match Statistics for a given Alliance in a given Match."""

    # Get a fluid key from the internal data dictionary.
    def get(self, key):
        """Get a fluid key from the internal data dictionary."""
        if not key in self.keys():
            raise FluidKeyError
        else:
            return self[key]

    # When referenced in terminal without called attribute, output breakdown information.
    def __repr__(self):
        """Return breakdown information when referenced."""
        return '<tbapi.Breakdown>'

# BreakdownSet Data Class: Wrapper for Breakdowns for a given Match.
class BreakdownSet(Data):
    """BreakdownSet Data Class: Wrapper for Breakdowns for a given Match."""

    @property
    def red(self):
        """Breakdown for the red Alliance for a given Match."""
        return Breakdown(self['red'])

    @property
    def r(self):
        """Breakdown for the red Alliance for a given Match."""
        return Breakdown(self['red'])

    @property
    def blue(self):
        """Breakdown for the blue Alliance for a given Match."""
        return Breakdown(self['blue'])

    @property
    def b(self):
        """Breakdown for the blue Alliance for a given Match."""
        return Breakdown(self['blue'])

    # When referenced in terminal without called attribute, output breakdown set information.
    def __repr__(self):
        """Return breakdown set information when referenced."""
        return '<tbapi.BreakdownSet>'


# Match Data Class: Represents a match played at a given event and its corresponding data.
class Match(Data):
    """Match Data Class: Represents a match at a given event and its corresponding data."""

    @property
    def key(self):
        """The Match Key for the given match.  Includes event_key as a Substring."""
        return self['key']

    @property
    def event_key(self):
        """The Event Key of the Event at which the given match was played."""
        return self['event_key']

    @property
    def comp_level(self):
        """The Competition Level at which the given Match was played. (qm, qf, sf, f, etc.)"""
        return self['comp_level']

    @property
    def level(self):
        """The Competition Level at which the given Match was played. (qm, qf, sf, f, etc.)"""
        return self['comp_level']

    @property
    def match_number(self):
        """The ID number of the given Match"""
        return self['match_number']

    @property
    def number(self):
        """The ID number of the given Match"""
        return self['match_number']

    @property
    def set_number(self):
        """The ID number of the given Match in the current Match set."""
        return self['set_number']

    @property
    def raw_time(self):
        """A Unix-Time representation of the Match Time."""
        return self['time']

    @property
    def time(self):
        """A Datetime representation of the Match Time."""
        return datetime.datetime.fromtimestamp(int(self['time']))

    @property
    def raw_predicted_time(self):
        """A Unix-Time representation of the Scheduled Match Time."""
        return self['predicted_time']

    @property
    def predicted_time(self):
        """A Datetime representation of the Scheduled Match Time."""
        return datetime.datetime.fromtimestamp(int(self['predicted_time']))

    @property
    def raw_post_time(self):
        """A Unix-Time representation of the Score Post Time."""
        return self['post_result_time']

    @property
    def raw_post_result_time(self):
        """A Unix-Time representation of the Score Post Time."""
        return self['post_result_time']

    @property
    def post_time(self):
        """A Datetime representation of the Score Post Time."""
        return datetime.datetime.fromtimestamp(int(self['post_result_time']))

    @property
    def post_result_time(self):
        """A Datetime representation of the Score Post Time."""
        return datetime.datetime.fromtimestamp(int(self['post_result_time']))

    @property
    def videos(self):
        """A DataList of Videos showing the given Match."""
        modified_video_list = []

        for video_item in self['videos']:
            modified_video = video_item.copy()
            modified_video['match'] = self['key']
            modified_video_list += [modified_video]

        return DataList([Video(video_item) for video_item in modified_video_list], self['videos'])

    @property
    def winning_alliance(self):
        """A String representing the color of the winning alliance."""
        return self['winning_alliance']

    @property
    def alliances(self):
        """A Wrapper containing both alliances that participated in the represented match."""
        return AllianceSet(self['alliances'])

    @property
    def red_alliance(self):
        """The red Alliance that participated in the represented match."""
        return Alliance(self['alliances']['red'])

    @property
    def blue_alliance(self):
        """The red Alliance that participated in the represented match."""
        return Alliance(self['alliances']['blue'])

    # When referenced in terminal without called attribute, output match information.
    def __repr__(self):
        """Return match information when referenced."""
        return '<tbapi.Match: {} - {}>'.format(self['key'], '{} Alliance ({} pts)'.format(self['winning_alliance'].capitalize(), self['alliances'][self['winning_alliance']]['score']) if not self['winning_alliance'] == '' else 'tied')


# Recipient Data Class: Represents the Recipient of an Award given at a defined Event.
class Recipient(Data):
    """Recipient Data Class: Represents the Recipient of an Award given at a defined Event."""

    @property
    def team_key(self):
        """The key of the Recipient Team"""
        return self['team_key']

    @property
    def team(self):
        """The key of the Recipient Team"""
        return self['team_key']

    @property
    def awardee(self):
        """The Individual Person to who'm the award was presented."""
        return self['awardee']

    # When referenced in terminal without called attribute, output recipient information.
    def __repr__(self):
        """Return Recipient Information when referenced."""
        return '<tbapi.Recipient: {}'.format(self['team_key'])



# Awards Data Class: Represents an Award given at a defined Event.
class Award(Data):
    """Awards Data Class: Represents an Award given at a defined Event."""

    @property
    def name(self):
        """The name of the represented Award."""
        return self['name']

    @property
    def award_type(self):
        """An Integer representing the type of represented Award."""
        return self['award_type']

    @property
    def type(self):
        """An Integer representing the type of represented Award."""
        return self['award_type']

    @property
    def event_key(self):
        """The key for the Event at which the Award was given."""
        return self['event_key']

    @property
    def recipient_list(self):
        """A list of Recipients to which the represented award was presented."""
        return DataList([Recipient(recipient_item) for recipient_item in self['recipient_list']], self['recipient_list'])

    # When referenced in terminal without called attribute, output award information.
    def __repr__(self):
        """Return Award Information when referenced."""
        return '<tbapi.Award: {} @ {}'.format(self['name'], self['event_key'])


# Cache Database Defaults Class: Used for setting up default columns in the cache database.
class CacheTable(object):
    """Database Cache Defaults:  Holds default cache table column information."""
    def __init__(self):
        self.columns = ['REQUEST', 'RESPONSE', 'REQUESTED', 'LAST_MODIFIED', 'MAX_AGE']
        self.datatypes = ['TEXT PRIMARY KEY NOT NULL', 'TEXT NOT NULL', 'TEXT NOT NULL', 'TEXT NOT NULL', 'TEXT NOT NULL']
        self.seed = []


# Main Parser Class:  All requests routed through this class's methods.
class Parser:
    """TBA Parser Class: Routes API requests and handles caching. Requires v3 API Key from TBA."""

    # Initiate Information needed for connection to TBA v3 (api_key)
    def __init__(self, api_key, *, cache=True, force_cache=False, log_cache=False, cache_multiplier=1):
        self.api_key = api_key # TBA API v3 API key
        self.cache = cache
        self.force_cache = force_cache
        self.log_cache = log_cache
        self.cache_multiplier = cache_multiplier
        self.base_url = 'http://www.thebluealliance.com/api/v3'

        if self.cache:
            self.storage_path = os.path.dirname(sys.executable) + '/.tbapi'

            if not os.path.exists(self.storage_path):
                try:
                    os.makedirs(self.storage_path)
                except:
                    self.storage_path = os.getcwd()

            self.cache_db = sq.Connect(self.storage_path + '/cache')

            if not self.cache_db.table('cache_data').tableExists():
                cache_preset = CacheTable()
                self.cache_db.table('cache_data').init(cache_preset)

    # Modify the response when outputted in the terminal or when converted to a string.
    def __repr__(self):
        """Modified Response Return"""
        return '<tbapi.Parser: \'{}\'>'.format(self.api_key)

    # Method to pull JSON array from TBA v3 API.  Includes Caching and Offline Support.
    def pull_response_json(self, path, *, force_new=False, force_cache=False, log_cache=False):
        """Pull the JSON response to a given path from the TBA API servers or the response cache."""
        
        if not path.startswith('/'):
            path = '/' + path

        current_time = datetime.datetime.now() # Get the Current Time at the start of method execution

        if self.cache and force_new == False: # If caching is enabled, and a new response is not forced, attempt pulling from cache

            cache_reply = self.cache_db.table('cache_data').select('RESPONSE', 'REQUESTED', 'LAST_MODIFIED', 'MAX_AGE').where('REQUEST').equals(path).execute() # Query Cache Database for last stored response

            # Default Values
            cache_response = None
            cache_requested = None
            cache_last_modified = None
            cache_last_modified_str = ''
            cache_max_age = ''

            # Pull Data from Database:  Queried Variable is primary key, so only one row is possible.
            for entry in cache_reply:
                cache_response = json.loads(entry[0]) # Convert stored response back to Python Dictionaries and Lists
                cache_requested = datetime.datetime.strptime(entry[1].strip(), '%a, %d %b %Y %H:%M:%S') # Convert Strings to Datetime objects
                cache_last_modified = datetime.datetime.strptime(entry[2].strip(), '%a, %d %b %Y %H:%M:%S %Z') # Convert Strings to Datetime objects
                cache_last_modified_str = entry[2]
                cache_max_age = entry[3]

            if not cache_response is None: # If Database Response NOT blank:  AKA, if database value for given path not null
                request = (self.base_url + path) # Full Request URL generation based on base_url as set in __init__
                header = {'X-TBA-Auth-Key': self.api_key, 'If-Modified-Since': cache_last_modified_str} # Form headers, but substitute in last_modified string from database to see if data has changed since last database pull.

                if force_cache or self.force_cache:
                    if self.log_cache or log_cache:
                        print('Forcing Read from Cache...')

                    if cache_response == []:
                        raise EmptyError

                    return cache_response

                try:
                    response = requests.get(request, headers=header)
                except:
                    cache_expire_offset = float(cache_max_age) * float(self.cache_multiplier)
                    cache_expire = cache_requested + datetime.timedelta(seconds=int(cache_expire_offset))

                    if current_time <= cache_expire:
                        if self.log_cache or log_cache:
                            print('Offline: Reading from Cache...')

                        if cache_response == []:
                            raise EmptyError

                        return cache_response
                    else:
                        raise OfflineError

                if response.status_code == 304:
                    if self.log_cache or log_cache:
                        print('304 NOT MODIFIED: Reading from Cache...')

                    if cache_response == []:
                        raise EmptyError

                    return cache_response
                else:
                    if self.log_cache or log_cache:
                        print('Data Modified, Ignoring Cache...')

                    try:
                        json_array = response.json()
                    except:
                        raise ParseError

                    response_string = json.dumps(json_array)
                    response_headers = response.headers
                    response_last_modified = response_headers['Last-Modified']
                    response_cache_control = response_headers['Cache-Control']
                    current_time_str = current_time.strftime('%a, %d %b %Y %H:%M:%S')

                    response_max_age = ''
                    cache_control_array = response_cache_control.split(',')

                    for cache_control_item in cache_control_array:
                        cache_control_item = cache_control_item.strip()
                        if cache_control_item.startswith('max-age='):
                            response_max_age = cache_control_item.strip()[8:]

                    self.cache_db.table('cache_data').update('RESPONSE', 'REQUESTED', 'LAST_MODIFIED', 'MAX_AGE').insert(response_string, current_time_str, response_last_modified, response_max_age).where('REQUEST').equals(path).execute()

                    if json_array == []:
                        raise EmptyError

                    return json_array

        request = (self.base_url + path)
        header = {'X-TBA-Auth-Key': self.api_key}

        try:
            response = requests.get(request, headers=header)

            if self.log_cache or log_cache:
                print('No Cache Available, Pulling New Data...')
        except:
            raise OfflineError

        try:
            json_array = response.json()
        except:
            raise ParseError

        if self.cache:
            response_string = json.dumps(json_array)
            response_headers = response.headers
            last_modified = response_headers['Last-Modified']
            cache_control = response_headers['Cache-Control']
            current_time_str = current_time.strftime('%a, %d %b %Y %H:%M:%S')

            response_max_age = ''
            cache_control_array = cache_control.split(',')

            for cache_control_item in cache_control_array:
                cache_control_item = cache_control_item.strip()
                if cache_control_item.startswith('max-age='):
                    response_max_age = cache_control_item.strip()[8:]

            self.cache_db.table('cache_data').insert(path, response_string, current_time_str, last_modified, response_max_age).into('REQUEST', 'RESPONSE', 'REQUESTED', 'LAST_MODIFIED', 'MAX_AGE')

        if json.dumps(json_array) == '[]':
            raise EmptyError

        return json_array


    ### CALL METHODS
    # Get TBA API Status
    def get_status(self, *, force_new=False, force_cache=False, log_cache=False):
        return Status(self.pull_response_json('/status', force_new=False, force_cache=False, log_cache=False))

    # Get a List of FRC Teams
    def get_team_list(self, *, page=None, year=None, force_new=False, force_cache=False, log_cache=False):
        """Get a list of teams.  'page' and 'year' values optional."""
        if not page is None:
            return self.__get_team_list_page(page, year=year, force_new=force_new, force_cache=force_cache, log_cache=log_cache)
        else:
            team_list = DataList([], [])

            for prospective_page in range(0,100):
                try:
                    partial_list = self.__get_team_list_page(prospective_page, year=year, force_new=force_new, force_cache=force_cache, log_cache=log_cache)
                except EmptyError:
                    break

                team_list += partial_list
                team_list.raw += partial_list.raw

        return team_list

    # HELPER: get single page of team data
    def __get_team_list_page(self, page, *, year=None, force_new=False, force_cache=False, log_cache=False):
        """HELPER METHOD: Get a single page of teams."""
        return_array = self.pull_response_json('/teams/{}{}'.format('{}/'.format(year) if not year is None else '', str(page)), force_new=force_new, force_cache=force_cache, log_cache=log_cache)

        page_list = DataList([], return_array)

        for item in return_array:
            team_obj = Team(item)
            page_list.append(team_obj)

        return page_list

    # Get a List of FRC Team Keys
    def get_team_key_list(self, *, page=None, year=None, force_new=False, force_cache=False, log_cache=False):
        """Get a list of team keys.  'page' and 'year' values optional."""
        if not page is None:
            return self.__get_team_list_page(page, year=year, force_new=force_new, force_cache=force_cache, log_cache=log_cache)
        else:
            key_list = []

            for prospective_page in range(0,100):
                try:
                    partial_list = self.__get_team_key_list_page(prospective_page, year=year, force_new=force_new, force_cache=force_cache, log_cache=log_cache)
                except EmptyError:
                    break

                key_list += partial_list

        return key_list
    
    # HELPER: get single page of team keys
    def __get_team_key_list_page(self, page, *, year=None, force_new=False, force_cache=False, log_cache=False):
        """HELPER METHOD: Get a single page of team keys."""
        return self.pull_response_json('/teams/{}{}/keys'.format('{}/'.format(year) if not year is None else '', str(page)), force_new=force_new, force_cache=force_cache, log_cache=log_cache)


    # HELPER: convert team_number or team_key input to uniform team_key
    def __get_team_key(self, team_identifier):
        """Convert team_number or team_key to uniform team_key for request path generation."""
        if str(team_identifier).startswith('frc'):
            return team_identifier
        else:
            try:
                int(team_identifier)
            except ValueError:
                raise KeyInputError

            return 'frc' + str(team_identifier)

    # Get information about a single FRC Team by team number or team key
    def get_team(self, team_identifier, *, force_new=False, force_cache=False, log_cache=False):
        """Get a single team, by 'team_key' or 'team_number'."""
        return Team(self.pull_response_json('/team/{}'.format(self.__get_team_key(team_identifier)), force_new=force_new, force_cache=force_cache, log_cache=log_cache))

    # Get a list containing the years in which a given team has participated
    def get_team_years_participated(self, team_identifier, *, force_new=False, force_cache=False, log_cache=False):
        """Get a list containing the years in which a given team has participated."""
        return self.pull_response_json('/team/{}/years_participated'.format(self.__get_team_key(team_identifier)), force_new=force_new, force_cache=force_cache, log_cache=log_cache)
    
    # Get a list of Districts that the given team has competed in
    def get_team_districts(self, team_identifier, *, force_new=False, force_cache=False, log_cache=False):
        """Get a list of districts in which the given team has competed in."""
        district_list = self.pull_response_json('/team/{}/districts'.format(self.__get_team_key(team_identifier)), force_new=force_new, force_cache=force_cache, log_cache=log_cache)
        return DataList([District(district_item) for district_item in district_list], district_list)

    # Get a list of Robots built and operated by a given team
    def get_team_robots(self, team_identifier, *, force_new=False, force_cache=False, log_cache=False):
        """Get a list of robots built and operated by a given team."""
        robot_list = self.pull_response_json('/team/{}/robots'.format(self.__get_team_key(team_identifier)), force_new=force_new, force_cache=force_cache, log_cache=log_cache)
        return DataList([Robot(robot_item) for robot_item in robot_list], robot_list)

    # Get a list of Social Media Presences operated by a given team.
    def get_team_social_media(self, team_identifier, *, force_new=False, force_cache=False, log_cache=False):
        """Get a list of Social Media Presences operated by a given team."""
        social_list = self.pull_response_json('/team/{}/social_media'.format(self.__get_team_key(team_identifier)), force_new=force_new, force_cache=force_cache, log_cache=log_cache)
        return DataList([Social(social_item) for social_item in social_list], social_list)

    # ALIAS: get_team_social_media
    def get_team_social(self, team_identifier, *, force_new=False, force_cache=False, log_cache=False):
        """Get a list of Social Media Presences operated by a given team."""
        return self.get_team_social_media(team_identifier, force_new=force_new, force_cache=force_cache, log_cache=log_cache)

    # Get a list of events attended by a given team
    def get_team_events(self, team_identifier, year=None, *, force_new=False, force_cache=False, log_cache=False):
        """Get a list of Events attended by a given team."""
        if not year:
            event_list = self.pull_response_json('/team/{}/events'.format(self.__get_team_key(team_identifier)), force_new=force_new, force_cache=force_cache, log_cache=log_cache)
            return DataList([Event(event_item) for event_item in event_list], event_list)
        else:
            event_list = self.pull_response_json('/team/{}/events/{}'.format(self.__get_team_key(team_identifier), str(year)), force_new=force_new, force_cache=force_cache, log_cache=log_cache)
            return DataList([Event(event_item) for event_item in event_list], event_list)

    # Get a list of Matches played by a given Team at a given Event
    def get_team_event_matches(self, team_identifier, event_key, *, force_new=False, force_cache=False, log_cache=False):
        """Get a list of Matches played by a given Team at a given Event."""
        match_list = self.pull_response_json('/team/{}/event/{}/matches'.format(self.__get_team_key(team_identifier), event_key), force_new=force_new, force_cache=force_cache, log_cache=log_cache)
        return DataList([Match(match_item) for match_item in match_list], match_list)

    # Get a list of Awards presented to a given Team at a given Event
    def get_team_event_awards(self, team_identifier, event_key, *, force_new=False, force_cache=False, log_cache=False):
        """Get a list of Awards presented to a given Team at a given Event."""
        award_list = self.pull_response_json('/team/{}/event/{}/awards'.format(self.__get_team_key(team_identifier), event_key), force_new=force_new, force_cache=force_cache, log_cache=log_cache)
        return DataList([Award(award_item) for award_item in award_list], award_list)

    # Get a list of Awards presented to a given Team throughout their History
    def get_team_awards(self, team_identifier, year=None, *, force_new=False, force_cache=False, log_cache=False):
        """Get a list of Awards presented to a given Team throughout their History."""
        award_list = self.pull_response_json('/team/{}/awards{}'.format(self.__get_team_key(team_identifier), '/{}'.format(year) if year else ''), force_new=force_new, force_cache=force_cache, log_cache=log_cache)
        return DataList([Award(award_item) for award_item in award_list], award_list)
        