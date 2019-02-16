
from GUIconnection import GUIconnection
from Distance import Distance
from Pt import Pt

PLUGINS_FILE = 'plugins.txt'

class nthPoint(GUIconnection):
    """
    This class takes care of the functionality behind the nthPoint method in line simplification. It also have the
    displayName method which will extract the name of the method from the plugins file.
    """

    def displayName(self):
        """
        Uses to get the method names.
        :return: Returns the first method in the plugins file.
        """
        plugins_file_list = []  # list of available methods extracted from the plugins text file
        plugins_file_content = open(PLUGINS_FILE, 'r')
        for line in plugins_file_content:
            line = line.strip('\n')
            plugins_file_list.append(line)
        del plugins_file_list[0]  # to disregard the first line, '-plugin file names-'
        plugins_file_content.close()
        nthpoint_method_name = plugins_file_list[1]  # the index can be easily changed to get the other method names

        return(nthpoint_method_name)


    def thinPoints(self, pts, param):
        """
        Gets a dictionary of points and a parameter. Starts from point no1 and removes a number of entries equal to param
        minus one and returns a dictionary with the existing entries only.
        :param pts: a dictionary  with point references as keys and tuples of (X,Y) as their values.
        :param param: a number represents the desired number of points to be disregarded between each two references points plus one
        :return: The new dictionary doesn't contain the disregarded points and the values have been rearranged starting
        from 1 increasing 1 for each next smallest key value.
        """

        new_dic = {}
        var = 1 # key value of the existing dictionary
        new_var = 1 # key value of the new dictionary
        try:
            int_param = int(param)
            if int_param < len(pts): # Only process when parameter is smaller than the number of available points in the dictionary
                while var <= len(pts): # loops until the var variable exceeds the largest key value of the dictionary (equals to legnth of the dictionary)
                    new_dic[new_var] = pts[var] # sets a new entry for the new dictionary
                    var += int_param # sets the key value variable to previous variable plus the parameter
                    new_var += 1 # sets the new_var which is a potential key value for the new dictionary as the previous one plus one
            else: # When the number of existing points are smaller than the n input given by the user
                print('Choosen n smaller than the number of existing points')
        except ValueError: # asks users to enter valid integer instead of floeats, string, etc
            print('Please enter a valid number')

        return new_dic
