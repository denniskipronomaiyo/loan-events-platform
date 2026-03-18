-- Fast filtering by application
CREATE INDEX idx_loan_events_application 
ON loan_events(application_id);

-- Fast analytics on time-based queries
CREATE INDEX idx_loan_events_timestamp 
ON loan_events(event_timestamp);

-- Filter by event type (e.g. disbursed/defaulted)
CREATE INDEX idx_loan_events_type 
ON loan_events(event_type);

-- Composite index (real-world optimization)
CREATE INDEX idx_events_type_timestamp 
ON loan_events(event_type, event_timestamp);