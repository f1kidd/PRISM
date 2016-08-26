# path = "C:/Users/f1kidd/OneDrive/prism/2014"

def prec_call(filedir,date_list=None):
    # here filedir is ../prism/year
    import numpy as np
    from numpy import ma
    import glob,os, zipfile, shutil
    from datetime import timedelta, date

    filedir = filedir + "/"
    updir = filedir[:-5]+'prec/'
    if not os.path.exists(updir):
        os.mkdir(updir)
    path_prec= filedir + "ppt/"
    prec_list = glob.glob1(path_prec,'*.bil')



    date_list_prec = []
    for file in prec_list:
        date_list_prec.append(file[-16: -8])

    if(date_list == None):
        date_list = date_list_prec

    prec_perm = np.array([])

    d = 1
    for date in date_list:
        prec_file = glob.glob1(path_prec,'*'+date+'_bil.bil')[0]

        temp_prec = open(path_prec+prec_file,"rb")
        prec_data = np.fromfile(temp_prec,'f')
        prec_mask = ma.masked_equal(prec_data,-9999.0)
        temp_prec.close()

        if(len(prec_perm)==0):
            prec_perm = prec_mask
        else:
            prec_perm = prec_perm + prec_mask

        print str(d),'out of',str(len(date_list)),'days calculated.'
        d+=1


    prec_perm = np.where(prec_mask.mask,-9999.0,prec_perm)

    outfile = 'prec' + str(date)[0:4]
    fout = open(updir + outfile + ".bil","wb")
    prec_perm.tofile(fout)
    fout.close()

    file_pattern = prec_file.split('.')[0]
    # print file_pattern
    for file_copy in glob.glob1(path_prec,file_pattern+'.*'):
        extension = '.'.join(file_copy.split('.')[1:])
        if extension != 'bil':
            shutil.copy(path_prec+file_copy,updir)
            if os.path.exists(updir+outfile+'.'+extension):
                os.remove(updir+outfile+'.'+extension)
            os.rename(updir+file_copy,updir+outfile+'.'+extension)

    # delete
    for root, dirs, files in os.walk(path_prec):
        for f in files:
    	    os.unlink(os.path.join(root, f))
        for d in dirs:
    	    shutil.rmtree(os.path.join(root, d))

    print "Cumulated Precipitation calculation routine completed. Panpan out."
    return True


# a = prec_call(path)











