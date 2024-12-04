import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import AvatarGroup from '@mui/material/AvatarGroup';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Chip from '@mui/material/Chip';
import Grid from '@mui/material/Grid2';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import FormControl from '@mui/material/FormControl';
import InputAdornment from '@mui/material/InputAdornment';
import OutlinedInput from '@mui/material/OutlinedInput';
import { styled } from '@mui/material/styles';
import SearchRoundedIcon from '@mui/icons-material/SearchRounded';
import RssFeedRoundedIcon from '@mui/icons-material/RssFeedRounded';
import Button from "@mui/material/Button";
import {useState, useEffect} from "react";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";

const SyledCard = styled(Card)(({ theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  padding: 0,
  height: '100%',
  backgroundColor: theme.palette.background.paper,
  '&:hover': {
    backgroundColor: 'transparent',
    cursor: 'pointer',
  },
  '&:focus-visible': {
    outline: '3px solid',
    outlineColor: 'hsla(210, 98%, 48%, 0.5)',
    outlineOffset: '2px',
  },
}));

const SyledCardContent = styled(CardContent)({
  display: 'flex',
  flexDirection: 'column',
  gap: 4,
  padding: 16,
  flexGrow: 1,
  '&:last-child': {
    paddingBottom: 16,
  },
});

const StyledTypography = styled(Typography)({
  display: '-webkit-box',
  WebkitBoxOrient: 'vertical',
  WebkitLineClamp: 2,
  overflow: 'hidden',
  textOverflow: 'ellipsis',
});

const StyledDialogActions = styled(DialogActions)({
    display: "flex",
    justifyContent: "center",
})

interface Ticket {
  id: string;
  name: string;
  description?: string;
  date: string;
  category: string;
  price: number;
  buyer_id?: number;
  seller_id: number;
}

interface SearchProps {
  onSearch: (query: string) => void;
}

function Author({ authors }: { authors: { name: string; avatar: string }[] }) {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'row',
        gap: 2,
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '16px',
      }}
    >
      <Box
        sx={{ display: 'flex', flexDirection: 'row', gap: 1, alignItems: 'center' }}
      >
        <AvatarGroup max={3}>
          {authors.map((author, index) => (
            <Avatar
              key={index}
              alt={author.name}
              src={author.avatar}
              sx={{ width: 24, height: 24 }}
            />
          ))}
        </AvatarGroup>
        <Typography variant="caption">
          {authors.map((author) => author.name).join(', ')}
        </Typography>
      </Box>
      <Typography variant="caption">July 14, 2021</Typography>
    </Box>
  );
}

export function Search({ onSearch }: SearchProps) {
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = () => {
    onSearch(searchQuery);
  };

  return (
    <Box
      sx={{
        display: 'flex',
        alignItems: 'center',
        width: { xs: '100%', md: '25ch' },
        gap: 1,
      }}
    >
      <OutlinedInput
        size="small"
        id="search"
        placeholder="Search…"
        sx={{
          flex: 1,
        }}
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        inputProps={{
          'aria-label': 'search',
        }}
      />
      <IconButton
        size="medium"
        aria-label="search"
        onClick={handleSearch}
        sx={{
          flexShrink: 0,
        }}
      >
        <SearchRoundedIcon />
      </IconButton>
    </Box>
  );
}

export default function MainContent() {
  const [focusedCardIndex, setFocusedCardIndex] = React.useState<number | null>(
    null,
  );
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [selectedTicketId, setSelectedTicketId] = useState<string | null>(null);
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [filteredTickets, setFilteredTickets] = useState<Ticket[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [categories, setCategories] = useState<string[]>([]);
  const [selectedTicket, setSelectedTicket] = useState<Ticket | null>(null);

  const handleFocus = (index: number) => {
    setFocusedCardIndex(index);
  };

  const handleBlur = () => {
    setFocusedCardIndex(null);
  };

  // const handleClick = () => {
  //   console.info('You clicked the filter chip.');
  // };
  const handleBuyClick = async (ticketId:string) => {
    console.log(`Confirming to buy ticket`);
    setSelectedTicketId(ticketId);
    setIsDialogOpen(true);
  };
  const handleDialogClose = async (confirm: boolean) => {
    if (confirm && selectedTicketId) {
      console.log(`Buying ticket with ID: ${selectedTicketId}`);
      // Call your ticket purchase function here
      // purchaseTicket(selectedTicketId);
      const payload = {
        id: selectedTicketId || ''
      };
      const backendUrl = process.env.REACT_APP_BACKEND_URL || "localhost:8502";
      try {
        const response = await fetch(`http://${backendUrl}/api/tickets/buy`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(payload),
        });
        const responseData = await response.json();
        if (!response.ok) {
          console.log(responseData)
        }
        return;
      }
      catch (error) {
        console.error('There was an error!', error);
      }
    }
    setIsDialogOpen(false);
    setSelectedTicketId(null);

  };

  useEffect(() => {
    const fetchTickets = async () => {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || "localhost:8502";
      try {
        const response = await fetch(`http://${backendUrl}/api/tickets/alltickets`); // Adjust the API endpoint as needed
        if (response.ok) {
          const data: Ticket[] = await response.json();
          setTickets(data);
          setFilteredTickets(data);


          const uniqueCategories = Array.from(new Set(data.map(ticket => ticket.category)));
          setCategories(uniqueCategories);

          console.log(tickets)
        } else {
          console.error('Failed to fetch tickets');
        }
      } catch (error) {
        console.error('Error fetching tickets:', error);
      }
    };

    fetchTickets();
  }, []);

  // Handle category selection and filtering
  const handleCategoryClick = (category: string) => {
    setSelectedCategory(category);
    console.info(category)
    if (category === '' || category === 'all') {
      setFilteredTickets(tickets);
    } else {
      setFilteredTickets(tickets.filter(ticket => ticket.category === category));
    }
  };


  const handleTicketClick = (ticket: Ticket) => {
    setSelectedTicket(ticket);
  };


  const handleCloseModal = () => {
    setSelectedTicket(null);
  };

  // Handle the search functionality
  const handleSearch = (query: string) => {
    if (!query) {
      setFilteredTickets(tickets);
      return;
    }

    const lowerCaseQuery = query.toLowerCase();
    const filtered = tickets.filter(
      (ticket) =>
        ticket.name.toLowerCase().includes(lowerCaseQuery) ||
        (ticket.description && ticket.description.toLowerCase().includes(lowerCaseQuery))
    );
    setFilteredTickets(filtered);
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
      <div>
        <Typography variant="h1" gutterBottom>
          Tickets
        </Typography>
        <Typography>Stay in the loop with the latest tickets</Typography>
      </div>
      <Box
        sx={{
          display: { xs: 'flex', sm: 'none' },
          flexDirection: 'row',
          gap: 1,
          width: { xs: '100%', md: 'fit-content' },
          overflow: 'auto',
        }}
      >
      </Box>
      <Box
        sx={{
          display: 'flex',
          flexDirection: { xs: 'column-reverse', md: 'row' },
          width: '100%',
          justifyContent: 'space-between',
          alignItems: { xs: 'start', md: 'center' },
          gap: 4,
          overflow: 'auto',
        }}
      >
        <Box
          sx={{
            display: 'inline-flex',
            flexDirection: 'row',
            gap: 3,
            overflow: 'auto',
          }}
        >
          <Box sx={{ display: 'flex', overflowX: 'auto', mb: 2 }}>
            <Chip
            key="all"
            label="All Tickets"
            size="medium"
            onClick={() => handleCategoryClick("all")}
            sx={{
              marginRight: 1,
              backgroundColor: selectedCategory === "all" ? 'lightblue' : 'transparent',
              border: 'none',
              cursor: 'pointer',
            }}
          />
        {categories.map((category) => (
          <Chip
            key={category}
            label={category}
            size="medium"
            onClick={() => handleCategoryClick(category)}
            sx={{
              marginRight: 1,
              backgroundColor: selectedCategory === category ? 'lightblue' : 'transparent',
              border: 'none',
              cursor: 'pointer',
            }}
          />
        ))}
      </Box>
        </Box>
        <Box
          sx={{
            display: { xs: 'none', sm: 'flex' },
            flexDirection: 'row',
            gap: 1,
            width: { xs: '100%', md: 'fit-content' },
            overflow: 'auto',
          }}
        >
      <Search onSearch={handleSearch} />
        </Box>
      </Box>

     <Dialog
        open={isDialogOpen}
        onClose={() => handleDialogClose(false)}
        aria-labelledby="confirmation-dialog-title"
      >
        <DialogTitle id="confirmation-dialog-title">
          Do you want to buy this ticket?
        </DialogTitle>
        <StyledDialogActions>
          <Button onClick={() => handleDialogClose(true)} color="primary" autoFocus>
            Yes
          </Button>
          <Button onClick={() => handleDialogClose(false)} color="secondary">
            No
          </Button>
        </StyledDialogActions>
      </Dialog>

      <Grid container spacing={2} columns={12}>
        {filteredTickets.map((ticket, index) => (
        <Grid key={ticket.id} size={{ xs: 12, md: 6 }}>
          <SyledCard
            variant="outlined"
            onFocus={() => handleFocus(index)}
            onBlur={handleBlur}
            tabIndex={0}
            className={focusedCardIndex === index ? 'Mui-focused' : ''}
            onClick={() => handleTicketClick(ticket)} // Open modal on click
          >
            <SyledCardContent>
              <Typography gutterBottom variant="caption" component="div">
                {ticket.category}
              </Typography>
              <Typography gutterBottom variant="h6" component="div">
                {ticket.name}
              </Typography>
              <StyledTypography variant="body2" color="text.secondary" gutterBottom>
                {ticket.description}
              </StyledTypography>
            </SyledCardContent>
            <Button
              variant="contained"
              color="primary"
              onClick={() => handleBuyClick(ticket.id)}
            >
              Buy Ticket
            </Button>
          </SyledCard>
        </Grid>
      ))}
      </Grid>

      {selectedTicket && (
        <Dialog
          open={Boolean(selectedTicket)}
          onClose={handleCloseModal}
          maxWidth="md"
          fullWidth
        >
          <DialogTitle sx={{ fontWeight: 'bold', fontSize: '1.8rem', textAlign: 'center'}}>{selectedTicket.name}</DialogTitle>
<DialogContent>
  <Typography variant="h6" sx={{ fontWeight: 'bold', fontSize: '1.2rem' }}>Category: {selectedTicket.category}</Typography>

  <Typography
    variant="body1"
    sx={{ marginTop: 2, fontSize: '1rem', marginBottom: 2 }}
    gutterBottom
  >
    {selectedTicket.description}
  </Typography>

  <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
    <Typography
      variant="h5"
      sx={{ fontWeight: 'bold', fontSize: '1.2rem' }}
      gutterBottom
    >
      Price: ${selectedTicket.price}
    </Typography>

    <Typography
      variant="h5"
      sx={{ fontWeight: 'bold', fontSize: '1.2rem' }}
      gutterBottom
    >
      Date: {new Date(selectedTicket.date).toLocaleDateString()}
    </Typography>
  </Box>
</DialogContent>

          <DialogActions>
            <Button onClick={handleCloseModal} color="primary">
              Close
            </Button>
          </DialogActions>
        </Dialog>
      )}
    </Box>
  );
}
