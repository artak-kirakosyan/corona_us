#!/usr/bin/env python
import json
from matplotlib import pyplot as plt


DEATHS_JSON = 'data/deaths_list.json'
POPULATION_JSON = 'data/population_list.json'


def load_and_form_dictionary(path):
    with open(path) as f:
        data_list = json.load(f)


    data_dict = {}
    for year, month, numb in data_list:
        try:
            curr_year = data_dict[year]
        except KeyError:
            data_dict[year] = {}
            curr_year = data_dict[year]
    
        curr_year[month] = numb
    return data_dict


def form_min_max(data, year_to_start_from=1900):
    months_mins = [float('Inf')]*12
    months_maxs = [0]*12

    for year, vals in data.items():
        for month, val in vals.items():
            # year 2020 should not be participating in min max calculaiton.
            if year == 2020:
                continue
            if year > year_to_start_from:
                months_mins[month-1] = min(months_mins[month-1], val)
                months_maxs[month-1] = max(months_maxs[month-1], val)
    return months_mins, months_maxs


def normalize_per_1000(death_dictionary, population_dictionary):
    normalized_death_dictionary = {}
    for year in death_dictionary.keys():
        death_vals = death_dictionary[year]
        population_vals = population_dictionary[year]
        curr_year = {}
        for month in death_vals.keys():
            curr_year[month] = round(death_vals[month] * 1000 / population_vals[month], 3)
        normalized_death_dictionary[year] = curr_year
    return normalized_death_dictionary


def main():
    death_dictionary = load_and_form_dictionary(DEATHS_JSON)
    
    population_dictionary = load_and_form_dictionary(POPULATION_JSON)
    normalized_death_history = normalize_per_1000(death_dictionary, population_dictionary)

    normalized_mins, normalized_maxs = form_min_max(normalized_death_history)
    normalized_deaths_2020 = normalized_death_history[2020]

    plt.figure(num=None, figsize=(8, 6), dpi=600, facecolor='w', edgecolor='k')
    months = list(range(1, 13))
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    plt.ylim(bottom=0)
    plt.ylabel('Number of deaths(normalized per 1000 person')
    plt.xlabel('Month')
    plt.title('Minimum, maximum and current(2020) monthly deaths in US from 1999 to 2018.')
    plt.xticks(months, month_names)
    plt.plot(months, normalized_mins)
    plt.plot(months, normalized_maxs)
    plt.plot(list(normalized_deaths_2020.keys()), list(normalized_deaths_2020.values()))
    plt.legend(['Minimum from 1999 to 2018', 'Maximum from 1999 to 2018', '2020'])
    plt.savefig('normalized_to_1000.png')


    plt.clf()
    plt.ylim(bottom=0, top = 320000)
    plt.ylabel('Absolute number of deaths')
    plt.xlabel('Month')
    plt.title('Minimum, maximum and current(2020) monthly deaths in US from 1999 to 2018.')
    plt.xticks(months, month_names)

    mins, maxs = form_min_max(death_dictionary)
    deaths_2020 = death_dictionary[2020]
    plt.plot(months, mins)
    plt.plot(months, maxs)
    plt.plot(list(deaths_2020.keys()), list(deaths_2020.values()))
    plt.legend(['Minimum from 1999 to 2018', 'Maximum from 1999 to 2018', '2020'])
    plt.savefig('absolute.png')


if __name__ == '__main__':
    main()

