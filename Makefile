SCRAPY = ~/.local/bin/scrapy

SPIDER = wikipedia_com
CRAWL_OUTPUT = ./crawler/storage/$(SPIDER).json

crawl:
	rm -f ./crawler/$(CRAWL_OUTPUT)
	cd ./crawler && $(SCRAPY) crawl $(SPIDER) -o $(CRAWL_OUTPUT)
