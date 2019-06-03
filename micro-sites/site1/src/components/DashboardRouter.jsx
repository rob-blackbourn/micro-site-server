import React, { Component } from 'react'
import PropTypes from 'prop-types'
import classNames from 'classnames'
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
    display: 'flex'
  },
  toolbar: {
    paddingRight: 0 // keep right padding when drawer closed
  },
  toolbarIcon: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: '0 8px',
    ...theme.mixins.toolbar
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen
    })
  },
  appBarShift: {
    marginLeft: drawerWidth,
    width: `calc(100% - ${drawerWidth}px)`,
    transition: theme.transitions.create(['width', 'margin'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen
    })
  },
  appBarSpacer: theme.mixins.toolbar,
  menuButton: {
    marginLeft: theme.spacing.unit * 0.5,
    marginRight: theme.spacing.unit * 3
  },
  menuButtonHidden: {
    display: 'none'
  },
  title: {
    flexGrow: 1
  },
  drawerPaper: {
    position: 'relative',
    whiteSpace: 'nowrap',
    width: drawerWidth,
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.enteringScreen
    })
  },
  drawerPaperClose: {
    overflowX: 'hidden',
    transition: theme.transitions.create('width', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen
    }),
    width: theme.spacing.unit * 7,
    [theme.breakpoints.up('sm')]: {
      width: theme.spacing.unit * 7
    }
  },
  drawerText: {
    marginLeft: 0,
    paddingLeft: 0
  },
  content: {
    flexGrow: 1,
    padding: theme.spacing.unit * 3,
    height: '100vh',
    overflow: 'auto'
  },
  chartContainer: {
    marginLeft: -22
  },
  tableContainer: {
    height: 320
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

  render () {
    const { classes, title, applications, basename, routes, links } = this.props

    return (
      <BrowserRouter basename={basename}>
        <div className={classes.root}>
          {/* App bar */}
          <AppBar
            position='absolute'
            className={classNames(
              classes.appBar,
              this.state.open && classes.appBarShift
            )}
          >
            <Toolbar
              disableGutters={!this.state.open}
              className={classes.toolbar}
            >
              <IconButton
                color='inherit'
                aria-label='Open drawer'
                onClick={this.handleDrawerOpen}
                className={classNames(
                  classes.menuButton,
                  this.state.open && classes.menuButtonHidden
                )}
              >
                <MenuIcon />
              </IconButton>
              <Typography
                component='h1'
                variant='h6'
                color='inherit'
                noWrap
                className={classes.title}
              >
                {title}
              </Typography>
            </Toolbar>
          </AppBar>

          {/* Drawer */}
          <Drawer
            variant='permanent'
            classes={{
              paper: classNames(
                classes.drawerPaper,
                !this.state.open && classes.drawerPaperClose
              )
            }}
            open={this.state.open}
          >
            {/* Header of drawer */}
            <div className={classes.toolbarIcon}>
              <IconButton onClick={this.handleDrawerClose}>
                <ChevronLeftIcon />
              </IconButton>
            </div>
            <Divider />
            {/* Applications in the drawer */}
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
          {/* Page content */}
          <main className={classes.content}>
            <div className={classes.tableContainer}>
              {routes()}
            </div>
          </main>
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
