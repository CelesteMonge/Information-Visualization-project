# Information-Visualization-project

Education is often cited as a key driver of economic development, personal advancement, and social mobility. However, not all countries achieve the same results from their investments. With access to reliable open data sources from Eurostat and Our World In Data, I saw an opportunity to investigate whether there is a measurable correlation between the level of investment in higher education and its effectiveness in terms of graduation output and employability.
This project aims to visualize and explore these relationships through an interactive dashboard built with Dash and Plotly. The goal is not only to uncover patterns or outliers among European countries but also to understand which countries are more efficient in transforming public investment into tangible results. By doing so, we can raise questions about policy design, equity, and the potential for applying similar strategies in other regions, such as Latin America.

The datasets were obtained from Eurostat and Our World In Data open repositories. All data were downloaded in .csv format and cleaned using Pandas (prepare_data.py).

Final Columns:
Country, Year, Expenditure, EmploymentRate_Females, EmploymentRate_Males, BachelorRate and MasterRate
Output File: education_analysis_dataset_clean.csv

I developed this project using Python with libraries such as dash, plotly and pandas. Dash is a productive Python framework for building web-based analytic applications with no need to write JavaScript. It allows creation of highly interactive dashboards. At the same time, Plotly is used for generating visually appealing and interactive charts (scatter plots, line charts, choropleth maps, bar charts).


#Running the Application
To run the dashboard locally it is necessary to install required libraries.

pip install dash plotly pandas

Then the following files must be in the same folder:

app.py (main script)
education_analysis_dataset_clean.csv (clean dataset)
assets/fondo.jpg (background image)

Finally, launch the server,  open a browser and go to http://127.0.0.1:8050
The dashboard runs on a local server and does not require deployment to the cloud, which simplifies setup for the presentation and review.

