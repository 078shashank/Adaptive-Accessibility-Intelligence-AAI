const path = require('path');
const CopyPlugin = require('copy-webpack-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

module.exports = {
  entry: {
    // Content script
    'content/content': './content/content.js',
    // Popup script
    'popup/popup': './popup/popup.js'
  },
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].js',
    clean: true
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env']
          }
        }
      },
      {
        test: /\.jsx$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-react']
          }
        }
      },
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader']
      },
      {
        test: /\.(png|svg|jpg|jpeg|gif)$/i,
        type: 'asset/resource'
      },
      {
        test: /\.(woff|woff2|eot|ttf|otf)$/i,
        type: 'asset/resource'
      }
    ]
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.jsx', '.js', '.json']
  },
  plugins: [
    new CleanWebpackPlugin(),
    new CopyPlugin({
      patterns: [
        { 
          from: 'manifest.json', 
          to: 'manifest.json' 
        },
        { 
          from: 'background.js', 
          to: 'background.js' 
        },
        { 
          from: 'popup/popup.html', 
          to: 'popup/popup.html' 
        },
        { 
          from: 'popup/popup.css', 
          to: 'popup/popup.css' 
        },
        { 
          from: 'styles/injected.css', 
          to: 'styles/injected.css' 
        },
        { 
          from: 'icons', 
          to: 'icons',
          noErrorOnMissing: true
        },
        { 
          from: 'fonts', 
          to: 'fonts',
          noErrorOnMissing: true
        }
      ]
    })
  ],
  mode: process.env.NODE_ENV === 'production' ? 'production' : 'development',
  devtool: process.env.NODE_ENV === 'production' ? false : 'source-map',
  optimization: {
    minimize: process.env.NODE_ENV === 'production'
  }
};
