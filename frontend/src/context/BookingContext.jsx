import { createContext, useContext, useState, useEffect } from "react";

const BookingContext = createContext();

export const BookingProvider = ({ children }) => {
  const [bookings, setBookings] = useState([]);

  // Load from localStorage on mount
  useEffect(() => {
    const stored = localStorage.getItem("bookings");
    if (stored) {
      setBookings(JSON.parse(stored));
    }
  }, []);

  // Save to localStorage whenever bookings change
  useEffect(() => {
    localStorage.setItem("bookings", JSON.stringify(bookings));
  }, [bookings]);

  const createBooking = (booking) => {
    setBookings((prev) => [
      ...prev,
      { ...booking, status: "requested", id: Date.now() },
    ]);
  };

  const updateStatus = (id, status) => {
    setBookings((prev) =>
      prev.map((b) =>
        b.id === id ? { ...b, status } : b
      )
    );
  };

  return (
    <BookingContext.Provider
      value={{ bookings, createBooking, updateStatus }}
    >
      {children}
    </BookingContext.Provider>
  );
};

export const useBookings = () => useContext(BookingContext);
