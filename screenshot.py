import asyncio
from playwright.async_api import async_playwright
import threading
import http.server
import socketserver
import os

PORT = 8080

def start_server():
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()

async def take_screenshots():
    # Start server in background
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    await asyncio.sleep(2) # wait for server to start
    
    os.makedirs('screenshots', exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # Desktop
        context_desk = await browser.new_context(viewport={'width': 1440, 'height': 900})
        page_desk = await context_desk.new_page()
        await page_desk.goto(f'http://localhost:{PORT}/index.html')
        await page_desk.wait_for_timeout(1000)
        await page_desk.screenshot(path='screenshots/index_desktop.png', full_page=True)
        
        # Mobile
        context_mobile = await browser.new_context(
            viewport={'width': 375, 'height': 812},
            is_mobile=True,
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
        )
        page_mobile = await context_mobile.new_page()
        await page_mobile.goto(f'http://localhost:{PORT}/index.html')
        await page_mobile.wait_for_timeout(1000)
        await page_mobile.screenshot(path='screenshots/index_mobile.png', full_page=True)
        
        await page_mobile.goto(f'http://localhost:{PORT}/tokushoho.html')
        await page_mobile.wait_for_timeout(1000)
        await page_mobile.screenshot(path='screenshots/tokushoho_mobile.png', full_page=True)
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(take_screenshots())
    print("Screenshots taken successfully.")
