###
#
# used to import any of the robot failure datasets
#
#  ******EXAMPLE******
# import DataImport as dataImport
#
# data = dataImport.getDataInstances("lp4.data")
#
# print "*****\nDATA\n*****"
# for datum in data:
#     print "\nFailure type %d" % datum.intFailureType
#     print "Force x-component:"
#     print datum.FxVector
#     print "Force y-component:"
#     print datum.FyVector
#     print "Force z-component:"
#     print datum.FzVector
#     print "Torque x-component:"
#     print datum.TxVector
#     print "Torque y-component:"
#     print datum.TyVector
#     print "Torque z-component:"
#     print datum.TzVector
###


## class for a datum in the dataset
class DataInstance:

    def __init__(self, intFailureType, fx, fy, fz, tx, ty, tz):

        ## Failure type int codes:
        ## lp1 - {0: normal,
        ##        1: collision,
        ##        2: obstruction,
        ##        3: front collision}
        ##
        ## lp2 - {0: normal,
        ##        1: front collision,
        ##        2: back collision,
        ##        3: collision to right,
        ##        4: collision to left}
        ##
        ## lp3 - {0: ok,
        ##        1: slightly moved,
        ##        2: moved,
        ##        3: lost}
        ##
        ## lp4 - {0: normal,
        ##        1: collision,
        ##        2: obstruction}
        ##
        ## lp5 - {0: normal,
        ##        1: bottom collision,
        ##        2: bottom obstruction,
        ##        3: collision in part,
        ##        4: collision in tool}
        self.intFailureType = intFailureType

        # each is a list of 15 integers
        self.FxVector = fx
        self.FyVector = fy
        self.FzVector = fz
        self.TxVector = tx
        self.TyVector = ty
        self.TzVector = tz




#
# strDataset is the name of any file in the data directory
#
def getDataInstances(strDataset):

    #list that will contain all data instances
    dataInstances = []

    #get raw data in file
    with open("data/" + strDataset, "r") as dataFile:
        #raw data in string - replace new line with white space
        strDataset = dataFile.read().replace("\n", " ")


    # put every text segment separated by white space as an
    # element in a list
    datasetList = strDataset.split()


    intFailureType = -1 #type of failure

    ## vectors of force and torque components
    fx = []
    fy = []
    fz = []
    tx = []
    ty = []
    tz = []

    countHelper = 0 ## used to track which force value we are on

    ## go through each text segment in dataset
    for n in range(len(datasetList)):

        # check if this is a failure title
        if ((n % 91) == 0):

            # get failure type
            if (datasetList[n] == "normal" or
                        datasetList[n] == "ok"):
                intFailureType = 0

            elif (datasetList[n] == "collision" or
                        datasetList[n] == "front_col" or
                        datasetList[n] == "slightly_moved" or
                        datasetList[n] == "bottom_collision"):
                intFailureType = 1

            elif (datasetList[n] == "obstruction" or
                        datasetList[n] == "back_col" or
                        datasetList[n] == "moved" or
                        datasetList[n] == "bottom_obstruction"):
                intFailureType = 2

            elif (datasetList[n] == "fr_collision" or
                        datasetList[n] == "right_col" or
                        datasetList[n] == "lost" or
                        datasetList[n] == "collision_in_part"):
                intFailureType = 3

            elif (datasetList[n] == "collision_in_tool" or
                        datasetList[n] == "left_col"):
                intFailureType = 4


        # otherwise this is a force or torque value
        else:

            if ((countHelper % 6) == 0):
                fx.append(int(datasetList[n]))
            elif ((countHelper % 6) == 1):
                fy.append(int(datasetList[n]))
            elif ((countHelper % 6) == 2):
                fz.append(int(datasetList[n]))
            elif ((countHelper % 6) == 3):
                tx.append(int(datasetList[n]))
            elif ((countHelper % 6) == 4):
                ty.append(int(datasetList[n]))
            elif ((countHelper % 6) == 5):
                tz.append(int(datasetList[n]))

            ## increment
            countHelper = countHelper + 1

        # check if complete with this datum
        if (n%91 == 90):

            ## add to list of all data instances
            dataInstances.\
                append(DataInstance(intFailureType, fx, fy, fx, tx, ty, tz))

            # clear old lists
            fx = []
            fy = []
            fz = []
            tx = []
            ty = []
            tz = []


    # return all dataset elements
    return dataInstances



