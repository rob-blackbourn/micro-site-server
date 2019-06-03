import React from 'react'
import PropTypes from 'prop-types'
import { BrowserRouter as Router, Route, Link } from 'react-router-dom'
import Page1 from './Page1'
import Page2 from './Page2'
import ExternalRoute from './ExternalRoute'
import { SITE_NAVIGATOR_URL } from '../config'

class AuthenticatedSite extends React.Component {
  state = {
    sites: []
  }
  pages = [
    { name: 'Page1', url: '/page1/' },
    { name: 'Page2', url: '/page2/' }
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
        this.setState({ sites: sites.filter(({ name, url }) => !window.location.pathname.startsWith(url)) })
      }).catch(error => {
        console.error(error)
      })
  }

  renderPage1 = () => {
    return <Page1 authenticator={this.props.authenticator} />
  }

  renderPage2 = () => {
    return <Page2 authenticator={this.props.authenticator} />
  }

  render () {
    const { sites } = this.state

    return (
      <Router basename='/micro-site/site1/ui'>
        <div>
          <h1>Site 1</h1>
          <nav>
            <ul>
              {this.pages.map(({ name, url }) => (
                <li key={name}>
                  <Link to={url}>{name}</Link>
                </li>
              ))}
              {sites.map(({ name, path, url }) => (
                <li key={name}>
                  {/* <a href={url} target='_blank'>{name}</a> */}
                  <Link to={path}>{name}</Link>
                </li>
              ))}
            </ul>
          </nav>

          <Route path='/' exact component={this.renderPage1} />
          <Route path='/page1/' component={this.renderPage1} />
          <Route path='/page2/' component={this.renderPage2} />

          {sites.map(({ name, path, url }) => (
            <ExternalRoute exact path={path} link={url} />
          ))}

        </div>
      </Router>
    )
  }
}

AuthenticatedSite.propTypes = {
  authenticator: PropTypes.object.isRequired
}

export default AuthenticatedSite
