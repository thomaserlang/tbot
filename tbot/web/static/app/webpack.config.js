const webpack = require('webpack');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const HtmlWebpackPlugin = require('html-webpack-plugin');
const path = require("path");

pages = [
  'twitch/widgets/goal',
]

let entries = {}
pages.forEach(name => {
    entries[name.replace(/\//gi, '_')] = {
        import: './src/'+name+'/index.jsx',
        dependOn: 'vendor',
    }
})

plugins = pages.map(name => {
    return new HtmlWebpackPlugin({
        'filename': '../../../templates/'+name+'.html',
        'template': './src/'+name+'/index.html',
        'chunks': [name.replace(/\//gi, '_'), 'vendor'],
        'publicPath': '/static',        
        'minify': false
    })
})

module.exports = {
  entry: {
    main: {
      import: './src/index.jsx',
      dependOn: 'vendor',
    },
    vendor: [
      'axios', 
      'react', 
      'react-router-dom',
      'react-router-config',
      'query-string',
      'moment',
      'downshift',
    ],
    ...entries
  },
  devtool: "source-map",
  resolve: {
    extensions: ['.js', '.jsx'],
    alias: {
      tbot: path.resolve(__dirname, 'src'),
    }
  },    
  module: {
    rules: [
      {
        test: /\.(jsx|js)?$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        },
      },
      {
        test: /\.(scss)$/,
        use: [
          MiniCssExtractPlugin.loader,
          { loader: 'css-loader', options: { url: false, sourceMap: true } },
          { loader: 'sass-loader', options: { sourceMap: true } }
        ],
      }
    ]
  },
  plugins: [
    new webpack.ProvidePlugin({
      "React": "react",
    }),
    new MiniCssExtractPlugin({
      filename: "[name].[contenthash].css",
      chunkFilename: "[id].[contenthash].css",
    }),
    new HtmlWebpackPlugin({
      'filename': '../../../templates/react.html',
      'template': './src/index.html',
      'chunks': ['main', 'vendor'],
      'publicPath': '/static',
      'minify': false
    }),
    ...plugins
  ],
  output: {
    filename: '[name].[contenthash].js',
    path: path.resolve(__dirname, 'dist'),
    clean: true,
  },
};