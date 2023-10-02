# find-portaventura-offers
Find best days to visit Portaventura

## Download prices
```bash
poetry run python portaventura_offers_cli.py download-rates --date-ini 2023-10-02 --date-end 2023-10-05 --adults 2 --children 2 --children-ages 6,10 
```

```bash
poetry run python portaventura_offers_cli.py download-rates --date-ini 2023-10-02 --date-end 2023-10-05
```

## find offers in download prices
```bash
poetry run python portaventura_offers_cli.py find-offers --data-path downloaded_data/20231002.json
```