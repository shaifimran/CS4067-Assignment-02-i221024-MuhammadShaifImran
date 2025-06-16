package com.notification.model;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data

public class Notification {
    private String userEmail;
    private String message;

    // Constructor
    public Notification(String userEmail, String message) {
        this.userEmail = userEmail;
        this.message = message;
    }

    // Getters (Important!)
    public String getUserEmail() {
        return userEmail;
    }

    public String getMessage() {
        return message;
    }

    // Setters (if needed)
    public void setUserEmail(String userEmail) {
        this.userEmail = userEmail;
    }

    public void setMessage(String message) {
        this.message = message;
    }
}