# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 09:12:05 2018

@author: 10540
"""

import lifetimes as lt
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

from lifetimes.utils import summary_data_from_transaction_data

from lifetimes import BetaGeoFitter

# Read transaction data and select only the Billed data

tran_df=pd.read_csv('C:/Projects/Hasbro/sample1.csv')

tran_df['bill_date_new']= pd.to_datetime(tran_df['bill_date']).dt.date

tran_df.head()

cols=['customer_id','bill_date_new','Productname']

tran_pa_all = tran_df[cols]
#tran_df['bill_date_new']= pd.to_datetime(tran_df['bill_date']).dt.date

summary = summary_data_from_transaction_data(tran_pa_all, 'customer_id', 'bill_date_new', observation_period_end='2017-12-31')
plt.figure(1)
plt.subplot(211)
#plt.axis(0,50,0,60000)
plt.title('Histogram of frequency')
plt.hist(summary['frequency'])


plt.figure(2)
plt.subplot(212)
plt.title('Histogram of recency')
plt.hist(summary['recency'])

summary.describe(include='all')
print(summary.head)

#fit model

bgf = BetaGeoFitter(penalizer_coef=0.0)
bgf.fit(summary['frequency'], summary['recency'], summary['T'])
print(bgf)
# <lifetimes.BetaGeoFitter: fitted with 5000 customers, a: 1.85, alpha: 1.86, r: 0.16, b: 3.18>

# heat map for FR and live customers
from lifetimes.plotting import plot_frequency_recency_matrix

plot_frequency_recency_matrix(bgf)

from lifetimes.plotting import plot_probability_alive_matrix

plot_probability_alive_matrix(bgf)


#validation of model

from lifetimes.utils import calibration_and_holdout_data

summary_cal_holdout = calibration_and_holdout_data(tran_pa_all, 'customer_id', 'bill_date_new', 
                                        calibration_period_end='2017-09-01',
                                        observation_period_end='2017-12-31' )   
print(summary_cal_holdout.head())

from lifetimes.plotting import plot_calibration_purchases_vs_holdout_purchases

bgf.fit(summary_cal_holdout['frequency_cal'], summary_cal_holdout['recency_cal'], summary_cal_holdout['T_cal'])
plot_calibration_purchases_vs_holdout_purchases(bgf, summary_cal_holdout)

#t = 10 #predict purchases in 10 periods
#individual = summary.iloc[20]
# The below function may be renamed to `predict` in a future version of lifetimes
#bgf.conditional_expected_number_of_purchases_up_to_time(t, individual['frequency'], individual['recency'], individual['T'])

t = 31*2
summary['predicted_purchases'] = bgf.conditional_expected_number_of_purchases_up_to_time(t, summary['frequency'], summary['recency'], summary['T'])
summary.sort_values(by='predicted_purchases').tail(10)