package com.flights.api.flightsapi.persistence;

import java.io.IOException;

import com.flights.api.flightsapi.model.Flight;

/**
 * Defines the interface for Hero object persistence
 * 
 * @author SWEN Faculty
 */
public interface FlightDAO {
   
	
	String verifyBooking(String passport) throws IOException;
	
    Flight getBooking(String code) throws IOException;
  
    Boolean createBooking(Flight flight) throws IOException;

}
