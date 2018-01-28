
"""
Notes:
To view files in different folders the path string variable must be changed in the main function.
The data files selected must be .csv format.
The csv file must list at the top all of the types of data being read.
The program still has trouble with graphing Position-X in relation to Position-Y.

Make sure to use files that do not have appended data at the end, because the strings of the headers will screw up the parser.

***
The purpose of this program is to read data and create readily readable graphical information for users.
***


Improve/Bugs:
For Pandas to work properly, the usecols should be a number, otherwise data is terrible.
Possibly use mathematical functions to smooth the data for better analysis?
"""
def get_velocity_intervals():
    """
    This function is to determine whether the user wants a histogram of velocity intervals
    """
    velocity_available = False
    if any("Velocity" in strings for strings in datatypes):
        velocity_available = True


    if velocity_available == True:
        vel_hist = input("Do you want a histogram of the velocity intervals? (y / n)\n")

        try:
            if (vel_hist[0] == "y"
                    or vel_hist[0] == "Y"
                    or vel_hist[0] == "t"
                    or vel_hist[0] == "T"):
                vel_hist = True
                return vel_hist
            elif (vel_hist[0] == "n"
                    or vel_hist[0] == "N"
                    or vel_hist[0] == "f"
                    or vel_hist[0] == "F"):
                vel_hist = False
                return vel_hist
            else:
                print("Invalid input, try again!")
                get_velocity_intervals()
        except IndexError:
            print("Invalid input, try again!")
            get_velocity_intervals()

def velocity_histograms(data, name_one):
    """
    This function is to create histograms of the velocity intervals.

    :param pandas dataframe data: this is the dataframe of all the data
    """
    import numpy as np
    import matplotlib.pyplot as plt
    #Loop through the data to make it all positive
    data = data.abs()

    bins = np.linspace(0, 10000)        #Sets the min and max of bins and automatically spaces the bins evenly

    y_limit = data[name_one][(len(data) - 1)]

    plt.hist(data['Velocity-X'], range=(0, 10000))
    #################Get the histogram to show time instead of frequency!!!!!!!!!!
    plt.show()

def get_file_name():
    """
    This function gets the name of the file to be used from the user.

    :return string path: this is the path of the .csv file to be read

    Note: all csv files must be in the Data folder, otherwise the code must be changed.
    """

    file_name = input("Please enter the exact name of the file: ")      #Gets the name of the file.
    if (len(file_name) > 0):
        if file_name[(len(file_name) - 4):] == '.csv':      #Checks to see if user included .csv at the end of the name
            pass                                        #If the user included it, pass
        else:
            file_name += ".csv"                         #Otherwise put it in

        path = "..\..\Data\\" + file_name

        return path, file_name
    else:
        print("Try again.\n")
        return get_file_name()

def get_available_datatypes(path, file_name):
    """
    This function reads the csv file and prints the names of all the available datatypes the user can use.

    :param string path: this is the string of the path to the csv file
    """
    number = 0

    import csv
    try:
        with open(path, "r") as f:
            reader = csv.reader(f)
            datatypes = next(reader)         #Creates a list of the column headers

            print("These are the available datatypes for use: ")

            for available_datatype in datatypes:
                print(str(number) + ". " + available_datatype)
                number += 1

            return datatypes, file_name
    except FileNotFoundError:
        print("\nThe file you entered was not found in the data file directory.\n" \
            "\nCheck to make sure the file is in the Data folder and that you entered the name correctly.\n" \
            "Try again.\n")
        #Gets the new path for trying again.
        path, file_name = get_file_name()
        #Restarts the function
        get_available_datatypes(path, file_name)



def graph_derivatives():
    """
    This function determines if the user wants to graph derivative graphs alongside the taken data.

    :return boolean graph_deriv: graph_deriv is returned to determine to graph derivatives or not
    """
    graph_deriv = input("Do you want to also graph derivatives? (y / n)")

    try:
        if (graph_deriv[0] == "y"
                or graph_deriv[0] == "Y"
                or graph_deriv[0] == "t"
                or graph_deriv[0] == "T"):
            graph_deriv = True
            return graph_deriv
        elif (graph_deriv[0] == "n"
                or graph_deriv[0] == "N"
                or graph_deriv[0] == "f"
                or graph_deriv[0] == "F"):
            graph_deriv = False
            return graph_deriv
        else:
            print("Invalid input, try again!")
            graph_derivatives()
    except IndexError:
        print("Invalid input, try again!")
        graph_derivatives()

def num_of_graphs(datatypes):
    """
    This functions determines whether the user wants to use multiple graphs or a singular graph for representation.
    This function also is the final step and graphs all of the graphs to matplotlib.

    :param list datatypes: the list of the names of available data for graphing
    """
    try:
        information = int(input("How many types of data would you like to graph? (2, 3 or 4)\n"))

        if information == 2:
            data, name_one, name_two = get_pozyx_data_two(file_name, datatypes)
            create_graph_two(data, name_one, name_two)

            if velocity_histogram == True: #Checks to graph the histograms of velocity
                velocity_histograms(data, name_one)

        elif information == 3:
            data, name_one, name_two, name_three = get_pozyx_data_three(file_name, datatypes)
            create_graph_three(data, name_one, name_two, name_three)

            if velocity_histogram == True:  #Checks to graph the histograms of velocity
                velocity_histograms(data, name_one)

        elif information == 4:
            data, name_one, name_two, name_three, name_four = get_pozyx_data_four(file_name, datatypes)
            create_graph_four(data, name_one, name_two, name_three, name_four)

            if velocity_histogram == True:  #Checks to graph the histograms of velocity
                velocity_histograms(data, name_one)

        else:
            print("Invalid input, try again!")
            num_of_graphs(datatypes)

    except ValueError:
        print("Invalid input, try again!")
        num_of_graphs(datatypes)

def regular_graphing_method():
    """
    This function was created to determine whether the user wants to graph the data on top of each other or on separate graphs.

    :return boolean regular_ontop: regular_ontop is returned to determine how the data will graph

    Note: if regular_ontop is true, the non-derivative data will all graph on one graph
    """

    regular_ontop = input("Do you want to graph the originally selected data on top of each other? (y / n)")

    try:
        if (regular_ontop[0] == "y"
                or regular_ontop[0] == "Y"
                or regular_ontop[0] == "t"
                or regular_ontop[0] == "T"):
            regular_ontop = True
            return regular_ontop
        elif (regular_ontop[0] == "n"
                or regular_ontop[0] == "N"
                or regular_ontop[0] == "f"
                or regular_ontop[0] == "F"):
            regular_ontop = False
            return regular_ontop
        else:
            print("Invalid input, try again!")
            regular_graphing_method()
    except IndexError:
        print("Invalid input, try again!")
        regular_graphing_method()

def deriv_graphing_method():
    """
    This function determines how the user desires to graph the derivatives if they want to
    """
    deriv_method = 0

    try:
        #Loop until get desired value
        while (deriv_method != 1 or deriv_method != 2 or deriv_method != 3):
            #Obtain the desired input from the user
            deriv_method = int(input("Do you want to graph the derivatives:\n" \
                            "1. On their own graphs\n"\
                            "2. All together on their own graph\n" \
                            "3. On top of the original data\n"))

            #Checks to see if user input was appropriate
            if (deriv_method == 1 or deriv_method == 2 or deriv_method == 3):
                return deriv_method
            #Message if the user did not input desired value
            else:
                print("Invalid input, try again!")

    #Exception to handle non-integer input
    except ValueError:
        print("Invalid input, try again!")
        deriv_graphing_method()

def get_pozyx_data_two(file_name, datatypes):
    """
    Function to get data for graphing one type of data over another.

    :param string file_name: the name of the file that will be used for parsing
    :param list datatypes: the list of the types of data the file has available

    :return datatype: this returns the dataframe of all the data that will be used for graphing
    :return name_one: this returns the name of the x-variable chosen
    :return name_two: this returns the name of the y-variable chosen

    The user inputs which to use.
    The data is collected from the csv file and returned in the return statement along with the names of the types of data chosen
    """

    try:
        col_one = int(input("Which data type would you like to use for the X axis? (Default is time.)\n"))
    except ValueError:
        col_one = datatypes.index('Time')

    try:
        col_two = int(input("Which data type would you like to use for the Y axis? (Default is X-Position.)\n"))
    except ValueError:
        try:
            col_two = datatypes.index("Position-X")
        except ValueError:
            print("Default set failed, set to X-Acceleration")
            col_two = datatypes.index("Acceleration-X")

    name_one = ""
    name_two = ""

    """
    These if statements set the appropriate colums to the right names.
    If the user does not input an integer between 0 and 29, then the X-Axis defaults to time.
    """
    try:
        if col_one == 0:
            name_one = datatypes[0]
        elif col_one == 1:
            name_one = datatypes[1]
        elif col_one == 2:
            name_one = datatypes[2]
        elif col_one == 3:
            name_one = datatypes[3]
        elif col_one == 4:
            name_one = datatypes[4]
        elif col_one == 5:
            name_one = datatypes[5]
        elif col_one == 6:
            name_one = datatypes[6]
        elif col_one == 7:
            name_one = datatypes[7]
        elif col_one == 8:
            name_one = datatypes[8]
        elif col_one == 9:
            name_one = datatypes[9]
        elif col_one == 10:
            name_one = datatypes[10]
        elif col_one == 11:
            name_one = datatypes[11]
        elif col_one == 12:
            name_one = datatypes[12]
        elif col_one == 13:
            name_one = datatypes[13]
        elif col_one == 14:
            name_one = datatypes[14]
        elif col_one == 15:
            name_one = datatypes[15]
        elif col_one == 16:
            name_one = datatypes[16]
        elif col_one == 17:
            name_one = datatypes[17]
        elif col_one == 18:
            name_one = datatypes[18]
        elif col_one == 19:
            name_one = datatypes[19]
        elif col_one == 20:
            name_one = datatypes[20]
        elif col_one == 21:
            name_one = datatypes[21]
        elif col_one == 22:
            name_one = datatypes[22]
        elif col_one == 23:
            name_one = datatypes[23]
        elif col_one == 24:
            name_one = datatypes[24]
        elif col_one == 25:
            name_one = datatypes[25]
        elif col_one == 26:
            name_one = datatypes[26]
        elif col_one == 27:
            name_one = datatypes[27]
        elif col_one == 28:
            name_one = datatypes[28]
        elif col_one == 29:
            name_one = datatypes[29]
        else:
            name_one = "Time"
    except IndexError:
        name_one = "Time"

    try:
        if col_two == 0:
            name_two = datatypes[0]
        elif col_two == 1:
            name_two = datatypes[1]
        elif col_two == 2:
            name_two = datatypes[2]
        elif col_two == 3:
            name_two = datatypes[3]
        elif col_two == 4:
            name_two = datatypes[4]
        elif col_two == 5:
            name_two = datatypes[5]
        elif col_two == 6:
            name_two = datatypes[6]
        elif col_two == 7:
            name_two = datatypes[7]
        elif col_two == 8:
            name_two = datatypes[8]
        elif col_two == 9:
            name_two = datatypes[9]
        elif col_two == 10:
            name_two = datatypes[10]
        elif col_two == 11:
            name_two = datatypes[11]
        elif col_two == 12:
            name_two = datatypes[12]
        elif col_two == 13:
            name_two = datatypes[13]
        elif col_two == 14:
            name_two = datatypes[14]
        elif col_two == 15:
            name_two = datatypes[15]
        elif col_two == 16:
            name_two = datatypes[16]
        elif col_two == 17:
            name_two = datatypes[17]
        elif col_two == 18:
            name_two = datatypes[18]
        elif col_two == 19:
            name_two = datatypes[19]
        elif col_two == 20:
            name_two = datatypes[20]
        elif col_two == 21:
            name_two = datatypes[21]
        elif col_two == 22:
            name_two = datatypes[22]
        elif col_two == 23:
            name_two = datatypes[23]
        elif col_two == 24:
            name_two = datatypes[24]
        elif col_two == 25:
            name_two = datatypes[25]
        elif col_two == 26:
            name_two = datatypes[26]
        elif col_two == 27:
            name_two = datatypes[27]
        elif col_two == 28:
            name_two = datatypes[28]
        elif col_two == 29:
            name_two = datatypes[29]
        else:
            name_two = "Time"
    except IndexError:
        name_two = "Time"

    """
    This line stores the data in a structure to be used for graphing.

    Due to unknown error, we must add one to col_two to get the correct data points.
    """
    datatype = pandas.read_csv(path, delimiter = ',', header = 0, usecols = [col_one, col_two], names = [name_one, name_two], na_values = 'error')



    return datatype, name_one, name_two


def get_pozyx_data_three(file_name, datatypes):
    """
    Function to get data for graphing two types of data over another.

    :param string file_name: the name of the file that will be used for parsing
    :param list datatypes: the list of the types of data the file has available

    :return datatype: this returns the dataframe of all the data that will be used for graphing
    :return name_one: this returns the name of the x-variable chosen
    :return name_two: this returns the name of the y-variable chosen
    :return name_three: this returns the name of the second y-variable chosen

    The user inputs which to use.
    The data is collected from the csv file and returned in the return statement along with the names of the types of data chosen
    """


    try:
        col_one = int(input("Which data type would you like to use for the X axis? (Default is time.)\n"))
    except ValueError:
        col_one = datatypes.index("Time")

    try:
        col_two = int(input("Which data type would you like to use for the Y axis? (Default is X-Position.)\n"))
    except ValueError:
        try:
            col_two = datatypes.index("Position-X")
        except ValueError:
            print("Default set failed, set to X-Acceleration")
            col_two = datatypes.index("Acceleration-X")

    try:
        col_three = int(input("Which data type would you like to use for the Y axis? (Default is Y-Position.)\n"))
    except ValueError:
        try:
            col_three = datatypes.index("Position-Y")
        except ValueError:
            print("Default set failed, set to Y-Acceleration")
            col_three = datatypes.index("Acceleration-Y")


    name_one = ""
    name_two = ""
    name_three = ""


    try:
        if col_one == 0:
            name_one = datatypes[0]
        elif col_one == 1:
            name_one = datatypes[1]
        elif col_one == 2:
            name_one = datatypes[2]
        elif col_one == 3:
            name_one = datatypes[3]
        elif col_one == 4:
            name_one = datatypes[4]
        elif col_one == 5:
            name_one = datatypes[5]
        elif col_one == 6:
            name_one = datatypes[6]
        elif col_one == 7:
            name_one = datatypes[7]
        elif col_one == 8:
            name_one = datatypes[8]
        elif col_one == 9:
            name_one = datatypes[9]
        elif col_one == 10:
            name_one = datatypes[10]
        elif col_one == 11:
            name_one = datatypes[11]
        elif col_one == 12:
            name_one = datatypes[12]
        elif col_one == 13:
            name_one = datatypes[13]
        elif col_one == 14:
            name_one = datatypes[14]
        elif col_one == 15:
            name_one = datatypes[15]
        elif col_one == 16:
            name_one = datatypes[16]
        elif col_one == 17:
            name_one = datatypes[17]
        elif col_one == 18:
            name_one = datatypes[18]
        elif col_one == 19:
            name_one = datatypes[19]
        elif col_one == 20:
            name_one = datatypes[20]
        elif col_one == 21:
            name_one = datatypes[21]
        elif col_one == 22:
            name_one = datatypes[22]
        elif col_one == 23:
            name_one = datatypes[23]
        elif col_one == 24:
            name_one = datatypes[24]
        elif col_one == 25:
            name_one = datatypes[25]
        elif col_one == 26:
            name_one = datatypes[26]
        elif col_one == 27:
            name_one = datatypes[27]
        elif col_one == 28:
            name_one = datatypes[28]
        elif col_one == 29:
            name_one = datatypes[29]
        else:
            name_one = "Time"
    except IndexError:
        name_one = "Time"

    try:
        if col_two == 0:
            name_two = datatypes[0]
        elif col_two == 1:
            name_two = datatypes[1]
        elif col_two == 2:
            name_two = datatypes[2]
        elif col_two == 3:
            name_two = datatypes[3]
        elif col_two == 4:
            name_two = datatypes[4]
        elif col_two == 5:
            name_two = datatypes[5]
        elif col_two == 6:
            name_two = datatypes[6]
        elif col_two == 7:
            name_two = datatypes[7]
        elif col_two == 8:
            name_two = datatypes[8]
        elif col_two == 9:
            name_two = datatypes[9]
        elif col_two == 10:
            name_two = datatypes[10]
        elif col_two == 11:
            name_two = datatypes[11]
        elif col_two == 12:
            name_two = datatypes[12]
        elif col_two == 13:
            name_two = datatypes[13]
        elif col_two == 14:
            name_two = datatypes[14]
        elif col_two == 15:
            name_two = datatypes[15]
        elif col_two == 16:
            name_two = datatypes[16]
        elif col_two == 17:
            name_two = datatypes[17]
        elif col_two == 18:
            name_two = datatypes[18]
        elif col_two == 19:
            name_two = datatypes[19]
        elif col_two == 20:
            name_two = datatypes[20]
        elif col_two == 21:
            name_two = datatypes[21]
        elif col_two == 22:
            name_two = datatypes[22]
        elif col_two == 23:
            name_two = datatypes[23]
        elif col_two == 24:
            name_two = datatypes[24]
        elif col_two == 25:
            name_two = datatypes[25]
        elif col_two == 26:
            name_two = datatypes[26]
        elif col_two == 27:
            name_two = datatypes[27]
        elif col_two == 28:
            name_two = datatypes[28]
        elif col_two == 29:
            name_two = datatypes[29]
        else:
            name_two = "Position-X"
    except IndexError:
        name_two = "Position-X"

    try:
        if col_three == 0:
            name_three = datatypes[0]
        elif col_three == 1:
            name_three = datatypes[1]
        elif col_three == 2:
            name_three = datatypes[2]
        elif col_three == 3:
            name_three = datatypes[3]
        elif col_three == 4:
            name_three = datatypes[4]
        elif col_three == 5:
            name_three = datatypes[5]
        elif col_three == 6:
            name_three = datatypes[6]
        elif col_three == 7:
            name_three = datatypes[7]
        elif col_three == 8:
            name_three = datatypes[8]
        elif col_three == 9:
            name_three = datatypes[9]
        elif col_three == 10:
            name_three = datatypes[10]
        elif col_three == 11:
            name_three = datatypes[11]
        elif col_three == 12:
            name_three = datatypes[12]
        elif col_three == 13:
            name_three = datatypes[13]
        elif col_three == 14:
            name_three = datatypes[14]
        elif col_three == 15:
            name_three = datatypes[15]
        elif col_three == 16:
            name_three = datatypes[16]
        elif col_three == 17:
            name_three = datatypes[17]
        elif col_three == 18:
            name_three = datatypes[18]
        elif col_three == 19:
            name_three = datatypes[19]
        elif col_three == 20:
            name_three = datatypes[20]
        elif col_three == 21:
            name_three = datatypes[21]
        elif col_three == 22:
            name_three = datatypes[22]
        elif col_three == 23:
            name_three = datatypes[23]
        elif col_three == 24:
            name_three = datatypes[24]
        elif col_three == 25:
            name_three = datatypes[25]
        elif col_three == 26:
            name_three = datatypes[26]
        elif col_three == 27:
            name_three = datatypes[27]
        elif col_three == 28:
            name_three = datatypes[28]
        elif col_three == 29:
            name_three = datatypes[29]
        else:
            name_three = "Position-Y"
    except IndexError:
        name_three = "Position-Y"



    datatype = pandas.read_csv(path, delimiter = ',', header = 0, usecols = [col_one, col_two, col_three], names = [name_one, name_two, name_three], na_values = 'error')



    return datatype, name_one, name_two, name_three

def get_pozyx_data_four(file_name, datatypes):
    """
    Function to get data for graphing two types of data over another.

    :param string file_name: the name of the file that will be used for parsing
    :param list datatypes: the list of the types of data the file has available

    :return datatype: this returns the dataframe of all the data that will be used for graphing
    :return name_one: this returns the name of the x-variable chosen
    :return name_two: this returns the name of the y-variable chosen
    :return name_three: this returns the name of the second y-variable chosen
    :return name_four: this returns the name of the third y-variable chosen

    The user inputs which to use.
    The data is collected from the csv file and returned in the return statement along with the names of the types of data chosen
    """


    try:
        col_one = int(input("Which data type would you like to use for the X axis? (Default is time.)\n"))
    except ValueError:
        col_one = datatypes.index("Time")


    try:
        col_two = int(input("Which data type would you like to use for the Y axis? (Default is X-Position.)\n"))
    except ValueError:
        try:
            col_two = datatypes.index("Position-X")
        except ValueError:
            print("Default set failed, set to X-Acceleration")
            col_two = datatypes.index("Acceleration-X")

    try:
        col_three = int(input("Which data type would you like to use for the Y axis? (Default is Y-Position.)\n"))
    except ValueError:
        try:
            col_three = datatypes.index("Position-Y")
        except ValueError:
            print("Default set failed, set to Y-Acceleration")
            col_three = datatypes.index("Acceleration-Y")

    try:
        col_four = int(input("Which data type would you like to use for the Y axis? (Default is Z-Position.)\n"))
    except ValueError:
        try:
            col_four = datatypes.index("Position-Z")
        except ValueError:
            print("Default set failed, set to Z-Acceleration")
            col_four = datatypes.index("Acceleration-Z")


    name_one = ""
    name_two = ""
    name_three = ""
    name_four = ""

    try:
        if col_one == 0:
            name_one = datatypes[0]
        elif col_one == 1:
            name_one = datatypes[1]
        elif col_one == 2:
            name_one = datatypes[2]
        elif col_one == 3:
            name_one = datatypes[3]
        elif col_one == 4:
            name_one = datatypes[4]
        elif col_one == 5:
            name_one = datatypes[5]
        elif col_one == 6:
            name_one = datatypes[6]
        elif col_one == 7:
            name_one = datatypes[7]
        elif col_one == 8:
            name_one = datatypes[8]
        elif col_one == 9:
            name_one = datatypes[9]
        elif col_one == 10:
            name_one = datatypes[10]
        elif col_one == 11:
            name_one = datatypes[11]
        elif col_one == 12:
            name_one = datatypes[12]
        elif col_one == 13:
            name_one = datatypes[13]
        elif col_one == 14:
            name_one = datatypes[14]
        elif col_one == 15:
            name_one = datatypes[15]
        elif col_one == 16:
            name_one = datatypes[16]
        elif col_one == 17:
            name_one = datatypes[17]
        elif col_one == 18:
            name_one = datatypes[18]
        elif col_one == 19:
            name_one = datatypes[19]
        elif col_one == 20:
            name_one = datatypes[20]
        elif col_one == 21:
            name_one = datatypes[21]
        elif col_one == 22:
            name_one = datatypes[22]
        elif col_one == 23:
            name_one = datatypes[23]
        elif col_one == 24:
            name_one = datatypes[24]
        elif col_one == 25:
            name_one = datatypes[25]
        elif col_one == 26:
            name_one = datatypes[26]
        elif col_one == 27:
            name_one = datatypes[27]
        elif col_one == 28:
            name_one = datatypes[28]
        elif col_one == 29:
            name_one = datatypes[29]
        else:
            name_one = "Time"
    except IndexError:
        name_one = "Time"

    try:
        if col_two == 0:
            name_two = datatypes[0]
        elif col_two == 1:
            name_two = datatypes[1]
        elif col_two == 2:
            name_two = datatypes[2]
        elif col_two == 3:
            name_two = datatypes[3]
        elif col_two == 4:
            name_two = datatypes[4]
        elif col_two == 5:
            name_two = datatypes[5]
        elif col_two == 6:
            name_two = datatypes[6]
        elif col_two == 7:
            name_two = datatypes[7]
        elif col_two == 8:
            name_two = datatypes[8]
        elif col_two == 9:
            name_two = datatypes[9]
        elif col_two == 10:
            name_two = datatypes[10]
        elif col_two == 11:
            name_two = datatypes[11]
        elif col_two == 12:
            name_two = datatypes[12]
        elif col_two == 13:
            name_two = datatypes[13]
        elif col_two == 14:
            name_two = datatypes[14]
        elif col_two == 15:
            name_two = datatypes[15]
        elif col_two == 16:
            name_two = datatypes[16]
        elif col_two == 17:
            name_two = datatypes[17]
        elif col_two == 18:
            name_two = datatypes[18]
        elif col_two == 19:
            name_two = datatypes[19]
        elif col_two == 20:
            name_two = datatypes[20]
        elif col_two == 21:
            name_two = datatypes[21]
        elif col_two == 22:
            name_two = datatypes[22]
        elif col_two == 23:
            name_two = datatypes[23]
        elif col_two == 24:
            name_two = datatypes[24]
        elif col_two == 25:
            name_two = datatypes[25]
        elif col_two == 26:
            name_two = datatypes[26]
        elif col_two == 27:
            name_two = datatypes[27]
        elif col_two == 28:
            name_two = datatypes[28]
        elif col_two == 29:
            name_two = datatypes[29]
        else:
            name_two = "Position-X"
    except IndexError:
        name_two = "Position-X"

    try:
        if col_three == 0:
            name_three = datatypes[0]
        elif col_three == 1:
            name_three = datatypes[1]
        elif col_three == 2:
            name_three = datatypes[2]
        elif col_three == 3:
            name_three = datatypes[3]
        elif col_three == 4:
            name_three = datatypes[4]
        elif col_three == 5:
            name_three = datatypes[5]
        elif col_three == 6:
            name_three = datatypes[6]
        elif col_three == 7:
            name_three = datatypes[7]
        elif col_three == 8:
            name_three = datatypes[8]
        elif col_three == 9:
            name_three = datatypes[9]
        elif col_three == 10:
            name_three = datatypes[10]
        elif col_three == 11:
            name_three = datatypes[11]
        elif col_three == 12:
            name_three = datatypes[12]
        elif col_three == 13:
            name_three = datatypes[13]
        elif col_three == 14:
            name_three = datatypes[14]
        elif col_three == 15:
            name_three = datatypes[15]
        elif col_three == 16:
            name_three = datatypes[16]
        elif col_three == 17:
            name_three = datatypes[17]
        elif col_three == 18:
            name_three = datatypes[18]
        elif col_three == 19:
            name_three = datatypes[19]
        elif col_three == 20:
            name_three = datatypes[20]
        elif col_three == 21:
            name_three = datatypes[21]
        elif col_three == 22:
            name_three = datatypes[22]
        elif col_three == 23:
            name_three = datatypes[23]
        elif col_three == 24:
            name_three = datatypes[24]
        elif col_three == 25:
            name_three = datatypes[25]
        elif col_three == 26:
            name_three = datatypes[26]
        elif col_three == 27:
            name_three = datatypes[27]
        elif col_three == 28:
            name_three = datatypes[28]
        elif col_three == 29:
            name_three = datatypes[29]
        else:
            name_three = "Position-Y"
    except IndexError:
        name_three = "Position-Y"


    try:
        if col_four == 0:
            name_four = datatypes[0]
        elif col_four == 1:
            name_four = datatypes[1]
        elif col_four == 2:
            name_four = datatypes[2]
        elif col_four == 3:
            name_four = datatypes[3]
        elif col_four == 4:
            name_four = datatypes[4]
        elif col_four == 5:
            name_four = datatypes[5]
        elif col_four == 6:
            name_four = datatypes[6]
        elif col_four == 7:
            name_four = datatypes[7]
        elif col_four == 8:
            name_four = datatypes[8]
        elif col_four == 9:
            name_four = datatypes[9]
        elif col_four == 10:
            name_four = datatypes[10]
        elif col_four == 11:
            name_four = datatypes[11]
        elif col_four == 12:
            name_four = datatypes[12]
        elif col_four == 13:
            name_four = datatypes[13]
        elif col_four == 14:
            name_four = datatypes[14]
        elif col_four == 15:
            name_four = datatypes[15]
        elif col_four == 16:
            name_four = datatypes[16]
        elif col_four == 17:
            name_four = datatypes[17]
        elif col_four == 18:
            name_four = datatypes[18]
        elif col_four == 19:
            name_four = datatypes[19]
        elif col_four == 20:
            name_four = datatypes[20]
        elif col_four == 21:
            name_four = datatypes[21]
        elif col_four == 22:
            name_four = datatypes[22]
        elif col_four == 23:
            name_four = datatypes[23]
        elif col_four == 24:
            name_four = datatypes[24]
        elif col_four == 25:
            name_four = datatypes[25]
        elif col_four == 26:
            name_four = datatypes[26]
        elif col_four == 27:
            name_four = datatypes[27]
        elif col_four == 28:
            name_four = datatypes[28]
        elif col_four == 29:
            name_four = datatypes[29]
        else:
            name_four = "Position-Z"
    except IndexError:
        name_four = "Position-Z"


    datatype = pandas.read_csv(path, delimiter = ',', header = 0, usecols = [col_one, col_two, col_three, col_four], names = [name_one, name_two, name_three, name_four], na_values = 'error')



    return datatype, name_one, name_two, name_three, name_four



def create_graph_two(data, name_one, name_two):
    """
    Function to graph a type of data over another along with the derivative of the plot.

    :param dataframe data: this is the data from the csv file retrieved by Pandas
    :param string name_one: the name of the x-variable
    :param string name_two: the name of the y-variable
    :param string name_three: the name of the second y-variable
    """
    x = data[name_one]
    y1 = data[name_two]
    try:
        y1_deriv = data.diff(1,0)[name_two]
    except TypeError:
        print("\nThe data contains is contains non-numeric values.\n\n"  \
                "Either edit the file to only contain numeric values after the header or\n" \
                "try using another file.")
        import sys
        sys.exit()


    if graph_deriv == False:
        #Graphs the original data separate
        if regular_ontop == False:
            plt.plot(x, y1)
            plt.xlabel(name_one)
            plt.legend()
            plt.title(name_two + " vs. " + name_one)
            plt.legend()
        #Graphs the original data together
        if regular_ontop == True:
            plt.plot(x, y1)
            plt.xlabel(name_one)
            plt.legend()
            plt.title(name_two + " vs. " + name_one)
            plt.legend()

    if graph_deriv == True:
        #Graphs the original data together and the derivatives on their own graphs
        if (regular_ontop == True and deriv_method == 1):
            plt.subplot(2, 2, (1,2))
            plt.plot(x, y1, label = name_two)
            plt.legend( loc=2, prop={'size': 6})
            plt.title(name_two + " vs. " + name_one)
            plt.ylabel(name_two)

            plt.subplot(2, 2, (3,4))
            plt.plot(x, y1_deriv, label = ("Derivative of " + name_two))
            plt.legend( loc=2, prop={'size': 6})
            plt.title("Derivative of " + name_two + " vs. " + name_one)
            plt.ylabel(name_two)

        #Graphs the original data together and the derivatives together on their own graph
        if (regular_ontop == True and deriv_method == 2):
            plt.subplot(2, 2, (1,2))
            plt.plot(x, y1, label = name_two)
            plt.legend( loc=2, prop={'size': 6})
            plt.title(name_two + " vs. " + name_one)
            plt.ylabel(name_two)

            plt.subplot(2, 2, (3,4))
            plt.plot(x, y1_deriv, label = ("Derivative of", name_two))
            plt.legend( loc=2, prop={'size': 6})
            plt.title("Derivative of " + name_two + " vs. " + name_one)
            plt.ylabel(name_two)

        #Graphs the original data together and the derivatives on top of the original data
        if (regular_ontop == True and deriv_method == 3):
            plt.plot(x, y1, label = name_two)
            plt.plot(x, y1_deriv, label = ("Derivative of " + name_two))
            plt.legend( loc=2, prop={'size': 6})
            plt.title(name_two + " & " + "Derivative of " + name_two + " vs. " + name_one)
            plt.ylabel(name_two)

        #Graphs the original data separate and the derivatives on their own graphs
        if (regular_ontop == False and deriv_method == 1):
            plt.subplot(2, 2, (1,2))
            plt.plot(x, y1, label = name_two)
            plt.legend( loc=2, prop={'size': 6})
            plt.title(name_two + " vs. " + name_one)
            plt.ylabel(name_two)

            plt.subplot(2, 2, (3,4))
            plt.plot(x, y1_deriv, label = ("Derivative of", name_two))
            plt.legend( loc=2, prop={'size': 6})
            plt.title("Derivative of " + name_two + " vs. " + name_one)
            plt.ylabel(name_two)

        #Graphs the original data separate and the derivatives together on their own graph
        if (regular_ontop == False and deriv_method == 2):
            plt.subplot(2, 2, (1,2))
            plt.plot(x, y1, label = name_two)
            plt.legend( loc=2, prop={'size': 6})
            plt.title(name_two + " vs. " + name_one)
            plt.ylabel(name_two)

            plt.subplot(2, 2, (3,4))
            plt.plot(x, y1_deriv, label = ("Derivative of", name_two))
            plt.legend( loc=2, prop={'size': 6})
            plt.title("Derivative of " + name_two + " vs. " + name_one)
            plt.ylabel(name_two)

        #Graphs the original data separate and the derivatives on top of the original data
        if (regular_ontop == False and deriv_method == 3):
            plt.subplot(2, 2, (1,2))
            plt.plot(x, y1, label = name_two)
            plt.legend( loc=2, prop={'size': 6})
            plt.title(name_two + " vs. " + name_one)
            plt.ylabel(name_two)

            plt.subplot(2, 2, (3,4))
            plt.plot(x, y1_deriv, label = ("Derivative of", name_two))
            plt.legend( loc=2, prop={'size': 6})
            plt.title("Derivative of " + name_two + " vs. " + name_one)
            plt.ylabel(name_two)

    plt.show()

    """
    if regular_ontop == True and graph_deriv == True:
        plt.plot(x, y1, label = name_two)
        plt.plot(x, y1_deriv, label = ("Derivative of " + name_two))
        plt.xlabel(name_one)
        plt.legend()
        plt.title(name_two + " & Derivative of " + name_two + " vs. " + name_one)
        plt.legend()

    elif regular_ontop == True and graph_deriv == False:
        plt.plot(x, y1)
        plt.xlabel(name_one)
        plt.legend()
        plt.title(name_two + " vs. " + name_one)
        plt.legend()

    elif regular_ontop == False and graph_deriv == True:
        plt.subplot(2, 1, 1)
        plt.plot(x, y1)
        plt.legend( loc=2, prop={'size': 6})
        plt.title(name_two + " & Derivative of " + name_two + " vs. " + name_one)
        plt.ylabel(name_two)

        plt.subplot(2, 1, 2)
        plt.plot(x, y1_deriv, label = ("Derivative of " + name_two))
        plt.legend(loc=2, prop={'size': 6})
        plt.xlabel(name_one)
        plt.ylabel("Derivative of " + name_two)

    elif regular_ontop == False and graph_deriv == False:
        plt.plot(x, y1)
        plt.xlabel(name_one)
        plt.legend()
        plt.title(name_two + " vs. " + name_one)
        plt.legend()
    """



def create_graph_three(data, name_one, name_two, name_three):
    """
    Function to graph two types of data over another.

    :param dataframe data: this is the data from the csv file retrieved by Pandas
    :param string name_one: the name of the x-variable
    :param string name_two: the name of the y-variable
    :param string name_three: the name of the second y-variable
    """
    x = data[name_one]
    y1 = data[name_two]
    y2 = data[name_three]

    try:
        y1_deriv = data.diff(1,0)[name_two]
        y2_deriv = data.diff(1,0)[name_three]
    except TypeError:
        print("\nThe data contains is contains non-numeric values.\n\n"  \
                "Either edit the file to only contain numeric values after the header or\n" \
                "try using another file.")
        import sys
        sys.exit()

    if graph_deriv == False:
        if regular_ontop == False:
            plt.subplot(2, 1, 1)
            plt.plot(x, y1, label = name_two)
            plt.legend( loc=2, prop={'size': 6})
            plt.title(name_two + " & " + name_three + " vs. " + name_one)
            plt.ylabel(name_two)

            plt.subplot(2, 1, 2)
            plt.plot(x, y2, label = name_three)
            plt.legend(loc=2, prop={'size': 6})
            plt.xlabel(name_one)
            plt.ylabel(name_three)

        if regular_ontop == True:
            plt.plot(x, y1, label = name_two)
            plt.plot(x, y2, label = name_three)
            plt.xlabel(name_one)
            plt.legend()
            plt.title(name_two + " & " + name_three + " vs. " + name_one)
            plt.legend()

    if graph_deriv == True:
        #Graphs the original data together and the derivatives on their own graphs
        if (regular_ontop == True and deriv_method == 1):
            plt.subplot(2, 2, (1,2))
            plt.plot(x, y1, label = name_two)
            plt.plot(x, y2, label = name_two)
            plt.legend( loc=2, prop={'size': 6})
            plt.title(name_two + " " + name_three + " vs. " + name_one)

            plt.subplot(2, 2, 3)
            plt.plot(x, y1_deriv, label = ("Derivative of", name_two))
            plt.legend( loc=2, prop={'size': 6})
            plt.xlabel(name_one)

            plt.subplot(2, 2, 4)
            plt.plot(x, y2_deriv, label = ("Derivative of", name_three))
            plt.legend( loc=2, prop={'size': 6})
            plt.xlabel(name_one)

        #Graphs the original data together and the derivatives together on their own graph
        if (regular_ontop == True and deriv_method == 2):
            plt.subplot(2, 1, 1)
            plt.plot(x, y1, label = name_two)
            plt.plot(x, y2, label = name_two)
            plt.legend( loc=2, prop={'size': 6})
            plt.title(name_two + " " + name_three + " vs. " + name_one)

            plt.subplot(2, 1, 2)
            plt.plot(x, y1_deriv, label = name_two)
            plt.plot(x, y2_deriv, label = name_two)
            plt.legend( loc=2, prop={'size': 6})
            plt.xlabel(name_one)

        #Graphs the original data together and the derivatives on top of the original data
        if (regular_ontop == True and deriv_method == 3):
            plt.plot(x, y1, label = name_two)
            plt.plot(x, y2, label = name_three)
            plt.plot(x, y1_deriv, label = ("Derivative of " + name_two))
            plt.plot(x, y2_deriv, label = ("Derivative of " + name_three))
            plt.xlabel(name_one)
            plt.legend()
            plt.title(name_two + " & " + name_three + " vs. " + name_one)


        #Graphs the original data separate and the derivatives on their own graphs
        if (regular_ontop == False and deriv_method == 1):
            plt.subplot(2, 2, 1)
            plt.plot(x, y1, label = name_two)
            plt.legend( loc=2, prop={'size': 6})
            plt.title(name_two + " & " + name_three + " vs. " + name_one)
            plt.ylabel(name_two)

            plt.subplot(2, 2, 2)
            plt.plot(x, y1_deriv, label = ("Derivative of " + name_two))
            plt.legend( loc=2, prop={'size': 6})
            plt.title("Derivative of " + name_two + " & " + name_three + " vs. " + name_one)

            plt.subplot(2, 2, 3)
            plt.plot(x, y2, label = name_three)
            plt.legend(loc=2, prop={'size': 6})
            plt.xlabel(name_one)
            plt.ylabel(name_three)

            plt.subplot(2, 2, 4)
            plt.plot(x, y2_deriv, label = ("Derivative of " + name_three))
            plt.legend( loc=2, prop={'size': 6})
            plt.xlabel(name_one)

        #Graphs the original data separate and the derivatives together on their own graph
        if (regular_ontop == False and deriv_method == 2):
            plt.subplot(2, 2, 1)
            plt.plot(x, y1, label = name_two)
            plt.legend( loc=2, prop={'size': 6})
            plt.title(name_two + " vs. " + name_one)
            plt.ylabel(name_two)

            plt.subplot(2, 2, 2)
            plt.plot(x, y2, label = name_three)
            plt.legend(loc=2, prop={'size': 6})
            plt.title(name_three + " vs. " + name_one)

            plt.subplot(2, 2, (3,4))
            plt.plot(x, y1_deriv, label = ("Derivative of " + name_two))
            plt.plot(x, y2_deriv, label = ("Derivative of " + name_three))
            plt.legend( loc=2, prop={'size': 6})
            plt.xlabel(name_one)
            plt.ylabel(name_three)
            plt.title("Derivative of " + name_two + " & " + name_three + " vs. " + name_one)


        #Graphs the original data separate and the derivatives on top of the original data
        if (regular_ontop == False and deriv_method == 3):
            plt.subplot(2, 1, 1)
            plt.plot(x, y1, label = name_two)
            plt.plot(x, y1_deriv, label = ("Derivative of " + name_two))
            plt.legend( loc=2, prop={'size': 6})
            plt.title(name_two + " & " + "Derivative of " + name_two + " vs. " + name_one)

            plt.subplot(2, 1, 2)
            plt.plot(x, y2, label = name_three)
            plt.plot(x, y2_deriv, label = ("Derivative of " + name_three))
            plt.legend( loc=2, prop={'size': 6})
            plt.title(name_three + " & " + "Derivative of " + name_three + " vs. " + name_one)
            plt.xlabel(name_one)

    """
    if regular_ontop == True and graph_deriv == False:
        plt.plot(x, y1, label = name_two)
        plt.plot(x, y2, label = name_three)
        plt.xlabel(name_one)
        plt.legend()
        plt.title(name_two + " & " + name_three + " vs. " + name_one)
        plt.legend()

    elif regular_ontop == True and graph_deriv == True:
        plt.plot(x, y1, label = name_two)
        plt.plot(x, y2, label = name_three)
        plt.plot(x, y1_deriv, label = ("Derivative of " + name_two))
        plt.plot(x, y2_deriv, label = ("Derivative of " + name_three))
        plt.xlabel(name_one)
        plt.legend()
        plt.title(name_two + " & " + name_three + " vs. " + name_one)
        plt.legend()

    elif regular_ontop == False and graph_deriv == False:
        plt.subplot(2, 1, 1)
        plt.plot(x, y1, label = name_two)
        plt.legend( loc=2, prop={'size': 6})
        plt.title(name_two + " & " + name_three + " vs. " + name_one)
        plt.ylabel(name_two)

        plt.subplot(2, 1, 2)
        plt.plot(x, y2, label = name_three)
        plt.legend(loc=2, prop={'size': 6})
        plt.xlabel(name_one)
        plt.ylabel(name_three)

    elif regular_ontop == False and graph_deriv == True:
        plt.subplot(2, 2, 1)
        plt.plot(x, y1, label = name_two)
        plt.legend( loc=2, prop={'size': 6})
        plt.title(name_two + " & " + name_three + " vs. " + name_one)
        plt.ylabel(name_two)

        plt.subplot(2, 2, 2)
        plt.plot(x, y1_deriv, label = ("Derivative of " + name_two))
        plt.legend( loc=2, prop={'size': 6})
        plt.title("Derivative of " + name_two + " & " + name_three + " vs. " + name_one)

        plt.subplot(2, 2, 3)
        plt.plot(x, y2, label = name_three)
        plt.legend(loc=2, prop={'size': 6})
        plt.xlabel(name_one)
        plt.ylabel(name_three)

        plt.subplot(2, 2, 4)
        plt.plot(x, y2_deriv, label = ("Derivative of " + name_three))
        plt.legend( loc=2, prop={'size': 6})
        plt.xlabel(name_one)
    """
    plt.show()


def create_graph_four(data, name_one, name_two, name_three, name_four):
    """
    Function to graph three types of data over another.

    :param dataframe data: this is the data from the csv file retrieved by Pandas
    :param string name_one: the name of the x-variable
    :param string name_two: the name of the y-variable
    :param string name_three: the name of the second y-variable
    :param string name_four: the name of the third y-variable
    """

    x = data[name_one]
    y1 = data[name_two]
    y2 = data[name_three]
    y3 = data[name_four]

    try:
        y1_deriv = data.diff(1,0)[name_two]
        y2_deriv = data.diff(1,0)[name_three]
        y3_deriv = data.diff(1,0)[name_four]
    except TypeError:
        print("\nThe data contains is contains non-numeric values.\n\n"  \
                "Either edit the file to only contain numeric values and 'error' after the header or\n" \
                "try using another file.")
        import sys
        sys.exit()


    if graph_deriv == False:
        #Graphs the original data separate, or on their own graphs
        if regular_ontop == False:
            plt.subplot(3, 1, 1)
            plt.plot(x, y1)
            plt.legend( loc=2, prop={'size': 6})
            plt.title(name_two + " & " + name_three + " & " + name_four + " vs. " + name_one)
            plt.ylabel(name_two)

            plt.subplot(3, 1, 2)
            plt.plot(x, y2)
            plt.legend(loc=2, prop={'size': 6})
            plt.xlabel(name_one)
            plt.ylabel(name_three)

            plt.subplot(3, 1, 3)
            plt.plot(x, y3)
            plt.legend(loc=2, prop={'size': 6})
            plt.xlabel(name_one)
            plt.ylabel(name_four)
        #Graphs the original data all together
        if regular_ontop == True:
            plt.plot(x, y1)
            plt.plot(x, y2)
            plt.plot(x, y3)
            plt.xlabel(name_one)
            plt.legend()
            plt.title(name_two + " & " + name_three + " & " + name_four + " vs. " + name_one)
            plt.legend()

    if graph_deriv == True:
        #Graphs the original data together and the derivatives on their own graphs
        if (regular_ontop == True and deriv_method == 1):
            plt.subplot(2, 3, (1,2,3))
            plt.plot(x, y1, label = name_two)
            plt.plot(x, y2, label = name_two)
            plt.legend( loc=2, prop={'size': 6})
            plt.title(name_two + " " + name_three + " " + name_four + " vs. " + name_one)

            plt.subplot(2, 3, 4)
            plt.plot(x, y1_deriv, label = ("Derivative of", name_two))
            plt.legend( loc=2, prop={'size': 6})
            plt.xlabel(name_one)

            plt.subplot(2, 3, 5)
            plt.plot(x, y2_deriv, label = ("Derivative of", name_three))
            plt.legend( loc=2, prop={'size': 6})
            plt.xlabel(name_one)

            plt.subplot(2, 3, 6)
            plt.plot(x, y3_deriv, label = ("Derivative of", name_four))
            plt.legend( loc=2, prop={'size': 6})
            plt.xlabel(name_one)

        #Graphs the original data together and the derivatives together on their own graph
        if (regular_ontop == True and deriv_method == 2):
            plt.subplot(2, 3, (1,2,3))
            plt.plot(x, y1, label = name_two)
            plt.plot(x, y2, label = name_two)
            plt.legend( loc=2, prop={'size': 6})
            plt.title(name_two + " " + name_three + " " + name_four + " vs. " + name_one)

            plt.subplot(2, 3, (4,5,6))
            plt.plot(x, y1_deriv, label = ("Derivative of", name_two))
            plt.plot(x, y2_deriv, label = ("Derivative of", name_three))
            plt.plot(x, y3_deriv, label = ("Derivative of", name_four))
            plt.legend( loc=2, prop={'size': 6})
            plt.xlabel(name_one)

        #Graphs the original data together and the derivatives on top of the original data
        if (regular_ontop == True and deriv_method == 3):
            plt.plot(x, y1)
            plt.plot(x, y2)
            plt.plot(x, y3)
            plt.plot(x, y1_deriv, label = ("Derivative of " + name_two))
            plt.plot(x, y2_deriv, label = ("Derivative of " + name_three))
            plt.plot(x, y3_deriv, label = ("Derivative of " + name_four))
            plt.xlabel(name_one)
            plt.legend()
            plt.title(name_two + " & " + name_three + " & " + name_four + " vs. " + name_one)
            plt.legend()

        #Graphs the original data separate and the derivatives on their own graphs
        if (regular_ontop == False and deriv_method == 1):
            plt.subplot(3, 2, 1)
            plt.plot(x, y1)
            plt.legend( loc=2, prop={'size': 6})
            plt.title(name_two + " & " + name_three + " & " + name_four + " vs. " + name_one)
            plt.ylabel(name_two)

            plt.subplot(3, 2, 2)
            plt.plot(x, y1_deriv, label = ("Derivative of" + name_two))
            plt.legend( loc=2, prop={'size': 6})
            plt.title("Derivative of " + name_two + " & " + name_three + " & " + name_four + " vs. " + name_one)

            plt.subplot(3, 2, 3)
            plt.plot(x, y2)
            plt.legend(loc=2, prop={'size': 6})
            plt.ylabel(name_three)

            plt.subplot(3, 2, 4)
            plt.plot(x, y2_deriv, label = ("Derivative of " + name_three))
            plt.legend(loc=2, prop={'size': 6})

            plt.subplot(3, 2, 5)
            plt.plot(x, y3)
            plt.legend(loc=2, prop={'size': 6})
            plt.xlabel(name_one)
            plt.ylabel(name_four)

            plt.subplot(3, 2, 6)
            plt.plot(x, y3_deriv, label = ("Derivative of " + name_four))
            plt.legend(loc=2, prop={'size': 6})
            plt.xlabel(name_one)

        #Graphs the original data separate and the derivatives together on their own graph
        if (regular_ontop == False and deriv_method == 2):
            plt.subplot(2, 3, 1)
            plt.plot(x, y1, label = name_two)
            plt.ylabel(name_two)
            plt.legend(loc=2, prop={'size': 6})
            plt.title(name_two + " vs. " + name_one)

            plt.subplot(2, 3, 2)
            plt.plot(x, y2, label = name_three)
            plt.ylabel(name_three)
            plt.legend(loc=2, prop={'size': 6})
            plt.title(name_three + " vs. " + name_one)

            plt.subplot(2, 3, 3)
            plt.plot(x, y3, label = name_four)
            plt.ylabel(name_four)
            plt.legend(loc=2, prop={'size': 6})
            plt.title(name_four + " vs. " + name_one)

            plt.subplot(2, 3, (4,5,6))
            plt.plot(x, y1_deriv, label = ("Derivative of " + name_two))
            plt.plot(x, y2_deriv, label = ("Derivative of " + name_three))
            plt.plot(x, y3_deriv, label = ("Derivative of " + name_four))
            plt.xlabel(name_one)
            plt.legend(loc=2, prop={'size': 6})


        #Graphs the original data separate and the derivatives on top of the original data
        if (regular_ontop == False and deriv_method == 3):
            plt.subplot(3, 1, 1)
            plt.plot(x, y1, label = name_two)
            plt.plot(x, y1_deriv, label = ("Derivative of " + name_two))
            plt.legend( loc=2, prop={'size': 6})
            plt.title(name_two + " & " + "Derivative of " + name_two + " vs. " + name_one)
            plt.ylabel(name_two + " & " + "Derivative of " + name_two)

            plt.subplot(3, 1, 2)
            plt.plot(x, y2, label = name_three)
            plt.plot(x, y2_deriv, label = ("Derivative of " + name_three))
            plt.legend( loc=2, prop={'size': 6})
            plt.ylabel(name_three + " & " + "Derivative of " + name_three)

            plt.subplot(3, 1, 3)
            plt.plot(x, y3, label = name_four)
            plt.plot(x, y3_deriv, label = ("Derivative of " + name_four))
            plt.legend( loc=2, prop={'size': 6})
            plt.xlabel(name_one)
            plt.ylabel(name_four + " & " + "Derivative of " + name_four)


    """
    if regular_ontop == True and graph_deriv == False:
        plt.plot(x, y1)
        plt.plot(x, y2)
        plt.plot(x, y3)
        plt.xlabel(name_one)
        plt.legend()
        plt.title(name_two + " & " + name_three + " & " + name_four + " vs. " + name_one)
        plt.legend()

    elif regular_ontop == True and graph_deriv == True:
        plt.plot(x, y1)
        plt.plot(x, y2)
        plt.plot(x, y3)
        plt.plot(x, y1_deriv, label = ("Derivative of " + name_two))
        plt.plot(x, y2_deriv, label = ("Derivative of " + name_three))
        plt.plot(x, y3_deriv, label = ("Derivative of " + name_four))
        plt.xlabel(name_one)
        plt.legend()
        plt.title(name_two + " & " + name_three + " & " + name_four + " vs. " + name_one)
        plt.legend()

    elif regular_ontop == False and graph_deriv == False:
        plt.subplot(3, 1, 1)
        plt.plot(x, y1)
        plt.legend( loc=2, prop={'size': 6})
        plt.title(name_two + " & " + name_three + " & " + name_four + " vs. " + name_one)
        plt.ylabel(name_two)

        plt.subplot(3, 1, 2)
        plt.plot(x, y2)
        plt.legend(loc=2, prop={'size': 6})
        plt.xlabel(name_one)
        plt.ylabel(name_three)

        plt.subplot(3, 1, 3)
        plt.plot(x, y3)
        plt.legend(loc=2, prop={'size': 6})
        plt.xlabel(name_one)
        plt.ylabel(name_four)

    elif regular_ontop == False and graph_deriv == True:
        plt.subplot(3, 2, 1)
        plt.plot(x, y1)
        plt.legend( loc=2, prop={'size': 6})
        plt.title(name_two + " & " + name_three + " & " + name_four + " vs. " + name_one)
        plt.ylabel(name_two)

        plt.subplot(3, 2, 2)
        plt.plot(x, y1_deriv, label = ("Derivative of" + name_two))
        plt.legend( loc=2, prop={'size': 6})
        plt.title("Derivative of " + name_two + " & " + name_three + " & " + name_four + " vs. " + name_one)

        plt.subplot(3, 2, 3)
        plt.plot(x, y2)
        plt.legend(loc=2, prop={'size': 6})
        plt.ylabel(name_three)

        plt.subplot(3, 2, 4)
        plt.plot(x, y2_deriv, label = ("Derivative of " + name_three))
        plt.legend(loc=2, prop={'size': 6})

        plt.subplot(3, 2, 5)
        plt.plot(x, y3)
        plt.legend(loc=2, prop={'size': 6})
        plt.xlabel(name_one)
        plt.ylabel(name_four)

        plt.subplot(3, 2, 6)
        plt.plot(x, y3_deriv, label = ("Derivative of " + name_four))
        plt.legend(loc=2, prop={'size': 6})
        plt.xlabel(name_one)
    """
    plt.show()

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import pandas as pandas


    regular_ontop = regular_graphing_method()         #Determines if the user wants data on top of each other

    graph_deriv = graph_derivatives()           #Determines if user wants derivatives with graphs

    if graph_deriv == True:                     #If the user wants to graph derivatives, this determines how
        deriv_method = deriv_graphing_method()

    path, file_name = get_file_name()           #Gets the name of the file to be used and creates the path

    datatypes, file_name = get_available_datatypes(path, file_name)   #Prints and gets the available types of data for graphing

    velocity_histogram = get_velocity_intervals()                       #Determines if user wants velocity histograms

    num_of_graphs(datatypes)
