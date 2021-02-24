
"""
Checkpoint 1b

*First complete the steps in checkpoint1a.pdf

Here you will create a script to preprocess the data given in starbucks.csv. You may want to use
a jupyter notebook or python terminal to develop your code and test each function as you go...
you can import this file and its functions directly:

    - jupyter notebook: include the lines `%autoreload 2` and `import preprocess`
                        then just call preprocess.remove_percents(df) to test

    - python terminal: run `from importlib import reload` and `import preprocess`
                       each time you modify this file, run `reload(preprocess)`

Once you are finished with this program, you should run `python preprocess.py` from the terminal.
This should load the data, perform preprocessing, and save the output to the data folder.

"""

import pandas as pd

def remove_percents(df, col):
    # iterate through values in column to replace %
    for i in range(len(df[col])):
        # check type (if not str, can't use .replace func), check if %
        if ((type(df[col][i]) == str) and (df[col][i][-1] == '%')):
            df[col][i] = df[col][i].replace('%', '')
        else:  
            df[col][i] = df[col][i]
    return df

def fill_zero_iron(df):
    # Nan is type float
    # replace type float with 0
    for i in range(len(df['Iron (% DV)'])):
        if (type(df['Iron (% DV)'][i]) == float):
            df['Iron (% DV)'][i] = 0
    return df

def fix_caffeine(df):
    a = df['Caffeine (mg)']
    # changes weird data to -1
    for i in range(len(a)):
        if (a[i] == 'varies') or (a[i] == 'Varies'):
            a[i] = -1
        elif (type(a[i]) == float):
            a[i] = -1
        else:
            a[i] = int(a[i])

    # get mean of data > -1
    df_caff = df[df['Caffeine (mg)'] > -1]
    num_caff = df_caff['Caffeine (mg)']
    m = int(round(num_caff.mean()))

    # replace weird data with mean m
    for i in range(len(a)):
        if (a[i] == -1):
            a[i] = m
        else:
            a[i] = a[i]    
    return df

def standardize_names(df):
    names = list(df.columns)
    for i in range(len(names)):
        names[i] = names[i].lower()
        names[i] = names[i].replace('_', ' ')
        names[i] = names[i].split('(')[0]
    df.columns = names
    return df

def fix_strings(df, col):
    a = df[col]
    for i in range(len(a)):
        # make lowercase
        a[i] = a[i].lower()
        a[i] = a[i].replace('è','e');
        a[i] = a[i].replace('&','and');
        # remove remaining non-alph characters
        for j in range(len(a[i])):
            if (((ord(a[i][j]) < 97) or (ord(a[i][j]) > 122)) and not(a[i][j] == ' ')):
                 a[i] = a[i].replace(a[i][j], ' ')
        a[i] = a[i].replace('  ',' ');
    return df


def main():

    # first, read in the raw data
    df = pd.read_csv('../data/starbucks.csv')

    # the columns below represent percent daily value and are stored as strings with a percent sign, e.g. '0%'
    # complete the remove_percents function to remove the percent symbol and convert the columns to a numeric type
    pct_DV = ['Vitamin A (% DV)', 'Vitamin C (% DV)', 'Calcium (% DV)', 'Iron (% DV)']
    for col in pct_DV:
        df = remove_percents(df, col)

    # the column 'Iron (% DV)' has missing values when the drink has no iron
    # complete the fill_zero_iron function to fix this
    df = fill_zero_iron(df)

    # the column 'Caffeine (mg)' has some missing values and some 'varies' values
    # complete the fix_caffeine function to deal with these values
    # note: you may choose to fill in the values with the mean/median, or drop those values, etc.
    df = fix_caffeine(df)

    # the columns below are string columns... starbucks being starbucks there are some fancy characters and symbols in their names
    # complete the fix_strings function to convert these strings to lowercase and remove non-alphabet characters
    names = ['Beverage_category', 'Beverage']
    for col in names:
        df = fix_strings(df, col)

    # the column names in this data are clear but inconsistent
    # complete the standardize_names function to convert all column names to lower case and remove the units (in parentheses)
    df = standardize_names(df)

    # now that the data is all clean, save your output to the `data` folder as 'starbucks_clean.csv'
    # you will use this file in checkpoint 2
    df.to_csv('../data/starbucks_clean.csv')


if __name__ == "__main__":
    main()
