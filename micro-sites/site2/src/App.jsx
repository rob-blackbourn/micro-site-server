import { hot } from 'react-hot-loader'
import React from 'react'
import CssBaseline from '@material-ui/core/CssBaseline'
import SiteAuthenticationProvider from './components/SiteAuthenticationProvider'

const App = () => (
  <React.Fragment>
    <CssBaseline />
    <SiteAuthenticationProvider />
  </React.Fragment>
)

export default hot(module)(App)
