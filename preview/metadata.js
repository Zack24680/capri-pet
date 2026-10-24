window.CAPRI_METADATA = {
  "name": "Capri",
  "version": "1.0.0",
  "description": "A playful, self-assured digital construct inspired by Capri, with buoyant pink curls, curious ring eyes, mischievous grins and elastic reactions.",
  "sprite": {
    "file": "assets/capri.png",
    "version": 2,
    "width": 1536,
    "height": 2288,
    "columns": 8,
    "rows": 11,
    "cellWidth": 192,
    "cellHeight": 208,
    "sha256": "cfd4a14f51dde57049bad38da9cd5e65f5434466256edfa339d0ac5f3f4d0ae6"
  },
  "states": [
    {
      "id": "idle",
      "label": "Idle",
      "row": 0,
      "frames": 6,
      "durationsMs": [
        280,
        110,
        110,
        140,
        140,
        320
      ],
      "cycleMs": 1100,
      "motion": "A small buoyant bob, a grin and a brief blink."
    },
    {
      "id": "running-right",
      "label": "Travel right",
      "row": 1,
      "frames": 8,
      "durationsMs": [
        120,
        120,
        120,
        120,
        120,
        120,
        120,
        220
      ],
      "cycleMs": 1060,
      "motion": "Right-facing floating bounds with alternating curved limbs."
    },
    {
      "id": "running-left",
      "label": "Travel left",
      "row": 2,
      "frames": 8,
      "durationsMs": [
        120,
        120,
        120,
        120,
        120,
        120,
        120,
        220
      ],
      "cycleMs": 1060,
      "motion": "A separately generated left-facing cycle, preserving asymmetric details."
    },
    {
      "id": "waving",
      "label": "Wave",
      "row": 3,
      "frames": 4,
      "durationsMs": [
        140,
        140,
        140,
        280
      ],
      "cycleMs": 700,
      "motion": "A loose wrist greeting and cheerful eye squint."
    },
    {
      "id": "jumping",
      "label": "Jump",
      "row": 4,
      "frames": 5,
      "durationsMs": [
        140,
        140,
        140,
        140,
        280
      ],
      "cycleMs": 840,
      "motion": "Anticipation, lift, airborne spread, descent and landing."
    },
    {
      "id": "failed",
      "label": "Failure / recovery",
      "row": 5,
      "frames": 8,
      "durationsMs": [
        140,
        140,
        140,
        140,
        140,
        140,
        140,
        240
      ],
      "cycleMs": 1220,
      "motion": "Surprise, a soft curl/slump and recovery."
    },
    {
      "id": "waiting",
      "label": "Needs input",
      "row": 6,
      "frames": 6,
      "durationsMs": [
        150,
        150,
        150,
        150,
        150,
        260
      ],
      "cycleMs": 1010,
      "motion": "An expectant open-hand gesture for approval or help."
    },
    {
      "id": "running",
      "label": "Active work",
      "row": 7,
      "frames": 6,
      "durationsMs": [
        120,
        120,
        120,
        120,
        120,
        220
      ],
      "cycleMs": 820,
      "motion": "Focused face and hand movements; this is stationary task work."
    },
    {
      "id": "review",
      "label": "Review",
      "row": 8,
      "frames": 6,
      "durationsMs": [
        150,
        150,
        150,
        150,
        150,
        280
      ],
      "cycleMs": 1030,
      "motion": "Chin/cheek touch, narrowed eyes and a satisfied head cock."
    }
  ],
  "looks": [
    {
      "angle": "000",
      "direction": "up",
      "row": 9,
      "column": 0
    },
    {
      "angle": "022.5",
      "direction": "up-right",
      "row": 9,
      "column": 1
    },
    {
      "angle": "045",
      "direction": "up-right",
      "row": 9,
      "column": 2
    },
    {
      "angle": "067.5",
      "direction": "up-right",
      "row": 9,
      "column": 3
    },
    {
      "angle": "090",
      "direction": "right",
      "row": 9,
      "column": 4
    },
    {
      "angle": "112.5",
      "direction": "down-right",
      "row": 9,
      "column": 5
    },
    {
      "angle": "135",
      "direction": "down-right",
      "row": 9,
      "column": 6
    },
    {
      "angle": "157.5",
      "direction": "down-right",
      "row": 9,
      "column": 7
    },
    {
      "angle": "180",
      "direction": "down",
      "row": 10,
      "column": 0
    },
    {
      "angle": "202.5",
      "direction": "down-left",
      "row": 10,
      "column": 1
    },
    {
      "angle": "225",
      "direction": "down-left",
      "row": 10,
      "column": 2
    },
    {
      "angle": "247.5",
      "direction": "down-left",
      "row": 10,
      "column": 3
    },
    {
      "angle": "270",
      "direction": "left",
      "row": 10,
      "column": 4
    },
    {
      "angle": "292.5",
      "direction": "up-left",
      "row": 10,
      "column": 5
    },
    {
      "angle": "315",
      "direction": "up-left",
      "row": 10,
      "column": 6
    },
    {
      "angle": "337.5",
      "direction": "up-left",
      "row": 10,
      "column": 7
    }
  ],
  "sources": [
    {
      "url": "https://www.youtube.com/shorts/GG50EpyoRpA",
      "intervals": [
        "00:00\u201300:03",
        "00:25\u201300:45"
      ]
    },
    {
      "url": "https://www.youtube.com/watch?v=Nli_SZ-DBco",
      "intervals": [
        "00:20\u201300:30",
        "00:46\u201300:54",
        "02:07\u201302:12",
        "04:05\u201304:08",
        "04:23\u201304:26"
      ]
    }
  ],
  "metadataNote": "Portable project metadata for the included preview player; not an undocumented native ChatGPT pet configuration format."
};
