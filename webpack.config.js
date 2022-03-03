const webpack = require('webpack');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const HtmlWebpackPlugin = require('html-webpack-plugin');
const path = require("path");

module.exports = {
  entry: {
    main: {
      import: './tbot/web/ui/index.jsx',
    },
  },
  devtool: "source-map",
  resolve: {
    extensions: ['.js', '.jsx'],
    alias: {
      tbot: path.resolve(__dirname, 'tbot/web/ui/'),
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
      'filename': path.resolve(__dirname, 'tbot/web/templates/ui/react.html'),
      'template': './tbot/web/ui/index.html',
      'chunks': ['main'],
      'publicPath': '/static/ui',
    }),
  ],
  output: {
    filename: '[name].[contenthash].js',
    path: path.resolve(__dirname, 'tbot/web/static/ui'),
    clean: true,
  },
};