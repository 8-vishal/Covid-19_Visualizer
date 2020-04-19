# Covid-19_Visualizer
Visualize the spread of COVID-19 epidemic with SEIR model.

Dataset for the Epidemic model visualization used is scraped from the website www.covid19india.org and saved into a csv file with help of pandas. 

Data for date APRIL-19-2020 has been included, to visualize the model for the current date you have to scrap the data again by running CSV_creator function in utilities module, it will automatically save the data in csv file named "Todays_data.csv" 

To see the graph run Visualize function from the main.py file, the model works on SEIR model of epidemic visualization for more details for the model refer to this link https://www.idmod.org/docs/hiv/model-seir.html. The recovered in the dataset might not be updated so try to input the values in by hand for certain states. 
