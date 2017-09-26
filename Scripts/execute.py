# This is the wrapping up script for the whole set of tools in this pack. If you wish to download prism daily data, please call funtion prism().
# gdd_exec executes growing degree days accumulation, where user can specify multiple years, starting month (from the first day), ending month (till the last day),
# and the upper and lower temperature threshold.
# prec_exec

import numpy as np
from numpy import ma
import glob,os, zipfile, shutil
from datetime import timedelta, date

from Prism2 import prism,datelist
from gdd import gdd_call
from precip import prec_call
from extreme import extreme_call

path = "C:/Users/f1kidd/OneDrive/prism"
# path = "/Users/xindeji/OneDrive/prism"

start_month,end_month,start_year,end_year = 4,9,2014,2014

def gdd_exec(path,start_year,end_year,start_month=4,end_month=9,tmin=8,tmax=32,date_range_gdd=None):

    for year in range(start_year,end_year+1):
        start_date = date(year, start_month, 1)
        end_date = date(year, end_month + 1, 1)
        date_range = datelist(start_date, end_date)

        year_path = path + '/' + str(year)
        prism(path, date_range, 'tmax')
        prism(path, date_range, 'tmin')
        gdd_call(year_path,date_range_gdd,tmin,tmax)

# gdd_exec(path,start_year,end_year)


def prec_exec(path,start_year,end_year,start_month=6,end_month=9,date_range_prec=None):

    for year in range(start_year,end_year+1):
        start_date = date(year, start_month, 1)
        end_date = date(year, end_month + 1, 1)
        date_range = datelist(start_date, end_date)

        year_path = path + '/' + str(year)
        prism(path, date_range, 'ppt')
        prec_call(year_path,date_range_prec)

# prec_exec(path,start_year,end_year)


def extreme_exec(path,start_year,end_year,start_month=4,end_month=9,theat=30,date_range_exm=None,outdir=None):

    for year in range(start_year,end_year+1):
        start_date = date(year, start_month, 1)
        end_date = date(year, end_month + 1, 1)
        date_range = datelist(start_date, end_date)

        year_path = path + '/' + str(year)
        prism(path, date_range, 'tmax')
        prism(path, date_range, 'tmin')
        if(outdir is None):
            extreme_call(year_path,date_range_exm,theat)
        else:
            extreme_call(year_path, date_range_exm, theat,outdir=outdir)
extreme_exec(path,start_year,end_year,outdir="extreme30")