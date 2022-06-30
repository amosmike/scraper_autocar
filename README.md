# Website Scraper - Autocar
> In this repositry it's possible to use the code to scrape the Autocar website for the car of your choice,in the quantity of your choice. The scraper will then gather the: name, year, number of miles, price, picture, the link for the car, and it will also assign this row of information with a user friendly ID and a uuid. This infomation can then be exported locally into a json file and uploaded to S3 or RDS. 

> Live demo [_here_](https://www.example.com). <!-- If you have the project hosted somewhere, include the link here. -->

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Screenshots](#screenshots)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)
* [Lessons Learnt](#lessons-learnt)
<!-- * [License](#license) -->


## General Information
- Project gathes car data for the intention of quickly getting a real world value of a car of a particular make, age, and milage.
- I undertook this project as I'd like to sell my car and wanted to eaily find what the market price for cars with similar specs were. 

<!-- - Provide general information about your project here.
- What problem does it (intend to) solve?
- What is the purpose of your project?
- Why did you undertake it?
You don't have to answer all the questions - just the ones relevant to your project.  -->

## Technologies Used
- selenium==4.1.5
- sqlalchemy==1.4.32
- webdriver-manager==3.7.0
- pandas==1.4.2
- boto3==1.24.12
- PyYAML # Installs yaml
- psycopg2==2.9.3  
- Docker 
- Prometheus
- Gafana

## Features
List the ready features here:
- Scraped will check data scraped isn't already stored in RDS
- Option to truncate RDS

## Screenshots

## Setup
> In order to use this directory you must add in a Git Token and the details for your RDS database, templates provided.

## Usage
> To run the scraper, you can pull the docker image using: docker pull amosmichael/data_pipeline13 and run docker run docker run --platform linux/x86_64 amosmichael/data_pipeline13.

## Project-status
> Finished, but continuously improving

## Room-for-improvement
- Node prometheus not working
- Make repeatable

## Acknowledgements
- AICore instructors for their guidance

## Contact
- See my github overview for contact details.

<!--

## Lessons Learnt 

 - M7 T4
  docker build -t "imagename" --platform linux/x86_64 .
  
  docker run --platform linux/x86_64 "imagename"
  
  docker tag "Image_Id" "imagename"
  
  docker push "imagename"
  
 - M7 T5
 Connect to EC2
 
 ssh -i <key-pair-name>.pem ec2-user@<public-dns>
 
 ssh -i autocarkey.pem ec2-user@ec2-18-168-199-1.eu-west-2.compute.amazonaws.com
  
 scp -i autocarkey.pem /Users/michaelamos/Documents/AICore/Autocar/autocar_scraper/data_pipeline13.py ec2-user@ec2-18-168-199-1.eu-west-2.compute.amazonaws.com:  
  
 - M8 T1
  sudo docker run --rm -d -p 9090:9090 --name prometheus -v /Users/michaelamos/Downloads/prometheus-2.36.2.darwin-amd64/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus --config.file=/etc/prometheus/prometheus.yml --web.enable-lifecycle

  For in prometheus.yaml
  static_configs:
  
    - targets: ["host.docker.internal:9090"]

 - T2 EC2 
  sudo docker run --rm -d -p 9090:9090 --name prometheus -v /home/ec2-user/prometheus.yml prom/prometheus --config.file=/etc/prometheus/prometheus.yml --web.enable-lifecycle

  curl -X POST http://localhost:9090/-/reload
  
- targets: ['localhost:9090']
  
  EC2 IP: 172.17.0.1
  
{
  "metrics-addr" : "172.17.0.1:9323",
  "experimental": true,
  "features": {
  "buildkit": true
  }
}
  
  
  EDIT PROM FILE HERE: (sudo nano) /root/prometheus.yml

global:
  scrape_interval: '15s'  # By default, scrape targets every 15 seconds.
  scrape_timeout: '10s'
  external_labels:
    monitor: 'codelab-monitor'

scrape_configs:

  'Prometheus monitoring itself'
  - job_name: 'prometheus v2'
    scrape_interval: '10s'
    static_configs:
      - targets: ['localhost:9090', '18.168.199.1:9090']

  'OS monitoring'
  - job_name: 'node'
    scrape_interval: '30s'
    static_configs:
      - targets: ['172.17.0.1:9100']

  'Docker monitoring'
  - job_name: 'docker'
         - 'metrics_path defaults to '/metrics''
         - 'scheme defaults to 'http'.'
    static_configs:
      - targets: ['172.17.0.1:9323'] # metrics address from our daemon.json file

- T4

https://grafana.com/docs/grafana/next/setup-grafana/installation/mac/

-->
