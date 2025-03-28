package com.notification.config;

import org.springframework.amqp.core.Queue;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class RabbitMQConfig {

    @Value("${notification.queue.name}")  // Read from environment
    private String queueName;

    @Bean
    public Queue notificationQueue() {
        return new Queue(queueName, true);
    }
}
