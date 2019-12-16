#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 22:21:56 2019

@author: mark
"""

import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

"""
    Variables:
    MAKE - the make of car
"""

MAKE = 'SUZUKI'
filter_values = ['Enhanced Search Image Link', 'Go to advert and open live chat']
dealer_filter = ['Dealer', 'Private']

car_desc = []
dealer_values = []
year_data = []
mileage_data = []
engine_data = []
accessory_data = []
prices = []

for i in range(22):
    url ='https://www.carzone.ie/used-cars/'+MAKE.lower()+'?make='+MAKE+'&page=' + str(i)
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page)

    all_cars = soup.find_all('stock-summary-item')
    for car in all_cars:
        car_details = car.find_all('a')
        dealer_details = car.find_all('strong')
        price_details = car.find_all('span', class_='ng-star-inserted')
        accessory_details = car.find_all('p', class_='stock-summary__description ng-star-inserted')
        #print(accessory_details)
        #print(price_details)
        if len(accessory_details) > 0:
            for accessory_detail in accessory_details:
                accessory_data.append(accessory_detail.contents[0])
        else:
            accessory_data.append('')
        for price_detail in price_details:
            prices.append(price_detail.contents[0])
        for car_detail in car_details:
            car_label = car_detail.get('aria-label')
            if car_label not in filter_values and car_label is not None:
                car_desc.append(car_label)
        for dealer_detail in dealer_details:
    #        print(dealer_detail)
            if dealer_detail.contents[0] in dealer_filter:
    #            print(dealer_detail.contents[0])
                dealer_values.append(dealer_detail.contents[0])
            elif not dealer_detail.has_attr('class'):
                car_values = dealer_detail.contents[0].split('•')
                #print(car_values)
#                print(car_values)
                if len(car_values) == 2:
                    mileage_data.append('')
                    year_data.append(car_values[0])
                    engine_data.append(car_values[1])
                elif len(car_values) == 3:
                    year_data.append(car_values[0])
                    mileage_data.append(car_values[1])
                    engine_data.append(car_values[2])
#                year_data.append(car_values[0])
#                mileage_data.append(car_values[1])
#                engine_data.append(car_values[2])
#                car_values.append(dealer_detail.contents[0])

print('Length of dealer values', len(dealer_values))
print('Length of car_desc values', len(car_desc))
print('Length of price values', len(prices))
print('Length of mileage values', len(mileage_data))
print('Length of engine values', len(engine_data))
print('Length of year values', len(year_data))
print('Length of accessory values', len(accessory_data))

carzone_data = pd.DataFrame({'car_description': car_desc, 'dealer': dealer_values, 
                             'prices': prices, 'year': year_data,
                             'mileage': mileage_data, 'engine_size': engine_data,
                             'accessories': accessory_data})
    
carzone_data.head()