"use strict";
(() => {
  const meta = window.CAPRI_METADATA;
  const canvas = document.querySelector("#pet");
  const context = canvas.getContext("2d");
  const select = document.querySelector("#state");
  const pause = document.querySelector("#pause");
  const image = new Image();
  let state = meta.states[0].id;
  let started = performance.now();
  let paused = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let frozenElapsed = 0;
  let tourIndex = -1;
  let lastFrame = -1;
  let drawnFrames = 0;
  const tourStates = [...meta.states.map((s) => s.id), "look"];
  for (const item of [...meta.states, { id: "look", label: "Look around" }]) {
    const option = document.createElement("option");
    option.value = item.id;
    option.textContent = item.label;
    select.append(option);
  }
  function configuration() {
    if (state === "look")
      return {
        label: "Look around",
        motion:
          "An ordered clockwise gaze sweep; the small body stays anchored.",
        durationsMs: meta.looks.map(() => 220),
        cycleMs: 3520,
      };
    return meta.states.find((item) => item.id === state);
  }
  function setState(id, keepTour = false) {
    if (!tourStates.includes(id)) throw new Error("Unknown animation state");
    state = id;
    select.value = id;
    started = performance.now();
    frozenElapsed = 0;
    lastFrame = -1;
    if (!keepTour) tourIndex = -1;
    const config = configuration();
    document.querySelector("#player-title").textContent = config.label;
    document.querySelector("#motion").textContent = config.motion;
  }
  function draw(row, column, target = context) {
    target.clearRect(0, 0, 192, 208);
    target.drawImage(image, column * 192, row * 208, 192, 208, 0, 0, 192, 208);
  }
  function render(now) {
    const config = configuration();
    const elapsed = paused ? frozenElapsed : now - started;
    if (tourIndex >= 0 && elapsed >= config.cycleMs * 2) {
      tourIndex = (tourIndex + 1) % tourStates.length;
      setState(tourStates[tourIndex], true);
    }
    const active = configuration();
    let position = (paused ? frozenElapsed : now - started) % active.cycleMs;
    let frame = 0;
    while (
      frame < active.durationsMs.length - 1 &&
      position >= active.durationsMs[frame]
    ) {
      position -= active.durationsMs[frame];
      frame++;
    }
    if (frame !== lastFrame) {
      const look = state === "look" ? meta.looks[frame] : null;
      draw(look ? look.row : active.row, look ? look.column : frame);
      lastFrame = frame;
      drawnFrames++;
      document.querySelector("#frame").textContent =
        state === "look"
          ? `${look.angle}° · ${look.direction}`
          : `Frame ${frame + 1}/${active.frames} · ${active.cycleMs} ms cycle`;
    }
    requestAnimationFrame(render);
  }
  pause.textContent = paused ? "Play" : "Pause";
  pause.addEventListener("click", () => {
    if (paused) started = performance.now() - frozenElapsed;
    else frozenElapsed = performance.now() - started;
    paused = !paused;
    pause.textContent = paused ? "Play" : "Pause";
  });
  select.addEventListener("change", () => setState(select.value));
  document.querySelector("#scale").addEventListener("change", (event) => {
    const scale = Number(event.target.value);
    canvas.style.width = `${192 * scale}px`;
    canvas.style.height = `${208 * scale}px`;
  });
  document.querySelector("#tour").addEventListener("click", () => {
    paused = false;
    pause.textContent = "Pause";
    tourIndex = 0;
    setState(tourStates[0], true);
  });
  image.addEventListener("load", () => {
    for (const item of meta.states) {
      const card = document.createElement("article");
      card.className = "card";
      const holder = document.createElement("div");
      holder.className = "image";
      const gif = document.createElement("img");
      gif.src = `media/states/${item.id}.gif`;
      gif.alt = `${item.label}: ${item.motion}`;
      holder.append(gif);
      const copy = document.createElement("div");
      copy.className = "copy";
      for (const [tag, text, className] of [
        ["h3", item.label, ""],
        ["p", `${item.frames} frames · ${item.cycleMs} ms`, "timing"],
        ["p", item.motion, ""],
      ]) {
        const node = document.createElement(tag);
        node.textContent = text;
        node.className = className;
        copy.append(node);
      }
      card.append(holder, copy);
      document.querySelector("#state-grid").append(card);
    }
    for (const look of meta.looks) {
      const card = document.createElement("div");
      card.className = "look-card";
      const cell = document.createElement("canvas");
      cell.width = 192;
      cell.height = 208;
      cell.setAttribute(
        "aria-label",
        `${look.angle} degrees, ${look.direction}`,
      );
      draw(look.row, look.column, cell.getContext("2d"));
      const label = document.createElement("span");
      label.textContent = `${look.angle}°`;
      card.append(cell, label);
      document.querySelector("#look-grid").append(card);
    }
    window.Capri = {
      loaded: true,
      setState,
      status: () => ({ state, paused, frame: lastFrame, drawnFrames }),
    };
    setState(state);
    requestAnimationFrame(render);
  });
  image.addEventListener("error", () => {
    document.querySelector("#motion").textContent =
      "The sprite sheet could not be loaded. Check that assets/capri.png is present.";
  });
  image.src = meta.sprite.file;
})();
