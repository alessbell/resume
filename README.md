# resume!

Inspired by [`dcousineau/resume`](https://github.com/dcousineau/resume) -- especially the clever strategy of using `releases` as an archive of various "built" states over time.

If you're on a mac, `brew cask install mactex && pdflatex resume.tex`

# automated releases

As of October 2019, I've automated the process for generating GitHub releases of new versions of my resume.

First, I compile a new `resume.pdf` using this excellent [LaTeX Action](https://github.com/xu-cheng/latex-action) which uses `pdfLaTeX` under the hood. Then I use the [GH Release action](https://github.com/marketplace/actions/gh-release) to upload the newly-generated `resume.pdf` as a release asset. 🎉

Finally, I kick off a GitHub Action in my blog's repo, [`alessbell/aless.co`](https://github.com/alessbell/aless.co), and open a PR with the PDF release asset from the latest release. I've written more about how I've automated this flow [here](https://aless.co/resume-as-code/).
