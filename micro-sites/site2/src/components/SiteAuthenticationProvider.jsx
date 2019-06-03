import React from 'react'
import { AuthenticationProvider } from '../authentication/components'
import SiteAuthenticationConsumer from './SiteAuthenticationConsumer'
import { HOST, AUTH_LOGIN_PATH } from '../config'

class SiteAuthenticationProvider extends React.Component {
  render () {
    return (
      <div>
        <AuthenticationProvider
          host={HOST}
          path={AUTH_LOGIN_PATH}
        >
          <SiteAuthenticationConsumer />
        </AuthenticationProvider>
      </div>
    )
  }
}

export default SiteAuthenticationProvider
