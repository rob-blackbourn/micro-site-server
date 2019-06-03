import React from 'react'
import { AuthenticationConsumer } from '../authentication/components'
import AuthenticatedSite from './AuthenticatedSite'

class SiteAuthenticationProvider extends React.Component {
  render () {
    return (
      <div>
        <AuthenticationConsumer>
          {authenticator => (
            <AuthenticatedSite authenticator={authenticator} />
          )}
        </AuthenticationConsumer>
      </div>
    )
  }
}

export default SiteAuthenticationProvider
