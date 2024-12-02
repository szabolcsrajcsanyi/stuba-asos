import React, { useState } from "react";
import Container from "@mui/material/Container";
import CssBaseline from "@mui/material/CssBaseline";
import AppAppBar from "../../events/AppAppBar";
import AppTheme from "../../shared-theme/AppTheme";
import {
  TextField,
  Button,
  MenuItem,
  Select,
  InputLabel,
  FormControl,
  FormHelperText,
  Dialog,
  DialogTitle,
  DialogContent,
} from "@mui/material";
import { DateTimePicker } from "@mui/x-date-pickers/DateTimePicker";
import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFnsV3";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { PasswordRounded } from "@mui/icons-material";
import { Navigate, useNavigate } from "react-router-dom";

export default function SellTicketForm(props: {
  disableCustomTheme?: boolean;
}) {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [date, setDate] = useState<Date | null>(null);
  const [category, setCategory] = useState("");
  const [price, setPrice] = useState<number | string>("");
  const [error, setError] = useState<string>("");
  const [success, setSuccess] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    // Validate form
    if (!name || !date || !category || !price) {
      setError("All fields except Description field, are required.");
      return;
    } else {
      setError("");
    }
    // Submit form data
    const data = new FormData(event.currentTarget);
    const formData = new FormData();

    const ticketData = {
      name: name,
      description: description,
      date: date.toISOString(),
      category: category,
      price: parseFloat(price as string),
    };
    console.log(ticketData);
    try {
      const backendUrl = process.env.REACT_APP_BACKEND_URL || "localhost:8502";
      // const backendUrl = 'localhost:8080';
      const response = await fetch(`http://${backendUrl}/api/tickets/sell`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify(ticketData),
      });

      const responseData = await response.json();
      if (!response.ok) {
        console.log(responseData.detail);
        setError(responseData.detail);
      } else {
        setSuccess(true);
        setTimeout(() => navigate("/tickets"), 4000);
      }
    } catch (error) {
      console.error("Error occurred calling backend!", error);
    }
  };

  return (
    <AppTheme {...props}>
      <CssBaseline enableColorScheme />
      <AppAppBar />
      <Container
        maxWidth="lg"
        component="main"
        sx={{ display: "flex", flexDirection: "column", my: 16, gap: 4 }}
      >
        <h2>Sell Ticket</h2>
        <form
          onSubmit={handleSubmit}
          style={{ display: "flex", flexDirection: "column", gap: "16px" }}
        >
          {error && <div style={{ color: "red" }}>{error}</div>}

          {/* Name Field */}
          <TextField
            label="Name"
            variant="outlined"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />

          {/* Description Field */}
          <TextField
            label="Description"
            variant="outlined"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />

          {/* Date Field (DateTimePicker) */}
          <LocalizationProvider dateAdapter={AdapterDateFns}>
            <DateTimePicker
              label="Date"
              value={date}
              onChange={(newDate) => setDate(newDate)}
            />
          </LocalizationProvider>

          {/* Category Field */}
          <FormControl fullWidth required>
            <TextField
              label="Category"
              variant="outlined"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              type="text"
              required
            />
            <FormHelperText>Choose a category</FormHelperText>
          </FormControl>

          {/* Price Field */}
          <TextField
            label="Price"
            variant="outlined"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
            type="number"
            required
          />

          {/* Submit Button */}
          <Button variant="contained" color="primary" type="submit">
            Submit
          </Button>
        </form>

        {/* Success Modal */}
        <Dialog open={success} onClose={() => setSuccess(false)}>
          <DialogTitle>Success</DialogTitle>
          <DialogContent>
            <p>Your ticket has been successfully created!</p>
            <p>You will be redirected to the homepage shortly.</p>
          </DialogContent>
        </Dialog>
        
      </Container>
    </AppTheme>
  );
}
