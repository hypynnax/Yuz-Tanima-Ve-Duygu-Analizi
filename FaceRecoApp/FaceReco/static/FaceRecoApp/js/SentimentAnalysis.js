const tableData = JSON.parse(document.getElementById("analysis-data").textContent);
let currentPage = 1;
let rowsPerPage = 25;

function renderTable() {
    const tableBody = document.getElementById('dataTable').querySelector('tbody');
    tableBody.innerHTML = '';

    const start = (currentPage - 1) * rowsPerPage;
    const end = start + rowsPerPage;
    const keys = Object.keys(tableData);
    const pageKeys = keys.slice(start, end);

    pageKeys.forEach(key => {
        const rowData = tableData[key];
        const row = document.createElement('tr');

        const columns = [
            rowData.id,
            rowData.name,
            rowData.surname,
            rowData.job,
            rowData.old,
            rowData.gender,
            rowData.dateDetected,
            rowData.detectedEmotion
        ];

        columns.forEach(cellData => {
            const cell = document.createElement('td');
            cell.textContent = cellData;
            row.appendChild(cell);
        });

        tableBody.appendChild(row);
    });

    document.getElementById('prevPage').disabled = currentPage === 1;
    document.getElementById('nextPage').disabled = end >= tableData.length;
}

document.getElementById('prevPage').addEventListener('click', () => {
    if (currentPage > 1) {
        currentPage--;
        renderTable();
    }
});

document.getElementById('nextPage').addEventListener('click', () => {
    alert("asdfşkjasdf");
    const maxPage = Math.ceil(tableData.length / rowsPerPage);
    if (currentPage < maxPage) {
        currentPage++;
        renderTable();
    }
});

document.getElementById('rowsPerPage').addEventListener('change', (event) => {
    rowsPerPage = parseInt(event.target.value);
    currentPage = 1;
    renderTable();
});

renderTable();