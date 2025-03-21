package com.notification.controller;

import com.notification.model.Notification;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/notifications")
public class NotificationController {

    @Autowired
    private RabbitTemplate rabbitTemplate;

    @PostMapping("/send")
    public String sendNotification(@RequestBody Notification notification) {
        rabbitTemplate.convertAndSend("notifications", notification);
        return "Notification Sent!";
    }
}