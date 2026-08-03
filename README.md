# NDE Lab — Research Group Website

This is the implementation for group website. Our group Non-Destructive Evaluation (NDE) Labe under guidance of **Prof. Biju N**, Cochin University of Science and Technology (CUSAT). Structure and information architecture are modelled here for our site; the visual identity uses a **red / white** academic scheme.

Some content is in lorem epsum and lorem picsum for place holders.

---

## What's inside

```
asdg-site/
├── index.html          Home
├── about.html          About · Director's message · Mission/Vision/Values
├── research.html       Focus areas · Themes · Projects
├── people.html         PI · Scholars · Students · Alumni
├── publications.html   Filterable publication list
├── facilities.html     Labs & equipment
├── news.html           News & events
├── contact.html        Contact form + map
├── css/style.css       Full design system (all styling)
├── js/main.js          Nav, hero slider, scroll reveals, filters
├── assets/favicon.svg  Logo mark
├── build.py            Optional generator (regenerates all HTML)
└── README.md
```

The `.html` files are **fully standalone static pages** — no build step or server
is required. Open `index.html` in a browser and it just works.

---

## Quick start

**Preview locally** — just double-click `index.html`, or run a tiny server:

```bash
cd asdg-site
python3 -m http.server 8000
# then open http://localhost:8000
```

---

## Publish free on GitHub Pages

1. Create a new GitHub repository.
2. Upload **all** files from this folder to the repo root (keep the folder
   structure — `css/`, `js/`, `assets/` must stay as-is).
3. In the repo: **Settings → Pages → Build and deployment → Source: Deploy from a
   branch**, pick `main` and `/ (root)`, then **Save**.
4. Your site goes live at `https://<username>.github.io/asdg-website/` in a minute
   or two.

> A `.nojekyll` file is included so GitHub Pages serves every file as-is.

---

## Customising the content

You have two equally valid options.

### Option A — edit the HTML directly (simplest)
Open any `.html` file and replace the lorem ipsum text and Picsum image URLs. The
markup is readable and commented by section. This is all most people need.

### Option B — edit `build.py` and regenerate (best for bulk changes)
The site was generated from `build.py`, which defines the shared header, footer and
all page content in one place. This is handy when you want to change something on
**every** page at once (e.g. the group name, nav links, or footer).

```bash
python3 build.py     # rewrites all .html files
```

Key things to edit in `build.py`:

| What | Where |
|------|-------|
| Group name, email, phone, address | `SITE = { ... }` near the top |
| Navigation menu & dropdowns | `NAV = [ ... ]` |
| People / publications / projects | the `build_*()` function for that page |
| Colours & fonts | `css/style.css` → `:root` variables (not build.py) |

### Replacing images
Search-and-replace `https://picsum.photos/seed/...` URLs with your own image paths,
e.g. put files in `assets/img/` and reference `assets/img/rig.jpg`.

### Colours
Every colour lives in CSS variables at the top of `css/style.css`:

```css
:root {
  --red:        #b01e28;   /* primary */
  --red-dark:   #8a141c;   /* hover */
  --red-bright: #e63946;   /* accents */
  --ink:        #1a1417;   /* text */
  --paper:      #faf8f6;   /* background */
}
```

Change these five and the whole site re-themes.

### Fonts
Loaded from Google Fonts in each page's `<head>`: **Source Serif 4** (headings),
**Inter** (body), **IBM Plex Mono** (labels). Swap the `<link>` and the
`--serif / --sans / --mono` variables to change them.

---

## Making the contact form actually send

The form is front-end only (it validates and shows a demo message). To receive
submissions without a backend, connect it to a free service:

- **[Formspree](https://formspree.io)** — set the form's `action` to your Formspree
  endpoint and change the submit handler, or
- **Netlify Forms** — add `netlify` to the `<form>` tag if hosting on Netlify.

See the note inside `js/main.js` (`#contact-form` handler).

---

## Notes

- Responsive from large desktop down to small phones.
- Keyboard-accessible nav, visible focus states, and `prefers-reduced-motion`
  respected.
- The map on the Contact page uses a free OpenStreetMap embed pointed at the CUSAT
  area — adjust the coordinates in `contact.html` for the exact building.

Placeholder content throughout — replace before publishing. 🚩
