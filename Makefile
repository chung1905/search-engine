DOCKER_SOLR = docker-compose exec solr
DOCKER_SOLR_BIN = $(DOCKER_SOLR) /opt/solr/bin/solr
DOCKER_SOLR_POST = $(DOCKER_SOLR) /opt/solr/bin/post
SOLR_CORE_NAME = solr_core

solr_import:
	$(DOCKER_SOLR_POST) -c $(SOLR_CORE_NAME) /var/crawler
solr_core_create:
	$(DOCKER_SOLR_BIN) create_core -c $(SOLR_CORE_NAME)
solr_core_delete:
	$(DOCKER_SOLR_BIN) delete -c $(SOLR_CORE_NAME)
solr_reimport: solr_core_delete solr_core_create solr_import

stop_crawl:
	docker-compose stop scrapy
start_crawl:
	docker-compose start scrapy
log_crawler:
	docker-compose logs -f --tail=100 scrapy
