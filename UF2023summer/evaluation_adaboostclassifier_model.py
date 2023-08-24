import pandas as pd
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


if __name__ == '__main__':
    # load the csv file using pandas
    data_df = pd.read_csv('data.csv')
    florida_df = pd.read_csv('Florida_ct.csv')
    # Merge the two DataFrames based on the FIPS column
    merged_df = pd.merge(data_df, florida_df, left_on='FIPS', right_on='full_ct_fips', how='inner')
    # Select the desired columns
    merged_df['other_series_of_vehicles_p'] = 100 - merged_df['pickup_p'] - merged_df['suv_p'] - merged_df['sedan_p']
    merged_df['other_type_of_vehicle_p'] = 100 - merged_df['japan_p'] - merged_df['us_p']
    # df.loc[df['other_p'] < 0, 'other_p'] = 0
    test_df = merged_df[['FIPS',
                         'property_value_median',
                         'pickup_p', 'suv_p', 'sedan_p',
                         'other_series_of_vehicles_p',
                         'japan_p', 'us_p',
                         'other_type_of_vehicle_p']]
    test_df.head()
    test_df['property_value_discrete'] = 1
    test_df.loc[test_df['property_value_median'] < 200000, 'property_value_discrete'] = 0
    var_list = ['pickup_p', 'suv_p', 'sedan_p',
                'japan_p', 'us_p'
                ]

    y = test_df['property_value_discrete']
    X = test_df[var_list]
    # X = sm.add_constant(X)

    # change the data format
    X = X.values
    y = y.values

    # creating the training and testing split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=16)

    # Define parameter grid for grid search
    param_grid = {
        'n_estimators': [50],   # Try different numbers of weak classifiers
        'learning_rate': [1.0]  # Try different learning rates
    }

    # Instantiate AdaBoostClassifier
    ada_boost = AdaBoostClassifier(random_state=16)

    grad_boost = GradientBoostingClassifier(random_state=16)

    # Perform grid search using cross-validation
    grid_search = GridSearchCV(grad_boost, param_grid, cv=5, scoring='accuracy')
    grid_search.fit(X_train, y_train)

    # Get the best parameters and estimator from grid search
    best_params = grid_search.best_params_
    best_ada_boost = grid_search.best_estimator_

    # Fit the best model to the training data
    best_ada_boost.fit(X_train, y_train)

    # Evaluate the best model
    train_predictions = best_ada_boost.predict(X_train)
    train_acc = accuracy_score(y_train, train_predictions)
    print("Best Model Training Accuracy: {:.4%}".format(train_acc))

    test_predictions = best_ada_boost.predict(X_test)
    test_acc = accuracy_score(y_test, test_predictions)
    print("Best Model Testing Accuracy: {:.4%}".format(test_acc))
