const path = require('path');
const webpack = require('webpack');

module.exports = {
  context: __dirname,
  entry: {
    datasource: path.join(__dirname, 'assets', 'js', 'datasource', 'index.jsx'),
    art: path.join(__dirname, 'assets', 'js', 'art', 'index.jsx'),
  },
  mode: 'development',
  devtool: 'source-map',
  output: {
    path: path.join(__dirname, 'assets', 'bundles'),
    filename: '[name].js',
    publicPath: '/static/',
  },
  resolve: {
    alias: {
      CABQ_DATASOURCE: path.join(__dirname, 'assets', 'js', 'datasource'),
      ArtQuestState: path.join(__dirname, 'assets', 'js', 'artquest'),
      ArtLocations: path.join(__dirname, 'assets', 'js', 'locations'),
    },
  },
  module: {
    rules: [
      {
        test: /\.js(x?)$/,
        loader: 'babel-loader',
        options: {
          presets: ['@babel/preset-react'],
        },
        include: [
          path.join(__dirname, 'assets', 'js'),
        ],
      }
    ],
  },
};
