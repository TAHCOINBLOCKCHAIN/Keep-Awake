import asyncio
from playwright.async_api import async_playwright

# List of all target Hugging Face Spaces
SPACES = [
    "https://huggingface.co/spaces/aysha918t2/Ayre",
    "https://huggingface.co/spaces/aysha918t2/Dilabe",
    "https://huggingface.co/spaces/aysha918t2/KitaJeneRe",
    "https://huggingface.co/spaces/aysha918t2/Kitare",
    "https://huggingface.co/spaces/aysha918t2/Nare",
    "https://huggingface.co/spaces/aysha918t2/Oyre",
    "https://huggingface.co/spaces/t32588605/Hmmm",
    "https://huggingface.co/spaces/t32588605/Owtare",
    "https://huggingface.co/spaces/t32588605/Owreder",
    "https://huggingface.co/spaces/t32588605/KemneDer",
    "https://huggingface.co/spaces/t32588605/KitaDilaiBeRe",
    "https://huggingface.co/spaces/t32588605/OwMorbo",
    "https://huggingface.co/spaces/rofik1985/DilaJesaTa",
    "https://huggingface.co/spaces/rofik1985/KitaDilaiteRe",
    "https://huggingface.co/spaces/rofik1985/JetaDibarDila",
    "https://huggingface.co/spaces/rofik1985/DilaDukan",
    "https://huggingface.co/spaces/rofik1985/KailaKunta",
    "https://huggingface.co/spaces/rofik1985/BulisNaKunta"
]

async def process_space(page, url):
    print(f"\n[+] Processing: {url}")
    try:
        # Navigate to the Space URL
        await page.goto(url, timeout=60000, wait_until="domcontentloaded")
        await page.wait_for_timeout(5000) # Give it a few seconds to evaluate state
        
        # Look for the 'Restart this Space' button if it is sleeping
        restart_btn = page.get_by_role("button", name="Restart this Space", exact=False)
        
        if await restart_btn.is_visible():
            print(f"    [!] Space is sleeping. Clicking 'Restart this Space'...")
            await restart_btn.click()
            
            # Wait for the build/restart process to initialize and load the app container
            print("    [*] Waiting 45 seconds for initialization...")
            await page.wait_for_timeout(45000)
            print("    [✓] Restart initiated successfully.")
        else:
            print("    [✓] Space is already active or waking up dynamically.")
            
    except Exception as e:
        print(f"    [X] Error accessing {url}: {str(e)}")

async def main():
    async with async_playwright() as p:
        # Launch headless browser with specific user-agent to mimic standard browser
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = await context.new_page()
        
        for space_url in SPACES:
            await process_space(page, space_url)
            
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
