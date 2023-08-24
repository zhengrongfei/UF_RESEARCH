import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import xgboost as xgb
import lightgbm as lgb
import catboost as cb

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, log_loss

## import the sklearn models
# logistic regression
from sklearn.linear_model import LogisticRegression

# K nearest neighbor
from sklearn.neighbors import KNeighborsClassifier

# support vector machine
from sklearn.svm import SVC, LinearSVC
# SVC: support vector classification (using kernel methods)

# decision tree
from sklearn.tree import DecisionTreeClassifier

# ensemble methods, e.g., random forest
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier

# naive Bayesian
from sklearn.naive_bayes import GaussianNB

# discriminant analysis
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

# neural network
from sklearn.neural_network import MLPClassifier


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
                         'other_type_of_vehicle_p',
                         'car_sum']]
    test_df.head()
    test_df['property_value_discrete'] = 1
    test_df.loc[test_df['property_value_median'] < 200000, 'property_value_discrete'] = 0
    var_list = ['pickup_p', 'suv_p', 'sedan_p',
                'japan_p', 'us_p',
                ]

    y = test_df['property_value_discrete']
    X = test_df[var_list]
    # X = sm.add_constant(X)

    # change the data format
    X = X.values
    y = y.values

    # creating the training and testing split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=16)

    # initialize logistic regression
    # instantiate the model (using the default parameters)
    logreg = LogisticRegression(random_state=16)

    # fit the model with training data only
    logreg.fit(X_train, y_train)

    # check the performance
    train_predictions = logreg.predict(X_train)
    acc = accuracy_score(y_train, train_predictions)
    print("Training Accuracy: {:.4%}".format(acc))

    test_predictions = logreg.predict(X_test)
    acc = accuracy_score(y_test, test_predictions)
    print("Testing Accuracy: {:.4%}".format(acc))

    """ML classifiers"""
    # check the performance for all the classifiers.
    classifiers = [
        LogisticRegression(random_state=16),
        KNeighborsClassifier(3),
        SVC(kernel="rbf", C=0.025, probability=True),
        DecisionTreeClassifier(),
        RandomForestClassifier(),
        GaussianNB(),
        MLPClassifier(alpha=1e-10, hidden_layer_sizes=(20, 2), random_state=1),
        AdaBoostClassifier(),
        GradientBoostingClassifier(),
        LinearDiscriminantAnalysis(),
        QuadraticDiscriminantAnalysis(),
        # new model try
        xgb.XGBClassifier(),
        lgb.LGBMClassifier(),
        cb.CatBoostClassifier()
    ]

    # Logging for Visual Comparison
    log_cols = ["Classifier", "Train Accuracy", "Train Log Loss", "Test Accuracy", "Test Log Loss"]
    log = pd.DataFrame(columns=log_cols)

    for clf in classifiers:
        clf.fit(X_train, y_train)
        name = clf.__class__.__name__

        print("=" * 30)
        print(name)

        print('****Results****')
        # training
        train_predictions = clf.predict(X_train)
        train_acc = accuracy_score(y_train, train_predictions)
        print("Training Accuracy: {:.4%}".format(train_acc))

        train_predictions = clf.predict_proba(X_train)
        train_ll = log_loss(y_train, train_predictions)
        print("Training Log Loss: {}".format(train_ll))

        # testing
        test_predictions = clf.predict(X_test)
        test_acc = accuracy_score(y_test, test_predictions)
        print("Testing Accuracy: {:.4%}".format(test_acc))

        test_predictions = clf.predict_proba(X_test)
        test_ll = log_loss(y_test, test_predictions)
        print("Testing Log Loss: {}".format(test_ll))

        log_entry = pd.DataFrame([[name, train_acc * 100, train_ll, test_acc * 100, test_ll]], columns=log_cols)
        log = pd.concat([log, log_entry])

    # Visualize the performance.
    sns.set_color_codes("muted")
    plt.figure(figsize=(20, 16))
    sns.barplot(x='Test Accuracy', y='Classifier', data=log, color="b")
    plt.xlabel(' Accuracy %')
    plt.title('Classifier Accuracy')
    plt.show()

    # Visualize the performance.
    sns.set_color_codes("muted")
    plt.figure(figsize=(20, 16))
    sns.barplot(x='Test Log Loss', y='Classifier', data=log, color="g")
    plt.xlabel('Log Loss')
    plt.title('Classifier Log Loss')
    plt.show()
