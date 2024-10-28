import { jwtDecode } from 'jwt-decode';
import { JWTPayload } from './types';

export const getUserDataFromToken = (): JWTPayload | null => {
    const token = localStorage.getItem('token');
  
    if (!token) return null;
  
    try {
      const decoded = jwtDecode<JWTPayload>(token);
      return decoded;
    } catch (error) {
      console.error("Failed to decode token", error);
      return null;
    }
  };