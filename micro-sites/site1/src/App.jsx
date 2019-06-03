import { hot } from 'react-hot-loader'
import React from 'react'
import './App.css'
import Site from './components/SiteAuthenticationProvider'

const App = () => (
  <div className='App'>
    <Site />
  </div>
)

export default hot(module)(App)
