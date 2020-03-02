var commonConfig = require('./webpack.common.config.js');
var webpackMerge = require('webpack-merge');
var webpack = require('webpack');
var helpers = require('./helpers');

module.exports = webpackMerge(commonConfig, {
    watch: true,
    entry: {
    
        'rtc': './js_apps/rtc/main.ts'
        
    },
    plugins: [
        new webpack.optimize.UglifyJsPlugin(),
        new webpack.ContextReplacementPlugin(/\@angular(\\|\/)core(\\|\/)esm5/, helpers.root('./js_apps')),
        new webpack.optimize.CommonsChunkPlugin({
            name: ['rtc']
          })
      ]
});
