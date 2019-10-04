# resume!

Inspired by [`dcousineau/resume`](https://github.com/dcousineau/resume) -- especially the clever strategy of using `releases` as an archive of various "built" states over time.

If you're on a mac, `brew cask install mactex && pdflatex resume.tex`

# automated releases

As of October 2019, I've automated the process for generating GitHub releases of new versions of my resume.

First, I compile a new `resume.pdf` using this excellent [LaTeX Action](https://github.com/xu-cheng/latex-action) which uses `pdfLaTeX` under the hood. Then I use the [GH Release action](https://github.com/marketplace/actions/gh-release) to upload the newly-generated `resume.pdf` as a release asset. 🎉
