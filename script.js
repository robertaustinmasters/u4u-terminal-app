// U4U Terminal - Frontend Logic

// --- 1. Master Bridge Pipeline ---
async function routeToMasterBridge(commandName, userText) {
    try {
        const response = await fetch("/api/synthesize", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            body: JSON.stringify({
                command: commandName,
                text: userText
            })
        });

        const data = await response.json();

        if (data.status === "success") {
            return data.response;
        } else {
            return "Error: Master Bridge rejected the payload.";
        }
    } catch (error) {
        return "Critical Error: Could not reach the U4U Master Bridge. Check uplink.";
    }
}

// --- 2. Terminal UI Logic ---
document.addEventListener("DOMContentLoaded", () => {
    const outputDiv = document.getElementById("terminal-output");
    const inputField = document.getElementById("terminal-input");

    if (!inputField || !outputDiv) {
        console.warn("System Notice: Please ensure your HTML contains <div id='terminal-output'></div> and <input id='terminal-input'>");
        return;
    }

    function printToTerminal(text, isCommand = false) {
        const newLine = document.createElement("div");
        newLine.style.marginBottom = "10px";
        newLine.style.whiteSpace = "pre-wrap";
        newLine.innerText = isCommand ? "> " + text : text;
        
        outputDiv.appendChild(newLine);
        outputDiv.scrollTop = outputDiv.scrollHeight;
    }

    inputField.addEventListener("keydown", async (event) => {
        if (event.key === "Enter") {
            const rawInput = inputField.value.trim();
            if (!rawInput) return;

            printToTerminal(rawInput, true);
            inputField.value = "";
            
            const parts = rawInput.split(" ");
            const command = parts[0].toLowerCase();
            const payloadText = parts.slice(1).join(" ");

            const validCommands = ["/job_lead", "/grant_lead", "swarm", "apex", "evolve"];

            if (validCommands.includes(command)) {
                printToTerminal("Uplinking to Master Bridge... [Awaiting Phase Lock]");
                inputField.disabled = true;
                
                const result = await routeToMasterBridge(command, payloadText || "Execute standard protocol.");
                
                printToTerminal(result);
                inputField.disabled = false;
                inputField.focus();
            } else {
                printToTerminal(`Unrecognized command. Valid protocols: /job_lead, /grant_lead, swarm, apex, evolve`);
            }
        }
    });
    
    printToTerminal("U4U Terminal Initialized. Enter a protocol to begin (e.g., /job_lead Hello).");
});
