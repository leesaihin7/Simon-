# Aris Mansor Sofiyan – Portfolio, CV and Slides

Plain HTML and CSS, no build step.

## Files
- `index.html`, `style.css`: the website
- `assets/Aris-Mansor-Sofiyan-CV.pdf`: one-page CV (visitors can download it)
- `assets/Aris-Mansor-Sofiyan-Slides.pdf`: six-slide profile deck
- `tools/build_pdfs.py`: regenerates both PDFs

## Update your details
1. Edit the text in `index.html`.
2. Edit the same details at the top of `tools/build_pdfs.py` (the CONTENT section).
3. Run `pip install reportlab` then `python tools/build_pdfs.py` to rebuild the PDFs.
4. Optional: put `Roboto-Regular.ttf`, `Roboto-Medium.ttf` and `Roboto-Bold.ttf` in `fonts/` first and the PDFs will use Roboto too.

## Deploy with GitHub and Netlify
1. Upload this whole folder to a new GitHub repository.
2. In Netlify: Add new site, Import an existing project, GitHub, pick the repo.
3. Leave the build command empty and the publish directory blank, then Deploy.
