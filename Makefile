# SCRAPY = ~/.local/bin/scrapy
SCRAPY = /usr/local/bin/scrapy

# SPIDER = wikipedia_com
SPIDER = dantri_com
# CRAWL_OUTPUT = ./crawler/storage/$(SPIDER).json
CRAWL_OUTPUT = /Users/hahoang/Z_School/Search/crawl_out/$(SPIDER).json

crawl:
	rm -f ./crawler/$(CRAWL_OUTPUT)
	cd ./crawler && $(SCRAPY) crawl $(SPIDER) -o $(CRAWL_OUTPUT)
