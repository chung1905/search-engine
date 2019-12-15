SCRAPY = ~/.local/bin/scrapy

SPIDER = wikipedia_com

crawl:
	cd ./crawler && $(SCRAPY) crawl $(SPIDER)

CRAWL_OUTPUT = ./crawler/storage/$(SPIDER).json
crawl_to_json:
	rm -f ./crawler/$(CRAWL_OUTPUT)
	cd ./crawler && $(SCRAPY) crawl $(SPIDER) -o $(CRAWL_OUTPUT)

mongo_start: mongodb_start mongo_express_start
mongo_stop: mongo_express_stop mongodb_stop

DOCKER_SOLR_NAME = search-solr
DOCKER_SOLR_BIN = docker exec -it $(DOCKER_SOLR_NAME) /opt/solr/bin/solr
DOCKER_SOLR_POST = docker exec -it $(DOCKER_SOLR_NAME) /opt/solr/bin/post
SOLR_CORE_NAME = solr_first_core
solr_start: network_create
	docker run --rm -d --name $(DOCKER_SOLR_NAME) \
	-v `pwd`/crawler/crawler/storage:/opt/crawler \
	--network=$(NETWORK_NAME) \
	-p 8983:8983 \
	solr:8
solr_stop:
	docker stop $(DOCKER_SOLR_NAME)
solr_import:
	$(DOCKER_SOLR_POST) -c $(SOLR_CORE_NAME) /opt/crawler/
solr_core_create:
	$(DOCKER_SOLR_BIN) create_core -c $(SOLR_CORE_NAME)
solr_core_delete:
	$(DOCKER_SOLR_BIN) delete -c $(SOLR_CORE_NAME)

DOCKER_MONGO_NAME = search-mongo
mongodb_start: network_create
	docker run --rm -d --name $(DOCKER_MONGO_NAME) \
	--network=$(NETWORK_NAME) --ip=10.3.0.6 \
	-v `pwd`/mongo/data:/data/db \
	mongo:4.2
mongodb_stop:
	docker stop $(DOCKER_MONGO_NAME)

DCOKER_MONGO_EXPRESS_NAME = search-mongo-express
mongo_express_start:
	docker run --rm -d -p 8081:8081 --network=$(NETWORK_NAME) \
	--name $(DCOKER_MONGO_EXPRESS_NAME) \
	-e ME_CONFIG_MONGODB_SERVER=$(DOCKER_MONGO_NAME) \
	mongo-express:latest
mongo_express_stop:
	docker stop $(DCOKER_MONGO_EXPRESS_NAME)

NETWORK_NAME = search-network
network_create:
	docker network create --subnet=10.3.0.0/16 $(NETWORK_NAME) && touch network_create
network_remove:
	rm -f network_create
	docker network rm $(NETWORK_NAME)

setup: install_python_module
install_python_module:
	pip install --user scrapy pymongo
