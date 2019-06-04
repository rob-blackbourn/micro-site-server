import React from 'react'
import PropTypes from 'prop-types'
import { withStyles } from '@material-ui/core/styles'
import { SITE1_INFO1_URL } from '../config'

const styles = theme => ({
  root: {
    padding: theme.spacing(1)
  }
})

class Page1 extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      message: 'No message'
    }
  }

  componentDidMount () {
    const { authenticator } = this.props

    authenticator.fetch(SITE1_INFO1_URL)
      .then(response => {
        if (response.status >= 300) {
          throw new Error('Invalid status')
        }
        return response.json()
      }).then(data => {
        console.log(data)
        this.setState({ message: data.message })
      }).catch(error => {
        console.error(error)
      })
  }

  render () {
    const { classes } = this.props

    return (
      <div className={classes.root}>
        <p>
          {this.state.message}
        </p>
      </div>
    )
  }
}

Page1.propTypes = {
  classes: PropTypes.object.isRequired,
  authenticator: PropTypes.object.isRequired
}

export default withStyles(styles)(Page1)
