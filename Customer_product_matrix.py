# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 16:30:31 2018

@author: 10540
"""

import pandas as pd
import numpy as np
import mlxtend as mlx
import lifetimes as lt
import pymysql


# Read transaction data and select only the Billed data

tran_df=pd.read_csv('C:/Projects/Hasbro/sample1.csv')

tran_df.head()

#split years of transaction - 2016 & 2017
import datetime

tran_df['year']=pd.DatetimeIndex(tran_df['bill_date']).year
tran_df['Qty']=1
tran_df['Productname'] = tran_df['Productname'].str.strip()

#tran_2016=tran_df.loc[tran_df['year']==2016]


cols=['customer_id','bill_date','Productname','Qty']

tran_pa_all = tran_df[cols]
tran_pa_all['bill_date_new']= pd.to_datetime(tran_pa_all['bill_date']).dt.date

#sort dataframe by date

tran_pa_all.sort_values(by=['bill_date_new'],inplace=True)
#pivoting for transaction data formating

mba_all=pd.pivot_table(tran_pa_all,index=['customer_id'],values=['Qty'],
                        columns=['Productname'],aggfunc=np.sum)
mba_all_flat=pd.DataFrame(mba_all.to_records()).fillna(0)

mba_all_flat.columns = [hdr.replace("('Qty', ", "").replace(")", "").replace("'","") \
                     for hdr in mba_all_flat.columns]

#write output to csv

mba_all_flat.to_csv("C:\Projects\Hasbro/Customer_product_matrix.csv",index=False)
#drop date column

#mba_2016_flat.drop('bill_date_new',inplace=True)
mba_all_flat.reset_index()
mba_all_flat.drop('customer_id',inplace=True,axis=1)
mba_all_flat.drop('bill_date_new',inplace=True,axis=1)

#basket.drop('bill_date_new',inplace=True,axis=1)

# Applying apriori algorithm

from mlxtend.preprocessing import OnehotTransactions
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

#oht=OnehotTransactions()
#oht_ary = oht.fit(mba_2016_flat).transform(mba_2016_flat)
#basket_set_2016 = pd.DataFrame(oht_ary, columns=oht.columns_)
frequent_itemsets_all = apriori(mba_all_flat, min_support=0.07, use_colnames=True)

rules_all = association_rules(frequent_itemsets_all, metric="confidence",min_threshold=0.1)
