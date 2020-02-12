#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import pandas as pd


# In[6]:
parameter_list=['Pregnancies','Glucose','BloodPressure','SkinThickness','Insulin','BMI','DiabetesPedigreeFunction','Age']
parameter_input_values=[]
parameter_description=['Number of times pregnant','Plasma glucose concentration over 2 hours in an oral glucose tolerance test','Diastolic blood pressure (mm Hg)','Triceps skin fold thickness (mm)','2-Hour serum insulin (mu U/ml)','Body mass index (weight in kg/(height in m)2)','Diabetes pedigree function (a function which scores likelihood of diabetes based on family history)','Age (years)']
parameter_default_values=['6','148','72','35','0','33.6','0.627','50','1']
st.title('My Diabetes Prediction App \n\n')
for parameter,parameter_df,parameter_desc in zip(parameter_list,parameter_default_values,parameter_description):
	#print (parameter,parameter_df,parameter_desc)
	st.subheader('Input value for '+parameter)
	parameter_input_values.append(st.number_input(parameter_desc,key=parameter,value=float(parameter_df)))
	
#st.write(parameter_val) for parameter_val in parameter_values
#parameter_values=[st.text_input('Age') for parameter in parameter_list]
	
parameter_dict=dict(zip(parameter_list, parameter_input_values)) 

st.write('\n','\n')
st.title('Your Input Summary')

st.write(parameter_dict)
#pd.DataFrame.from_dict(parameter_dict)
#st.write(pd.DataFrame.from_records([parameter_dict]))
# In[8]:

import requests 
import json
URL = 'https://mhemani-diabetes-streamlit.herokuapp.com/api_diabetes'

st.write('\n','\n')

if st.button("Click Here to Predict"):

	PARAMS={'data':','.join(map(str,list(parameter_dict.values())))}
	#st.write(PARAMS)
	
	#PARAMS = {'data':'1,121,78,39,74,39.0,0.261,28'} 
	headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
	r = requests.post(url = URL, json=PARAMS, headers=headers) 
	
	st.write('\n','\n')
	prediction_value=r.json().get('prediction')
	prediction_proba=str(round(float(r.json().get('prediction_proba')),1)*100)+'%'
	prediction='Positive' if float(prediction_value) >0.4 else 'Negative'
	
	st.write('Your Diabetes Prediction is:**',prediction,' **with **',prediction_proba,'** confidence')





# In[ ]:




