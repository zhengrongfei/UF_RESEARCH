# import packages
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from absl import app
import argparse

parser = argparse.ArgumentParser("Open Set Recognition")
parser.add_argument('--independent_variable_type', type=str, default='type_of_vehicles',
                    help="num_vehicles,series_of_vehicles,type_of_vehicles")


def num_vehicles(df):
    # Baseline Regression 1
    # Select the desired columns
    test_df = df[['FIPS', 'car_sum', 'property_value_median']]
    # First baseline regression (univariate regression)
    # choose the independent variable
    X = test_df['car_sum']
    # add a constant to the independent variable
    X = sm.add_constant(X)
    # choose the dependent var
    y = test_df['property_value_median']

    # fitting the model.
    # launch the model using the independent and dependent variables
    model = sm.OLS(y, X)
    # fitting the model
    results = model.fit()
    test_df.to_csv('num_vehicles.csv', index=False)

    # plot the fitted line
    property_value_predicted = results.predict()

    # plot
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(test_df['car_sum'], test_df['property_value_median'], color='grey', alpha=0.6)
    ax.plot(test_df['car_sum'], property_value_predicted, color='red', lw=4)
    ax.set_xlabel('num_cars', fontsize=15)
    ax.set_ylabel('Property Values', fontsize=15)
    ax.set_title('Linear regression for property values and num_cars', fontsize=15)
    plt.show()

    return results


def series_of_vehicles(df):
    # Regression with multiple independent variables
    # Calculate the new columns
    df['other_p'] = 100 - df['japan_p'] - df['us_p']
    # Select the desired columns
    test_df = df[['FIPS', 'property_value_median', 'japan_p', 'us_p', 'other_p']]
    # choose the independent variable
    var_list = ['japan_p', 'us_p', 'other_p']
    X = test_df[var_list]
    # add a constant to the independent variable
    X = sm.add_constant(X)
    # choose the dependent var
    y = test_df['property_value_median']

    # fitting the model.
    # launch the model using the independent and dependent variables
    model = sm.OLS(y, X)
    # fitting the model
    results = model.fit()
    test_df.to_csv('series_of_vehicles.csv', index=False)

    # plot the fitted line
    property_value_predicted = results.predict()

    # plot
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(test_df['japan_p'], test_df['property_value_median'], color='blue', marker='o',
               label='Data points (japan_car)')
    ax.scatter(test_df['us_p'], test_df['property_value_median'], color='red', marker='x',
               label='Data points (us_car)')
    ax.plot(test_df['japan_p'], property_value_predicted, color='blue', linestyle='-', lw=2,
            label='Fitted regression line (japan_car)')
    ax.plot(test_df['us_p'], property_value_predicted, color='red', linestyle='--', lw=2,
            label='Fitted regression line (us_car)')
    # other_car
    ax.scatter(test_df['other_p'], test_df['property_value_median'], color='yellow', marker='x',
               label='Data points (other_car)')
    ax.plot(test_df['other_p'], property_value_predicted, color='grey', linestyle='--', lw=2,
            label='Fitted regression line (other_car)')

    ax.set_xlabel('Car Variables', fontsize=15)
    ax.set_ylabel('Property Values', fontsize=15)
    ax.set_title('Linear regression for property values and series_of_vehicles', fontsize=15)
    ax.legend()
    plt.show()
    return results


def type_of_vehicle(df):
    # Regression with multiple independent variables
    # Select the desired columns
    df['other_p'] = 100 - df['pickup_p'] - df['suv_p'] - df['sedan_p']
    df.loc[df['other_p'] < 0, 'other_p'] = 0
    test_df = df[['FIPS', 'property_value_median', 'pickup_p', 'suv_p', 'sedan_p', 'other_p']]
    # create the third regression (multivariate regression)
    # choose the independent variable
    var_list = ['pickup_p',
                'suv_p',
                'sedan_p',
                'other_p'
                ]
    X = test_df[var_list]
    # add a constant to the independent variable
    X = sm.add_constant(X)
    # choose the dependent var
    y = test_df['property_value_median']

    # fitting the model.
    # launch the model using the independent and dependent variables
    model = sm.OLS(y, X)
    # fitting the model
    results = model.fit()
    test_df.to_csv('type_of_vehicle.csv', index=False)

    # plot the fitted line
    property_value_predicted = results.predict()

    # plot
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.scatter(test_df['pickup_p'], test_df['property_value_median'], color='blue', marker='o',
               label='Data points (pickup_p)')
    ax.scatter(test_df['suv_p'], test_df['property_value_median'], color='green', marker='x',
               label='Data points (suv_p)')
    ax.scatter(test_df['sedan_p'], test_df['property_value_median'], color='red', marker='s',
               label='Data points (sedan_p)')
    ax.plot(test_df['pickup_p'], property_value_predicted, color='blue', linestyle='-', lw=2,
            label='Fitted regression line (pickup_p)')
    ax.plot(test_df['suv_p'], property_value_predicted, color='green', linestyle='--', lw=2,
            label='Fitted regression line (suv_p)')
    ax.plot(test_df['sedan_p'], property_value_predicted, color='red', linestyle='-.', lw=2,
            label='Fitted regression line (sedan_p)')
    # other_p
    ax.scatter(test_df['other_p'], test_df['property_value_median'], color='yellow', marker='x',
               label='Data points (other_car)')
    ax.plot(test_df['other_p'], property_value_predicted, color='grey', linestyle='--', lw=2,
            label='Fitted regression line (other_car)')

    ax.set_xlabel('Car Type Variables', fontsize=15)
    ax.set_ylabel('Property Values', fontsize=15)
    ax.set_title('Linear regression for property values and car type variables', fontsize=15)
    ax.legend()
    plt.show()

    return results


if __name__ == '__main__':
    args = parser.parse_args()
    options = vars(args)

    # load the csv file using pandas
    data_df = pd.read_csv('data.csv')
    florida_df = pd.read_csv('Florida_ct.csv')
    # Merge the two DataFrames based on the FIPS column
    merged_df = pd.merge(data_df, florida_df, left_on='FIPS', right_on='full_ct_fips', how='inner')

    # Choose ways of regression

    if options['independent_variable_type'] == 'num_vehicles':
        result = num_vehicles(merged_df)

    if options['independent_variable_type'] == 'series_of_vehicles':
        result = series_of_vehicles(merged_df)

    if options['independent_variable_type'] == 'type_of_vehicles':
        result = type_of_vehicle(merged_df)

    # report the results.
    print(result.summary())

