import React, { useState, useEffect } from "react";
import Container from "@mui/material/Container";
import CssBaseline from "@mui/material/CssBaseline";
import AppAppBar from "../../events/AppAppBar";
import AppTheme from "../../shared-theme/AppTheme";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import Modal from "@mui/material/Modal";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";

export default function MyTickets(props: { disableCustomTheme?: boolean }) {
  const [tickets, setTickets] = useState<any[]>([]);
  const [editTicket, setEditTicket] = useState<any | null>(null);
  const [error, setError] = useState<string>("");

  const backendUrl = process.env.REACT_APP_BACKEND_URL || "localhost:8502";

  useEffect(() => {
    const fetchTickets = async () => {
      try {
        const response = await fetch(`http://${backendUrl}/api/tickets/my-tickets`, {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });

        if (!response.ok) {
          throw new Error("Failed to fetch tickets.");
        }

        const responseData = await response.json();
        setTickets(responseData);
      } catch (err) {
        setError((err as Error).message);
      }
    };

    fetchTickets();
  }, [backendUrl]);

  const handleEdit = (ticket: any) => {
    setEditTicket(ticket); // Open modal with ticket data
  };

  const handleEditSubmit = async (updatedTicket: any) => {
    try {
      const response = await fetch(
        `http://${backendUrl}/api/tickets/my-tickets/${updatedTicket.id}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
          body: JSON.stringify(updatedTicket),
        }
      );

      if (!response.ok) {
        throw new Error("Failed to update ticket.");
      }

      const updatedData = await response.json();
      setTickets((prevTickets) =>
        prevTickets.map((ticket) => (ticket.id === updatedData.id ? updatedData : ticket))
      );
      setEditTicket(null); // Close modal
    } catch (err) {
      setError((err as Error).message);
    }
  };

  const handleDelete = async (ticketId: string) => {
    try {
      const response = await fetch(
        `http://${backendUrl}/api/tickets/my-tickets/${ticketId}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to delete ticket: ${errorText}`);
      }

      setTickets((prevTickets) => prevTickets.filter((ticket) => ticket.id !== ticketId));
    } catch (err) {
      setError((err as Error).message);
    }
  };

  const EditModal = ({ ticket, onClose, onSubmit }: any) => {
    const [formValues, setFormValues] = useState(ticket);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      setFormValues({
        ...formValues,
        [e.target.name]: e.target.value,
      });
    };

    const handleSubmit = () => {
      onSubmit(formValues);
    };

    return (
      <Modal open={Boolean(ticket)} onClose={onClose}>
        <Box sx={{ p: 4, backgroundColor: "white", margin: "auto", maxWidth: "500px" }}>
          <Typography variant="h6">Edit Ticket</Typography>
          <TextField
            label="Name"
            name="name"
            value={formValues.name}
            onChange={handleChange}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Description"
            name="description"
            value={formValues.description || ""}
            onChange={handleChange}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Date"
            name="date"
            type="datetime-local"
            value={formValues.date}
            onChange={handleChange}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Category"
            name="category"
            value={formValues.category}
            onChange={handleChange}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Price"
            name="price"
            type="number"
            value={formValues.price}
            onChange={handleChange}
            fullWidth
            margin="normal"
          />
          <Box sx={{ mt: 2, display: "flex", justifyContent: "flex-end", gap: 2 }}>
            <Button onClick={onClose} variant="outlined">
              Cancel
            </Button>
            <Button onClick={handleSubmit} variant="contained" color="primary">
              Save
            </Button>
          </Box>
        </Box>
      </Modal>
    );
  };

  return (
    <AppTheme {...props}>
      <CssBaseline enableColorScheme />
      <AppAppBar />
      <Container maxWidth="lg" sx={{ my: 16 }}>
        <Typography variant="h4" gutterBottom>
          My Tickets
        </Typography>
        {error && (
          <Typography variant="body1" color="error">
            {error}
          </Typography>
        )}
        <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
          {tickets.map((ticket) => (
            <Box
              key={ticket.id}
              sx={{
                border: "1px solid #ccc",
                borderRadius: "8px",
                padding: "16px",
                backgroundColor: "#f9f9f9",
                position: "relative",
              }}
            >
              <Typography variant="h6">{ticket.name}</Typography>
              <Typography variant="body2" color="textSecondary">
                {ticket.description || "No description provided."}
              </Typography>
              <Typography variant="body2">
                <strong>Date:</strong> {new Date(ticket.date).toLocaleString()}
              </Typography>
              <Typography variant="body2">
                <strong>Category:</strong> {ticket.category}
              </Typography>
              <Typography variant="body2">
                <strong>Price:</strong> ${ticket.price.toFixed(2)}
              </Typography>
              <Box
                sx={{
                  position: "absolute",
                  top: "8px",
                  right: "8px",
                  display: "flex",
                  gap: 1,
                }}
              >
                <IconButton
                  onClick={() => handleEdit(ticket)}
                  sx={{
                    "&:hover": { color: "blue" },
                  }}
                >
                  <EditIcon />
                </IconButton>
                <IconButton
                  onClick={() => handleDelete(ticket.id)}
                  sx={{
                    "&:hover": { color: "red" },
                  }}
                >
                  <DeleteIcon />
                </IconButton>
              </Box>
            </Box>
          ))}
        </Box>
        {editTicket && (
          <EditModal
            ticket={editTicket}
            onClose={() => setEditTicket(null)}
            onSubmit={handleEditSubmit}
          />
        )}
      </Container>
    </AppTheme>
  );
}
