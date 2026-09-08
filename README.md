# Clark's Botanicals — interactive mockup

A pixel-close, self-contained static replica of [clarksbotanicals.com](https://clarksbotanicals.com),
built by Growisto as a CRO prototype. No build step, no dependencies — every page is plain
HTML with inlined CSS/JS, and every image is localised into `assets/`, so it runs offline
by opening `index.html` in a browser.

**Password gate:** `clarks2026` (client-side only — it hides the page, it does not secure it).

## Pages

| File | What it is |
| --- | --- |
| `index.html` | Hub linking the three pages |
| `home.html` | Hero, Editor's Favorites, press bands, Real People rail, before/after, subscription banner |
| `collection.html` | Sticky Sort/Filter toolbar, 16 products, working filters + sort |
| `product.html` | DNA-42 Clinicalift Serum — gallery, Subscribe + Save, accordions, before/after, Amalfi |

Shared across every page: announcement bar, sticky header with hover mega menus, mobile
drill-down drawer, predictive search panel, mini-cart drawer, variant modal, footer.

## Interactive behaviour

Everything is vanilla JS — no framework, no external runtime.

- Mega menus on hover, drill-down mobile drawer, predictive search panel
- Mini-cart with quantity, remove, subscription lines, Most Loved, `CHECKOUT · $X`
- Variant modal (Quick add) reused from cards, cart and Most Loved
- PLP product-type filters with active-filter chips, and five sort orders
- Draggable before/after comparison sliders
- PDP gallery with thumbnail rail, quantity stepper, Subscribe + Save pricing
- Cart state persists in `localStorage`

## Regenerating

The pages are generated, not hand-edited. Edit the generator and re-run it rather than
patching the HTML.

```bash
cd build
python3 build_mockups.py     # writes the HTML and downloads + localises every asset
python3 optimize.py          # resizes/recompresses assets (needs Pillow and ffmpeg)
```

`build_mockups.py` reads product data from `cap/data_products.json` (scraped from the live
store's `products.json`) and PDP copy from `cap/pdp_accordions.json`.

- `parts_css.py` — the full stylesheet
- `parts_js.py` — the full client-side script
- `build_mockups.py` — page markup, nav tree, section stack, asset localiser
- `optimize.py` — image/GIF compression pass

Set a different gate password with `CB_PW=yourpassword python3 build_mockups.py`.

## Deployment

Static — Vercel serves the repository root as-is. `vercel.json` only sets cache headers and
keeps `.html` URLs literal (no clean-URL rewrites), so in-page links like `home.html` resolve
without a redirect hop.

## Notes

Product imagery, copy and pricing are reproduced from the live Clark's Botanicals store for
prototyping purposes. Content and trademarks belong to Clark's Botanicals.
