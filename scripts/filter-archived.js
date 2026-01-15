// Override index generator to exclude archived posts from main listing
// This fixes pagination to only count non-archived posts

const pagination = require('hexo-pagination');

// Remove the default index generator
hexo.extend.generator.register('index', function(locals) {
  const config = this.config;
  const posts = locals.posts.sort(config.index_generator.order_by).filter(function(post) {
    return !post.archived;
  });

  const paginationDir = config.pagination_dir || 'page';
  const path = config.index_generator.path || '';
  const perPage = config.index_generator.per_page;

  return pagination(path, posts, {
    perPage: perPage,
    layout: ['index', 'archive'],
    format: paginationDir + '/%d/',
    data: {
      __index: true
    }
  });
});
