import React, { Component } from 'react'
import PropTypes from 'prop-types'
import clsx from 'clsx'
import { withStyles } from '@material-ui/core/styles'
import Drawer from '@material-ui/core/Drawer'
import AppBar from '@material-ui/core/AppBar'
import Toolbar from '@material-ui/core/Toolbar'
import Tooltip from '@material-ui/core/Tooltip'
import List from '@material-ui/core/List'
import ListItem from '@material-ui/core/ListItem'
import ListItemIcon from '@material-ui/core/ListItemIcon'
import ListItemText from '@material-ui/core/ListItemText'
import Typography from '@material-ui/core/Typography'
import Divider from '@material-ui/core/Divider'
import IconButton from '@material-ui/core/IconButton'
import MaterialIcon from 'material-icons-react'
import MenuIcon from '@material-ui/icons/Menu'
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft'
import { BrowserRouter, Link } from 'react-router-dom'

const drawerWidth = 210

const styles = theme => ({
  root: {
    display: 'flex',
    flexWrap: 'nowrap',
    flexDirection: 'column',
    width: '100%',
    height: '100%'
  },
  toolbarIcon: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: '0 8px',
    ...theme.mixins.toolbar
  },
  appBar: {
    flexShrink: 0,
    transition: theme.transitions.create(['margin', 'width'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen
    })
  },
  appBarShift: {
    width: `calc(100% - ${drawerWidth}px)`,
    marginLeft: drawerWidth,
    transition: theme.transitions.create(['margin', 'width'], {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen
    })
  },
  menuButton: {
    marginRight: theme.spacing(2)

  },
  menuButtonHidden: {
    display: 'none'
  },
  drawer: {
    width: drawerWidth,
    flexShrink: 0
  },
  drawerPaper: {
    width: drawerWidth
  },
  drawerText: {
    marginLeft: 0,
    paddingLeft: 0
  },
  content: {
    flexGrow: 1,
    overflow: 'auto',
    minHeight: '1em',
    transition: theme.transitions.create('margin', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen
    })
  },
  contentShift: {
    transition: theme.transitions.create('margin', {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen
    }),
    marginLeft: drawerWidth
  }
})

class DashboardRouter extends Component {
  state = {
    open: false
  }

  handleDrawerOpen = () => {
    this.setState({ open: true })
  }

  handleDrawerClose = () => {
    this.setState({ open: false })
  }

  renderAppBar = () => {
    const { classes, title } = this.props
    const { open } = this.state

    return (
      <AppBar
        position='static'
        className={clsx(classes.appBar, {
          [classes.appBarShift]: open
        })}
      >
        <Toolbar disableGutters={!open}>
          <IconButton
            color='inherit'
            aria-label='Open drawer'
            onClick={this.handleDrawerOpen}
            className={clsx(classes.menuButton, open && classes.menuButtonHidden)}
          >
            <MenuIcon />
          </IconButton>
          <Typography component='h6' color='inherit' noWrap>
            {title}
          </Typography>
        </Toolbar>
      </AppBar>
    )
  }

  renderSideBar = () => {
    const { classes, applications, links } = this.props
    const { open } = this.state

    return (
      <Drawer
        className={classes.drawer}
        variant='temporary'
        open={open}
        classes={{ paper: classes.drawerPaper }}
      >
        <div className={classes.toolbarIcon}>
          <IconButton onClick={this.handleDrawerClose}>
            <ChevronLeftIcon />
          </IconButton>
        </div>
        <Divider />

        <List>
          {applications.map(application => (
            <Tooltip
              title={
                <Typography variant='subtitle2' color='inherit'>
                  {application.description}
                </Typography>}
              key={application.code}>
              <ListItem button component='a' href={application.url}>
                <ListItemIcon>
                  <MaterialIcon icon={application.icon} />
                </ListItemIcon>
                <ListItemText className={classes.drawerText} primary={application.title} />
              </ListItem>
            </Tooltip>
          ))}
        </List>
        <Divider />
        {/* Links for a given application */}
        <List>
          {links.map(link => (
            <Tooltip
              title={
                <Typography variant='subtitle2' color='inherit'>
                  {link.description}
                </Typography>
              }
              key={link.code}>
              <ListItem button component={Link} to={link.path}>
                <ListItemIcon>
                  <MaterialIcon icon={link.icon} />
                </ListItemIcon>
                <ListItemText className={classes.drawerText} primary={link.title} />
              </ListItem>
            </Tooltip>
          ))}
        </List>
      </Drawer>
    )
  }

  renderContent = () => {
    const { classes, routes } = this.props
    const { open } = this.state

    return (
      <main className={clsx(classes.content, { [classes.contentShift]: open })}>
        {routes()}
      </main>
    )
  }

  render () {
    const { classes, basename } = this.props

    return (
      <BrowserRouter basename={basename}>
        <div className={classes.root}>
          { this.renderAppBar() }

          { this.renderSideBar() }

          { this.renderContent() }
        </div>
      </BrowserRouter>
    )
  }
}

DashboardRouter.propTypes = {
  classes: PropTypes.object.isRequired,
  applications: PropTypes.array.isRequired,
  title: PropTypes.string.isRequired,
  basename: PropTypes.string,
  routes: PropTypes.func.isRequired,
  links: PropTypes.array.isRequired
}

DashboardRouter.defaultProps = {
  basename: '/'
}

export default withStyles(styles)(DashboardRouter)
