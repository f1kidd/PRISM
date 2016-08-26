
def prism(filedir,datelist,var):
########################
# function prism: downloads and unzips prism data from server.
# variables description:
# Filedir: a string file directory to store the data. use ../prism
# date: The date to be processed. Formatted as yyyy/mm/dd, string format.
# var can be one of (ppt, tmax, tmin, tmean, tdmean, vpdmin, vpdmax, vpr). String format.
# see http://prism.oregonstate.edu/documents/PRISM_datasets.pdf for detailed data type description.
    import numpy as np
    from numpy import ma
    import glob,os, zipfile, shutil
    from datetime import timedelta, date

    filedir += '/'
    for datestr in datelist:
        # change to output directory with os.chdir(....
        os.chdir(filedir)
        print("\n\nGetting " + var + " data for " + datestr + "\n\n")

        # separate the date into day, month, year and assign to variables
        year, month, day = datestr.split('/')

        # set the prism file code for var (prism files use a differnt code in the name by types
        if var == 'ppt':
            dval = 'D2'
        else:
            dval = 'D1'

        # create a new folder with the year in output folder
        # set the name
        year_folder = filedir + year + "/"

        # if it does not already exist, make a new one
        if os.path.exists(year_folder) == False:
            os.mkdir(year_folder)

        # change to the directory whether just created or not
        os.chdir(year_folder)
        # create a new directory inside the year directory (if needed) for the variable to be downloaded
        # set the name
        var_folder = year_folder + var + "/"

        # if it does not already exist, make a new one
        if os.path.exists(var_folder) == False:
            os.mkdir(var_folder)

        # change to the directory whether just created or not
        outdir = var_folder
        os.chdir(outdir)

        # make a string (day) to match the format of the download file for the day to retrieve
        # based on the dcumentation from prism (year, 2 character month, 2 character day)
        # date = year+month+day
        date = str(year) + "{0:02d}".format(int(month)) + "{0:02d}".format(int(day))

        # create the rest of the prism file name format (http location + variable + the day to retrieve as getfile
        getfile = 'http://services.nacse.org/prism/data/public/4km/' + var + "/" + date
        # check if the file has been downloaded previously and skip if so (use variable 'name')
        name = date
        if name in os.listdir('.'):
            print("File " + name + " already exists.  Download is skipped")

            # notify that the file will be downloaded
        else:
            print("\n\nRetrieving " + getfile)

            # use wget to download the file with os.system
            os.system("wget " + getfile)
            print(outdir + name)
            # unzip the zip files
            zfile = zipfile.ZipFile(outdir + name)
            zfile.extractall()

        # make the possible bil file names - 3 are possible - check for which one exists (stable, provisional, or early)
        bilfile1 = 'PRISM_' + var + '_early_4km' + dval + '_' + date + '_bil.bil'
        bilfile2 = 'PRISM_' + var + '_stable_4km' + dval + '_' + date + '_bil.bil'
        bilfile3 = 'PRISM_' + var + '_provisional_4km' + dval + '_' + date + '_bil.bil'

        if os.path.exists(bilfile1):
            bilfile = bilfile1
        elif os.path.exists(bilfile2):
            bilfile = bilfile2
        else:
            bilfile = bilfile3

        bilpath = outdir + bilfile

        print "File", bilfile, "processed, Panda yeah!!"

        # report that you are loading the map into the current map view (when we get this into arcGIS) - does not work in external
        # scripts - but you can manually add the layer to see that it was downlaoded correctly.
        # arcpy.AddMessage("\n\nLoading new file " + bilpath + " to the map\n\n")


        # get the map document - arcpy.mapping module (we will open this part up later)
        # mxd = arcpy.mapping.MapDocument("CURRENT")

        # get the data frame
        # df = ma.ListDataFrames(mxd,"*")[0]

        # arcpy.AddMessage(bilpath)
        # create a new layer
        # newlayer = ma.Layer(bilpath)

        # add the layer to the map in data frame 0
        # ma.AddLayer(df, newlayer,"AUTO_ARRANGE")
    print str(len(datelist)),"file downloaded and processed. Panda Out."



def datelist(start_date,end_date,form="%Y/%m/%d"):
    # inputs two python (date)
    from datetime import timedelta, date
    result=[]
    def daterange(start_date, end_date):
        for n in range(int ((end_date - start_date).days)):
            yield start_date + timedelta(n)
    for single_date in daterange(start_date, end_date):
        result.append(single_date.strftime(form))
    return result


# prism(path,date_range,"tmin")

