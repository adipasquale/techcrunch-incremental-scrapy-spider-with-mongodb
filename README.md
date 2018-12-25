# Techcrunch Incremental Scrapy Spider With MongoDB

This project is the support for this blog post : [Incremental crawler with Scrapy and MongoDB](https://blog.dipasquale.fr/en/2018/12/17/incremental-scraping-with-scrapy-and-mongo/)

## Local setup

```sh
pip3 install -r requirements.txt
```

Setup a local MongoDB server. On Mac OS X :

```sh
brew install mongodb
brew services start mongodb
```

## Run

```sh
scrapy crawl techcrunch -a limit_pages=2
```


