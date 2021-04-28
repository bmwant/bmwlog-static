### Installation

```bash
$ npm install
$
```

### Editing
```bash
$ hexo new [layout] <title>  # check `scaffolds` directory for available layouts
$ hexo new post "Test post"
```


### Deployment
```bash
$ firebase init  # first time only
$ hexo clean  # just to make sure old/removed pages are cleaned up
$ hexo generate
$ firebase deploy --only hosting
```
