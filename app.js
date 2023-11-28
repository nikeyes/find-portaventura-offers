document.addEventListener("DOMContentLoaded", function() {
    fetchData();
});

async function fetchData() {
    try {
        const response = await fetch('https://raw.githubusercontent.com/nikeyes/find-portaventura-offers/main/downloaded_data/hotels_20231127_a2_c2_6_9.json');
        const data = await response.json();
        displayData(data);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function displayData(data) {
    const appContainer = document.getElementById('app');

    const container = document.createElement('div');
    container.classList.add('container');

    const table = document.createElement('table');
    table.classList.add('table');

    // Create table headers
    const headers = ['Fecha', 'Nombre del Hotel', 'Tarifa', 'Tarifa Antigua', 'Descuento'];
    const headerRow = document.createElement('tr');
    headers.forEach(headerText => {
        const th = document.createElement('th');
        th.textContent = headerText;

        // Add filter input and event listener
        if (headerText !== 'Fecha') {
            const filterInput = document.createElement('input');
            filterInput.type = 'text';
            filterInput.placeholder = `Filtrar por ${headerText.toLowerCase()}`;
            th.appendChild(filterInput);

            filterInput.addEventListener('input', function() {
                filterTable(headerText.toLowerCase(), this.value);
            });
        }

        headerRow.appendChild(th);
    });
    table.appendChild(headerRow);

    // Populate table with data
    data.hotels_rate.forEach(item => {
        const row = document.createElement('tr');
        const dateCell = document.createElement('td');
        dateCell.textContent = item.date;
        row.appendChild(dateCell);

        const nameCell = document.createElement('td');
        nameCell.textContent = item.name;
        row.appendChild(nameCell);

        const rateCell = document.createElement('td');
        rateCell.textContent = item.rate;
        row.appendChild(rateCell);

        const rateOldCell = document.createElement('td');
        rateOldCell.textContent = item.rate_old !== null ? item.rate_old : 'N/A';
        row.appendChild(rateOldCell);

        const discountCell = document.createElement('td');
        discountCell.textContent = item.discount;
        row.appendChild(discountCell);

        table.appendChild(row);
    });

    container.appendChild(table);
    appContainer.appendChild(container);
}

function filterTable(columnIndex, value) {
    const table = document.querySelector('.table');
    const rows = table.querySelectorAll('tr');

    for (let i = 1; i < rows.length; i++) {
        const row = rows[i];
        const cells = row.querySelectorAll('td');

        if (cells[columnIndex].textContent.toLowerCase().includes(value.toLowerCase())) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    }
}
