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
  
 scp -i autocarkey.pem /Users/michaelamos/Documents/AICore/Autocar/autocar_scraper/data_pipeline13.py ec2-user@ec2-18-168-199-1.eu-west-2.compute.amazonaws.com:  
  
## M8 T1
sudo docker run --rm -d -p 9090:9090 --name prometheus -v /Users/michaelamos/Downloads/prometheus-2.36.2.darwin-amd64/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus --config.file=/etc/prometheus/prometheus.yml --web.enable-lifecycle

  For in prometheus.yaml
  static_configs:
  
    - targets: ["host.docker.internal:9090"]

## T2 EC2 
sudo docker run --rm -d -p network=host --name prometheus -v /Users/michaelamos/Downloads/prometheus-2.36.2.darwin-amd64/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus prom/prometheus --config.file=/etc/prometheus/prometheus.yml --web.enable-lifecycle

- targets: ['localhost:9090']
