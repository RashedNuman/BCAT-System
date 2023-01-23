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

/**
 * Implements the functionality for JSON file-based peristance for Heroes
 * 
 * {@literal @}Component Spring annotation instantiates a single instance of this
 * class and injects the instance into other classes as needed
 * 
 * @author SWEN Faculty
 */
@Component
public class FlightFileDAO implements FlightDAO {
    private static final Logger LOG = Logger.getLogger(FlightFileDAO.class.getName());
    Map<String,Flight> flights;   // Provides a local cache of the hero objects
                                // so that we don't need to read from the file
                                // each time
    private ObjectMapper objectMapper;  // Provides conversion between Hero
                                        // objects and JSON text format written
                                        // to the file
    private static int nextId;  // The next Id to assign to a new hero
    private String filename;    // Filename to read from and write to

    /**
     * Creates a Hero File Data Access Object
     * 
     * @param filename Filename to read from and write to
     * @param objectMapper Provides JSON Object to/from Java Object serialization and deserialization
     * 
     * @throws IOException when file cannot be accessed or read from
     */
    public FlightFileDAO(@Value("${flights.file}") String filename,ObjectMapper objectMapper) throws IOException {
        this.filename = filename;
        this.objectMapper = objectMapper;
        load();  // load the heroes from the file
    }

    /**
     * Generates random unique booking code for a flight booking
     * @return booking code as String
     */
    private synchronized static String newCode() {
    	
    	String AlphaNumericString = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"; // to generate unique booking code
    	
    	StringBuilder sb = new StringBuilder();
        Random random = new Random();
        for (int i = 0; i < 6; i++) {
            sb.append(AlphaNumericString.charAt(random.nextInt(AlphaNumericString.length())));
        }
        
        String code = sb.toString();

        return code;
    }

    /**
     * Generates an array of {@linkplain Hero heroes} from the tree map
     * 
     * @return  The array of {@link Hero heroes}, may be empty
     */
    private Flight[] getFlightsArray() {
        return getFlightsArray(null);
    }

    /**
     * Generates an array of {@linkplain Hero heroes} from the tree map for any
     * {@linkplain Hero heroes} that contains the text specified by containsText
     * <br>
     * If containsText is null, the array contains all of the {@linkplain Hero heroes}
     * in the tree map
     * 
     * @return  The array of {@link Hero heroes}, may be empty
     */
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

    /**
     * Saves the {@linkplain Hero heroes} from the map into the file as an array of JSON objects
     * 
     * @return true if the {@link Hero heroes} were written successfully
     * 
     * @throws IOException when file cannot be accessed or written to
     */
    private boolean save() throws IOException {
        Flight[] flightArray = getFlightsArray();

        // Serializes the Java Objects to JSON objects into the file
        // writeValue will thrown an IOException if there is an issue
        // with the file or reading from the file
        objectMapper.writeValue(new File(filename),flightArray);
        return true;
    }

    /**
     * Loads {@linkplain Hero heroes} from the JSON file into the map
     * <br>
     * Also sets next id to one more than the greatest id found in the file
     * 
     * @return true if the file was read successfully
     * 
     * @throws IOException when file cannot be accessed or read from
     */
    private boolean load() throws IOException {
    	flights= new TreeMap<>();
        nextId = 0;

        // Deserializes the JSON objects from the file into an array of heroes
        // readValue will throw an IOException if there's an issue with the file
        // or reading from the file
        Flight[] flightArray = objectMapper.readValue(new File(filename),Flight[].class);

        // Add each hero to the tree map and keep track of the greatest id
        for (Flight flight : flightArray) {
            flights.put(flight.getId(),flight);
           // if (flight.getId() > nextId)
               // nextId = flight.getId(); NO NEED FOR THIS
        }
        // Make the next id one greater than the maximum from the file
        //++nextId;
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
     
    @Override
    public Hero[] findHeroes(String containsText) {
        synchronized(heroes) {
            return getHeroesArray(containsText);
        }
    }*/

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
            							  flight.getDate(), flight.DepartureTime(), flight.getBoarding());
            
            flights.put(newFlight.getCode(),newFlight);
            save(); // may throw an IOException
            return true;
        }
    }



	@Override
	public String verifyBooking(String passport) throws IOException {
		// TODO Auto-generated method stub
		return null;
	}

}













