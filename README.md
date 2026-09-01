# KO Resume

Inspired by [`alessbell/resume`](https://github.com/alessbell/resume)

If you're on a mac, `brew install --cask mactex && pdflatex resume.tex`

## Single source of truth

`resume.tex` is the origin. The website's downloadable JSON + vCard **and** the
rendered page's data (`_data/resume.yml`) are all **generated** from it so they
can't silently drift:

```sh
python3 scripts/tex2resume.py resume.tex \
  --json ../obrien-k.github.io/assets/resume.json \
  --vcf  ../obrien-k.github.io/assets/resume.vcf \
  --yaml ../obrien-k.github.io/_data/resume.yml
```

After editing `resume.tex`: rebuild the PDF (`pdflatex resume.tex`, or push a
`v*.*` tag for the CI release), run the command above, and commit the refreshed
`resume.pdf` / `resume.json` / `resume.vcf` into the site repo. The generator is
idempotent — re-running on an unchanged `.tex` produces no diff.
