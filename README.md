# Capri — a custom pet for Codex

A soft, rounded fan-made Capri pet for Codex desktop, with flowing hot-pink curls, a tiny flexible body, expressive green-and-blue eyes and a mischievous grin.

**[Download Capri's sprite sheet](https://github.com/Zack24680/capri-pet/releases/download/v1.0.0/capri.png)**

**9 animation states · 16 gaze directions · transparent PNG**

![Capri waving](media/states/waving.gif) ![Capri jumping](media/states/jumping.gif) ![Capri looking around](media/look-loop.gif)

## Install in Codex

1. Download **`capri.png`** using the link above. This is the only file you need.
2. In Codex desktop, open **Settings > Pets > Create pet**. Attach `capri.png` in the chat that opens and send:

   > Install the attached sprite sheet as a custom pet named Capri. It is an existing v2 sprite sheet, with 8 columns and 11 rows of 192 × 208 pixel cells. Use the supplied artwork without regenerating it.

3. When installation finishes, return to **Settings > Pets**, select **Refresh**, and choose **Capri**. Enter `/pet` to show her.

Requires a desktop app version with custom Pets support. See the [official Pets guide](https://learn.chatgpt.com/docs/pets?surface=app) for the creation flow and pet controls.

## See Capri move

![All nine animation states](media/all-states.gif)

| State | What Capri does |
| --- | --- |
| Idle | A buoyant bob, a grin and a brief blink. |
| Travel right | Right-facing floating bounds with loose, curved limbs. |
| Travel left | A separately drawn left-facing cycle that preserves her asymmetric details. |
| Wave | A loose wrist greeting and cheerful eye squint. |
| Jump | Crouch, lift, airborne spread and a soft landing. |
| Failure / recovery | Surprise, a small curl or slump, then recovery. |
| Needs input | An expectant open-hand gesture. |
| Active work | Focused face and hand movements while working in place. |
| Review | A cheek/chin touch, narrowed eyes and a satisfied head cock. |

The sixteen gaze poses add side glances, upward curiosity and downward looks. The GIFs preview the supplied artwork; playback speed depends on the app.

## Character and artwork

Capri brings confident, teasing energy with flashes of impatience and quieter curiosity. Broad pink curls, a large head, a small pliant body and loose wrists give her a soft, fluid silhouette. Squints, winks and cheek/chin gestures carry her expressions.

The download is a transparent **v2 sprite sheet, 1536 × 2288 pixels**. The artwork passed the bundled structural and quality checks. Some intermediate gaze directions are subtle; the [validation notes](docs/validation.md) document the reviewed warnings and checks.

[Character and motion notes](docs/character-and-motion.md) cover the references, design and animation details. [Media inventory](docs/media-inventory.md) and [quality report](qa/quality-validation.json) provide the technical evidence.

## Attribution

This is an unofficial fan-made adaptation of Capri / Project Capricorn from *Cyberpunk: Edgerunners 2*. The character and franchise rights remain with their respective owners; this repository does not grant a license over them.

Artwork was generated with OpenAI's built-in image generator and assembled with the bundled Pets tools. Reference links and inspected intervals are listed in the [source notes](docs/character-and-motion.md).
