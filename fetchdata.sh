wget "https://covid.ourworldindata.org/data/owid-covid-data.csv" -O owid-covid-data.csv
wget "https://pomber.github.io/covid19/timeseries.json" -O timeseries.json 
wget "https://raw.githubusercontent.com/covid19india/api/gh-pages/raw_data.json" -O raw_data.json
git clone https://github.com/datameet/covid19
wget "https://api.rootnet.in/covid19-in/hospitals/medical-colleges" -O medical-colleges.json
wget "https://api.rootnet.in/covid19-in/hospitals/beds" -O beds.json
echo "Done"
