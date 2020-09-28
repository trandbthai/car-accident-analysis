'''
<ALY 6140 Group 5 Capstone Project: Analysis on New York Car Crashes that lead to an Injury>

Copyright (c) 2019
Licensed
Written by < Jinchao Hou, 
			 Dien Bao Tran Thai (Tran Thai), 
			 Chunbing  Yang, 
			 Ben Raborn>
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def cross_tab(dataset, column1, column2, action=0):
    '''
    The function will return a cross table based on the column1, column2.
    @param dataset: Records DataFrame
    @param column1: Column name of the column to group by in the rows
    @param column2: Column name of the column to group by in the columns
    @param action: action to decide the return format. If the action is 0: The function
                    return a cross table,if the action is 1: the function return a column
                    normalized cross table.
                    If the action is 2: the function return a index normalized cross table.
    @return: DataFrame format cross table.
    '''
    if (action == 0):
        cross = pd.crosstab(dataset[column1], dataset[column2])
    elif (action == 1):
        cross = pd.crosstab(dataset[column1], dataset[column2], normalize='columns')
    elif (action == 2):
        cross = pd.crosstab(dataset[column1], dataset[column2], normalize='index')
    df = pd.DataFrame(cross)
    df = df.reset_index()
    df = df.rename(columns={'index': column1})

    index = list(range(100))
    d = {'DOWindex': index}
    DOW_index = pd.DataFrame(d)

    df = DOW_index.merge(df, left_on='DOWindex', right_index=True)
    df = df.drop('DOWindex', axis=1)
    return df

def plot_bar(cross_tab, vertical=True):
    '''
    Plot the bar plot based on the cross table
    @param cross_tab: DataFrame cross table
    @param vertical: Boolean Default is True. return vertical bar or not.
    @return: plot
    '''
    x_labels = cross_tab.iloc[:,0]
    stack_labels = cross_tab.columns[1:]
    num = cross_tab.iloc[:,1:]

    for i in range(cross_tab.shape[1]-1):
        if vertical == True:
            plt.bar(x_labels, height=cross_tab.iloc[:,i+1].values, bottom=np.sum(num.values[:,range(i)], axis=1), label=stack_labels[i])
        else:
            plt.barh(x_labels, width=cross_tab.iloc[:, i + 1].values, left=np.sum(num.values[:, range(i)], axis=1),
                     label=stack_labels[i])
    plt.legend()
    return plt.show()

def plot_line(cross_tab):
    '''
    Plot the line plot based on the cross table
    @param cross_tab: DataFrame cross table
    @return: line plot
    '''
    stack_labels = cross_tab.columns[1:]
    num = cross_tab.iloc[:,1:]
    for i in range(cross_tab.shape[1]-1):
        plt.plot(cross_tab.values[:,0], cross_tab.iloc[:,i+1], label=stack_labels[i])
    plt.legend()
    #plt.ylim(0,1)
    return plt.show()


def bar_number(dataset, column, large_n=1000, small_n=None):
    '''
    plot the Bar plot for records DataFrame
    @param dataset: Records DataFrame
    @param column: str, Name of the column which contain the records we want to plot
    @param large_n: int, The number of largest n categorical will show in the bar plot
    @param small_n: int, The number of smallest n categorical will show in the bar plot
    @return:
    '''
    if small_n is None:
        ax = dataset[column].value_counts().nlargest(large_n).plot(kind='barh', width=0.5, color='green', fontsize=13)
        ax.set_title(f'Top {large_n} {column} by Count of Records', fontsize=18)
    else:
        ax = dataset[column].value_counts().nsmallest(small_n).plot(kind='barh', width=0.5, color='green', fontsize=13)
        ax.set_title(f'Least {small_n} {column} by Count of Records', fontsize=18)
    ax.set_xlabel("Number of Records", fontsize=18);
    ax.invert_yaxis()
    for i in ax.patches:
        ax.text(i.get_width() + .3, i.get_y() + .38, str(i.get_width()), fontsize=13)
    return ax

def summary(dataset, column):
    '''
    Get the count and percentage of each unique values in the column
    @param dataset: DataFrame
    @param column: str, The name of the column
    @return: DataFrame, which contains the counts and percent.
    '''
    a = dataset[column]
    count = a.value_counts()
    percent = a.value_counts(normalize = True)
    b = pd.DataFrame({'count': count, 'percent':percent})
    b = b.reset_index()
    b = b.rename(columns = {'index': column})
    if column == 'Day_of_Week':
        #create DOW_indx
        DOW = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday','Sunday']
        index = [0,1,2,3,4,5,6]
        d = {'Day_of_Week': DOW, 'DOWindex': index }
        DOW_index = pd.DataFrame(d)
        b = DOW_index.merge(b,left_on = 'Day_of_Week', right_on = 'Day_of_Week')
        b = b.drop('DOWindex', axis = 1)
    return b

def lower_objects_fun(df):
    """
    Change the object type in DataFrame to lower string.
    :param df: DataFrame, a pandas data frame
    :return: DataFrame returns the data frame with every column of dtype "object" in lower case
    """
    df2=df.copy()
    for i in range(df2.shape[1]):
        if df2.iloc[:,i].dtypes == 'O':
            df2.iloc[:,i]  = df2.iloc[:,i].str.lower()
    return(df2)