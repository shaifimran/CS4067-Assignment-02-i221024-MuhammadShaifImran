package com.notification.service;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
public class NotificationService {

    private final ObjectMapper objectMapper = new ObjectMapper();

    @Value("${notification.queue.name}") // Get queue name from env
    private String queueName;

    @RabbitListener(queues = "${notification.queue.name}")
    public void receiveMessage(String message) {
        try {
            JsonNode jsonNode = objectMapper.readTree(message);
            int bookingId = jsonNode.get("booking_id").asInt();
            int userId = jsonNode.get("user_id").asInt();
            String status = jsonNode.get("status").asText();

            System.out.println("Received message from queue: " + queueName);
            System.out.println("Subject: Booking Confirmation");
            System.out.println("Message: Your booking (ID: " + bookingId + ") is now " + status);

        } catch (Exception e) {
            System.err.println("Error processing message: " + e.getMessage());
        }
    }
}
