# Techcrunch Incremental Scrapy Spider With MongoDB

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


