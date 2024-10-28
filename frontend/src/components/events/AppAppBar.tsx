import * as React from 'react';
import { useNavigate } from 'react-router-dom';
import { alpha, styled, Theme } from '@mui/material/styles';
import Box from '@mui/material/Box';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import Container from '@mui/material/Container';
import Divider from '@mui/material/Divider';
import MenuItem from '@mui/material/MenuItem';
import Drawer from '@mui/material/Drawer';
import MenuIcon from '@mui/icons-material/Menu';
import CloseRoundedIcon from '@mui/icons-material/CloseRounded';
import Sitemark from './SitemarkIcon';
import AlertDialog from '../alert/AlertDialog';
import ColorModeIconDropdown from '../shared-theme/ColorModeIconDropdown';
import { getUserDataFromToken } from '../utils';

const StyledToolbar = styled(Toolbar)(({ theme }: { theme: Theme & { vars?: any } }) => ({
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  flexShrink: 0,
  borderRadius: `calc(${theme.shape.borderRadius}px + 8px)`,
  backdropFilter: 'blur(24px)',
  border: '1px solid',
  borderColor: (theme.vars || theme).palette.divider,
  backgroundColor: theme.vars
    ? `rgba(${theme.vars.palette.background.defaultChannel} / 0.4)`
    : alpha(theme.palette.background.default, 0.4),
  boxShadow: (theme.vars || theme).shadows[1],
  padding: '8px 12px',
}));

export default function AppAppBar() {
  const [open, setOpen] = React.useState(false);
  const [openToggled, setOpenedToggled] = React.useState(false);
  const [alertText, setAlertText] = React.useState('');
  const userData = getUserDataFromToken();
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/');
  };

  const handleDeleteAccount = async () => {
    try {
      const response = await fetch('http:/46.101.254.37/api/users/me', {
      // const response = await fetch('http://localhost:8502/api/users/me', {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`, // Optional: Add token if authentication is required
          'Content-Type': 'application/json',
        },
      });

      const responseData = await response.json();

      if (!response.ok) {
        setOpen(true);
        setAlertText(responseData.detail);
      } else {
        localStorage.removeItem('token');
        navigate('/login');
      }

    } catch (error) {
      console.error('There was an error!', error);
    }
  };

  const toggleDrawer = (newOpen: boolean) => () => {
    setOpenedToggled(newOpen);
  };

  return (
    <AppBar
      position="fixed"
      enableColorOnDark
      sx={{
        boxShadow: 0,
        bgcolor: 'transparent',
        backgroundImage: 'none',
        mt: 'calc(var(--template-frame-height, 0px) + 28px)',
      }}
    >
      <Container maxWidth="lg">
        <StyledToolbar variant="dense" disableGutters>
          <Box sx={{ flexGrow: 1, display: 'flex', alignItems: 'center', px: 0 }}>
            <Sitemark />
            <Box sx={{ display: { xs: 'none', md: 'flex' } }}>
              <Button variant="text" color="info" size="small">
                Buy tickets
              </Button>
              <Button variant="text" color="info" size="small">
                Sell tickets
              </Button>
              <Button variant="text" color="info" size="small">
                My tickets
              </Button>
            </Box>
          </Box>
          <Box
            sx={{
              display: { xs: 'none', md: 'flex' },
              gap: 1,
              alignItems: 'center',
            }}
          >
            {userData && (
              <Box sx={{ mr: 2 }}>
                <span>Welcome, {userData.firstname}!</span>
              </Box>
            )}
            <Button color="primary" variant="text" size="small" onClick={handleLogout}>
              Log out
            </Button>
            <Button color="primary" variant="contained" size="small" onClick={handleDeleteAccount}>
              Delete account
            </Button>
            <ColorModeIconDropdown />
          </Box>
          <Box sx={{ display: { xs: 'flex', md: 'none' }, gap: 1 }}>
            <ColorModeIconDropdown size="medium" />
            <IconButton aria-label="Menu button" onClick={toggleDrawer(true)}>
              <MenuIcon />
            </IconButton>
            <Drawer
              anchor="top"
              open={openToggled}
              onClose={toggleDrawer(false)}
              PaperProps={{
                sx: {
                  top: 'var(--template-frame-height, 0px)',
                },
              }}
            >
              <Box sx={{ p: 2, backgroundColor: 'background.default' }}>
                <Box
                  sx={{
                    display: 'flex',
                    justifyContent: 'flex-end',
                  }}
                >
                  <IconButton onClick={toggleDrawer(false)}>
                    <CloseRoundedIcon />
                  </IconButton>
                </Box>
                <MenuItem>Buy tickets</MenuItem>
                <MenuItem>Sell tickets</MenuItem>
                <MenuItem>My tickets</MenuItem>
                <Divider sx={{ my: 3 }} />
                <MenuItem>
                  <Button color="primary" variant="contained" fullWidth onClick={handleLogout}>
                    Log out
                  </Button>
                </MenuItem>
                <MenuItem>
                  <Button color="error" variant="outlined" fullWidth onClick={handleDeleteAccount}>
                    Delete account
                  </Button>
                </MenuItem>
              </Box>
            </Drawer>
          </Box>
        </StyledToolbar>
      </Container>
      <AlertDialog open={open} setOpen={setOpen} alertText={alertText} />
    </AppBar>
  );
}
