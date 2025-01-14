"""Defines the Location and Locations classes."""


class Location:
    """
    A class to represent a location in the simulated environment.

    Attributes:
    -----------
    name : str
        The name of the location.
    description : str
        A brief description of the location.

    Methods:
    --------
    describe():
        Prints the description of the location.
    """

    def __init__(self, name, description):  # noqa
        self.name = name
        self.description = description

    def __str__(self):  # noqa
        return self.name

    def describe(self):  # noqa
        print(self.description)


class Locations:
    """
    A class to represent a collection of locations in the simulated environment.

    Attributes:
    -----------
    locations : dict
        A dictionary of locations, with keys as the location names and values as Location objects.

    Methods:
    --------
    add_location(name, description):
        Adds a new location to the collection.

    get_location(name):
        Returns the Location object with the given name.

    __str__():
        Returns a string representation of the collection of locations.
    """

    def __init__(self):  # noqa
        self.locations = {}

    def add_location(self, name, description):  # noqa
        self.locations[name] = Location(name, description)

    def get_location(self, name):  # noqa
        return self.locations.get(name)

    def __str__(self):  # noqa
        return "\n".join([str(location) for location in self.locations.values()])
