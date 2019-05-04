var path = require('path')
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

exports.assetsPath = function (_path) {
  var assetsSubDirectory = '';
  return path.posix.join(assetsSubDirectory, _path)
}

exports.cssLoaders = function (options) {
  options = options || {}

  const cssLoader = {
    loader: 'css-loader'
  }

  // generate loader string to be used with extract text plugin
  function generateLoaders(loader, loaderOptions) {
    var loaders = [cssLoader]
    if (loader) {
      const opt = {
        loader: loader + '-loader',
      };
      if (loaderOptions) {
        opt.options = Object.assign({}, loaderOptions, {
          sourceMap: options.sourceMap
        });
      }
      loaders.push(opt)
    }

    // Extract CSS when that option is specified
    // (which is the case during production build)
    if (options.extract) {
      return [MiniCssExtractPlugin.loader].concat(loaders);
      // console.log(use);
      // return {
      //   use,
      //   fallback: 'vue-style-loader'
      // };
    } else {
      return ['vue-style-loader'].concat(loaders)
    }
  }

  // https://vue-loader.vuejs.org/en/configurations/extract-css.html
  return {
    css: generateLoaders(),
    postcss: generateLoaders(),
    less: generateLoaders('less'),
    sass: generateLoaders('sass', { indentedSyntax: true, includePaths: [path.resolve(__dirname, "../../node_modules")] }),
    scss: generateLoaders('sass', { includePaths: [path.resolve(__dirname, "../../node_modules")] }),
    stylus: generateLoaders('stylus'),
    styl: generateLoaders('stylus')
  }
}

// Generate loaders for standalone style files (outside of .vue)
exports.styleLoaders = function (options) {
  var output = []
  var loaders = exports.cssLoaders(options)
  for (var extension in loaders) {
    var loader = loaders[extension]
    output.push({
      test: new RegExp('\\.' + extension + '$'),
      use: loader
    })
  }
  return output
}
