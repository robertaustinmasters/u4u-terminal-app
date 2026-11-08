import asyncio
from playwright.async_api import async_playwright

# Paste your live Render destination URL here:
DESTINATION_URL = "https://u4u-master-bridge.onrender.com" 

async def run_automator():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        print(f"[*] Navigating to live destination: {DESTINATION_URL}...")
        response = await page.goto(DESTINATION_URL)
        print(f"[HTTP {response.status}] {DESTINATION_URL}/")
        
        await page.wait_for_selector("#terminal-input")
        print("[*] Production terminal interface loaded successfully.")
        
        protocols = [
            "/job_lead Automate the AI mesh pipeline",
            "/grant_lead Secure regional research funding",
            "swarm --init --nodes=4",
            "apex --target=bridge --sync",
            "evolve --commit --version=4.1.0"
        ]
        
        for cmd in protocols:
            print(f"[*] Executing protocol on live server: {cmd}")
            await page.fill("#terminal-input", cmd)
            await page.press("#terminal-input", "Enter")
            await page.wait_for_timeout(1500)
            
        print("[*] All production browser protocol tests completed successfully.")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_automator())
