const path = require("path");
// const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const MinifyPlugin = require("babel-minify-webpack-plugin");

module.exports = {
    entry: './assets/main.js',
    output: {
        filename: 'main.js',
        path: path.resolve(__dirname, 'academy/static/js')
    },
    mode: 'production',
    // devtool: 'inline-source-map',
    module: {},
}
