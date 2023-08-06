# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Copyright (c) 2016-2017, Michael Reuter
# Distributed under the MIT License. See LICENSE for more information.
# ------------------------------------------------------------------------------
from enum import Enum
import math
from operator import itemgetter

import ephem

from pylunar import mjd_to_date_tuple, tuple_to_string

__all__ = ["MoonInfo"]

class PhaseName(Enum):
    NEW_MOON = 0
    WAXING_CRESENT = 1
    FIRST_QUARTER = 2
    WAXING_GIBBOUS = 3
    FULL_MOON = 4
    WANING_GIBBOUS = 5
    THIRD_QUARTER = 6
    WANING_CRESENT = 7

class MoonInfo(object):
    """Handle all moon information.

    Attributes
    ----------
    observer : ephem.Observer instance.
        The instance containing the observer's location information.
    moon : ephem.Moon instance
        The instance of the moon object.
    """

    DAYS_TO_HOURS = 24.0

    def __init__(self, latitude, longitude, name=None):
        """Initialize the class.

        Parameters
        ----------
        latitude : tuple of 3 ints
            The latitude of the observer.
        longitude : tuple of 3 ints
            The longitude of the observer.
        name : str, optional
            A name for the observer's location.
        """
        self.observer = ephem.Observer()
        self.observer.lat = tuple_to_string(latitude)
        self.observer.long = tuple_to_string(longitude)
        self.moon = ephem.Moon()

    def age(self):
        """The moon's age in days.

        Returns
        -------
        float
        """
        prev_new = ephem.previous_new_moon(self.observer.date)
        return self.observer.date - prev_new

    def altitude(self):
        """The moon's altitude in degrees.

        Returns
        -------
        float
        """
        return math.degrees(self.moon.alt)

    def azimuth(self):
        """The moon's azimuth in degrees.

        Returns
        -------
        float
        """
        return math.degrees(self.moon.az)

    def colong(self):
        """The moon's selenographic colongitude in degrees.

        Returns
        -------
        float
        """
        return math.degrees(self.moon.colong)

    def fractional_phase(self):
        """The moon's fractional illumination. Always less than 1.0.

        Returns
        -------
        float
        """
        return self.moon.moon_phase

    def libration_lat(self):
        """The moon's current latitudinal libration in degrees.

        Returns
        -------
        float
        """
        return math.degrees(self.moon.libration_lat)

    def libration_lon(self):
        """The moon's current longitudinal libration in degrees.

        Returns
        -------
        float
        """
        return math.degrees(self.moon.libration_long)

    def next_four_phases(self):
        """The next for phases in date sorted order (closest phase first).

        Returns
        -------
        list[(str, float)]
            Set of moon phases specified by an abbreviated phase name and Modified Julian Date.
        """
        phases = {}
        phases["new"] = ephem.next_new_moon(self.observer.date)
        phases["fq"] = ephem.next_first_quarter_moon(self.observer.date)
        phases["full"] = ephem.next_full_moon(self.observer.date)
        phases["tq"] = ephem.next_last_quarter_moon(self.observer.date)

        sorted_phases = sorted(phases.items(), key=itemgetter(1))
        sorted_phases = [(phase[0], mjd_to_date_tuple(phase[1])) for phase in sorted_phases]

        return sorted_phases

    def phase_name(self):
        """The standard name of the moon's phase, i.e. Waxing Cresent

        This function returns a standard name for the moon's phase based on the current selenographic
        colongitude.

        Returns
        -------
        str
        """
        colong = self.colong()
        if colong == 270.0:
            return PhaseName.NEW_MOON.name
        if 270.0 < colong < 360.0:
            return PhaseName.WAXING_CRESENT.name
        if colong == 0.0 or colong == 360.0:
            return PhaseName.FIRST_QUARTER.name
        if 0.0 < colong < 90.0:
            return PhaseName.WAXING_GIBBOUS.name
        if colong == 90.0:
            return PhaseName.FULL_MOON.name
        if 90.0 < colong < 180.0:
            return PhaseName.WANING_GIBBOUS.name
        if colong == 180.0:
            return PhaseName.THIRD_QUARTER.name
        if 180.0 < colong < 270.0:
            return PhaseName.WANING_CRESENT.name

    def time_from_new_moon(self):
        """The time (hours) from the previous new moon.

        This function calculates the time from the previous new moon.

        Returns
        -------
        float
        """
        previous_new_moon = ephem.previous_new_moon(self.observer.date)
        return MoonInfo.DAYS_TO_HOURS * (self.observer.date - previous_new_moon)

    def time_to_full_moon(self):
        """The time (days) to the next full moon.

        This function calculates the time to the next full moon.

        Returns
        -------
        float
        """
        next_full_moon = ephem.next_full_moon(self.observer.date)
        return next_full_moon - self.observer.date

    def time_to_new_moon(self):
        """The time (hours) to the next new moon.

        This function calculates the time to the next new moon.

        Returns
        -------
        float
        """
        next_new_moon = ephem.next_new_moon(self.observer.date)
        return MoonInfo.DAYS_TO_HOURS * (next_new_moon - self.observer.date)

    def update(self, datetime):
        """Update the moon information based on time.

        This fuction updates the Observer instance's datetime setting. The incoming datetime tuple should be
        in UTC with the following placement of values: (YYYY, m, d, H, M, S) as defined below::

            YYYY
                Four digit year

            m
                month (1-12)

            d
                day (1-31)

            H
                hours (0-23)

            M
                minutes (0-59)

            S
                seconds (0-59)

        Parameters
        ----------
        datetime : tuple
            The current UTC time in a tuple of numbers.
        """
        self.observer.date = datetime
        self.moon.compute(self.observer)
