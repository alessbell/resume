# resume!

Inspired by [`dcousineau/resume`](https://github.com/dcousineau/resume) -- especially the clever strategy of using `releases` as an archive of various "built" states over time.

If you're on a mac, `brew install --cask mactex && pdflatex resume.tex`

# automated releases

As of October 2019, I've automated the process for generating GitHub releases of new versions of my resume.

First, I compile a new `resume.pdf` using this excellent [LaTeX Action](https://github.com/xu-cheng/latex-action) which uses `pdfLaTeX` under the hood. Then I use the [GH Release action](https://github.com/marketplace/actions/gh-release) to upload the newly-generated `resume.pdf` as a release asset. 🎉

Finally, I kick off a GitHub Action in my blog's repo, [`alessbell/aless.co`](https://github.com/alessbell/aless.co), and open a PR with the PDF release asset from the latest release. I've written more about how I've automated this flow [here](https://aless.co/resume-as-code/).

# steps to publish

1. Cut a branch, make some changes and add a new commit. Then run e.g. `git tag -a v1.4 -m "Release v1.4, adds new job"` and create a PR.

2. Push local tags up with `git push origin --tags`. This will kick off the GitHub action. After it succeeds, merge the pull request.⚡️
