import React from 'react'
import PropTypes from 'prop-types'
import AuthenticationContext from './AuthenticationContext'

function AuthenticationConsumer ({ children }) {
  return (
    <AuthenticationContext.Consumer>
      {authenticator => children(authenticator)}
    </AuthenticationContext.Consumer>
  )
}

AuthenticationConsumer.propTypes = {
  children: PropTypes.func.isRequired
}

export default AuthenticationConsumer
