document.getElementById('ipForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const ip = document.getElementById('ip').value;
    const hostname = document.getElementById('hostname').value;
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('/ipam', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ ip, hostname, username, password }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        loadIPs();
    });
});

function loadIPs() {
    fetch('/ipam')
    .then(response => response.json())
    .then(data => {
        const tableBody = document.getElementById('ipTable').getElementsByTagName('tbody')[0];
        tableBody.innerHTML = '';
        data.ipam.forEach(entry => {
            let row = tableBody.insertRow();
            row.insertCell(0).textContent = entry.ip;
            row.insertCell(1).textContent = entry.hostname;
            row.insertCell(2).textContent = entry.username;
            row.insertCell(3).textContent = entry.password;
            let actionsCell = row.insertCell(4);
            actionsCell.innerHTML = `
                <button onclick="deleteEntry('${entry.ip}')" class="btn btn-danger">Supprimer</button>
                <button onclick="editEntry('${entry.ip}')" class="btn btn-warning">Modifier</button>
            `;
        });
    });
}

function deleteEntry(ip) {
    fetch(`/ipam/${ip}`, { method: 'DELETE' })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        loadIPs();
    });
}

function editEntry(ip) {
    // Récupérer les données actuelles depuis l'API
    fetch('/ipam')
        .then(response => response.json())
        .then(data => {
            // Trouver l'entrée correspondant à l'adresse IP
            const entry = data.ipam.find(item => item.ip === ip);

            if (entry) {
                // Pré-remplir le formulaire avec les données de l'entrée
                document.getElementById('ip').value = entry.ip;
                document.getElementById('hostname').value = entry.hostname;
                document.getElementById('username').value = entry.username;
                document.getElementById('password').value = entry.password;

                // Changer le texte du bouton pour indiquer qu'il s'agit d'une mise à jour
                document.querySelector('#ipForm button').textContent = 'Mettre à jour';

                // Ajouter un écouteur d'événement pour gérer la mise à jour
                document.getElementById('ipForm').onsubmit = function(event) {
                    event.preventDefault();
                    updateEntry(ip); // Appeler la fonction de mise à jour
                };
            } else {
                alert("Adresse IP non trouvée !");
            }
        })
        .catch(error => {
            console.error("Erreur lors de la récupération des données :", error);
        });
}

window.onload = loadIPs;