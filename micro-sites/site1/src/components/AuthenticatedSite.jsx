import React from 'react'
import PropTypes from 'prop-types'
import { Route } from 'react-router-dom'
import DashboardRouter from './DashboardRouter'
import Page1 from './Page1'
import Page2 from './Page2'
import { SITE_NAVIGATOR_URL } from '../config'

class AuthenticatedSite extends React.Component {
  state = {
    applications: []
  }

  links = [
    {
      code: 'page1',
      title: 'Page1',
      description: 'First page',
      path: '/page1/',
      icon: 'shopping_cart'
    },
    {
      code: 'page2',
      title: 'Page2',
      description: 'Second page',
      path: '/page2/',
      icon: 'history'
    }
  ]

  componentDidMount () {
    const { authenticator } = this.props

    authenticator.fetch(SITE_NAVIGATOR_URL)
      .then(response => {
        if (response.status >= 300) {
          throw new Error('Invalid status')
        }
        return response.json()
      }).then(sites => {
        const applications = sites.map(({ code, title, description, url, icon }) => ({
          code,
          title,
          description,
          url,
          icon,
          disabled: !window.location.pathname.startsWith(url)
        }))
        this.setState({ applications })
      }).catch(error => {
        console.error(error)
      })
  }

  renderPage1 = ({ ...renderProps }) => {
    return <Page1 authenticator={this.props.authenticator} />
  }

  renderPage2 = () => {
    return <Page2 authenticator={this.props.authenticator} />
  }

  render () {
    const { applications } = this.state

    return (
      <DashboardRouter
        title='Site 1'
        basename='/micro-site/site1/ui'
        applications={applications}
        routes={() => (
          <React.Fragment>
            <Route exact path='/' component={this.renderPage1} />
            <Route path='/page1' component={this.renderPage1} />
            <Route path='/page2' component={this.renderPage2} />
          </React.Fragment>
        )}
        links={this.links}
      />
    )
  }
}

AuthenticatedSite.propTypes = {
  authenticator: PropTypes.object.isRequired
}

export default AuthenticatedSite
