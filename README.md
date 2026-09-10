# Clark's Botanicals — interactive mockup

A pixel-close, self-contained static replica of [clarksbotanicals.com](https://clarksbotanicals.com),
built by Growisto as a CRO prototype. The published pages have no runtime dependencies —
every page is plain HTML with inlined CSS/JS, and every image is localised into `assets/`,
so it runs offline by opening `index.html` in a browser. The HTML itself is generated:
see [Regenerating](#regenerating) before editing anything.

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

## Sticky add-to-cart (PDP)

`product.html` carries a sticky add-to-cart panel that appears whenever the main
**Add to cart** button is outside the viewport, and hides again when it scrolls back in.
Desktop renders it as a bottom-centred card; below 760px it becomes a bottom sheet that
slides up. It mirrors the main buy box — variant options, quantity, free-shipping
progress, subscribe & save with a delivery frequency — and adds to the same cart.

The free-shipping threshold is a placeholder: `FREE_SHIP` in `build/build_mockups.py`
(the live store does not publish one). Subscription discount is `SUB_DISCOUNT`.

## CRO revision (Sept 2026)

A round of conversion changes on top of the pixel-match replica. All of it lives in the
generator — editing the HTML directly will be lost on the next build.

| Change | Where |
| --- | --- |
| Prices show `$105.00`, never `$105.00 USD`. The header currency selector still reads `USD $`. | `product_card()`, `parts_js.py`, `strip_usd()` for the scraped accordion copy |
| Rating stars use `--star` (`#C8880A`) for legibility on white | `review_badge()`, `.pc__star` / `.stars` |
| Card titles clamp to two lines with a reserved min-height, so a short title cannot shorten the card | `.pc__title` |
| Add-to-cart sits on the card baseline, level across every row | `.pc` flex column, `.pc__add { margin-top:auto }` |
| Sold-out cards render a disabled "Sold out" button instead of an active buy action | `add_button()` |
| Announcement bar becomes a single-line continuous marquee below 1000px, pausing on hover and static under `prefers-reduced-motion` | `announce()`, `.ann__track` |
| Mobile header carries the logo only | `.hdr__in` under 1000px |
| Fixed mobile bottom nav: menu, shop, search, cart, account. Reuses the existing drawer handlers and mirrors the cart count. | `mobile_bottom_nav()`, `.mobnav` |
| Desktop: announcement and logo scroll away, only the primary nav pins to the top | `body.nav-stuck .pnav`, sticky-nav observer in `parts_js.py` |
| Homepage Bestsellers and New Arrivals rails | `product_rail()`, `BESTSELLERS` / `NEW_ARRIVALS` |
| PDP "past purchases" rail for signed-in visitors | `recs_rail()`, `RECS` |

The rails hold **handles only** — `product_card()` supplies pricing, badges and review
counts, so they cannot drift from the catalogue. Anti-Puff Eye Cream is excluded from both
because it is in `SOLD_OUT`.

Two things to remove when this stops being a mockup:

- The **"Signed out · demo"** pill bottom-right. It toggles `body.is-signed-in` in
  `localStorage` so the PDP recommendation rail can be demonstrated; real accounts replace it.
- The `RECS` reason copy ("You reordered this in March") is illustrative. Real
  personalisation needs order history.

On mobile the PDP's sticky add-to-cart bar stacks **above** the bottom nav rather than over
it — `--satc-h` is measured in JS and keeps the demo pill clear of both.

## Regenerating

The pages are generated, not hand-edited. Edit the generator and re-run it rather than
patching the HTML — a direct edit to `home.html` survives until the next build and then
disappears silently. Output goes to `clarks-mockups/` (gitignored); copy the four HTML
files to the repository root to publish.

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
