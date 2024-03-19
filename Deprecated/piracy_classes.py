"""
This is the file with the classes required for the Piracy Data Analysis project in Computational Methods II.
No functions in this file are used as it was deprecated by use of Pandas.
We.are.pirates. Bum-ba-dum, dum-dum-dum-dum.
"""

__author__ = "Deryk Clary, Julia MacDonald, Michael Galvan, and MaryGrace Burke"
__credits__ = ["Deryk Clary", "Julia MacDonald", "Michael Galvan", "MaryGrace Burke"]
__email__ = ["deryk.clary@nps.edu", "julia.macdonald@nps.edu", "michael.galvan@nps.edu", "mary.burke@nps.edu"]
__status__ = "Deprecated"

# Import statements
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

    def get_incidents(self):
        """ Returns the dictionary of incidents for the ship. """
        return self.incidents

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

    f = open(csvfile, 'r', newline='')
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
