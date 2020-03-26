import operator
import json
import numpy as np
import matplotlib.pyplot as plt

from sklearn.linear_model import Ridge
import time

from sklearn.preprocessing import PolynomialFeatures

from data_scrapper.case_data_scrapper import CasesDataScrapper
from data_scrapper.death_data_scrapper import DeathsDataScrapper
from data_scrapper.active_case_data_scrapper import ActiveCasesDataScrapper
from data_scrapper.critical_case_data_scrapper import CriticalCasesDataScrapper
from data_scrapper.cured_case_data_scrapper import CuredCasesDataScrapper
from data_scrapper.data_scrapper import DataScrapper


def training_set(datascrapper_class, scrap_data_from_server=True, offline_dataset_date=""):
    scrapper = globals()[datascrapper_class]()
    dataset_date = ""

    if scrap_data_from_server:
        scrapper.scrap_data()
    else:
        dataset_date = offline_dataset_date

        if offline_dataset_date == "":
            raise Exception("Invalid date. Please update the 'offline_dataset_date' in the config file.")
    
    filename = scrapper.get_dataset_file_name(dataset_date=dataset_date)
    return np.genfromtxt("data/" + filename, delimiter=',').astype(np.int32)

def train_model(x, y, polynomial_degree):
    polynomial_features = PolynomialFeatures(degree=polynomial_degree)
    x_poly = polynomial_features.fit_transform(x)
    model = Ridge()
    model.fit(x_poly, y)

    return model

def get_predictions(x, model, polynomial_degree):
    polynomial_features = PolynomialFeatures(degree=polynomial_degree)
    x_poly = polynomial_features.fit_transform(x)

    return model.predict(x_poly)

def print_stats(model_name, model, x, y, polynomial_degree, days_to_predict):
    y_predicted = np.round(get_predictions(x, model, polynomial_degree), 0).astype(np.int32)
    print_forecast(model_name, model, polynomial_degree, beginning_day=len(x), limit=days_to_predict)
    plot_graph(model_name, x, y, y_predicted)


def plot_graph(model_name, x, y, y_predicted):
    
    plt.scatter(x, y, s=8)
    sort_axis = operator.itemgetter(0)
    sorted_zip = sorted(zip(x, y_predicted), key=sort_axis)
    x, y_predicted = zip(*sorted_zip)
    
    plt.plot(x, y_predicted, color='m')
    plt.title("Amount of " + model_name + " in each day")
    plt.xlabel("Days")
    plt.ylabel(model_name)
    plt.show()
    plt.savefig('graphs/' + model_name +'.jpg')

def print_forecast(model_name, model, polynomial_degree, beginning_day=0, limit=5):
    
    next_days_x = np.array(range(beginning_day, beginning_day + limit)).reshape(-1, 1)
    next_days_pred = np.round(get_predictions(next_days_x, model, polynomial_degree), 0).astype(np.int32)
    print("The predictions for " + model_name + " in the following " + str(limit) + " days is:")
    for i in range(0, limit):
        print(str(i + 1) + ": " + str(next_days_pred[i]))

def model(model_config):
    Training_set = training_set(model_config["datascrapper_class"], True, model_config["offline_dataset_date"])
    x = Training_set[:, 0].reshape(-1, 1)
    y = Training_set[:, 1]
    model = train_model(x, y, model_config["polynomial_degree"])

    print_stats(model_config["model_name"], model, x, y, model_config["polynomial_degree"], model_config["days_to_predict"])

if __name__ == "__main__":
    config = {}

    with open("config.json", "r") as f:
        config = json.load(f)

    for model_config in config["models"]:
        model(model_config)
        time.sleep(2)
