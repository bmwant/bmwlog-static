## bmwlog
This is static blog website generated with Hexo using [Artemis](https://github.com/Dreyer/hexo-theme-artemis) theme.

🌎 Check [the website](https://bmwlog.pp.ua/)

### Installation

```bash
$ npm install
$ cd themes/artemis && npm run build  # rebuild theme with different params
```

### Editing
```bash
$ hexo new [layout] <title>  # check `scaffolds` directory for available layouts
$ hexo new post "Test post"
$ hexo new draft "New draft"
```

### Deployment
```bash
$ firebase init  # first time only
$ hexo clean  # just to make sure old/removed pages are cleaned up
$ hexo generate
$ firebase deploy --only hosting
```

or simply

```bash
$ hexo deploy
$ hexo deploy -g  # to generate site before deployment
```
