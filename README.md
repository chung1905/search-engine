# Search Engine
## Requirements
1. [Docker](https://www.docker.com/)
2. [Make](https://www.gnu.org/software/make/)
3. [nodejs](https://nodejs.org/en/) and [npm](https://www.npmjs.com/)
4. [python](https://www.python.org/) and [pip](https://pypi.org/project/pip/)

## How to setup for the first time
1. Mongodb
```
make mongo_start
```
Mongodb interface at: http://localhost:8081/

2. Install scrapy:
```
make setup
```
3. Crawl:
```
make crawl_to_json
```
4. Solr:
```
make solr_start solr_core_create solr_import
```
5. Frontend:
```
make npm_install npm_start
```
6. Go to http://localhost:3000/ and search

## How to run
1. Start solr and frontend server:
```
make solr_start npm_start
```

## Known Issues:
1. Cannot crawl after setup
