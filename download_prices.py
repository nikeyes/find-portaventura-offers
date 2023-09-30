from datetime import datetime, timedelta
import requests
import json
from rich.progress import Progress
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)


date_ini = datetime(2023, 10, 1)
date_end = datetime(2023, 10, 4)

# Definir el paso (en este caso, un día)
step = timedelta(days=1)

# Iterar a través del intervalo de fechas
current_date = date_ini
num_days = (date_end-date_ini).days + 1
result = {}

progress_columns = (
            SpinnerColumn(),
            "[progress.description]{task.description}",
            BarColumn(),
            TaskProgressColumn(),
            "Elapsed:",
            TimeElapsedColumn(),
            "Remaining:",
            TimeRemainingColumn(),
        )
with Progress(*progress_columns, transient=False) as progress:
    analysing_task = progress.add_task(
                f"[cyan]Downloading {num_days} days", start=True, total=num_days
            )

    while current_date <= date_end:

        reqUrl = "https://book.portaventuraworld.com/funnel/hotels/chain"

        headersList = {
        "Content-Type": "application/json" 
        }

        endDate = current_date+timedelta(days=1)
        payload = json.dumps({
        "languageCode": "es",
        "startDate": current_date.strftime("%Y-%m-%d"),
        "endDate": endDate.strftime("%Y-%m-%d"),
        "children": 2,
        "adults": 3,
        "childrenAges": [6,10],
        "rooms": 1,
        "maxChildren": 2,
        "maxAdults": 3,
        "coupon": "",
        "couponType": "Discount",
        "roomsArray": [
            {
            "adults": 3,
            "children": 2,
            "childrenAges": [6,10]
            }
        ]
        })

        response = requests.request("POST", reqUrl, data=payload,  headers=headersList)
        
        result[current_date.strftime("%Y-%m-%d")] =  json.loads(response.text)

        current_date += step

        progress.update(analysing_task, advance=1)

    progress.update(analysing_task, completed=num_days)
    
 
with open(f'downloaded_data/{datetime.today().strftime("%Y%m%d")}.json', 'w') as archivo:
    json.dump(result, archivo, ensure_ascii=False, indent=4)

