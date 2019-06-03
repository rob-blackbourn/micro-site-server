import React, { Component } from 'react'
import { Route } from 'react-router-dom'

class ExternalRoute extends Component {
  render () {
    const { link, ...routeProps } = this.props

    return (
      <Route
        {...routeProps}
        render={() => {
          window.location.replace(link)
          return null
        }}
      />
    )
  }
}

export default ExternalRoute
