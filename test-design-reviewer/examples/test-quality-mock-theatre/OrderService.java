package com.example.order;

/**
 * Simple payment gateway interface for processing charges.
 */
interface PaymentGateway {
    boolean charge(double amount);
}

/**
 * Inventory management interface for reserving and releasing stock.
 */
interface InventoryService {
    boolean reserve(String itemId, int qty);
    void release(String itemId, int qty);
}

/**
 * Notification interface for sending order confirmations.
 */
interface NotificationService {
    void sendConfirmation(String orderId, String email);
}

/**
 * Result of placing an order.
 */
class OrderResult {
    private final boolean success;
    private final String orderId;
    private final String message;

    public OrderResult(boolean success, String orderId, String message) {
        this.success = success;
        this.orderId = orderId;
        this.message = message;
    }

    public boolean isSuccess() { return success; }
    public String getOrderId() { return orderId; }
    public String getMessage() { return message; }
}

/**
 * Service that coordinates order placement across inventory,
 * payment, and notification subsystems.
 */
public class OrderService {

    private final PaymentGateway paymentGateway;
    private final InventoryService inventoryService;
    private final NotificationService notificationService;

    public OrderService(PaymentGateway paymentGateway,
                        InventoryService inventoryService,
                        NotificationService notificationService) {
        this.paymentGateway = paymentGateway;
        this.inventoryService = inventoryService;
        this.notificationService = notificationService;
    }

    /**
     * Places an order: reserves inventory, charges payment, sends notification.
     * If payment fails after inventory is reserved, the reservation is released.
     */
    public OrderResult placeOrder(String orderId, String itemId, int qty,
                                  double amount, String email) {
        if (orderId == null || itemId == null || email == null) {
            return new OrderResult(false, orderId, "Invalid input");
        }

        boolean reserved = inventoryService.reserve(itemId, qty);
        if (!reserved) {
            return new OrderResult(false, orderId, "Out of stock");
        }

        boolean charged = paymentGateway.charge(amount);
        if (!charged) {
            inventoryService.release(itemId, qty);
            return new OrderResult(false, orderId, "Payment failed");
        }

        notificationService.sendConfirmation(orderId, email);
        return new OrderResult(true, orderId, "Order placed");
    }
}
