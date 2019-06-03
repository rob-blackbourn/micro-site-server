import { hot } from 'react-hot-loader'
import React from 'react'
import './App.css'
import SiteAuthenticationProvider from './components/SiteAuthenticationProvider'

const App = () => (
  <div className='App'>
    <SiteAuthenticationProvider />
  </div>
)

export default hot(module)(App)
