# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a static blog (bmwlog) built with [Hexo](https://hexo.io/) using the Artemis theme, deployed to Firebase Hosting.

## Common Commands

```bash
# Install dependencies
npm install
npm install -g grunt-cli  # required for theme building

# Local development
npm run serve              # start local server
npm run serve-drafts       # serve including draft posts

# Build
npm run build              # generate static site (hexo generate)
npm run clean              # clean generated files (hexo clean)

# Deploy (requires Firebase CLI)
npm run deploy             # deploy to Firebase hosting
hexo deploy -g             # generate and deploy in one step

# Theme development
cd themes/artemis && npm run build   # rebuild theme styles
cd themes/artemis && npm run watch   # watch for style changes

# Firebase local preview
firebase emulators:start   # serves on port 5050
```

## Content Management

```bash
# Create new content
hexo new post "Post Title"    # new post in source/_posts/
hexo new draft "Draft Title"  # new draft in source/_drafts/
hexo publish post "Draft"     # move draft to posts
```

## Project Structure

- `source/_posts/` - Published blog posts (markdown)
- `source/_drafts/` - Draft posts (not published)
- `source/images/` - Static images for posts
- `themes/artemis/` - Custom Hexo theme (uses Grunt/Sass)
- `scaffolds/` - Templates for new posts/drafts/pages
- `public/` - Generated static site (git-ignored)
- `_config.yml` - Main Hexo configuration
- `_config.artemis.yml` - Theme-specific configuration

## Node Version

Use Node.js 16.18 (see `.nvmrc`).

## Post Frontmatter

Posts use this frontmatter structure:
```yaml
---
title: Post Title
date: YYYY-MM-DD HH:mm:ss
tags: []
author: Misha Behersky
language: en
---
```

## Markdown Conventions

- Images: `![alt text](/images/picture.png)`
- Internal links: `[Link title](slug-for-the-article)`
