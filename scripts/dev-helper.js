// Helper to detect development mode in templates
hexo.extend.helper.register('is_dev', function() {
  return hexo.env.cmd === 'server' || hexo.env.cmd === 's';
});
