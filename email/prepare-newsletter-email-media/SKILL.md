---
name: Prepare newsletter email media
description: >-
  Use when a newsletter or email campaign's images and GIFs need converting,
  resizing, compressing, numbering and filing in the issue's storage folder
  before the email or website goes out.
---
# Prepare newsletter email media

The routine or request names where the draft lives (e.g. a Notion page) and the storage folder for the issue (e.g. Dropbox or Drive). This recipe is the how.

## Scope
Email-ready media only. No edits to the draft, no posting, no email scheduling.

## Scale (default rules)
| Item | Rule |
|---|---|
| Max width | 1280px (a typical email column is 640px, 2x for retina). Never upscale. |
| Still images | Always JPEG, including flat diagrams and PNGs with transparency (flatten on white). Quality 82, progressive, metadata stripped. Extension `.jpg`. |
| GIFs | Keep as GIF, max width 1280 (usually already smaller). Target each under ~3MB, hard cap 4MB. |
| GIF reduction order | 1) `gifsicle -O3 --lossy=30`, 2) reduce to 128 colours, 3) drop every other frame and double frame delay so duration stays the same, 4) repeat drop if still over. Keep original if optimising makes it bigger. Keep infinite loop. |
| Whole email | Aim for about 4MB total or less; flag if above, suggesting which GIF to thin. |
| Videos | Out of scope; note if present. |

## Naming & location
- Content files: `N.lowercase-hyphen-slug.ext`, numbered 1..N sequentially in order of appearance, even when the source filenames skip numbers.
- Hero/cover images pre-made by the author (square, OG 1200x630, social banners) stay as they are; don't re-upload one if it's byte-identical.
- Never overwrite or delete existing files in the storage folder.

## Steps
1. Find the issue that's ready (e.g. the draft marked as scheduled) and read its body.
2. Download every image/GIF in order of appearance to a working folder on your computer (e.g. `newsletter-media/issue-N/originals/`).
3. Process according to the scale above into `newsletter-media/issue-N/final/`. Check GIF frames by eye.
4. Upload to the issue's storage folder. If the storage connector can't upload images, use the storage website in the box browser (sign in with the login saved in the Grok Bot vault, or hand the browser to the owner). Afterwards verify every file with the connector's folder listing and check the sizes.
5. Report a table with original, final name, dimensions and size, the total weight, and any draft problems noticed (stray text, wrong dates).
