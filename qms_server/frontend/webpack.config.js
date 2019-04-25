const path = require('path');
const utils = require('./build/utils');
const webpack = require('webpack');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const OptimizeCSSPlugin = require('optimize-css-assets-webpack-plugin');
const safeParser = require('postcss-safe-parser');

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


  return {

    mode: 'development',

    entry: {
      app: ['@babel/polyfill', 'whatwg-fetch', './frontend/src/main.js']
    },
    resolve: {
      extensions: ['.js', '.vue', '.json'],
      alias: {
        'vue$': 'vue/dist/vue.esm.js',
        '@': resolve('src'),
        '@nextgis_common': resolve('../nextgis_common/frontend/src')
      }
    },
    module: {
      rules
    },
    // cheap-module-eval-source-map is faster for development
    devtool: isProduction ? 'none' : '#cheap-module-eval-source-map',

    output: {
      path: path.resolve(__dirname, './dist/'),
      filename: 'js/[name].js',
      chunkFilename: 'js/[name].js',
      publicPath: '../'
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

