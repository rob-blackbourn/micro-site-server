import React from 'react'
import PropTypes from 'prop-types'
import { SITE1_INFO_URL } from '../config'

class AuthenticatedSite extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      message: ''
    }
  }

  componentDidMount () {
    const { authenticator } = this.props

    authenticator.fetch(SITE1_INFO_URL)
      .then(response => {
        if (response.status >= 300) {
          throw new Error('Invalid status')
        }
        return response.json()
      }).then(data => {
        console.log(data)
      }).catch(error => {
        console.error(error)
      })
  }

  render () {
    return (
      <div>
        <p>
          Some text
        </p>
      </div>
    )
  }
}

AuthenticatedSite.propTypes = {
  authenticator: PropTypes.object.isRequired
}

export default AuthenticatedSite
