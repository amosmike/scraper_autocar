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
- Provide general information about your project here.
- What problem does it (intend to) solve?
- What is the purpose of your project?
- Why did you undertake it?
<!-- You don't have to answer all the questions - just the ones relevant to your project. -->


## Technologies Used
- Tech 1 - version 1.0
- Tech 2 - version 2.0
- Tech 3 - version 3.0


## Features
List the ready features here:
- Awesome feature 1
- Awesome feature 2

## Screenshots

## Setup

## Usage

## Project-status

## Room-for-improvement
- Node prometheus not working
- Make repeatable

## Acknowledgements

## Contact

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


