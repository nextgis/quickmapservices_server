const path = require('path');
const utils = require('./build/utils');
const webpack = require('webpack');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const OptimizeCSSPlugin = require('optimize-css-assets-webpack-plugin');
const safeParser = require('postcss-safe-parser');

const fs = require('fs');

function resolve(dir) {
  return path.join(__dirname, '.', dir)
}

module.exports = (env, argv) => {

  const isProduction = argv.mode === 'production';

  const rules = [
    {
      test: /\.vue$/,
      loader: 'vue-loader',
      options: {
        loaders: utils.cssLoaders({
          sourceMap: isProduction ? false : true,
          extract: true
        })
      }
    },
    {
      resourceQuery: /blockType=i18n/,
      type: 'javascript/auto',
      loader: '@kazupon/vue-i18n-loader'
    },
    {
      test: /\.js$/,
      loader: 'babel-loader',
      include: [resolve('src'), resolve('test')]
    },
    {
      test: /\.(png|jpe?g|gif|svg)(\?.*)?$/,
      loader: 'url-loader',
      options: {
        limit: 10000,
        name: utils.assetsPath('img/[name].[ext]')
      }
    },
    {
      test: /\.(woff2?|eot|ttf|otf)(\?.*)?$/,
      loader: 'url-loader',
      options: {
        limit: 10000,
        name: utils.assetsPath('fonts/[name].[ext]')
      }
    }
  ].concat(utils.styleLoaders({
    sourceMap: true,
    extract: true
  }));

  const plugins = [
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': JSON.stringify(argv.mode)
    }),

    new ExtractTextPlugin({
      filename: 'css/[name].css',
      allChunks: true,
    }),

    new VueLoaderPlugin(),

    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery',
      validator: 'jquery-validation'
    }),
  ];

  if (isProduction) {
    const CompressionWebpackPlugin = require('compression-webpack-plugin');

    plugins.push(
      new CompressionWebpackPlugin({
        test: new RegExp(
          '\\.(' +
          ['js', 'css'].join('|') +
          ')$'
        )
      })
    );
    plugins.push(
      new OptimizeCSSPlugin({
        cssProcessorOptions: {
          parser: safeParser,
          discardComments: {
            removeAll: true
          }
        }
      })
    );
  }

  // const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
  // plugins.push(new BundleAnalyzerPlugin());

  let alias = {
    'vue': 'vue/dist/vue.esm.js',
    '@': resolve('src'),
  }
  let alias_ext = JSON.parse(fs.readFileSync(__dirname + '/webpack.config.alias.ext.json', 'utf8'));
  alias = Object.assign({}, alias, alias_ext);

  let entry = {
    app: [
      '@babel/polyfill',
      'whatwg-fetch',
      './src/main.js'
    ]
  }
  let entry_ext = JSON.parse(fs.readFileSync(__dirname + '/webpack.config.entry.ext.json', 'utf8'));
  entry = Object.assign({}, entry, entry_ext);

  return {

    mode: 'development',

    entry: entry,

    resolve: {
      extensions: ['.js', '.vue', '.json'],
      alias: alias,
      modules: [ 
        path.resolve(__dirname, './node_modules'), 
        path.resolve(__dirname, '../nextgis_common/node_modules/'), 
      ]
    },
    module: {
      rules
    },
    // cheap-module-eval-source-map is postcss-safe-parseraster for development
    devtool: isProduction ? 'none' : '#cheap-module-eval-source-map',

    output: {
      path: path.resolve(__dirname, './dist/'),
      filename: 'js/[name].js',
      chunkFilename: 'js/[name].js',
      publicPath: '/static/'
    },

    optimization: {
      splitChunks: {
        cacheGroups: {
          vendor: {
            test: /node_modules/,
            chunks: 'initial',
            name: 'vendor',
            priority: 10,
            enforce: true
          }
        }
      },
      runtimeChunk: {
        name: 'manifest',
      },
    },

    plugins
  }


}

