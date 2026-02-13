package com.example.order;

import org.junit.jupiter.api.*;
import org.mockito.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

/**
 * Tests for OrderService
 *
 * WARNING: These tests demonstrate POOR test design practices.
 * They are intentionally written to showcase mock anti-patterns (AP1-AP4)
 * and serve as an example of what NOT to do.
 */
public class OrderServiceTest {

    // Shared mutable state -- mocks reused across tests without reset
    private static PaymentGateway gateway;
    private static InventoryService inventory;
    private static NotificationService notifier;

    @BeforeAll
    static void setupAll() {
        gateway = mock(PaymentGateway.class);
        inventory = mock(InventoryService.class);
        notifier = mock(NotificationService.class);
    }

    // ---------------------------------------------------------------
    // Test 1: AP1 -- Mock Tautology
    // Configures mock to return true, calls mock directly, asserts true.
    // No production code is exercised; the test proves only that
    // Mockito's when/thenReturn works.
    // ---------------------------------------------------------------
    @Test
    void test_chargePayment() {
        when(gateway.charge(49.99)).thenReturn(true);

        boolean result = gateway.charge(49.99);

        assertTrue(result);
    }

    // ---------------------------------------------------------------
    // Test 2: AP1 -- Mock Tautology
    // Same pattern: configure mock, call mock, assert the configured value.
    // ---------------------------------------------------------------
    @Test
    void test_reserveInventory() {
        when(inventory.reserve("ITEM-1", 2)).thenReturn(true);

        boolean reserved = inventory.reserve("ITEM-1", 2);

        assertTrue(reserved);
    }

    // ---------------------------------------------------------------
    // Test 3: AP2 -- No Production Code Exercised
    // All three dependencies are mocked. No OrderService is instantiated.
    // The test only calls mocks and verifies mock interactions.
    // ---------------------------------------------------------------
    @Test
    void test_placeOrder_allMocks() {
        when(inventory.reserve("SKU-100", 1)).thenReturn(true);
        when(gateway.charge(29.99)).thenReturn(true);

        inventory.reserve("SKU-100", 1);
        gateway.charge(29.99);
        notifier.sendConfirmation("ORD-1", "a@b.com");

        verify(inventory).reserve("SKU-100", 1);
        verify(gateway).charge(29.99);
        verify(notifier).sendConfirmation("ORD-1", "a@b.com");
    }

    // ---------------------------------------------------------------
    // Test 4: AP2 -- No Production Code Exercised
    // Mocks the notifier and verifies it was called, but there is no
    // OrderService anywhere. The test is pure mock choreography.
    // ---------------------------------------------------------------
    @Test
    void test_notificationSent() {
        notifier.sendConfirmation("ORD-42", "user@test.com");

        verify(notifier).sendConfirmation("ORD-42", "user@test.com");
    }

    // ---------------------------------------------------------------
    // Test 5: AP3 -- Over-Specified Mock Interactions
    // Verifies exact call counts with times(1) on every mock.
    // If the implementation ever batches or reorders calls, these
    // tests break even though the behavior is correct.
    // ---------------------------------------------------------------
    @Test
    void test_exactCallCounts() {
        OrderService service = new OrderService(gateway, inventory, notifier);
        when(inventory.reserve("ITEM-5", 3)).thenReturn(true);
        when(gateway.charge(99.99)).thenReturn(true);

        service.placeOrder("ORD-5", "ITEM-5", 3, 99.99, "user@test.com");

        verify(inventory, times(1)).reserve("ITEM-5", 3);
        verify(gateway, times(1)).charge(99.99);
        verify(notifier, times(1)).sendConfirmation("ORD-5", "user@test.com");
    }

    // ---------------------------------------------------------------
    // Test 6: AP3 -- Over-Specified Mock Interactions
    // Uses InOrder to enforce reserve → charge → notify sequence.
    // The test is brittle: any refactoring that changes call order
    // (even if the result is identical) will break it.
    // ---------------------------------------------------------------
    @Test
    void test_callOrdering() {
        OrderService service = new OrderService(gateway, inventory, notifier);
        when(inventory.reserve("ITEM-6", 1)).thenReturn(true);
        when(gateway.charge(50.00)).thenReturn(true);

        service.placeOrder("ORD-6", "ITEM-6", 1, 50.00, "order@test.com");

        InOrder inOrder = inOrder(inventory, gateway, notifier);
        inOrder.verify(inventory).reserve("ITEM-6", 1);
        inOrder.verify(gateway).charge(50.00);
        inOrder.verify(notifier).sendConfirmation("ORD-6", "order@test.com");
    }

    // ---------------------------------------------------------------
    // Test 7: AP3 -- Over-Specified Mock Interactions
    // verifyNoMoreInteractions on all mocks. Any new internal call
    // added to OrderService will break this test even if behavior
    // is correct.
    // ---------------------------------------------------------------
    @Test
    void test_noOtherInteractions() {
        PaymentGateway gw = mock(PaymentGateway.class);
        InventoryService inv = mock(InventoryService.class);
        NotificationService ns = mock(NotificationService.class);
        OrderService service = new OrderService(gw, inv, ns);

        when(inv.reserve("ITEM-7", 1)).thenReturn(true);
        when(gw.charge(10.00)).thenReturn(true);

        service.placeOrder("ORD-7", "ITEM-7", 1, 10.00, "x@y.com");

        verify(inv).reserve("ITEM-7", 1);
        verify(gw).charge(10.00);
        verify(ns).sendConfirmation("ORD-7", "x@y.com");

        verifyNoMoreInteractions(gw, inv, ns);
    }

    // ---------------------------------------------------------------
    // Test 8: AP4 -- Testing Internal Details
    // Uses ArgumentCaptor to inspect the exact string passed to the
    // notifier. This couples the test to the internal wiring of
    // OrderService, not its observable behavior.
    // ---------------------------------------------------------------
    @Test
    void test_captorInspection() {
        NotificationService ns = mock(NotificationService.class);
        OrderService service = new OrderService(gateway, inventory, ns);

        when(inventory.reserve("ITEM-8", 1)).thenReturn(true);
        when(gateway.charge(25.00)).thenReturn(true);

        service.placeOrder("ORD-8", "ITEM-8", 1, 25.00, "cap@test.com");

        ArgumentCaptor<String> orderCaptor = ArgumentCaptor.forClass(String.class);
        ArgumentCaptor<String> emailCaptor = ArgumentCaptor.forClass(String.class);
        verify(ns).sendConfirmation(orderCaptor.capture(), emailCaptor.capture());

        assertEquals("ORD-8", orderCaptor.getValue());
        assertEquals("cap@test.com", emailCaptor.getValue());
        assertTrue(orderCaptor.getValue().startsWith("ORD-"));
        assertTrue(emailCaptor.getValue().contains("@"));
    }

    // ---------------------------------------------------------------
    // Test 9: AP4 -- Testing Internal Details
    // Uses verify(never()) to assert that the notifier was NOT called.
    // High verify-to-assert ratio: 3 verify calls vs 1 assert.
    // ---------------------------------------------------------------
    @Test
    void test_verifyNever() {
        PaymentGateway gw = mock(PaymentGateway.class);
        InventoryService inv = mock(InventoryService.class);
        NotificationService ns = mock(NotificationService.class);
        OrderService service = new OrderService(gw, inv, ns);

        when(inv.reserve("ITEM-9", 1)).thenReturn(true);
        when(gw.charge(75.00)).thenReturn(false);

        OrderResult result = service.placeOrder("ORD-9", "ITEM-9", 1, 75.00, "fail@test.com");

        assertFalse(result.isSuccess());
        verify(inv).reserve("ITEM-9", 1);
        verify(gw).charge(75.00);
        verify(ns, never()).sendConfirmation(anyString(), anyString());
        verify(inv).release("ITEM-9", 1);
    }

    // ---------------------------------------------------------------
    // Test 10: AP1 + AP2 combo
    // Configures gateway mock to return false, calls mock directly,
    // asserts false. No OrderService is instantiated.
    // ---------------------------------------------------------------
    @Test
    void test_paymentFailed() {
        when(gateway.charge(999.99)).thenReturn(false);

        boolean charged = gateway.charge(999.99);

        assertFalse(charged);
        verify(gateway).charge(999.99);
    }

    // ---------------------------------------------------------------
    // Test 11: Multiple anti-patterns (AP1 + AP2 + AP3)
    // Mega-test combining tautological assertions, no production code,
    // and over-specified interactions. 10+ assertions in one method.
    // ---------------------------------------------------------------
    @Test
    void test_everything() {
        PaymentGateway gw = mock(PaymentGateway.class);
        InventoryService inv = mock(InventoryService.class);
        NotificationService ns = mock(NotificationService.class);

        // AP1: mock tautology -- configure and assert same value
        when(gw.charge(100.00)).thenReturn(true);
        assertTrue(gw.charge(100.00));

        when(inv.reserve("X", 1)).thenReturn(true);
        assertTrue(inv.reserve("X", 1));

        when(gw.charge(200.00)).thenReturn(false);
        assertFalse(gw.charge(200.00));

        // AP2: no production code, just call mocks
        ns.sendConfirmation("ORD-X", "e@x.com");

        // AP3: over-specified verification
        verify(gw, times(1)).charge(100.00);
        verify(gw, times(1)).charge(200.00);
        verify(inv, times(1)).reserve("X", 1);
        verify(ns, times(1)).sendConfirmation("ORD-X", "e@x.com");

        // More tautological assertions
        assertNotNull(gw);
        assertNotNull(inv);
        assertNotNull(ns);
    }

    // ---------------------------------------------------------------
    // Test 12: AP2 -- Trivial / Framework test
    // assertTrue(true) and assertNotNull(mock(...)) test only the
    // framework, not any production behavior.
    // ---------------------------------------------------------------
    @Test
    void test_framework() {
        assertTrue(true);
        assertNotNull(mock(PaymentGateway.class));
        assertNotNull(mock(InventoryService.class));
        assertNotNull(mock(NotificationService.class));
    }
}
