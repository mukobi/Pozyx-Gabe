

def write_to_file(single_line_output, filename):
    """
    Creating a new file to save data easily

    :param string single_line_output: the output to be printed to file
    :param string filename: the input for name of the text file

    If the input is blank, returns default_position_test as filename

    Put in main to get name of file,
    filename = input("Please enter a filename: ")
    filename = filename + ".txt"
    Put in while iterate_file to write data to file,
    write_to_file(singleLineOutput, filename)
    """
    if filename == "":
        filename = "default_position_test.csv"
    with open(filename, "a") as f:
        f.write (single_line_output + '\n')

def read_ranging(filename='',directory=''):
    '''Read in data from ready_to_range.py'''

    from astropy.io import ascii
    import numpy as np


    if directory=='':
        directory='/Users/CoraJune/Desktop/pozyx_testing/'
    if filename=='':
        filename='110precision.txt'

    data=ascii.read(directory+filename,data_start=3)

    time=np.array(data['col1'][:-2])
    distance=np.array(data['col2'][:-2])
    power=np.array(data['col3'][:-3])

    for ii in range(len(time)):
        time[ii]=float(time[ii][:-2])
    for ii in range(len(distance)):
        distance[ii]=float(distance[ii][:-2])
    for ii in range(len(power)):
        power[ii]=float(power[ii][:-3])


    time = time.astype(np.float)
    distance = distance.astype(np.float)
    power = power.astype(np.float)

    return time,distance,power


def zero_time(time):

    import numpy as np

    time_out=np.zeros_like(time)

    #import pdb;pdb.set_trace()

    for ii in range(len(time)):

        time_out[ii]=time[ii]-time[0]


    return time_out


def array_diff(array):

    import numpy as np


    darray=np.zeros_like(array[0:-1])

    for ii in range(len(array)-1):

        darray[ii] = array[ii+1]-array[ii]

    return darray


def array_stats(array,start=0,end=-1):
    '''stats for array'''

    import numpy as np

    # Average change in element value (dx = xi - xi-1)

    print('Mean')
    print(np.mean(array[start:end]))
    print('Median')
    print(np.median(array[start:end]))
    print('Standard Deviation')
    print(np.std(array[start:end]))






if __name__=='__main__':

    t,x,db=read_ranging()

    print(t)
    print(x)
