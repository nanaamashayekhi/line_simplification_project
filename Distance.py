
from GUIconnection import GUIconnection
from Pt import Pt

PLUGINS_FILE = 'plugins.txt'

class Distance(GUIconnection):
    """
    This class has two main purposes, first one is to get the original file and turn the data into a dictionary
    format which has the point references as keys and the tuple of (x, y) as the values for each point. The second
    purpose is to have a method to carry out the functionality behind the Distance method in line simplification.
    It also has the displayName method which will extract the name of the method from the plugins file.
    """

    def displayName(self):
        """
        gets the method names.
        :return: Returns the first method in the plugins file.
        """
        plugins_file_list = []  # list of available methods extracted from the plugins text file
        plugins_file_content = open(PLUGINS_FILE, 'r')
        for line in plugins_file_content:
            line = line.strip('\n')
            plugins_file_list.append(line)
        del plugins_file_list[0]  # to disregard the first line, '-plugin file names-'
        plugins_file_content.close()
        distance_method_name = plugins_file_list[0] # the index can be easily changed to get the other method names

        return(distance_method_name)

    def makeDic(self, file_name):
        """
        :param file_name: gets a file and converts the data into a dictionary with points references as keys and tuples
        of (X,Y) as their values. This will be the original file to be used to process the data in the other classes.
        :return: a dictionary containing all points with references as keys and tuples of (X,Y) as their values.
        """
        Distance.points_dic = {}
        try:
            file_content = open(file_name, "r")
            try:
                for line in file_content:
                    point_info = line.split(',')
                    point_ref = int(point_info[0].strip('"')) # gets the point reference
                    Distance.points_dic[point_ref] = (float(point_info[1]), float(point_info[2])) # gets the x & y and return them in a tuple
            finally:
                file_content.close()
        except IOError:
            print('Could not find the file')

        return Distance.points_dic # returns the completed dictionary of points


    def thinPoints(self, pts, param):
        """
        :param pts: a dictionary  with point references as keys and tuples of (X,Y) as their values.
        :param param: the minimum distance between two points. Any point closer than that to the previous entry will be disregarded
        :return: the dictionary of points with at least a minimum distance of param between each two points, starting from
        point reference no 1. It uses EuclideanDistance method defined in Pt class to calculate the distance.
        """

        new_dic = {} # the new revised dictionary of points
        new_dic[1] = pts[1] # sets the first point as the point with reference / key 1 in the original dictionary
        initial_var = 1 # key value of the last kept point, only increases when a new point with min distance is found
        var = 2 # key value of the received points dictionary to go through one by one. Point 1 is the initial point so it starts from 2
        the_key = 1 # the key for the new dictionary, only increased when new point is found that fulfills the distance requirement

        while var <= len(pts):
            initial_point = Pt(pts[initial_var][0], pts[initial_var][1]) # sets the initial point
            current_point = Pt(pts[var][0], pts[var][1]) # moves to the next point to check the distance
            distance = initial_point.EuclideanDistance(current_point) # EuclideanDistance method for distance between initial & current points
            if distance >= param: # if the distance is not smaller than param, it add the point reference with its (x, y) to the new dictionary
                new_dic[the_key] = pts[var] # add the key and associated tuple of (x, y) to the new dictionary
                the_key += 1 # increase the_key value so next found entry will have a key value of the previous key value plus one
                initial_var = var # sets this point as the initial point (last kept point)
                var = initial_var + 1 # the next point to be checked is the one with key value of the last kept point key value plus one
            else:
                var += 1 # if the distance is smaller then the current point is disregarded and the same process starts with the next point

        if len(new_dic) > 1: # Checks if there is any new entry, so there has been at least one point where the distance is bigger than the parameter
            return new_dic
        else: # In this situation the dictionary only contains the first point, no point that fulfills the requirement was found
            print('Choosen distance too large to process the data')
            empty_dic = {}
            return empty_dic # Returns an empty dictionary instead of a dictionary with one item so the errors can be handled correctly
