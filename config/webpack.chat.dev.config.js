var commonConfig = require('./webpack.common.config.js');
var webpackMerge = require('webpack-merge');
var webpack = require('webpack');
var helpers = require('./helpers');

module.exports = webpackMerge(commonConfig, {
    watch: true,
    entry: {
    
        'chat_vendor': './js_apps/chat/vendor.ts',
        'chat': './js_apps/chat/main.ts'
        
    },
    plugins: [
        new webpack.optimize.UglifyJsPlugin(),
        new webpack.ContextReplacementPlugin(/\@angular(\\|\/)core(\\|\/)esm5/, helpers.root('./js_apps')),
        new webpack.optimize.CommonsChunkPlugin({
            name: ['chat', 'chat_vendor']
          })
      ]
});
