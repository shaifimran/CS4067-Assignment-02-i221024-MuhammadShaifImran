package com.notification.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.notification.model.Notification;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class NotificationService {

    private final RestTemplate restTemplate = new RestTemplate();
    private final ObjectMapper objectMapper = new ObjectMapper();

    @RabbitListener(queues = "${rabbitmq.queue}")
    public void receiveMessage(String message) {
        try {
            JsonNode jsonNode = objectMapper.readTree(message);
            int bookingId = jsonNode.get("booking_id").asInt();
            int userId = jsonNode.get("user_id").asInt();
            String status = jsonNode.get("status").asText();

            // Fetch user email (assuming User Service exists)
            //String userEmail = getUserEmail(userId);

            // Send notification (replace with actual email sending logic)
            
            System.out.println("Subject: Booking Confirmation");
            System.out.println("Message: Your booking (ID: " + bookingId + ") is now " + status);

        } catch (Exception e) {
            System.err.println("Error processing message: " + e.getMessage());
        }
    }

    // private String getUserEmail(int userId) {
    //     try {
    //         String url = "http://USER_SERVICE_URL/users/" + userId;
    //         JsonNode response = restTemplate.getForObject(url, JsonNode.class);
    //         return response != null ? response.get("email").asText() : "unknown@example.com";
    //     } catch (Exception e) {
    //         System.err.println("Error fetching user email: " + e.getMessage());
    //         return "unknown@example.com";
    //     }
    // }
}