const standard = require('@neutrinojs/standardjs');
const react = require('@neutrinojs/react');

module.exports = {
  options: {
    root: __dirname,
  },
  use: [
    standard({
      env: {
        browser: true
      }
    }),
    react({
      html: {
        title: 'site1'
      },
      publicPath: '/micro-site/site1/ui/',
      devServer: {
        port: 10301,
        disableHostCheck: true,
        // historyApiFallback: {
        //   rewrites: [
        //     {
        //       from: /^\/chat\/ui\/.+$/,
        //       to: '/chat/ui/',
        //     },
        //   ],
        // },
      },
    }),
  ],
};
