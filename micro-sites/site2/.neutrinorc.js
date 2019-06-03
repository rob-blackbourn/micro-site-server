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
      publicPath: '/micro-site/site2/ui/',
      devServer: {
        port: 10302,
        disableHostCheck: true,
        historyApiFallback: {
          rewrites: [
            {
              from: /^\/micro-site\/site2\/ui\/.+$/,
              to: '/micro-site/site2/ui/',
            },
          ],
        },
      },
    }),
  ],
};
