"""
This is the main file required for the Piracy Data Analysis project in Computational Methods II.
We.are.pirates. Bum-ba-dum, dum-dum-dum-dum.
"""

__author__ = "Deryk Clary, Julia MacDonald, Michael Galvan, and MaryGrace Burke"
__credits__ = ["Deryk Clary", "Julia Macdonald", "Michael Galvan", "MaryGrace Burke"]
__email__ = "deryk.clary@nps.edu"
__status__ = "Development"

from piracy_classes import build_vessel_dict

vessel_dict = build_vessel_dict('Data_Files/IMO Piracy - 2000 to 2022 (PDV 01-2023).csv')
