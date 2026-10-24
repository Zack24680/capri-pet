#!/usr/bin/env python3
"""Capture the local sprite player, without using a personal browser profile."""
import asyncio
import json
from pathlib import Path
import shutil
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[1]


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


async def capture():
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    errors, failed_requests = [], []
    try:
        async with async_playwright() as pw:
            executable = shutil.which("google-chrome") or shutil.which("chromium")
            browser = await pw.chromium.launch(headless=True, **({"executable_path": executable} if executable else {}))
            context = await browser.new_context(viewport={"width": 1280, "height": 900}, device_scale_factor=1,
                                               record_video_dir=str(ROOT / ".capture"),
                                               record_video_size={"width": 1280, "height": 900})
            page = await context.new_page()
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.on("requestfailed", lambda request: failed_requests.append(request.url))
            await page.goto(f"http://127.0.0.1:{server.server_port}/index.html", wait_until="networkidle")
            await page.wait_for_function("window.Capri && window.Capri.loaded")
            await page.screenshot(path=str(ROOT / "media/screenshot-player.png"))
            await page.locator("#states").screenshot(path=str(ROOT / "media/screenshot-nine-states.png"))
            await page.locator("#look-grid").screenshot(path=str(ROOT / "media/screenshot-gaze.png"))
            assert await page.locator(".card").count() == 9
            assert await page.locator(".look-card").count() == 16
            # Exercise every actual player state and its visible labels.
            metadata = json.loads((ROOT / "metadata.json").read_text())
            tested = []
            for state in metadata["states"]:
                await page.select_option("#state", state["id"])
                await page.wait_for_timeout(100)
                status = await page.evaluate("Capri.status()")
                assert status["state"] == state["id"]
                assert await page.locator("#player-title").inner_text() == state["label"]
                tested.append(state["id"])
            await page.select_option("#state", "look")
            await page.wait_for_timeout(100)
            await page.locator("#pause").click()
            paused = await page.evaluate("Capri.status()")
            await page.wait_for_timeout(180)
            assert (await page.evaluate("Capri.status()"))["frame"] == paused["frame"]
            await page.locator("#pause").click()
            await page.select_option("#scale", "2")
            assert await page.locator("#pet").evaluate("el => el.getBoundingClientRect().width") == 384
            await page.select_option("#scale", "1")
            await page.evaluate("scrollTo(0,0)")
            await page.locator("#tour").click()
            await page.wait_for_timeout(25100)
            await page.screenshot(path=str(ROOT / "media/screenshot-demo-end.png"))
            assert not errors, errors
            assert not failed_requests, failed_requests
            recording = page.video
            await context.close()
            await recording.save_as(str(ROOT / "media/capri-demo.webm"))
            await browser.close()
            report = {"recording": "media/capri-demo.webm", "viewport": [1280, 900],
                      "tested_states": tested, "look_cells": 16, "pause_resume": "passed",
                      "native_and_double_scale": "passed", "page_errors": errors,
                      "failed_requests": failed_requests,
                      "scope": "Isolated local browser playback of the published atlas. Not a ChatGPT app runtime capture or a frame-rate benchmark."}
            (ROOT / "qa/browser-playback.json").write_text(json.dumps(report, indent=2) + "\n")
            print(json.dumps(report))
    finally:
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    asyncio.run(capture())
