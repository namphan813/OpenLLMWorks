-- OpenLLMWorks Operations Database
-- Migration 0001: Submission operations foundation
--
-- This database tracks operational workflow state.
-- It does NOT replace the canonical OpenLLMWorks benchmark database.

CREATE TABLE submissions (
    submission_id TEXT PRIMARY KEY,

    status TEXT NOT NULL
        CHECK (
            status IN (
                'received',
                'validation_pending',
                'validating',
                'validated',
                'awaiting_review',
                'rejected',
                'approved',
                'declined',
                'importing',
                'import_failed',
                'imported',
                'publishing',
                'publish_failed',
                'published'
            )
        ),

    object_key TEXT NOT NULL UNIQUE,

    received_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,

    validation_started_at TEXT,
    validated_at TEXT,
    validation_status TEXT
        CHECK (
            validation_status IS NULL
            OR validation_status IN ('passed', 'failed')
        ),
    validation_error TEXT,

    reviewed_at TEXT,
    review_decision TEXT
        CHECK (
            review_decision IS NULL
            OR review_decision IN ('approved', 'declined')
        ),

    imported_at TEXT,
    published_at TEXT,

    result_id TEXT,

    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_submissions_status
    ON submissions(status);

CREATE INDEX idx_submissions_received_at
    ON submissions(received_at);

CREATE TABLE submission_events (
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,

    submission_id TEXT NOT NULL,

    event_type TEXT NOT NULL,
    actor TEXT NOT NULL,

    details TEXT,

    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (submission_id)
        REFERENCES submissions(submission_id)
        ON DELETE CASCADE
);

CREATE INDEX idx_submission_events_submission_id
    ON submission_events(submission_id);

CREATE INDEX idx_submission_events_created_at
    ON submission_events(created_at);
