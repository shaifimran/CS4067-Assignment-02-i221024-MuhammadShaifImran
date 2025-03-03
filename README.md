# Online Event Booking Platform

This project is an Online Event Booking Platform developed using a microservices architecture. The platform allows users to browse events, book tickets, and receive notifications. It comprises several microservices, each responsible for specific functionalities.&#8203;:contentReference[oaicite:2]{index=2}

## Table of Contents

- [Microservices Overview](#microservices-overview)
- [User Service](#user-service)
- [Event Service](#event-service)
- [Booking Service](#booking-service)
- [Notification Service](#notification-service)
- [Payment Service](#payment-service)
- [Getting Started](#getting-started)
- [Contributors](#contributors)

## Microservices Overview

:contentReference[oaicite:3]{index=3}&#8203;:contentReference[oaicite:4]{index=4}

1. **User Service**: :contentReference[oaicite:5]{index=5}&#8203;:contentReference[oaicite:6]{index=6}
2. **Event Service**: :contentReference[oaicite:7]{index=7}&#8203;:contentReference[oaicite:8]{index=8}
3. **Booking Service**: :contentReference[oaicite:9]{index=9}&#8203;:contentReference[oaicite:10]{index=10}
4. **Notification Service**: :contentReference[oaicite:11]{index=11}&#8203;:contentReference[oaicite:12]{index=12}
5. **Payment Service**: :contentReference[oaicite:13]{index=13}&#8203;:contentReference[oaicite:14]{index=14}

## User Service

:contentReference[oaicite:15]{index=15} :contentReference[oaicite:16]{index=16}&#8203;:contentReference[oaicite:17]{index=17}

- **Register User**

  - **Endpoint**: :contentReference[oaicite:18]{index=18}&#8203;:contentReference[oaicite:19]{index=19}
  - **Description**: :contentReference[oaicite:20]{index=20}&#8203;:contentReference[oaicite:21]{index=21}
  - **Request Body**:
    ```json
    {
      "username": "string",
      "email": "string",
      "password": "string"
    }
    ```
  - **Response**:
    - **201 Created**: User registered successfully.
    - **400 Bad Request**: Invalid input data.

- **User Login**

  - **Endpoint**: :contentReference[oaicite:22]{index=22}&#8203;:contentReference[oaicite:23]{index=23}
  - **Description**: :contentReference[oaicite:24]{index=24}&#8203;:contentReference[oaicite:25]{index=25}
  - **Request Body**:
    ```json
    {
      "email": "string",
      "password": "string"
    }
    ```
  - **Response**:
    - **200 OK**: Authentication successful.
    - **401 Unauthorized**: Invalid credentials.

- **Get User Profile**

  - **Endpoint**: :contentReference[oaicite:26]{index=26}&#8203;:contentReference[oaicite:27]{index=27}
  - **Description**: :contentReference[oaicite:28]{index=28}&#8203;:contentReference[oaicite:29]{index=29}
  - **Headers**:
    - `Authorization: Bearer <token>`
  - **Response**:
    - **200 OK**: User profile data.
    - **401 Unauthorized**: Invalid or missing token.

## Event Service

:contentReference[oaicite:30]{index=30} :contentReference[oaicite:31]{index=31}&#8203;:contentReference[oaicite:32]{index=32}

- **Create Event**

  - **Endpoint**: :contentReference[oaicite:33]{index=33}&#8203;:contentReference[oaicite:34]{index=34}
  - **Description**: :contentReference[oaicite:35]{index=35}&#8203;:contentReference[oaicite:36]{index=36}
  - **Request Body**:
    ```json
    {
      "title": "string",
      "description": "string",
      "date": "string",
      "location": "string",
      "available_tickets": "integer"
    }
    ```
  - **Response**:
    - **201 Created**: Event created successfully.
    - **400 Bad Request**: Invalid input data.

- **Get All Events**

  - **Endpoint**: :contentReference[oaicite:37]{index=37}&#8203;:contentReference[oaicite:38]{index=38}
  - **Description**: :contentReference[oaicite:39]{index=39}&#8203;:contentReference[oaicite:40]{index=40}
  - **Response**:
    - **200 OK**: List of events.

- **Get Event by ID**

  - **Endpoint**: :contentReference[oaicite:41]{index=41}&#8203;:contentReference[oaicite:42]{index=42}
  - **Description**: :contentReference[oaicite:43]{index=43}&#8203;:contentReference[oaicite:44]{index=44}
  - **Response**:
    - **200 OK**: Event details.
    - **404 Not Found**: Event not found.

## Booking Service

:contentReference[oaicite:45]{index=45} :contentReference[oaicite:46]{index=46}&#8203;:contentReference[oaicite:47]{index=47}

- **Create Booking**

  - **Endpoint**: :contentReference[oaicite:48]{index=48}&#8203;:contentReference[oaicite:49]{index=49}
  - **Description**: :contentReference[oaicite:50]{index=50}&#8203;:contentReference[oaicite:51]{index=51}
  - **Request Body**:
    ```json
    {
      "user_id": "string",
      "event_id": "string",
      "number_of_tickets": "integer",
      "payment_details": {
        "card_number": "string",
        "expiry_date": "string",
        "cvv": "string"
      }
    }
    ```
  - **Response**:
    - **201 Created**: Booking created successfully.
    - **400 Bad Request**: Invalid input data.
    - **402 Payment Required**: Payment processing failed.

- **Get Booking by ID**

  - **Endpoint**: :contentReference[oaicite:52]{index=52}&#8203;:contentReference[oaicite:53]{index=53}
  - **Description**: :contentReference[oaicite:54]{index=54}&#8203;:contentReference[oaicite:55]{index=55}
  - **Response**:
    - **200 OK**: Booking details.
    - **404 Not Found**: Booking not found.

## Notification Service

:contentReference[oaicite:56]{index=56} :contentReference[oaicite:57]{index=57}&#8203;:contentReference[oaicite:58]{index=58}

- **Send Notification**

  - **Endpoint**: :contentReference[oaicite:59]{index=59}&#8203;:contentReference[oaicite:60]{index=60}
  - **Description**: Sends a
::contentReference[oaicite:61]{index=61}
 
