"""
Class: CS230--Section 001 
Name: Gayatri Ary Mahadewi
Description: Final Project (Skyscrapers)
I pledge that I have completed the programming assignment independently. 
I have not copied the code from a student or any source.
I have not given my code to any student. 
"""

import streamlit as st
import pandas as pd
# import re
import numpy as np
import matplotlib.pyplot as plt


# Data -----------------------------------------------------------------------------------------------------------------


def read_data(filename):  # Function to read the CSV file
    columns = ['RANK', 'NAME', 'CITY', 'Full Address', 'Latitude', 'Longitude', 'COMPLETION', 'Height',
               'Meters', 'Feet', 'FLOORS', 'MATERIAL', 'FUNCTION', 'Link']
    data = pd.read_csv(filename, usecols=columns).set_index("RANK")
    data.dropna(axis=1, inplace=True)
    return data


# Functions ------------------------------------------------------------------------------------------------------------


def city_freq(data):  # Function to count number of cities
    city_group = dict(data.groupby(['CITY'])['NAME'].count())
    return city_group


def material_freq(data):  # Function to count number of materials
    material_group = dict(data.groupby(['MATERIAL'])['NAME'].count())
    return material_group


def bar_chart(city, counts):  # Function to create a bar chart for the frequency of skyscrapers in different cities
    plt.bar(city, counts, color='red')
    plt.xlabel("City")
    plt.xticks(rotation=90, fontsize=6)
    plt.ylabel("Frequency of Skyscrapers")
    plt.ylim(0, 20)
    plt.title("Frequency of Skyscrapers by City")
    return plt


def bar_chart1(skyscraper, height, column_width):  # Function to create a bar chart for the heights of skyscrapers
    plt.figure(figsize=(20, 20))
    plt.bar(skyscraper, height, width=column_width, color='red')
    plt.xlabel("Skyscrapers")
    plt.xticks(rotation=90, fontsize=6)
    plt.ylabel("Height (Meters)")
    plt.yticks(np.arange(0, 830, 50))
    plt.ylim(0, 830)
    plt.title("Height Comparison of Skyscrapers")
    return plt


def pie_chart(labels_list, values_list):  # Function to create a pie chart for the materials of skyscrapers
    plt.title("Frequency in a Pie Chart")
    fig1, ax1 = plt.subplots()
    ax1.pie(values_list, labels=labels_list, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    return fig1


def paperclips(height):  # Function to count how many paperclips = a skyscraper's height (I'm really proud of this one!)
    paperclip = 3.4925
    total_paperclips = (height * 100) / paperclip
    return total_paperclips


def heights_list(data):  # Function to make a list of all the heights as integers
    height_list = data['Meters']
    meters_list = []
    for i in height_list:
        i.split()
        meters_list.append(int(i[0] + i[1] + i[2]))
    return meters_list


# Web Pages ------------------------------------------------------------------------------------------------------------


def page0():  # Home
    st.image("https://blog.allplan.com/hubfs/EN_Blog/Architecture/The%20Newest%20Skyscrapers%20Built%20in%202019/iStock-1133400370_NEU.jpg")

    st.header("Welcome!")

    st.markdown('''Hey everyone! This is my final project for my CS230 course. I developed this web-based 
    Python application through the coding skills that I have learnt in class. The real world data that I used
    for this is the World's Skyscrapers data. Hope you enjoy exploring my application and learning more about 
    skyscrapers!
    
    ~ Home: You're on it right now!
    ~ Rank: Rank of all skyscrapers based on their heights
    ~ Map: Locations of skyscrapers
    ~ Frequency: Frequency of skyscrapers in cities
    ~ Visual Comparison: Compare your skyscrapers through a bar graph
    ~ How Many Paperclips?: Find out how many paper clips is equivalent to the height of a skyscraper
    ~ Materials of Skyscrapers: Find out the different types of materials skyscrapers are made out
    ''')


def page1(data):  # Rank
    st.header("Rank of Skyscrapers Based on Height")
    dict1 = {}
    keys_list = list(data['NAME'])
    values_list = list(data['Height'])

    for key in keys_list:
        for value in values_list:
            dict1[key] = value
            values_list.remove(value)
            break

    dict1_dataframe = pd.DataFrame(list(dict1.items()), columns=['Skyscrapers', 'Heights'])
    st.write(dict1_dataframe)


def page2(data):  # Map
    st.header("Map of Skyscrapers")
    points = pd.DataFrame({'Name': data['NAME'], 'latitude': data['Latitude'], 'longitude': data['Longitude']})
    st.map(points)


def page3(data):  # Frequency
    count_city = city_freq(data)
    cities = []
    counts = []

    for i in count_city:
        cities.append(i)
    for i in count_city:
        counts.append(count_city.get(i))

    st.pyplot(bar_chart(cities, counts))


def page4(data):  # Visual Comparison
    st.header("Height Comparison of All Skyscrapers")
    column_width1 = st.slider('Width', 0.25, 0.50, 0.75,
                              help='Slide to change the column width of the bar chart below')
    st.pyplot(bar_chart1(data['NAME'], heights_list(data), column_width1))

    st.header("Comparison of Selected Skyscrapers")
    skyscrapers = sorted(list(set(data['NAME'])))
    sel_skyscrapers = st.multiselect("Select a skyscraper:", skyscrapers,
                                     help="Select specific skyscrapers you want to compare")

    names_lst = data['NAME']
    heights_lst = heights_list(data)
    dict_namesheights = {}
    sel_heights = []

    for key in names_lst:
        for value in heights_lst:
            dict_namesheights[key] = value
            heights_lst.remove(value)
            break

    for i in sel_skyscrapers:
        sel_heights.append(dict_namesheights[i])

    st.pyplot(bar_chart1(sel_skyscrapers, sel_heights, 0.5))


def page5(data):  # Paperclips
    st.header("Height of Skyscraper = Amount of Paperclips")
    st.image("https://www.freeiconspng.com/thumbs/paper-clip-icon/grey-paper-clip-icon-4.png")
    st.markdown("Find out a skyscraper's height in comparison to the size of an average paperclip (3.4925cm)")
    skyscrapers_list = sorted(list(set(data['NAME'])))
    option = st.selectbox("Select a skyscraper:", skyscrapers_list,
                          help="Select a skyscraper to find out its height in paperclips")
    skyscraper_index = skyscrapers_list.index(option)
    height = heights_list(data)[skyscraper_index]
    total_paperclips = paperclips(height)
    st.write(f"The height of {option} is {height}m, which is equivalent to {round(total_paperclips)} paperclips.")


def page6(data):  # Materials
    st.title("Materials of Skyscrapers")
    st.markdown("Percentages and counts of how many skyscrapers are made out of certain materials")
    count_material = material_freq(data)
    materials_list = []
    counts_list = []

    for m in count_material:
        materials_list.append(m)
        counts_list.append(count_material.get(m))

    st.pyplot(pie_chart(['Composite', 'Concrete', 'Steel', 'Steel/Concrete'], counts_list))

    dict2 = {}
    keys_list2 = materials_list
    values_list2 = counts_list

    for key in keys_list2:
        for value in values_list2:
            dict2[key] = value
            values_list2.remove(value)
            break

    dict2_dataframe = pd.DataFrame(list(dict2.items()), columns=['Functions', 'Counts'])
    st.write(dict2_dataframe)

# Program --------------------------------------------------------------------------------------------------------------


def main():
    st.title("CS230 Final Project - Skyscrapers")
    st.text("By: Gayatri Ary Mahadewi")
    filename = "Skyscrapers2021.csv"
    data = read_data(filename)
    st.sidebar.title("Menu")

    selection = st.sidebar.radio("Go to", ["Home", "Rank", "Map", "Frequency", "Visual Comparison",
                                           "How Many Paperclips?", "Materials of Skyscrapers"])
    if selection == "Home":
        page0()
    if selection == "Rank":
        page1(data)
    if selection == "Map":
        page2(data)
    if selection == "Frequency":
        page3(data)
    if selection == "Visual Comparison":
        page4(data)
    if selection == "How Many Paperclips?":
        page5(data)
    if selection == "Materials of Skyscrapers":
        page6(data)


main()
