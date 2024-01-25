"""
This is the file with the classes required for the Piracy Data Analysis project in Computational Methods II.
We.are.pirates. Bum-ba-dum, dum-dum-dum-dum.
"""

__author__ = "Deryk Clary, Julia MacDonald, Michael Galvan, and MaryGrace Burke"
__credits__ = ["Deryk Clary", "Julia Macdonald", "Michael Galvan", "MaryGrace Burke"]
__email__ = "deryk.clary@nps.edu"
__status__ = "Development"

import math
import csv
import datetime


class Coord:
    """
    An improved class to represent lat/lon values.
    Borrowed from oa3801_lab1.py.
    """

    def __init__(self, lat, lon):
        self.lat = float(lat)  # make sure it's a float
        self.lon = float(lon)

    # Follows the specification described in the Aviation Formulary v1.46
    # by Ed Williams (originally at http://williams.best.vwh.net/avform.htm)
    def dist_to(self, other):
        lat1 = Coord.deg2rad(self.lat)
        lon1 = Coord.deg2rad(self.lon)
        lat2 = Coord.deg2rad(other.lat)
        lon2 = Coord.deg2rad(other.lon)

        # implementation #2: (less subject to numerical error for short distances)
        dist_rad = 2 * math.asin(math.sqrt((math.sin((lat1 - lat2) / 2)) ** 2 +
                                           math.cos(lat1) * math.cos(lat2) * (math.sin((lon1 - lon2) / 2)) ** 2))

        return Coord.rad2nm(dist_rad)

    def __str__(self):
        return "(%f,%f)" % (self.lat, self.lon)

    def __repr__(self):
        return "Coord(%f,%f)" % (self.lat, self.lon)

    def deg2rad(self, degrees):
        """Converts degrees (in decimal) to radians."""
        return (math.pi / 180) * degrees

    def rad2nm(self, radians):
        """Converts a distance in radians to a distance in nautical miles."""
        return ((180 * 60) / math.pi) * radians
# end of class Coord


class Vessel:
    """
    Simple representation of a Vessel for use with piracy data.
    Borrowed from oa3801_lab1.py with edits.
    """

    def __init__(self, ship_name, ship_flag, ship_type):
        self.name = ship_name  # assumed to be unique and permanent
        self.flag = ship_flag
        self.type = ship_type
        self.incidents = dict()

    def add_inc(self, date, lat, lon, area, consequence, part, ship_status, weapon, crew_inj, crew_hostage,
                crew_missing, crew_death, crew_assaulted):
        """ Adds an incident to the incident dictionary
           'time' is assumed to be a string in the form '%m/%d/%Y'
           'lat','lon' are assumed to be compatible with Coord objects.
        """
        datestamp = datetime.datetime.strptime(date, '%m/%d/%Y')

        # Add lat, lon as coordinate object if present
        coord = None
        if lat != '' and lon != '':
            coord = Coord(lat, lon)

        # Create incident with passed data
        self.incidents[datestamp] = Incident(coord, consequence, area, part, ship_status, weapon, crew_inj,
                                             crew_hostage, crew_missing, crew_death, crew_assaulted)


    def num_incidents(self):
        """ Returns a count of the number of pings recorded in the track. """
        return len(self.incidents)

    def __str__(self):
        retval = self.name
        retval += '('
        if self.name:
            retval += "name='" + self.name + "'"
            if self.type:
                retval += ',type=' + str(self.type)
            else:
                retval += ',type=None'

            if self.flag:
                retval += ',flag=' + str(self.flag)

        retval += ',%d incidents' % self.num_incidents()
        retval += ')'
        return retval

    # def initial_position(self):
    #     time_series = sorted(self.track)
    #     # returns a tuple of (timestamp, Coord position)
    #     return time_series[0], self.track[time_series[0]]
    #
    # def final_position(self):
    #     time_series = sorted(self.track)
    #     # returns a tuple of (timestamp, Coord position)
    #     return time_series[-1], self.track[time_series[-1]]
    #
    # def total_track_distance(self):
    #     """return the total distance traveled in the track"""
    #     total_distance = 0.0
    #
    #     prev = None
    #     sorted_pings = sorted(self.track)
    #     for ping_key in sorted_pings:
    #         if prev is not None:
    #             total_distance += self.track[ping_key].dist_to(prev)
    #         prev = self.track[ping_key]
    #
    #     return total_distance
    #
    # def last_known_position(self, request_time):
    #     """ Find most recent position (and time), prior to and following a given datetime object
    #     :param request_time: Datetime to search track for
    #     :return: Tuple in form (nearest Datetime before the request time, Coord of that Datetime)
    #     """
    #     # returns a tuple of (timestamp, Coord position)
    #
    #     # we require that the request_time be a datetime object
    #     assert isinstance(request_time, datetime.datetime)
    #
    #     # step 1: create a time series of sorted datetime objects to be searched
    #     #   ( hint: look at initial_position() and final_position() )
    #     time_series = sorted(self.track)
    #
    #     # step 2: find the most recent announced position prior to the given request_time
    #     # note  : if request_time is before first announced position, then return (None,None);
    #     #         otherwise, return a tuple of (timestamp, position) corresponding to
    #     #         the most recent announced position prior the given request_time;
    #
    #     # Check if before first timestamp
    #     if request_time < self.initial_position()[0]:
    #         return None, None
    #
    #     # Binary search code snippet generated by ChatGPT3.5 on 20240118.
    #     # Prompt: 'Write an optimized function to search an ordered list of datetime objects in
    #     #          python for a value that's closest to the input'.
    #     low, high, mid = 0, len(time_series) - 1, 0
    #
    #     # Find exact match using binary search
    #     while low <= high:
    #         mid = (low + high) // 2
    #         mid_datetime = time_series[mid]
    #
    #         if mid_datetime == request_time:
    #             return mid_datetime, self.track[mid_datetime]  # Exact match found
    #
    #         # Move indexes
    #         if mid_datetime < request_time:
    #             low = mid + 1
    #         else:
    #             high = mid - 1
    #
    #     # No exact match, return closest one that's less than request_time
    #     if time_series[mid] < request_time:
    #         return time_series[mid], self.track[time_series[mid]]
    #     else:
    #         return time_series[mid - 1], self.track[time_series[mid - 1]]
# end of class Vessel


class Incident:
    """
    Class to represent an individual incident.
    """
    def __init__(self, coord, consequence, area, part, ship_status, weapon, crew_inj,
                 crew_hostage, crew_missing, crew_death, crew_assaulted):
        self.coord = coord
        self.consequence = consequence
        self.area = area
        self.part = part
        self.ship_status = ship_status
        self.weapon = weapon
        self.crew_inj = crew_inj
        self.crew_hostage = crew_hostage
        self.crew_missing = crew_missing
        self.crew_death = crew_death
        self.crew_assaulted = crew_assaulted

    def __str__(self):
        return (f'Incident Summary: coord={self.coord}, area={self.area}, consequence={self.consequence}, '
                f'part={self.part}, ship_status={self.ship_status}, weapon={self.weapon}, crew_inj={self.crew_inj}, '
                f'crew_hostage={self.crew_hostage}, crew_missing={self.crew_missing}, crew_death={self.crew_death}'
                f', crew_assaulted={self.crew_assaulted}')

def build_vessel_dict(csvfile):
    """
       Given the name of an appropriate csv file, open the file, read and parse it line-by-line,
       and create a dictionary of Vessel objects, with appropriate collection of pings in its track.
       Return the loaded dictionary.
       Borrowed from oa3801_lab1.py with edits.
    """
    vessel_dict = dict()

    f = open(csvfile, newline='')
    f.readline()  # skip the first line, we know it's a header
    linecount = 0
    reader = csv.reader(f)  # use the csv module to parse the file on commas
    for row in reader:
        linecount += 1
        # parse the individual fields as needed
        incident_date = row[0]
        ship_name = row[1]
        ship_flag = row[2]
        ship_type = row[3]
        inc_area = row[4]
        lat = row[5]
        lon = row[6]
        consequence = row[7]
        ship_part = row[8]
        ship_status = row[9]
        weapon_used = row[10]
        crew_injury = row[11]
        crew_hostage = row[12]
        crew_missing = row[13]
        crew_death = row[14]
        crew_assault = row[15]

        # if the ship_name of the current row is not in the dictionary, create an entry for it
        if ship_name not in vessel_dict:
            vessel_dict[ship_name] = Vessel(ship_name, ship_flag, ship_type)
        # add the ping data in the current row to the track of the corresponding Vessel
        vessel_dict[ship_name].add_inc(incident_date, lat, lon, inc_area, consequence, ship_part, ship_status,
                                       weapon_used, crew_injury, crew_hostage, crew_missing, crew_death, crew_assault)
    # end of for-loop
    f.close()

    print("Read %d lines." % linecount)
    print("Dictionary has %d vessels." % len(vessel_dict))

    return vessel_dict


# end of build_vessel_dict

def dms_to_decimal(degrees, minutes, seconds):
    """
    Converts coordinates in dms to decimals.
    Borrowed from oa3801_lab1.py.
    """

    return degrees + minutes / 60 + seconds / 3600
# End of dms_to_decimal()
