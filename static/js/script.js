let data = []

async function populateTable() {
    
    const tbody = document.getElementById("productTableBody");

    if (!tbody) {
        return;
    }

    tbody.querySelectorAll("tr").forEach(row => row.remove());

    try {
        const response = await fetch('http://127.0.0.1:5000/api/assets');
        if(!response.ok) {
            throw new Error('Result not found')
        }
        
       data = await response.json();

        if(!Array.isArray(data)) {
            throw new Error('Os dados recebidos pipipi popopo')
        }
   

    data.forEach(item => {
        console.log("Adicionando item:", item);

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${item.tag}</td>
            <td>${item.name}</td>
            <td>${item.serial_number}</td>
            <td>${item.status}</td>
            <td>${item.comments}</td>
            <td>${item.owner}</td>
            
        `;
        row.addEventListener("contextmenu", function(event) {
            event.preventDefault();
            
            let contextMenu = document.getElementById("contextMenu");
            let posX = event.pageX;
            let posY = event.pageY;

            contextMenu.style.top = posY + "px";
            contextMenu.style.left = posX + "px";
            contextMenu.style.display = "block";

            contextMenu.dataset.selectedRow = row.rowIndex
        })

        tbody.appendChild(row);
    });
    } catch (error) {
        console.log("Erros ao buscar api")        
    }
}

document.addEventListener("click", function (){
    document.getElementById("contextMenu").style.display = "none";
    
});

function searchAssets () {
    let input = document.getElementById("search").value.toLowerCase();
    let tablerows = document.querySelectorAll("#productTableBody tr");
    
    tablerows.forEach(row => {
        let rowText = row.innerHTML.toLowerCase();
        row.style.display = rowText.includes(input) ? "" : "none";
    });
}

document.addEventListener("DOMContentLoaded", function() {
    populateTable();
    document.getElementById("transferModal").style.display = "none";
    document.getElementById("historyModal").style.display = "none";
});


async function viewHistory() {
    let selectedRowIndex = document.getElementById("contextMenu").dataset.selectedRow;
    

    if(selectedRowIndex === undefined) {
        alert("Error selecting asset");
        return
    }

    const transactions = data[selectedRowIndex];

        if(!transactions) {
            alert("No history avaible for this asset");
            return;
        }

    try {
        const response = await fetch('http://127.0.0.1:5000/api/transactions?asset_tag=$transactions.tag}')
        if(!response.ok) {
            throw new Error('Failed to fetch transactions')
        }
        
        const transaction = await response.json()
        console.log("Transações recebidas:", transaction);

        let historyList = document.getElementById("historyList");
        historyList.innerHTML = "";

        transaction.forEach(entry => {
            let row = document.createElement("tr")
            row.innerHTML = `
                <td>${entry.asset_tag}</td>
                <td>${entry.responsible_coreid}</td>
                <td>${entry.date_transaction}</td>
            `;
                historyList.appendChild(row);
            });
        } catch (error) {
            console.error("Error fetching asset history:", error);
            alert("Failed to load asset history.")
        }
    document.getElementById("historyModal").style.display = "flex";
    
}

async function transferAsset() {
    let contextMenu = document.getElementById("contextMenu");
    let selectedRowIndex = parseInt(contextMenu.dataset.selectedRow) - 1;

    if (isNaN(selectedRowIndex) || selectedRowIndex < 0 || selectedRowIndex >= data.length) {
        alert("Erro ao selecionar ativo");
        return;
    }

    let selectedAsset = data[selectedRowIndex];

    if (!selectedAsset) {
        alert("Erro ao selecionar ativo");
        return;
    }

    console.log("Ativo selecionado:", selectedAsset);

    document.getElementById("ownerName").innerText = selectedAsset.owner;

    let assetsList = document.getElementById("assetsList");
    assetsList.innerHTML = "";

    let checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.value = selectedAsset.tag;
    checkbox.id = "checkbox-" + selectedAsset.tag;

    let label = document.createElement("label");
    label.htmlFor = checkbox.id;
    label.innerHTML = `${selectedAsset.tag} - ${selectedAsset.name}`;

    let div = document.createElement("div");
    div.appendChild(checkbox);
    div.appendChild(label);
    assetsList.appendChild(div);

    let newOwnerSelect = document.getElementById("newOwnerSelect");
    newOwnerSelect.innerHTML = "";

    fetch("http://127.0.0.1:5000/api/users")
    .then(response => {
        if (!response.ok) {
            throw new Error(`Erro HTTP: ${response.status}`);
        }
        return response.json();
    })
    .then(users => {
        console.log("Usuários carregados:", users); // Debug
        users.forEach(user => {
            if (user.id !== selectedAsset.owner_id) {
                let option = document.createElement("option");
                option.value = user.coreid;
                option.innerText = user.name;
                newOwnerSelect.appendChild(option);
            }
        });
    })
    .catch(error => console.error("Erro ao buscar usuários:", error));

    let transferModal = document.getElementById("transferModal");

    if (!transferModal) {
        console.error("Modal de transferência não encontrado!");
        return;
    }

    console.log("Abrindo modal de transferência...");
    transferModal.style.display = "flex";
}



function closeModal() {
    document.getElementById("transferModal").style.display = "none";
    document.getElementById("historyModal").style.display = "none";
}

async function confirmTransfer() {
    let selectedAssets = [];
    
    document.querySelectorAll("#assetsList input:checked").forEach(checkbox => {
        selectedAssets.push(checkbox.value);
    });

    let newOwnerCoreId = document.getElementById("newOwnerSelect").value;

    if (selectedAssets.length === 0) {
        alert("Nenhum ativo selecionado.");
        return;
    }

    if (!newOwnerCoreId) {
        alert("Selecione um novo dono.");
        return;
    }

    try {
        for (let assetTag of selectedAssets) {
            let transferData = {
                asset_tag: assetTag,
                new_owner_coreid: newOwnerCoreId
            };

            const response = await fetch('http://127.0.0.1:5000/api/assign', {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(transferData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || "Falha na transferência do ativo");
            }
        }

        alert(`Ativos transferidos com sucesso para o novo dono.`);
        
        // Atualizar os dados localmente
        data.forEach(asset => {
            if (selectedAssets.includes(asset.tag)) {
                asset.owner_id = parseInt(newOwnerCoreId);
                asset.owner = document.getElementById("newOwnerSelect").options[document.getElementById("newOwnerSelect").selectedIndex].text;

                if (!asset.history) asset.history = [];

                asset.history.push({
                    asset_tag: asset.tag,
                    responsible_coreid: newOwnerCoreId,
                    date_transaction: new Date().toISOString()
                });
            }
        });

        closeModal();
        populateTable();

    } catch (error) {
        console.error("Erro ao transferir ativo:", error);
        alert(error.message);
    }
}