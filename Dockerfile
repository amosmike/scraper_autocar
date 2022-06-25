# Run Selenium in a Docker Container

# '''
# These are the steps you have to follow to create the Dockerfile. For each of the steps, you have to figure out what Dockerfile instructions you have to use for each step


# 1. Pull a Python image. For example, python:3.8 will do the job

# 2. Adding trusting keys to apt for repositories, you can download and add them using the following command:
# `wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -`

# 3. Add Google Chrome. Use the following command for that
# `sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'`

# 4. Update apt:
# `apt-get -y update`

# 5. And install google chrome:
# `apt-get install -y google-chrome-stable`

# 6. Now you need to download chromedriver. First you are going to download the zipfile containing the latest chromedriver release:

# ```
# wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
# ```

# 7. You downloaded the zip file, so you need to unzip it:

# ```
# apt-get install -yqq unzip

# unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
# ```

# 8. Copy your application in a Docker image

# 9. Install your requirements

# 10. Run your application

###############

# FROM ubuntu:18.04


# # Creat Dockerfile for Chrome to use Selenium
# RUN apt-get -y update &&\
#     # apt install -y wget &&\
#     apt-get install -y chromium-browser &&\
#     # wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - &&\
#     sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' &&\
#     apt-get -y update &&\
#     apt-get install -y google-chrome-stable &&\
#     #install chromedriver
#     wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip &&\
#     apt-get install -yqq unzip &&\
#     unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# # Set display port
# ENV DISPLAY=:99
# # Copy local files
# COPY . .
# # Install dependencies
# RUN pip install -r ./requirements.txt
# # Define entrypoint 
# # ENTRYPOINT ["python", "data_pipeline12.py"]?
# CMD ["python", "data_pipeline12.py"]

###############

# FROM python:3.9

# #download & install google chrome
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - &&\
#     sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' &&\
#     apt-get -y update &&\
#     apt-get install -y google-chrome-stable &&\
#     #install chromedriver
#     wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip &&\
#     apt-get install -yqq unzip &&\
#     unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# #set display port to avoid crash
# ENV DISPLAY=:99
# #copy local files
# COPY . .
# #install dependencies
# RUN pip install -r ./requirements.txt
# #

##############

FROM python:3.9


# Update the system and install firefox
RUN apt-get update  
RUN apt -y upgrade 
RUN apt-get install -y firefox-esr
RUN /usr/local/bin/python -m pip install --upgrade pip

# get the latest release version of firefox 
RUN latest_release=$(curl -sS https://api.github.com/repos/mozilla/geckodriver/releases/latest \
    | grep tag_name | sed -E 's/.*"([^"]+)".*/\1/') && \
    # Download the latest release of geckodriver
    wget https://github.com/mozilla/geckodriver/releases/download/$latest_release/geckodriver-$latest_release-linux32.tar.gz \
    # extract the geckodriver
    && tar -xvzf geckodriver* \
    # add executable permissions to the driver
    && chmod +x geckodriver \
    # Move gecko driver in the system path
    && mv geckodriver /usr/local/bin

COPY . . 

RUN pip install -r requirements.txt

CMD ["python", "data_pipeline13.py"]
