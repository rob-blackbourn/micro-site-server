import React from 'react'
import PropTypes from 'prop-types'
import { BrowserRouter as Router, Route, Link } from 'react-router-dom'
import Page1 from './Page1'
import Page2 from './Page2'

class AuthenticatedSite extends React.Component {
  renderPage1 = () => {
    return <Page1 authenticator={this.props.authenticator} />
  }

  renderPage2 = () => {
    return <Page2 authenticator={this.props.authenticator} />
  }

  render () {
    return (
      <Router basename='/micro-site/site1/ui'>
        <div>
          <nav>
            <ul>
              <li key='home'>
                <Link to='/'>Home</Link>
              </li>
              <li key='page1'>
                <Link to='/page1/'>Page1</Link>
              </li>
              <li key='page2'>
                <Link to='/page2/'>Page2</Link>
              </li>
            </ul>
          </nav>

          <Route path='/' exact component={this.renderPage1} />
          <Route path='/page1/' exact component={this.renderPage1} />
          <Route path='/page2/' exact component={this.renderPage2} />
        </div>
      </Router>
    )
  }
}

AuthenticatedSite.propTypes = {
  authenticator: PropTypes.object.isRequired
}

export default AuthenticatedSite
