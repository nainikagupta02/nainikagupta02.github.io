# nainikagupta website setup

This site uses the original Academic Pages Jekyll template, with its layout and license retained.

Target repository: `nainikagupta02/nainikagupta.github.io`
Target URL after publishing: `https://nainikagupta02.github.io/nainikagupta.github.io/`

## Personalize

- `_config.yml`: name, sidebar bio, affiliation, email, and profile links.
- `_pages/home.md`: introduction and background on the homepage.
- `_pages/experience.md`: experience and education.
- `_pages/projects.md`: projects.
- `_pages/notes.md`: informal notes and writing.
- `_pages/writing-presentations.md`: conference presentations, articles, and white papers.
- `_pages/beyond-research.md`: leadership, service, awards, and recognition.
- `_pages/cv.md`: résumé content. Add an actual résumé PDF to `files/` before linking it.
- `_publications/`: one Markdown file per publication.
- `_data/navigation.yml`: visible menu items.
- `images/profile.png`: replace the template portrait with your own picture.

Original sample collections are preserved in `template-examples/` and excluded from the generated website. Copy an example into the corresponding collection and replace all sample content when adding a real item.

## Publish on GitHub Pages

1. Create a repository named `nainikagupta.github.io` under the `nainikagupta02` account.
2. Upload this folder's contents, including `.github/`, but not its `.git/` directory. Retain `LICENSE`.
3. In repository Settings → Pages, select **GitHub Actions** as the build source.
4. Run the **Deploy Academic Pages template site to Pages** workflow, or push to `main` or `master`.
5. Open the URL only after the workflow has completed successfully.

The site remote is https://github.com/nainikagupta02/nainikagupta.github.io.git. GitHub Pages uses the repository subpath `/nainikagupta.github.io`.

## Local preview

Use Ruby 3.3 and a current Bundler, then run:

```sh
bundle install
bundle exec jekyll serve --livereload
```

Open the localhost URL printed by Jekyll. Restart Jekyll after editing `_config.yml`.

The system Ruby is 2.6. This Mac also has a bundled Ruby 3.3.7 that can run the preview:

```sh
BUNDLE_PATH=vendor/bundle /usr/local/Homebrew/Library/Homebrew/vendor/portable-ruby/3.3.7/bin/ruby -S bundle exec jekyll serve --host 127.0.0.1 --port 4000
```

Then open http://127.0.0.1:4000. Keep the terminal running while viewing the site.
