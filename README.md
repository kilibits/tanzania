This repository is an extension of/built on top of https://github.com/everypolitician-scrapers/tanzania


TO RUN SCRAPPER:

Install pre-requisites

```pip install -r requirements.txt```

To run script

```python <script name>```


To run the API server

Pre-requisites : Install Golang(https://golang.org), install gin framework(https://gin-gonic.github.io/gin/)

```go run api.go```

visit ```localhost:8080/profiles``` to assert API server is running

Any problems should be submitted to issues, and any contributions should be submitted through pull requests


TODO

Scrappers:

1. Scrap for questions, supplementary questions, and contributions for every member of parliament
2. Migrate to Postgres


API:

1. Add new GET methods
2. Rename GET functions and routes
