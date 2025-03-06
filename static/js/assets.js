async function fetchAssets() {
    let token = localStorage.getItem("token");
    let response = await fetch('/assets', {
        headers: { "Authorization": `Bearer ${token}` }
    });
    let assets = await response.json();

    let assetList = document.getElementById("assetList");
    assetList.innerHTML = "";
    assets.forEach(asset => {
        let li = document.createElement("li");
        li.innerHTML = `${asset.name} - Owned by: ${asset.owner}`;
        assetList.appendChild(li);
    });
}

async function searchAssets() {
    let searchQuery = document.getElementById("search").value.toLowerCase();
    let token = localStorage.getItem("token");
    let response = await fetch('/assets', {
        headers: { "Authorization": `Bearer ${token}` }
    });

    let assets = await response.json();
    let filteredAssets = assets.filter(a => a.name.toLowerCase().includes(searchQuery));

    let assetList = document.getElementById("assetList");
    assetList.innerHTML = "";
    filteredAssets.forEach(asset => {
        let li = document.createElement("li");
        li.innerHTML = `${asset.name} - Owned by: ${asset.owner}`;
        assetList.appendChild(li);
    });
}

document.getElementById("logout").addEventListener("click", () => {
    localStorage.removeItem("token");
    window.location.href = "login.html";
});

fetchAssets();
