# heatmaster

Connect to Heatmaster boiler web interface
returns the data as json

To run:
docker build -t heatmater .
docker run -p 5000:5000 -e boilerip=<your ip> heatmaster:latest
  
The connect to your boilerip:5000
  
the data will be returned in json format
