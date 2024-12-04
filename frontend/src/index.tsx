import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import {
  BrowserRouter as Router,
  Routes,
  Route,
} from 'react-router-dom';

import SignInSide from './components/sign-in-side/SignInSide';
import SignUp from './components/sign-up/SignUp';
import SignIn from './components/sign-in/SignIn';
import Tickets from './components/events/Tickets';
import TicketsSell from './components/tickets/sell/TicketsSell';
import MyTickets from './components/tickets/my-tickets/MyTickets';
import PublicRoute from './components/route-priviliges/PublicRoute';
import ProtectedRoute from './components/route-priviliges/ProtectedRoute';

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);
root.render(
  <Router>
    <Routes>
      <Route path="/" element={<PublicRoute><SignInSide /></PublicRoute>} />
      <Route path="/register" element={<PublicRoute><SignUp /></PublicRoute>} />
      <Route path="/login" element={<PublicRoute><SignIn /></PublicRoute>} />
      <Route path="/tickets" element={<ProtectedRoute><Tickets /></ProtectedRoute>} />
      <Route path='/tickets/sell' element={<ProtectedRoute><TicketsSell/></ProtectedRoute>} />
      <Route path='/tickets/my-tickets' element={<ProtectedRoute><MyTickets/></ProtectedRoute>} />
    </Routes>
  </Router>
);
