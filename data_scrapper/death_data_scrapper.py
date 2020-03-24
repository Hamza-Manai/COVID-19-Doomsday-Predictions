from data_scrapper.data_scrapper import DataScrapper
import csv

class DeathsDataScrapper(DataScrapper):
    PREFIX = "death"

    def __init__(self):
        super()

    def scrap_data(self):
        data1, data2 = self.__get_deaths()
        filename = self.get_dataset_file_name()

        self.save_datas_to_file(filename, data1, data2)
        
    def save_datas_to_file(self, filename, data1, data2):
        data_to_save = []

        for i in range(0, len(data1)):
            data_to_save.append([i, data1[i], data2[i]])
        
        with open("data/" + filename, 'w', newline='') as f:
            csv_writer = csv.writer(f, delimiter=',')
            csv_writer.writerows(data_to_save)


    def __get_deaths(self):
        data1, data2 = self.get_table_content("coronavirus-death-toll", ".table-responsive", 0)

        return list(reversed(data1)), list(reversed(data2))

    def get_dataset_file_name(self, dataset_date=""):
        return super().get_dataset_file_name(DeathsDataScrapper.PREFIX, dataset_date=dataset_date)
