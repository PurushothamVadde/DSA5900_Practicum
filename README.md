# Predicting Business Owners Response on Social Media Using Data Science Approach

## About the Project:
93% of customers will read reviews of local businesses to determine their quality(BrightLocal). Social media is filled with a lot of reviews there are thousands of reviews available for each business on social media and we can also see the responses from the business owners for the reviews given by the public. In this project, we will develop a Data science approach to determine what causes business owners to respond to a comment on social media and how likely is a business owner to respond to a comment about their firm.
The outcome of this project will help in providing the key insights about the motivations and actions of a business owner who respond to online reviews for their firms. Developing a machine learning-based model and researching the root causes of engagement by owners will also help to expose other interesting insights into the use of social media by the firms.

## Data Collection:
* In this step, we are going to collect the Yelp reviews given by the customer for the business and the other data related to Business and Customers through Web scraping.
* We are going to collect the data based on the input Category and cities.
	* **Example** : city = Oklahoma, Seattle, LosAngeles, NewYork, Miami, Palmbeach 
    * category = HVAC, Painters, Plumbing, AutoRepair, Tires, TransmissionRepair, Flooring, Handyman

### Steps to Execute the code for Data Collection through IDE(Pycharm)
* use git clone https://github.com/PurushothamVadde/DSA5900_Practicum.git command from git bash to copy the code repository into your system
	* #### Part1: Extracting Business URL	
		1. Navigate to Data_HTML_Tags/Input.json set the category and city values that you are looking to get business reviews(city = Oklahoma, category = HVAC).
		2. Add the city and category folders in Data_Business_URL_City_and_Category_Wise/{city}/{category}.
		3. Navigate to the Code_Webscraping folder and open the Extracting_Business_URL_with_Zipcode.py 
		4. run the code
		5. the Business URL is extracted based on zipcodes for selected city.
	* #### Part2: Extracting Business URL
		1. Navigate to Code_Webscraping folder and open the Business_URL_Duplicate_Removal.py 
		2. run the code
		3. Duplicate url's are removed and single file with business links are stored into Data_Business_URL_Links
	* #### Part3: Extracting Business Reviews Data
		1. Navigate to Code_Webscraping folder and open the Yelp_Business_Reviews_Data.py
		2. run the code
		3. The customer reviews data is stored into Data_Business_Reviews folder
		
### Steps to Execute the code for Data Collection through Jupyter Notebook
* use git clone https://github.com/PurushothamVadde/DSA5900_Practicum.git  command from git bash to copy the code repository into your system
	* #### Part1: Extracting Business URL	
		1. Navigate to Data_HTML_Tags/Input.json set the category and city values that you are looking to get business reviews(city = Oklahoma, category = HVAC).
		2. Add the city and category folders in Data_Business_URL_City_and_Category_Wise/{city}/{category}.
		3. Navigate to the Code_Webscraping_Notebook folder and open the Extracting_Business_URL_with_Zipcodes.ipynb 
		4. run the code
		5. the Business URL is extracted based on zipcodes for selected city and stored into Data_Business_URL_Links
	* #### Part2: Extracting Business Reviews Data
		1. Navigate to Code_Webscraping_Notebook folder and open the Yelp_Business_Reviews_Data.ipynb
		2. run the code
		3. The customer reviews data is stored into Data_Business_Reviews folder	
		
	
		
