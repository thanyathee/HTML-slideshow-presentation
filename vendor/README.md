# vendor/

Source copied from three open-source projects, kept here for reference and reuse in the slideshow.
Copied as-is, not modified. Each project keeps its own license.

| Folder | Source | Commit | License |
|---|---|---|---|
| `react-three-fiber/` | https://github.com/pmndrs/react-three-fiber (`packages/fiber/src`) | d74622e | MIT (see `react-three-fiber/LICENSE`) |
| `liquid-glass-js/` | https://github.com/dashersw/liquid-glass-js (all source files, demo.gif left out) | 78cb6cc | MIT (see `liquid-glass-js/LICENSE`) |
| `shadergradient/` | https://github.com/ruucm/shadergradient (`packages/shadergradient`) | 68bdd74 | MIT, declared in package.json (the repo has no root LICENSE file) |

Notes
- react-three-fiber and shadergradient are React/TypeScript source. They need a build step (npm/pnpm) before they run in a browser, so they are not loaded by `index.html`.
- liquid-glass-js is plain JavaScript and CSS. Its `index.html` is a demo page.
