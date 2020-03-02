var path = require('path')
var webpack = require('webpack');
var helpers = require('./helpers');



module.exports = {
    output: {
        path: path.resolve(__dirname, '../', 'dj','main','static','dist'),
        publicPath: '/',
        filename: '[name].js'
    },
    resolve: {
        extensions: ['.ts', '.js']
      },
    module: {
        rules: [
            {
                test: /\.ts$/,
                loaders: ['awesome-typescript-loader', 'angular2-template-loader'],
                include: helpers.root('js_apps'),
            },
            {
                test: /\.css$/,
                loaders: 'style-loader!css-loader',
                include: helpers.root('js_apps')
            },

            {
                test: /\.html$/,
                loader: 'html-loader',
                include: helpers.root('js_apps')
            }

        ]    
    }
}

/*



    filename: '[name].[hash].js'

*/