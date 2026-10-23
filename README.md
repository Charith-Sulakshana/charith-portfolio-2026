# Charith Sulakshana: portfolio

Static site with no build step needed to host it. Drag this folder onto Netlify (or any static host) and `index.html` is the home page.

- `index.html`: the page (generated, see below)
- `css/style.css`, `js/app.js`: styles and behaviour (GSAP, ScrollTrigger and Lenis load from CDNs)
- `assets/img/`: every image from the Portfolio folder, converted to WebP
- `assets/media/`: the Bella Spencer reel (compressed, no sound) and its poster

## Editing text or adding work

All the words, captions and the order of the work are in `build.py`. Change them there, then run:

    python3 build.py

That rewrites `index.html` from `template.html`. To add an image, put a `.webp` in `assets/img/`, add its width and height to `assets/manifest.json`, then use it in `build.py` with `fig('slug', ...)`.

## Links

- `#analyst` at the end of the address opens the Business Analyst side directly.
