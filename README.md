# ENSF 338 Term Project - Campus Navigation and Event Management System

## Repository
GitHub Repository URL: *https://github.com/reyanshBadhwar26/ensf338-finalproject.git*

## Group Members
- Abdelrahman Attia
- Reyansh Badhwar
- Himaal Ishaq
- Alina Kobrusev
- Abiya Raheel
- Nayha Rehman

## Project Overview
This application simulates a campus system with the following features:

- Shortest path navigation between buildings  
- Route history with undo functionality  
- Room and event booking system  
- Priority-based service queue  
- Fast lookup of buildings and rooms  
- Incoming request processing  
- Bonus: Balanced AVL tree index for bookings 

## How to Run the Application

### 1. Navigate to the source folder
```
cd src
```

### 2. Run the program
```
python main.py
```

## Detailed Demo Instructions

Follow the steps below to reproduce all required demo scenarios.


### 1. Shortest Path Query
- From the main menu, select:
  - `1. Shortest path navigation`
- Enter two different pairs of source and destination buildings
- The system will display:
  - Full path (e.g., A -> B -> C)
  - Total travel time
- Repeat with a different pair of buildings


### 2. Undo Navigation
- Perform multiple shortest path queries using option `1`
- Then select:
  - `2. Undo last navigation`
- The system will revert to the previous route
- Repeat undo to demonstrate multiple levels of history
- Optionally, use:
  - `3. Show navigation history`
  to display all stored routes

### 3. Booking Range Query
- From the main menu, select:
  - `4. Room and event booking system`
- Then select:
  - `5. Query events in a time range`
- Enter:
  - Date
  - Start time
  - End time
- The system will display all bookings within that time window

### 4. Priority Queue Demo
- From the main menu, select:
  - `5. Priority service queue`
- Add multiple service requests using:
  - `1. Add service request`
  - Use different priorities: Emergency, Standard, Low
- Then select:
  - `2. Serve next request`
- Observe that requests are processed in correct priority order

### 5. Fast Lookup Demo
- From the main menu, select:
  - `6. Fast building / room lookup`
- Insert a building or room using options `1` or `4`
- Lookup an existing building or room using options `3` or `6`
- Then attempt a lookup for a non-existent key
    - The system will correctly indicate that the item is not found

### 6. Request Pipeline Demo
- From the main menu, select:
  - `7. Incoming request pipeline`
- Then select:
  - `5. Simulate 20 sequential requests`
- The system will:
  - Enqueue 20 requests in order
  - Dequeue them in the same FIFO order
- This demonstrates correct queue behavior

### (Bonus) AVL Tree Visualization
- From the main menu:
  - `4. Room and event booking system`
  - then select `7. Print booking AVL tree`
- Add bookings (preferably in chronological order)
- Print the AVL tree after insertions
- Observe:
  - Tree structure
  - Balance factors (should remain between -1 and 1)