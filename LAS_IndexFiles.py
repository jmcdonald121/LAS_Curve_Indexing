#-------------------------------------------------------------------------------
# Name: LAS File Curve Indexing
# Version: 0.9
# Start Date: 11/29/2021
# Version Date: 5/25/2022
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

import re #Library used for pattern matching, i.e. wildcards
import os

#This code will be used to index files in a folder
##os.listdir("C:\\Users\\James Mcdonald\\OneDrive\\Documents\\Python Scripts\\lasio-master\\lasio-master\\tests\\examples")
##testdir=os.listdir("C:\\Users\\10001810\\OneDrive - State of Ohio\\Documents\\Projects\\Python Scripts")
##print (testdir)

##flas = open("C:\\Users\\10001810\\OneDrive - State of Ohio\\Documents\\Projects\\Python Scripts\\lasio-master\\lasio-master\\tests\\examples\\6038187_v1.2.las", 'rt')
flas = open("C:\\Users\\10001810\\OneDrive - State of Ohio\\Documents\\Projects\\Python Scripts\\34169255870000.las", 'rt')

try:
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
                        print(nullstring1)
                        nullstring2 = nullstring1.split(":")
                        print(nullstring2)
##                        nullvalue=float(nullstring2[0])
                        nullvalue = float('-999.25')
                        print(nullvalue)
                    if wellparameter[0] == 'API':
                        apistring1 = wellparameter[1].strip().strip(" ")
                        apistring2 = apistring1.split(":")
                        apinumber = apistring2[0].strip().strip(" ")
##                        print(apinumber)

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

        #Get the curve values with depth
        if line[0] + line[1] == '~A': #ASCII Log Values block
            numberofcurves = len(curvelist) #Get the number of curves in the LAS file
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
##    print(curvelist)
##    print(curvestart)
##    print(curveend)
    print(csvrecord)
except Exception as other:
    print("Something Broke", other)
flas.close




