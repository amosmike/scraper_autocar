# scraper_autocar
autocar scraper

## M7 T4
  docker build -t "imagename" --platform linux/x86_64 .
  
  docker run --platform linux/x86_64 "imagename"
  
  docker tag "Image_Id" "imagename"
  
  docker push "imagename"
  
 ## M7 T5
 Connect to EC2
 
 ssh -i <key-pair-name>.pem ec2-user@<public-dns>
 
 ssh -i autocarkey.pem ec2-user@ec2-18-168-199-1.eu-west-2.compute.amazonaws.com
  
 scp -i autocarkey.pem /Users/michaelamos/Documents/AICore/Autocar/autocar_scraper/data_pipeline13.py ec2-user@ec2-18-168-199-1.eu-west-2.compute.amazonaws.com:  
  
## M8 T1
sudo docker run --rm -d -p 9090:9090 --name prometheus -v /Users/michaelamos/Downloads/prometheus-2.36.2.darwin-amd64/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus --config.file=/etc/prometheus/prometheus.yml --web.enable-lifecycle

  For in prometheus.yaml
  static_configs:
  
    - targets: ["host.docker.internal:9090"]

## T2 EC2 
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
  
## EDIT PROM FILE HERE: (sudo nano) /root/prometheus.yml

global:
  scrape_interval: '15s'  # By default, scrape targets every 15 seconds.
  scrape_timeout: '10s'
  external_labels:
    monitor: 'codelab-monitor'

scrape_configs:

  # Prometheus monitoring itself
  - job_name: 'prometheus v2'
    scrape_interval: '10s'
    static_configs:
      - targets: ['localhost:9090', '18.168.199.1:9090']

  # OS monitoring
  - job_name: 'node'
    scrape_interval: '30s'
    static_configs:
      - targets: ['172.17.0.1:9100']

  # Docker monitoring
  - job_name: 'docker'
         # metrics_path defaults to '/metrics'
         # scheme defaults to 'http'.
    static_configs:
      - targets: ['172.17.0.1:9323'] # metrics address from our daemon.json file

## T4

https://grafana.com/docs/grafana/next/setup-grafana/installation/mac/

## Milestone 8 TODO;

Need node and engine_daemon queries,
Docker not reading correct prometheus.yml
