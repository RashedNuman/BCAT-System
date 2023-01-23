package com.flights.api.flightsapi.model;

import java.util.logging.Logger;

import com.fasterxml.jackson.annotation.JsonProperty;
/**
 * Represents a Hero entity
 * 
 * @author SWEN Faculty
 */
public class Flight {
    private static final Logger LOG = Logger.getLogger(Flight.class.getName());

    // Package private for tests
    static final String STRING_FORMAT = "Hero [id=%d, name=%s]";

    @JsonProperty("code") String code;
    @JsonProperty("passport") String passport;
    @JsonProperty("name") String name;
    @JsonProperty("surname") String surname;
    @JsonProperty("departure") String departure;
    @JsonProperty("arrival") String arrival;
    @JsonProperty("seat") String seat;
    @JsonProperty("date") String date;
    @JsonProperty("departureTime") String departureTime;
    @JsonProperty("boarding") String boarding;
    /**
     * Create a hero with the given id and name
     * @param id The id of the hero
     * @param name The name of the hero
     * 
     * {@literal @}JsonProperty is used in serialization and deserialization
     * of the JSON object to the Java object in mapping the fields.  If a field
     * is not provided in the JSON object, the Java field gets the default Java
     * value, i.e. 0 for int
     */
    public Flight(@JsonProperty("code") String code, @JsonProperty("passport") String passport,  @JsonProperty("name") String name, @JsonProperty("surname") String surname,  
    			  @JsonProperty("departure") String departure,  @JsonProperty("arrival") String arrival,  @JsonProperty("seat") String seat,  @JsonProperty("date") String date,
    			  @JsonProperty("departureTime") String departureTime,  @JsonProperty("boarding") String boarding) {
    	
        this.code = code;
        this.passport = passport;
        this.name = name;
        this.surname = name;
        this.departure = departure;
        this.arrival = arrival;
        this.seat = seat;
        this.date = date;
        this.departureTime = departureTime;
        this.boarding = boarding;
        
        
    }
    
    public String getCode() {return code;}
    public void setCode(String code) {this.code = code;}
    
    public String getPassport() {return passport;}
    public void setPassport(String passport) { this.passport = passport;}
    
    public String getName() {return name;}
    public void setName(String name) {this.name = name;}
    
    public String getSurname() { return surname;}
    public void setSurname(String surname) {this.surname = surname;}
    
    public String getDeparture() {return departure;}
    public void setDeparture(String departure) {this.departure = departure;}
    
    public String getArrival() {return arrival;}
    public void setArrival(String arrival) {this.arrival = arrival;}
    
    public String getSeat() {return seat;}
    public void setSeat(String seat) {this.seat = seat;}
    
    public String getDate() {return date;}
    public void setDate(String date) {this.date = date;}
    
    public String getDepartureTime() {return departureTime;}
    public void setDepartureTime(String departureTime) {this.departureTime = departureTime;}
    
    public String getBoarding() {return boarding;}
    public void setBoarding(String boarding) {this.boarding = boarding;}
 

    /**
     * {@inheritDoc}
     */
    @Override
    public String toString() {
        return String.format(STRING_FORMAT, code);
    }
}