# news-image-20261122 — "The World in One Day"

Entry for make.fun bounty **news-image-20261122** (sum up 22 November's world
news in one image), built for account **@desnutt-y**.

## The image

`entry.png` is a newspaper-style front page for **Sunday, 22 November 2026**,
drawn from scratch with Python/PIL (`build_image.py`, system DejaVu fonts,
no photos, no external assets). It carries 8 stories, all reported on
22 November 2026 — see `SOURCES.md` for the source of each one:

1. **COP31 climate talks collapse** — no deal in Antalya, Turkey (lead)
2. **Mexico** — cartel boss "El Chapo Isidro" captured in Sinaloa; 11 killed
3. **War at sea** — suspected Ukrainian sea drones hit a Russian warship off Libya
4. **Indonesia** — candy factory fire in Cikande; 3 killed, dozens missing
5. **Israel** — coalition talks end with no deal; settler arson condemned
6. **Markets** — Asian governments step in as the AI sell-off eases
7. **Sport** — Liverpool 4–0 Manchester United at Anfield
8. **Nepal** — PM Balendra Shah begins his first visit to India

## Files

- `entry.png` — the image (1024×1024 PNG, ≤1 MiB)
- `main.ts` — Node 22, stdlib only: copies `entry.png` to
  `MAKEFUN_OUTPUT_DIR` (or `/output/entry.png`)
- `build_image.py` — the script that drew `entry.png` (re-run to rebuild it)
- `SOURCES.md` — every story with its source URL and date
- `LICENSE` — MIT, copied from the kit starter

## Test

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Run twice and compare: both runs must write identical bytes. Verified
2026-11-23: two runs produced identical SHA256, 1024×1024, under 1 MiB.
