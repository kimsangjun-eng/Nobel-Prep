from playwright.sync_api import sync_playwright
import pathlib

MOCK_NUM = "__MOCK_NUM__"  # <- edit this line for each new mock test

html_path = pathlib.Path("vocab_list.html").resolve()
out_path = f"Mock_Test_{MOCK_NUM}_RW_Vocab_List.pdf"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file://{html_path}")
    page.pdf(path=out_path, format="Letter", print_background=True)
    browser.close()

print("wrote", out_path)
