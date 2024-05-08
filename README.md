## bmwlog

![Deploy](https://github.com/bmwant/bmwlog-static/actions/workflows/firebase-hosting-deploy.yml/badge.svg)
[![EditorConfig](https://img.shields.io/badge/-EditorConfig-lightgrey?logo=editorconfig)](https://editorconfig.org/)

This is static blog website generated with [Hexo](https://hexo.io/) using [Artemis](https://github.com/Dreyer/hexo-theme-artemis) theme.

🌎 Check [the website](https://bmwant.link/)

### Installation

```bash
$ npm install
$ npm install -g grunt-cli
$ cd themes/artemis && npm run build  # rebuild theme with different params
$ npm run serve  # check website locally

$ cd themes/artemis && npm run watch  # for developing and changing styles

$ firebase emulators:start  # preview site locally with firebase
```

### Editing

```bash
$ npx hexo new [layout] <title>  # check `scaffolds` directory for available layouts
$ hexo new post "Test post"
$ hexo new draft "New draft"
$ hexo publish post "New draft"
```

### Deployment

```bash
$ firebase init  # first time only
$ firebase init hosting:github  # setup automated deployment via Github Actions
$ hexo clean  # just to make sure old/removed pages are cleaned up
$ hexo generate
$ firebase deploy --only hosting
```

or simply

```bash
$ hexo deploy
$ hexo deploy -g  # to generate site before deployment
```

### Post writing hints

- Insert image

```markdown
![alt text](/images/picture.png)
```

- Refer to another article

```markdown
[Link title](slug-for-the-article)
```
