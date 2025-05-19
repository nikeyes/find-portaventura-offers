TODAY=$(shell date +'%Y-%m-%d')
TODAY_WITHOUT_DASHES=$(shell date +'%Y%m%d')
DATE_END=2026-01-10
MAX_OFFERS=10
# FILE_HOTELS=downloaded_data/hotels_$(TODAY_WITHOUT_DASHES)_a3_c3_2_7_11.json
# FILE_HOTELS=downloaded_data/hotels_$(TODAY_WITHOUT_DASHES)_a2_c2_7_11.json
FILE_TICKETS=downloaded_data/tickets_$(TODAY_WITHOUT_DASHES).json

.PHONY: test
test:
poetry run pytest -v -m "not integration_tests" --cov=src --no-cov-on-fail --cov-report=term-missing --approvaltests-use-reporter='PythonNativeReporter'  --approvaltests-add-reporter="code" --approvaltests-add-reporter-args="--diff" tests/
# poetry run pytest -v --cov=src --no-cov-on-fail --cov-report=term-missing --approvaltests-use-reporter='PythonNativeReporter'  --approvaltests-add-reporter="code" --approvaltests-add-reporter-args="--diff" tests/
# poetry run pytest -v --cov=src --no-cov-on-fail --cov-report=term-missing tests/

.PHONY: download
download: test
	poetry run python src/main.py download-rates --date-ini $(TODAY) --date-end $(DATE_END) --adults 2 --children 3 --children-ages 2,8,11
	poetry run python src/main.py download-rates --date-ini $(TODAY) --date-end $(DATE_END) --adults 3 --children 3 --children-ages 2,8,11
	poetry run python src/main.py download-rates --date-ini $(TODAY) --date-end $(DATE_END) --adults 1 --children 0 

.PHONY: find
find:
	poetry run python src/main.py find-offers --hotel-prices $(FILE_HOTELS) --ticket-prices $(FILE_TICKETS) --date-end $(DATE_END) --max-offers $(MAX_OFFERS)

.PHONY: find_a1
find_a1:
	poetry run python src/main.py find-offers --hotel-prices downloaded_data/hotels_$(TODAY_WITHOUT_DASHES)_a1.json --ticket-prices $(FILE_TICKETS) --date-end $(DATE_END) --max-offers $(MAX_OFFERS)
		
.PHONY: find_a2
find_2:
	poetry run python src/main.py find-offers --hotel-prices downloaded_data/hotels_$(TODAY_WITHOUT_DASHES)_a2_c3_2_8_11.json --ticket-prices $(FILE_TICKETS) --date-end $(DATE_END) --max-offers $(MAX_OFFERS)

.PHONY: find_a3
find_3:
	poetry run python src/main.py find-offers --hotel-prices downloaded_data/hotels_$(TODAY_WITHOUT_DASHES)_a3_c3_2_8_11.json --ticket-prices $(FILE_TICKETS) --date-end $(DATE_END) --max-offers $(MAX_OFFERS)

# .PHONY: find_and_send
# find_and_send:
# 	poetry run python src/main.py find-offers --hotel-prices $(FILE_HOTELS) --ticket-prices $(FILE_TICKETS) --date-end $(DATE_END) --max-offers $(MAX_OFFERS) --emails evamoga@gmail.com  
