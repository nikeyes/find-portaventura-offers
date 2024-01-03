TODAY=$(shell date +'%Y-%m-%d')
TODAY_WITHOUT_DASHES=$(shell date +'%Y%m%d')
DATE_END=2025-01-09
MAX_OFFERS=30
FILE_HOTELS=downloaded_data/hotels_$(TODAY_WITHOUT_DASHES)_a2_c2_6_10.json
FILE_TICKETS=downloaded_data/tickets_$(TODAY_WITHOUT_DASHES).json

.PHONY: test
test:
	poetry run pytest -v --cov=src --no-cov-on-fail --cov-report=term-missing --approvaltests-use-reporter='PythonNativeReporter'  --approvaltests-add-reporter="code" --approvaltests-add-reporter-args="--diff" tests/
#	poetry run pytest -v --cov=src --no-cov-on-fail --cov-report=term-missing tests/

.PHONY: download
download: test
	poetry run python src/main.py download-rates --date-ini $(TODAY) --date-end $(DATE_END) --adults 2 --children 2 --children-ages 6,10

.PHONY: find
find:
	poetry run python src/main.py find-offers --hotel-prices $(FILE_HOTELS) --ticket-prices $(FILE_TICKETS) --date-end $(DATE_END) --max-offers $(MAX_OFFERS)

.PHONY: find_and_send
find_and_send:
	poetry run python src/main.py find-offers --hotel-prices $(FILE_HOTELS) --ticket-prices $(FILE_TICKETS) --date-end $(DATE_END) --max-offers $(MAX_OFFERS) --emails nikey_es@yahoo.es,evamoga@gmail.com  

