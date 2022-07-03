#-------------------------------------------------------------------------------
# Name: LAS File Curve Indexing
# Version: 0.9
# Start Date: 11/29/2021
# Version Date: 7/1/2022
# Abstract: This is a Python script that will go through a LAS file and create
# an index of all the curves and the footages for those curves. The data is
# then written to a CSV file. The CSV file can then be imported into MS
# SQL-Server database table.
#
#-------------------------------------------------------------------------------
# James McDonald
# Geology Program Supervisor
# Ohio Department of Natural Resources, Division of Geological Survey
# 2045 Morse Road
# Columbus, OH  43229-6693
# ph. (614) 265-6626
# email: james.mcdonald@dnr.ohio.gov
#-------------------------------------------------------------------------------

import os

try:
    #This code will be used to index files in a folder
    lasfiles=os.listdir("C:\\Users\\10001810\\OneDrive - State of Ohio\\Documents\\LASFiles_FY2023")
    findex = open("C:\\Users\\10001810\\OneDrive - State of Ohio\\Documents\\LASFiles_FY2023\\LASIndex.txt", 'wt')

    for lasfile in lasfiles:
        lasfullname=os.path.abspath(lasfile)
        if lasfullname[-3:] == "las" or lasfullname[-3:] == "LAS":
            flas = open(lasfullname,'rt')
            while True:
                line=flas.readline()
                if not line:
                    break
                
                #Get the API number
                if line[0] + line[1] == '~W': #Well Header block
                    while True:
                        line = flas.readline()
                        sline = line.strip().strip("\n") #Strips out the \n, i.e. newline character
                        if not line: #If at the end of the file, break out of the While loop
                            break
                        elif sline[0] == '~': #If entering a new parameter block, break out of the While loop
                            break
                        elif sline[0] == '#' or sline[0] == '': #If the new line is a comment or a blank line, read the next line
                            continue
                        else:
                            wellparameters = sline
                            wellparameter = wellparameters.split(".")
                            wellparameter[0] = wellparameter[0].strip().strip(" ") #Remove white spaces in the list
                            if wellparameter[0] == 'NULL':
                                nullstring1 = wellparameter[1].strip().strip(" ") #Remove white spaces in the list

                                nullstring2 = nullstring1.split(":")

                                nullvalue = float('-999.25')

                            if wellparameter[0] == 'API':
                                apistring1 = wellparameter[1].strip().strip(" ")
                                apistring2 = apistring1.split(":")
                                apinumber = apistring2[0].strip().strip(" ")
##                                print(apinumber)


                #Get the list of the curves
                if line[0] + line[1] == '~C': #Curve Information block
                    curvelist=[]
                    while True:
                        line = flas.readline()
                        sline = line.strip().strip("\n") #Strips out the \n, i.e. newline character
                        if not line: #If at the end of the file, break out of the While loop
                            break
                        elif sline[0] == '~': #If entering a new parameter block, break out of the While loop
                            break
                        elif sline[0] =='#' or sline[0] == '': #If the new line is a comment, read the next line
                            continue
                        else:
                            curves = sline
                            curve = curves.split(".") #Split the string into a list, based upon the '.'
                            curve[0] = curve[0].strip().strip(" ") #Remove white spaces in the list
                            curvelist.append(curve[0])

##                    print(curvelist)
                            
                #Get the curve values with depth
                if line[0] + line[1] == '~A': #ASCII Log Values block
                    numberofcurves = len(curvelist) #Get the number of curves in the LAS file
                    print("Number of Curves = " + str(numberofcurves))
                    curvestart = []
                    curveend = []
                    i=0
                    while i <= len(curvelist)-1:
                        curvestart.append(nullvalue)
                        curveend.append(nullvalue)
                        i += 1
                    while True:
                        line = flas.readline()
                        if not line: #If at the end of the file, break out of the While loop
                            break
                        sline = line.strip().strip("\n") #Strips out the \n, i.e. newline character
                        curvevalues = sline
                        curvevalue = curvevalues.split(" ")
##                        print(curvevalues)
##                        print(curvevalue)

                        if curvevalues[0] != '~':
                            newcurve = [] #Create new list to remove the blank spaces from the curvevalue list
                            for curve in curvevalue:
                                if curve != '':
                                    newcurve.append(float(curve))
                            n=0
                            while n <= numberofcurves-1:
                                if newcurve[0] == nullvalue:
                                    break
                                if newcurve[n] != nullvalue and curvestart[n]==nullvalue:
                                    curvestart[n] = newcurve[0]
                                if newcurve[n] != nullvalue:
                                    curveend[n] = newcurve[0]
                                n+=1
                        if curvevalues[0] == '~':
                            break #Breaks out of the inner loop

            #Start creating CSV record for the LAS file
            curveindex=''
            n=1
            while n <= numberofcurves-1:
                curveindex = curveindex + curvelist[n] + '(' + str(curvestart[n]) + '-' + str(curveend[n]) + ')'
                if n < numberofcurves-1:
                    curveindex = curveindex + '|'
                n += 1
            filename = flas.name.split('\\')
            csvrecord = apinumber + ',' + curveindex + ',' + filename[-1]
            print(csvrecord)
            try:
                print(csvrecord, file=findex)
            except Exception as csvwriteissue:
                print("Some issue with the CSV writting", csvwriteissue)
            flas.close()
        else:
            continue
    findex.close()
except Exception as other:
    print("Something Broke", other)




