async function loadGame() {
    // Current Page ka URL get karo
    const pageName = window.location.pathname.split("/").pop(); // e.g., "game1.html"
    
    if (!pageName) {
        alert("Page name not found!");
        return;
    }

    try {
        const response = await fetch("https://games-maza.pages.dev/games.json"); // JSON file load karo
        const data = await response.json();

        if (data[pageName]) {
            document.getElementById("iframehtml5").src = data[pageName]; // JSON se URL set karo
        } else {
            alert("Game not found in JSON!");
        }
    } catch (error) {
        console.error("Error loading game:", error);
    }
}
