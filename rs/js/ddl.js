async function loadGame() {
    try {
        // Encoded JSON file URL
        const jsonUrl = atob("https://niksidbro.github.io/nkboss/games.json");
        
        // JSON file fetch karo
        const response = await fetch(jsonUrl);
        const data = await response.json();
        
        // Current page ka name get karo
        const pageName = window.location.pathname.split("/").pop();
        
        if (!pageName) {
            alert("Page name not found!");
            return;
        }

        // JSON me game URL check karo aur set karo
        if (data[pageName]) {
            document.getElementById("iframehtml5").src = data[pageName];
        } else {
            alert("Game not found in JSON!");
        }
    } catch (error) {
        console.error("Error loading game:", error);
    }
}

// Page load hone par function run karo
window.onload = loadGame;
