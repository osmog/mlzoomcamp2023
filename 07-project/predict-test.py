#!/usr/bin/env python
# coding: utf-8

import requests


url = 'http://localhost:9696/predict'

customer_id = 'cust123'
customer = {'occupation': 'engineer',
 'monthly_income': 4500,
 'credit_score': 250,
 'years_of_employment': 5,
 'finance_status': 'good',
 'finance_history': 'no_issues',
 'number_of_children': 1}

response = requests.post(url, json=customer).json()
print(response)

if response['carOwn'] == True:
    print('Customer with id %s has a car' % customer_id)
else:
    print('Customer with id %s has no car' % customer_id)