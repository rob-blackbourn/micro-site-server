import React from 'react'
import PropTypes from 'prop-types'
import { SITE1_INFO2_URL } from '../config'

class Page2 extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      message: 'No Message'
    }
  }

  componentDidMount () {
    const { authenticator } = this.props

    authenticator.fetch(SITE1_INFO2_URL)
      .then(response => {
        if (response.status >= 300) {
          throw new Error('Invalid status')
        }
        return response.json()
      }).then(data => {
        this.setState({ message: data.message })
      }).catch(error => {
        console.error(error)
      })
  }

  render () {
    return (
      <div>
        <p>
          {this.state.message}
        </p>
      </div>
    )
  }
}

Page2.propTypes = {
  authenticator: PropTypes.object.isRequired
}

export default Page2
