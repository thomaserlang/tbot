const webpack = require('webpack');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const path = require("path");

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
      filename: "[name].css",
      chunkFilename: "[id].css",
    }),
  ],
  output: {
    filename: '[name].js',
    path: path.resolve(__dirname, 'dist'),
    clean: true,
  },
};