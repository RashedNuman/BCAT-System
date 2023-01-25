package com.flights.api.flightsapi.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.flights.api.flightsapi.model.Flight;
import com.flights.api.flightsapi.persistence.FlightDAO;

import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;


@RestController
@RequestMapping("flights")
public class FlightsController {
    private static final Logger LOG = Logger.getLogger(FlightsController.class.getName());
    private FlightDAO flightDao;

    public FlightsController(FlightDAO flightDao) {
        this.flightDao = flightDao;
    }
    
    //WORKS
    // get a specific booking based on code
    @GetMapping("/{code}")
    public ResponseEntity<Flight> getFlight(@PathVariable String code) {
        LOG.info("GET /Booking/" + code);
        try {
            Flight booking = flightDao.getBooking(code);
            if (booking != null)
                return new ResponseEntity<Flight>(booking,HttpStatus.OK);
            else
                return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
        catch(IOException e) {
            LOG.log(Level.SEVERE,e.getLocalizedMessage());
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @GetMapping("")
    public ResponseEntity<Flight[]> getBookings() {
    	LOG.info("GET /Bookings");
        try {
            Flight[] bookings = flightDao.getBookings();
            if (bookings != null)
                return new ResponseEntity<Flight[]>(bookings,HttpStatus.OK);
            else
                return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
        catch(IOException e) {
            LOG.log(Level.SEVERE,e.getLocalizedMessage());
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }
    
    @PostMapping("")
    public ResponseEntity<Boolean> createBooking(@RequestBody Flight booking){
    	LOG.info("POST /booking " + booking);
    	
    	try {
    		boolean result = flightDao.createBooking(booking);
    		
    		if (result == true) {
    			return new ResponseEntity<>(true, HttpStatus.CREATED);
    			
    		}else {
    			return new ResponseEntity<>(false, HttpStatus.EXPECTATION_FAILED);
    		}
    	}catch(IOException e){
            LOG.log(Level.SEVERE,e.getLocalizedMessage());
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
            
    	}

    }
    
    @PostMapping("/verify/{passport}")
    public ResponseEntity<String> verifyBooking(@PathVariable String passport){
    	LOG.info("POST /verify " + passport);
    	
    	try {
    		String code = flightDao.verifyBooking(passport);
    		
    		if (!code.equals("NOT FOUND")) {
    			return new ResponseEntity<>(code, HttpStatus.FOUND);
    			
    		}else {
    			return new ResponseEntity<>(code, HttpStatus.EXPECTATION_FAILED);
    		}
    	}catch(IOException e){
            LOG.log(Level.SEVERE,e.getLocalizedMessage());
            return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR);
            
    	}

    }
}
