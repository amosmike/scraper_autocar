from re import L
from time import sleep
from tkinter import Y
from sqlalchemy import create_engine
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.chrome.service import Service
import pandas as pd
import requests
import boto3 
import math
import json
import uuid
import yaml
import os 

# os.environ['GH_TOKEN']= "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" # Expires Fri, Jul 1 2022. 

# Test
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# import test_product_2

class Scraper:

    '''
    This class is a scraper that works only for scraping the Autocar website 

    Attributes:
        URL (str): The webpage url
        ...
        (list all the things in __init__ method.)   
    
    
    '''

    def __init__(self, URL: str): # postcode: str, make: str, model: str, number_cars: int): # initialize driver, url
        self.truncate_opt()
        self.postcode = "CH646SE" # input('Postcode? \n')
        self.make = "SEAT" # input('Make of car to scrape? \n')
        self.model = "Ibiza" # input('Model of car to scrape? \n')
        self.number_cars = 3 # int(input('How many cars would you like to scrape? \n'))

        os.environ['GH_TOKEN']= self.git_token() # Expires Fri, Jul 1 2022. 

        ### DRIVER ###
        
            # Safari
        # self.driver = webdriver.Safari()

            # Chrome
        # options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
        # options.add_argument("--window-size=1920,1080")
        # options.add_argument("--remote-debugging-port=9222")
        # options.add_argument("user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005 Safari/537.36'")
        # self.driver = webdriver.Chrome(options=options)

            # Firefox
        options = webdriver.FirefoxOptions()
        # options.binary_location = r"C:/location/to/Firefox/Binary/firefox.exe"
        options.add_argument('--headless')
        # self.driver = webdriver.Firefox(options=options)
        
        ###

        # options = webdriver.FirefoxOptions()
        # options.add_argument('--headless')
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
        # options.add_argument("--window-size=1920,1080")
        # options.add_argument("--remote-debugging-port=9222")
        self.driver = Firefox(service = Service(GeckoDriverManager().install()), options=options)

        self.driver.get(URL)
        self.driver.maximize_window() # Maximize webpage

        sleep(2)

    def scrape(self):
        self._load_and_accept_cookies() # Private
        self._input_postcode(self.postcode) # Public 
        self._find_dropdownbox_and_select('//*[@id="make"]', self.make) # Public 
        self._find_dropdownbox_and_select('//*[@id="model"]', self.model) # Public 
        self._click_search() # Make private 
        self.car_data = self._makes_dict(self.number_cars)


    def gen_engine(self, creds = 'RDS_creds.yaml'): 

        with open(creds, 'r') as f:
            creds = yaml.safe_load(f)

        DATABASE_TYPE = creds['DATABASE_TYPE']
        DBAPI = creds['DBAPI']
        ENDPOINT = creds['ENDPOINT']
        USER = creds['USER']
        PASSWORD = creds['PASSWORD']
        PORT = creds['PORT']
        DATABASE = creds['DATABASE']
        
        engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")
        engine.connect() 

        return engine

    def git_token(self, token = 'geckodriver_token.yaml'): 

        with open(token, 'r') as t:
            token = yaml.safe_load(t)

        TOKEN = token['TOKEN']

        return TOKEN

    def truncate_tables(self, table_name):
        engine = self.gen_engine()
        engine.execute(f'''
        TRUNCATE TABLE {table_name}; 
        ''')

    def load_records(self):
        
        engine = self.gen_engine()

        df_scraped_id = pd.read_sql_query('SELECT id FROM car_dataset', engine)
        scraped_id_list = df_scraped_id['id'].values.tolist()

        return scraped_id_list

    def _load_and_accept_cookies(self):

        '''
        This fuction removes cookies if on separate frame.

        Attributes:
        ----------
        NONE

        Returns:
        NONE 
        
        '''

        try:
            self.driver.switch_to.frame('sp_message_iframe_576092') # This is the id of the frame
            accept_cookies_button = self.driver.find_element(By.XPATH, '//*[@id="notice"]/div[3]/div[2]/button[2]')
            accept_cookies_button.click()
            self.driver.switch_to.default_content()

        except:
            print("Pas cookies") #pass # If there is no cookies button, we won't find it, so we can pass
            pass # If there is no cookies button, we won't find it, so we can pass

        sleep(1)

    def _input_postcode(self, postcode: str): 

        '''
        
        Fuctions that finds text input box 'postcode' and types postcode attibute

        Attributes:
        -----------
        postcode: str

        Returns
        -------
        NONE
        
        '''

        postcode_bar = self.driver.find_element(By.XPATH, '//*[@id="postcode"]')
        postcode_bar.click()
        postcode_bar.send_keys(postcode)
        sleep(2)

    def _find_dropdownbox_and_select(self, dropdown_XPATH: str, selection: str): 
        '''
        
        Fuctions that finds dropdown box, print options, and selects selection atttribute

        Attributes:
        -----------
        dropdown_XPATH: str
        selection: str

        Returns
        -------
        NONE
        
        '''

        options_list = []

        # Find make button and select make
        dropdown_box = self.driver.find_element(By.XPATH, dropdown_XPATH)

        try: 
            option_container = self.driver.find_element(By.XPATH, dropdown_XPATH + '/optgroup[2]')
        except:
            option_container = self.driver.find_element(By.XPATH, dropdown_XPATH)

        children = option_container.find_elements(By.XPATH, "./child::*")
        for i in children:
            options_list.append(i.text)

        # print(options_list)

        dd = Select(dropdown_box)
        sleep(1)
        # <option value="SEAT">SEAT (8,747)</option> 
        dd.select_by_value(selection)
        sleep(2)

        try: 
            dd.select_by_value(selection)
        except: 
            pass

        print(f"Selected {selection}")

        sleep(1)

    def _click_search(self):
        search = self.driver.find_element(By.XPATH, '//*[@id="content"]/div/header/div[2]/div/div/form/div[2]/div[2]/button')
        search.click()

        try:
            search.click()
        except:
            pass
        
        sleep(1)

    def _get_page_links(self):

        '''

        Fuction that retrieves links from container on webpage

        Attributes:
        -----------
        NONE

        Returns
        -------
        list
            The links found from container on webpage
        
        '''

        link_list = []
        link_count = 0

        try: 
            link_container = self.driver.find_element(By.XPATH, '//*[@id="content"]/div/div[2]/ul') #Gets Xpath of all properties on page ## Make sure XPath is still valid 

        except: 
            link_container = self.driver.find_element(By.XPATH, '//*[@id="content"]/div/div/div[2]/ul') #Gets Xpath of all properties on page ## Make sure XPath is still valid 

        car_list = link_container.find_elements(By.XPATH, './*[@class="search-page__result"]') 


        for car in car_list: # Takes the big list of <div>s to different properties individually 
            
            try:
                a_tag_list = car.find_elements(By.XPATH, './/a') 
                a_tag = a_tag_list[2]

                link = a_tag.get_attribute('href')
                link_list.append(link) # Gets each link and puts it into link_list
                
                link_count += 1
                print("Link " + str(link_count) + " found")
                
            except: 
                link_count += 1
                print("Link " + str(link_count) + " NOT found")  

        return link_list

    def _get_all_links(self):

        '''
        
        Fuctions that combines all links found through multiple pages into one big list of links. 

        Attributes:
        -----------
        NONE

        Returns
        -------
        list
            list of links found throughout paes 
        
        '''

        # Retreive all cars on page

        big_list = []
        page_count = 1

        for page in range(math.ceil(self.number_cars/9)): # Number of pages calculated from number of cars wanted assuming each page gives 10 links
            
            print("Start of page " + str(page_count))
            big_list.extend(self._get_page_links()) # Call the function and extend the big list with the returned list

            # Click the next button. 
            next_button_list = ['//*[@id="content"]/div/div[3]/nav/ul/li[8]/a', '//*[@id="content"]/div/div/div[3]/nav/ul/li[8]/a/i',
            '//*[@id="content"]/div/div/div[3]/nav/ul/li[9]/a/i', '//*[@id="content"]/div/div/div[3]/nav/ul/li[10]/a/i']

            for next in next_button_list:
                try:
                    next_button = self.driver.find_element(By.XPATH, next)
                    next_button.click()
                
                except:
                    pass

            print("Page: " + str(page_count) + " complete")
            page_count += 1

            sleep(3)

            try:
                close_popup = self.driver.find_element(By.XPATH, '//*[@id="close"]')
                close_popup.click()
                print("Popup removed, page: " + str(page_count))

            except:
                pass # If there is no cookies button, we won't find it, so we can pass

        sleep(1)

        return big_list

    def _makes_dict(self, number_cars):

        '''
        
        Fuctions that scrapes the information from list of links and puts information into dictionary. 

        Attributes:
        -----------
        NONE

        Returns
        -------
        dict

        
        '''

        car_data = {'uuid': [], 'id': [], 'Name': [], 'Link': [], 'Picture': [], 'Price': [], 'Year': [], 'Miles': []}

        count = 0

        big_list = self._get_all_links()
        scraped_id_list = self.load_records()

        for link in big_list[:number_cars]:

            if link == ' ':
                continue            

            else:
                try:
                    self.driver.get(link)
                    sleep(1) 
                except:
                    pass
            
                ## Visit all the links, and extract the data if not already in SQL. 

                try:
                    name = self.driver.find_element(By.XPATH, '//*[@id="layout-desktop"]/aside/section[2]/h1').text

                except:
                    name = "UNKNOWN"

                try: 
                    picture_tag = self.driver.find_element(By.TAG_NAME, 'img')
                    picture = picture_tag.get_attribute('src')

                except: 
                    print("no piccy :(")

                try:
                    price = self.driver.find_element(By.XPATH, '//*[@id="layout-desktop"]/aside/section[2]/div[1]/div[1]/h2').text

                except:
                    price = "UNKNOWN"
                    print("Price Unknown")

                try:
                    year = self.driver.find_element(By.XPATH, '//*[@id="layout-desktop"]/aside/section[2]/p[1]').text

                except:
                    year = "UNKNOWN"
                    print("Year Unknown")

                try:
                    miles = self.driver.find_element(By.XPATH, '//*[@id="layout-desktop"]/article/section[2]/span[1]/span[3]').text

                except:
                    miles = "UNKNOWN"
                    print("Miles Unknown")
                    
                id = name + " " + year + " " + miles 
                
                if id in scraped_id_list:
                    print(f"{id} already scraped")
                    count += 1
                    print("Finished link " + str(count))
                    continue

                car_data['uuid'].append(uuid.uuid4().urn)
                car_data['id'].append(id)
                car_data['Name'].append(name) 
                car_data['Link'].append(link)
                car_data['Price'].append(price)
                car_data['Picture'].append(picture)
                car_data['Year'].append(year)
                car_data['Miles'].append(miles)
                
                # Saves picture locally 
                # os.mkdir(r'/Users/michaelamos/Documents/AICore/Autocar/autocar_scraper/car_pictures') 
                # img = urllib.request.urlretrieve(picture, str(id)+ ".jpg")
                # # img = urllib.request.urlretrieve(picture, str(id) + "_" + str(count) + ".jpg")
                # os.chdir(r'/Users/michaelamos/Documents/AICore/Autocar/autocar_scraper')

                # TODO save pictures in EC2/ dockerfile? 

                count += 1
                print("Finished link " + str(count))

                sleep(1)

        return car_data

    def upload_to_S3(self, path):
        '''
        Function that uploads files in path to S3 bucket
        
        '''
        s3_client = boto3.client('s3')
        os.chdir(path) # Google os methods to see other capabilities 
        # s3_client.upload_file(file_name, bucket, object_name)
        s3_client.upload_file('data.json', 'autotrader-data-bucket', 'car_data.json')

    def uploadDirectoryS3(self, path, bucketname):
        '''
        Function that uploads files and images in path to S3 bucket
        
        '''

        s3 = boto3.client('s3')
        path = '/Users/michaelamos/Documents/AICore/Practice/autotrader/car_pictures'
        bucketname = 'autotrader-data-bucket'
        for root,dirs,files in os.walk(path):
            for file in files:
                s3.upload_file(os.path.join(root,file), bucketname, file)

    def _download_from_s3(self): 
        url = 'https://autotrader-data-bucket.s3.eu-west-2.amazonaws.com/car_data.json'
        os.mkdir(r'/Users/michaelamos/Documents/AICore/Autocar/autocar_scraper/downloads')

        response = requests.get(url)
        with open('car_data.json', 'wb') as f:
            f.write(response.content)

    def upload_to_RDS(self, database_type: str = 'postgresql', dbapi: str = 'psycopg2', endpoint: str = 'aicoredb.cfomrz1jyxe6.eu-west-2.rds.amazonaws.com', 
    user: str = 'postgres', password: str = 'password', port: int = 5432, database: str = 'postgres'): 

        '''

        This fuction creates engine that can be used to upload database to RDS.

        Attributes:
        ----------
        database_type: str 
        dbapi: str
        endpoint: str 
        user: str
        password: str
        port: int
        database: str

        Returns:
        -------
        engine 

        '''

        engine = self.gen_engine()
        
        df = pd.DataFrame(self.car_data)
        df.head()

        df.to_sql('car_dataset', engine, if_exists='append') # append
        df2 = pd.read_sql_table('car_dataset', engine)
        df2.head()
        
        return

    def save_as_JSON(self, path):
        '''
        Function runs scraper and saves dictionary locally as JSON
        '''
        # os.mkdir(r'raw_data')
        os.chdir(path) # Google os methods to see other capabilities 
        with open('data.json', 'w') as f: # 'w' is write mode, 'f' is file
            json.dump(self.car_data, f)

    def truncate_opt(self):
        ans = input("Truncate previous data? (Y/N) \n")

        if ans in ['Y', 'y']:
            self.truncate_tables('car_dataset') # Truncate data?
            print('truncated')
        elif ans in ['N', 'n']:
            pass
        else: 
            print('try again')
            self.truncate_opt()
        

if __name__ == "__main__":

    # Run test file
    # suite = unittest.TestLoader().loadTestsFromModule(test_product_2)
    # unittest.TextTestRunner(verbosity=2).run(suite)

    autocar_scraper = Scraper("https://www.autotrader.co.uk") #, "CV326JA", "SEAT", "Ibiza", 5) # Public
    autocar_scraper.scrape()


        # Upload to RDS #
    autocar_scraper.upload_to_RDS('postgresql', 'psycopg2', 'aicoredb.cfomrz1jyxe6.eu-west-2.rds.amazonaws.com', 
    'postgres', 'password', 5432, 'postgres')  # Saves car data to RDS # User could input their details

        # Write to json
    autocar_scraper.save_as_JSON('raw_data')

        # Save locally as JSON #
    # autocar_scraper.save_as_JSON('/Users/michaelamos/Documents/AICore/Practice/autotrader/raw_data') # Saves car data to JSON # User could input their details
    
        # Upload to S3 # 
    # autocar_scraper.upload_to_S3('/Users/michaelamos/Documents/AICore/Practice/autotrader/raw_data') # Saves car data to S3 # User could input their details
    # autocar_scraper.uploadDirectoryS3('/Users/michaelamos/Documents/AICore/Practice/autotrader/car_pictures', 'autotrader-data-bucket')
    
        # Quiz driver #
    autocar_scraper.driver.quit()