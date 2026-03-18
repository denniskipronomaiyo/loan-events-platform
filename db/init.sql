-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =========================
-- 1. Customers
-- =========================
CREATE TABLE customers (
    customer_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name TEXT NOT NULL,
    region TEXT NOT NULL,
    date_of_birth DATE NOT NULL,
    business_type TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- =========================
-- 2. Loan Applications
-- =========================
CREATE TABLE loan_applications (
    application_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    customer_id UUID NOT NULL,
    product_type TEXT NOT NULL,
    amount_requested NUMERIC(12,2) NOT NULL,
    currency TEXT DEFAULT 'KES',
    submitted_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_customer
        FOREIGN KEY(customer_id)
        REFERENCES customers(customer_id)
        ON DELETE CASCADE
);

-- =========================
-- 3. Loan Events (Append-only)
-- =========================
CREATE TABLE loan_events (
    event_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    application_id UUID NOT NULL,
    event_type TEXT NOT NULL,
    event_timestamp TIMESTAMP NOT NULL,

    -- Optional payload fields
    amount_requested NUMERIC(12,2),
    amount_disbursed NUMERIC(12,2),
    currency TEXT DEFAULT 'KES',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_application
        FOREIGN KEY(application_id)
        REFERENCES loan_applications(application_id)
        ON DELETE CASCADE
);