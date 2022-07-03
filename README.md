![GeophyiscalLog_3401572533400000_CO2_Well](https://user-images.githubusercontent.com/54684336/177037061-23d886ad-bb24-4abb-a3a3-be6eb3c6ee8d.png)

# LAS Curve Indexing
This python script will read multiple files in a directory, read the curve information in each file, and then create an index of the top and bottom depths for all the curves in each file. The indexed curve information is then written to a CSV file that can be imported to a database table.

The Ohio Geological Survey is the archive for all geophysical well logs in Ohio. Almost the geophysical logs are available to public for download through the ODNR Oil and Gas Well Interactive Map (https://gis.ohiodnr.gov/MapViewer/?config=OilGasWells)

In order to release the LAS files to the public, they must be indexed into a SQL-Server database table. Hence, the reason why is python script is needed.

I am using this project to teach myself Python. I know there are many other LAS projects available on github that I can reference, but this is an effective way for me to learn Python.

Currently, the code is not optizmized as object oriented. That will be the next major iteration of the project.
