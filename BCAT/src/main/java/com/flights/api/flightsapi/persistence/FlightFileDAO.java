package com.flights.api.flightsapi.persistence;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Map;
import java.util.Random;
import java.util.TreeMap;
import java.util.logging.Logger;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.flights.api.flightsapi.model.Flight;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;


@Component
public class FlightFileDAO implements FlightDAO {
    private static final Logger LOG = Logger.getLogger(FlightFileDAO.class.getName());
    Map<String,Flight> flights;   // Provides a local cache of the hero objects
                                // so that we don't need to read from the file
                                // each time
    private ObjectMapper objectMapper;  // Provides conversion between Hero
                                        // objects and JSON text format written
                                        // to the file
    private String filename;    // Filename to read from and write to

   
   
    public FlightFileDAO(@Value("${bookings.file}") String filename,ObjectMapper objectMapper) throws IOException {
        this.filename = filename;
        this.objectMapper = objectMapper;
        load();  // load the heroes from the file
    }

    private synchronized static String newCode() {
    
    	String AlphaNumericString = "A1B2C3D4E5F6G7H8I9J0KLMNOPQRSTUVWXYZ"; // to generate unique booking code

    	StringBuilder sb = new StringBuilder();

        Random random = new Random();
    	
        for (int i = 0; i < 6; i++) {sb.append(AlphaNumericString.charAt(random.nextInt(AlphaNumericString.length())));}
    
        String code = sb.toString();
        return code;
    }

   
    private Flight[] getFlightsArray() {
        return getFlightsArray(null);
    }

   
    private Flight[] getFlightsArray(String passport) { // if containsText == null, no filter
        ArrayList<Flight> flightArrayList = new ArrayList<>();

        for (Flight flight : flights.values()) {
            if (passport == null || flight.getName().contains(passport)) {
                flightArrayList.add(flight);
            }
        }

        Flight[] flightArray = new Flight[flightArrayList.size()];
        flightArrayList.toArray(flightArray);
        return flightArray;
    }

   
    private boolean save() throws IOException {
        Flight[] flightArray = getFlightsArray();

        // Serializes the Java Objects to JSON objects into the file
        // writeValue will thrown an IOException if there is an issue
        // with the file or reading from the file
        objectMapper.writeValue(new File(filename),flightArray);
        return true;
    }


    private boolean load() throws IOException {
    	flights= new TreeMap<>();

        // Deserializes the JSON objects from the file into an array of heroes
        // readValue will throw an IOException if there's an issue with the file
        // or reading from the file
        Flight[] flightArray = objectMapper.readValue(new File(filename),Flight[].class);

        for (Flight flight : flightArray) {flights.put(flight.getCode(),flight);}
      
        return true;
    }

    /**
    ** {@inheritDoc}
     */
    @Override
    public Flight[] getBookings() {
        synchronized(flights) {
            return getFlightsArray();
        }
    }


    /**
    ** {@inheritDoc}
     */
    @Override
    public Flight getBooking(String code) {
        synchronized(flights) {
            if (flights.containsKey(code))
                return flights.get(code);
            else
                return null;
        }
    }

    /**
    ** {@inheritDoc}
     */
    @Override
    public Boolean createBooking(Flight flight) throws IOException {
        synchronized(flights) {
        	
            Flight newFlight = new Flight(newCode(), flight.getPassport(), flight.getName(), flight.getSurname(), 
            							  flight.getDeparture(), flight.getArrival(), flight.getSeat(),
            							  flight.getDate(), flight.getDepartureTime(), flight.getBoarding());
            
            flights.put(newFlight.getCode(),newFlight);
            save(); // may throw an IOException
            return true;
        }
    }

    /**
     ** {@inheritDoc}
      */
	@Override
	public String verifyBooking(String passport) throws IOException {
		
		    for (Flight flight : flights.values()) {
		        if (flight.getPassport().equals(passport)) {
		            return flight.getCode();
		        }
		    }
		
		return "NOT FOUND";
	}

}











