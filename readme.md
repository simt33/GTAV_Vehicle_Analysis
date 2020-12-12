A brief webscraping portfolio project which uses the requests library to scrape a json document from a website - 
'gtabase.com' containing GTAV vehicle details and statistics. 

This is then manipulated in Pandas and saved to an Excel file for visualisation in Tableau.

You can find the visualisation at: 
https://public.tableau.com/profile/simon.tunmore#!/vizhome/GTAVVehicleComparisonTool/VehiclesDashboard

Improvements & acknowledgments:

The attached code is manually run to output this data. In a production environment, I would want to automate a script like
this using something like CRON or Airflow, so that the data could be kept more up-to-date without manual input. 
If this were the case, I would also likely adapt this code using psycopg2 or similar to output the dataframe into a
Data Warehouse, which would further improve the workflow and accessibility to this data.

There are some issues within the source data which should be highlighted:
1. There are a number of redundant/null values for many of the fields provided. This is likely due to the fairly
inconsistent state of vehicles in the game at the moment, which fill a number of functions and roles. I have not included 
the majority of these in the analysis as the outcomes would be largely meaningless for comparison.

2. The stated fields of speed, acceleration, braking and weight are not well labelled in the source data, and so the 
numerical equivalence of these values is somewhat dubious. In a real dataset I would want more clarity on how these are 
measured, and in what terms.

3. Equally, the overall rating value is provided separately within the dataset (and not calculated internally). I am 
therefore not entirely sure how this has been calculated. In another instance it would be perhaps easier to calculate
this separately so that the criteria and ranges can be fully explained.

4. A very small number of vehicles belong to multiple categories, for example emergency and boat. This complicates the 
analysis somewhat, but for such a small number of vehicles it might be easier to classify these by their primary function.
Similarly it could be advantageous to group together some of these categories (such as 'Sports' and 'Sports Classic), but 
my concern would be for a loss of granular detail.

Many thanks to gtabase.com for this source data.
