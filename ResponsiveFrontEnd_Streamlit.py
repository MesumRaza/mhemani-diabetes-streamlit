#!/usr/bin/env python
# coding: utf-8


import streamlit as st
import pandas as pd
import urllib.parse



parameter_list=['Pregnancies','Glucose','BloodPressure','SkinThickness','Insulin','BMI','DiabetesPedigreeFunction','Age']
parameter_input_values=[]
parameter_description=['Number of times pregnant','Plasma glucose concentration over 2 hours in an oral glucose tolerance test','Diastolic blood pressure (mm Hg)','Triceps skin fold thickness (mm)','2-Hour serum insulin (mu U/ml)','Body mass index (weight in kg/(height in m)2)','Diabetes pedigree function (a function which scores likelihood of diabetes based on family history)','Age (years)']
parameter_default_values=['6','148','72','35','0','33.6','0.627','50','1']
st.title('My Diabetes Prediction App \n\n')
for parameter,parameter_df,parameter_desc in zip(parameter_list,parameter_default_values,parameter_description):
	#print (parameter,parameter_df,parameter_desc)
	st.subheader('Input value for '+parameter)
	parameter_input_values.append(st.number_input(parameter_desc,key=parameter,value=float(parameter_df)))
	
	
parameter_dict=dict(zip(parameter_list, parameter_input_values)) 

st.write('\n','\n')
st.title('Your Input Summary')

st.write(parameter_dict)

import requests 
import json

URL = 'https://mhemani-diabetes-fastapi.herokuapp.com/api_diabetes/'

st.write('\n','\n')

def call_predict_api(PARAMETERS):
	
	ENCODE_PARAMS=urllib.parse.urlencode({'payload':PARAMETERS.get('data')})
	
	response=requests.get(url = URL, params=ENCODE_PARAMS) 
	
	if response.status_code != 200:
        	raise Exception('API response: {}'.format(response.status_code))
	return response
	
if st.button("Click Here to Predict"):

	PARAMS={'data':','.join(map(str,list(parameter_dict.values())))}
	
	r=call_predict_api(PARAMS)
	
	st.write(r.url)
	
	st.write('\n','\n')
	prediction_value=r.json().get('prediction')
	prediction_proba=str(round(r.json().get('prediction_proba'),1)*100)+'%'
	prediction='Positive' if prediction_value >0.4 else 'Negative'
	
	st.write('Your Diabetes Prediction is:**',prediction,' **with **',prediction_proba,'** confidence')
	
	st.write("Click Here to show API Docs",'https://mhemani-diabetes-fastapi.herokuapp.com/docs')
