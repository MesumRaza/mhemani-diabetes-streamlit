#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
from sklearn.externals import joblib

#INITIALIZATION OF VARIABLES
parameter_list=['Pregnancies','Glucose','BloodPressure','SkinThickness','Insulin','BMI','DiabetesPedigreeFunction','Age']
parameter_input_values=[]
parameter_description=['Number of times pregnant','Plasma glucose concentration over 2 hours in an oral glucose tolerance test','Diastolic blood pressure (mm Hg)','Triceps skin fold thickness (mm)','2-Hour serum insulin (mu U/ml)','Body mass index (weight in kg/(height in m)2)','Diabetes pedigree function (a function which scores likelihood of diabetes based on family history)','Age (years)']
parameter_default_values=['6','148','72','35','0','33.6','0.627','50','1']

#CREATING INTERFACE & UI INTERACTIONS

#DISPLAY TITLE "My Diabetes Prediction App"
st.title('My Diabetes Prediction App \n\n')

#DISPLAY 6 Input Parameters for App Input
for parameter,parameter_df,parameter_desc in zip(parameter_list,parameter_default_values,parameter_description):
    #print (parameter,parameter_df,parameter_desc)
    st.subheader('Input value for '+parameter)
    parameter_input_values.append(st.number_input(parameter_desc,key=parameter,value=float(parameter_df)))
        
#CAPTURING USER INPUTS
parameter_dict=dict(zip(parameter_list, parameter_input_values)) 
parameter_user_values=list(parameter_dict.values())

#DISPLAYING USER INPUT DATA SUMMARY
st.write('\n','\n')
st.title('Your Input Summary')
st.write(parameter_dict)

#MODEL LOAD & PREDICT FUNCTION CREATION
model = joblib.load("diabeteseModel.pkl")
def predict(values):
    input_variables = pd.DataFrame([values],columns=parameter_list,dtype=float,index=['input'])    
    
    # Get the model's prediction
    prediction = model.predict(input_variables)
    print("Prediction: ", prediction)
    prediction_proba = model.predict_proba(input_variables)[0][1]
    print("Probabilities: ", prediction_proba)

    return [prediction,prediction_proba]


#CREATING A BUTTON TO EXECUTE MODEL PREDICTION
st.write('\n','\n')

if st.button("Click Here to Predict"):

    st.write('\n','\n')
    prediction_value=predict(parameter_user_values)[0]
    prediction_proba=str(round(float(predict(parameter_user_values)[1]),1)*100)+'%'
    prediction='Positive' if float(prediction_value) >0.4 else 'Negative'

    #DISPLAYING MODEL OUTPUT AND PREDICTION PROBABILITY 
    st.write('Your Diabetes Prediction is:**',prediction,' **with **',prediction_proba,'** confidence')