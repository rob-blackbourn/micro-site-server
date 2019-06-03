import React, { Component } from 'react'
import PropTypes from 'prop-types'

import AuthenticationContext from './AuthenticationContext'
import Authenticator from '../api/Authenticator'

class AuthenticationProvider extends Component {
  constructor (props) {
    super(props)
    this.authenticator = new Authenticator(this.props.host, this.props.path)
  }

  render () {
    return (
      <AuthenticationContext.Provider value={this.authenticator}>
        {this.props.children}
      </AuthenticationContext.Provider>
    )
  }
}

AuthenticationProvider.propTypes = {
  host: PropTypes.string.isRequired,
  path: PropTypes.string.isRequired
}

export default AuthenticationProvider
