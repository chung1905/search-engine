# Search Engine

## What is this?
- A crawler ([scrapy](https://scrapy.org/)) which crawl data from
  [Wikipedia](https://en.wikipedia.org/) (and [dantri](https://dantri.com/),
  [vnexpress](https://vnexpress.com/))
- Store crawl data to json file and mongodb
- Import data to [Solr](https://lucene.apache.org/solr/)
- Final, a frontend provide an interface to search data from Solr
- Every service is packaged as Docker container 

## Requirements
1. [Docker](https://www.docker.com/)
2. [Docker-compose](https://docs.docker.com/compose/)
3. [Make](https://www.gnu.org/software/make/) (optional, usually pre-install on linux)

## How to use
### 1. Start and build all services
```
docker-compose up -d
```

### 2. See crawl process
```
make log_crawler
```
Or see in `./crawler/data`

### 3. Import crawled data to Solr:
```
make solr_import
```

### 4. Start/Stop crawling:
```
make start_crawl
```
and
```
make stop_crawl
```

### 5. Search:
See your search at: `http://<<frontend-container-ip>>:3000/`

Get frontend container ip by command:
```
docker inspect -f '{{.Name}} - {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(docker ps -aq) | grep frontend
```

### 6. Done

## Known Issues:

