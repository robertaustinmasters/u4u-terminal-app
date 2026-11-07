const terminalInput = document.getElementById("terminal-input");
// Assuming you have a div for output; fallback to body if not found
const terminalOutput = document.getElementById("terminal-output") || document.body;

// Use a relative path since frontend and backend are on the same Render domain
const API_URL = "/api/synthesize"; 
const AUTH_TOKEN = "YOUR_SECURE_TOKEN_HERE";

terminalInput.addEventListener("keydown", async (event) => {
    if (event.key === "Enter") {
        const cmd = terminalInput.value.trim();
        if (!cmd) return;

        // Echo user command to the screen
        const cmdLine = document.createElement("div");
        cmdLine.textContent = `> ${cmd}`;
        terminalOutput.appendChild(cmdLine);
        terminalInput.value = "";

        try {
            const response = await fetch(API_URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "x-u4u-auth": AUTH_TOKEN
                },
                // Send BOTH keys to satisfy the FastAPI SynthesizeRequest schema
                body: JSON.stringify({ command: "web_terminal", text: cmd }) 
            });

            if (response.status === 401) {
                throw new Error("401 Unauthorized - Check MESH_AUTH_TOKEN");
            } else if (response.status === 422) {
                throw new Error("422 Unprocessable Entity - Invalid JSON Schema");
            } else if (!response.ok) {
                throw new Error(`Server returned ${response.status}`);
            }

            const data = await response.json();
            
            // Print success response
            const responseLine = document.createElement("div");
            responseLine.style.color = "#00ff00"; // Hacker green
            responseLine.textContent = data.response;
            terminalOutput.appendChild(responseLine);

        } catch (error) {
            // Print error
            const errLine = document.createElement("div");
            errLine.style.color = "red";
            errLine.textContent = `[ERROR] ${error.message}`;
            terminalOutput.appendChild(errLine);
        }

        // Auto-scroll to the bottom of the terminal
        if (terminalOutput.scrollHeight) {
            terminalOutput.scrollTop = terminalOutput.scrollHeight;
        }
    }
});
