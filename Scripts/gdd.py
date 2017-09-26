# path = "C:/Users/f1kidd/OneDrive/prism/2014"

def gdd_call(filedir,date_list=None,tmin=8,tmax=32,outname='gdd'):
    # here filedir is ../prism/year
    import numpy as np
    from numpy import ma
    import glob,os, zipfile, shutil
    from datetime import timedelta, date

    filedir = filedir + "/"
    updir = filedir[:-5]+'gdd/'
    if not os.path.exists(updir):
        os.mkdir(updir)
    path_max= filedir + "tmax/"
    path_min=filedir + "tmin/"
    max_list = glob.glob1(path_max,'*.bil')
    min_list = glob.glob1(path_min,'*.bil')

# checks if both tmin and tmax have the same files to work with
    date_list_max, date_list_min = [], []
    for file in max_list:
        date_list_max.append(file[-16: -8])
    for file in min_list:
        date_list_min.append(file[-16: -8])

    if(date_list == None): # use all available files.
        if date_list_max == date_list_min:
            date_list = date_list_max
            del date_list_max, date_list_min
        else:
            print "Date list not checked out. Abort program."
            return False
    else:
        if set(date_list).intersection(date_list_max) == set(date_list).intersection(date_list_min):
            date_list = list(set(date_list).intersection(date_list_max))
            del date_list_max, date_list_min
        else:
            print "Date list not checked out. Abort program."
            return False

    gdd_perm = np.array([])
# GDD calculation methods
    def gdd_method1(min_list,max_list,tmin,tmax):
        step1 = np.where((max_list+min_list)/2 >tmax,tmax-tmin,(max_list+min_list)/2-tmin)
        step2 = np.where(step1 <0,0.0,step1)
        return step2

    d = 1
    for date in date_list:
        max_file = glob.glob1(path_max,'*'+date+'_bil.bil')[0]
        min_file = glob.glob1(path_min,'*'+date+'_bil.bil')[0]

        temp_max = open(path_max+max_file,"rb")
        max_data = np.fromfile(temp_max,'f')
        max_mask = ma.masked_equal(max_data,-9999.0)
        temp_max.close()

        temp_min = open(path_min+min_file,"rb")
        min_data = np.fromfile(temp_min,'f')
        min_mask = ma.masked_equal(min_data,-9999.0)
        temp_min.close()

        temp_gdd = gdd_method1(min_mask,max_mask,tmin,tmax)
        if(len(gdd_perm)==0):
            gdd_perm = temp_gdd
        else:
            gdd_perm = gdd_perm + temp_gdd

        print str(d),'out of',str(len(date_list)),'days calculated.'
        d+=1

    # gdd_perm.mask = ma.nomask
    gdd_perm = np.where(max_mask.mask,-9999.0,gdd_perm)

    outfile = outname + str(date)[0:4]
    fout = open(updir + outfile + ".bil","wb")
    gdd_perm.tofile(fout)
    fout.close()

    file_pattern = max_file.split('.')[0]
    # print file_pattern
    for file_copy in glob.glob1(path_max,file_pattern+'.*'):
        extension = '.'.join(file_copy.split('.')[1:])
        if extension != 'bil':
            shutil.copy(path_max+file_copy,updir)
            if os.path.exists(updir+outfile+'.'+extension):
                os.remove(updir+outfile+'.'+extension)
            os.rename(updir+file_copy,updir+outfile+'.'+extension)

    print "GDD calculation routine completed. Panpan out."
    return True


# a = gdd_call(path)











