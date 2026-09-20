import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  Link,
  useParams,
} from "react-router-dom";

import "./Admin.css";

const API_BASE =
  "https://api.openllmworks.com/v1/admin/submissions";

const DECLINE_REASONS = [
  {
    value: "incomplete_evidence",
    label: "Incomplete evidence",
  },
  {
    value: "protocol_mismatch",
    label: "Protocol mismatch",
  },
  {
    value: "hardware_mismatch",
    label: "Hardware mismatch",
  },
  {
    value: "duplicate_submission",
    label: "Duplicate submission",
  },
  {
    value: "suspicious_result",
    label: "Suspicious result",
  },
  {
    value: "unsupported_configuration",
    label: "Unsupported configuration",
  },
  {
    value: "other",
    label: "Other",
  },
];

function formatDate(value) {
  if (!value) {
    return "—";
  }

  return new Date(value).toLocaleString();
}

function formatEventDetails(details) {
  if (!details) {
    return null;
  }

  try {
    return JSON.stringify(
      JSON.parse(details),
      null,
      2,
    );
  } catch {
    return details;
  }
}

function AdminSubmission() {
  const { submissionId } = useParams();

  const [submission, setSubmission] = useState(null);
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [reviewMode, setReviewMode] = useState(null);
  const [reasonCode, setReasonCode] = useState("");
  const [reasonDetail, setReasonDetail] = useState("");
  const [reviewing, setReviewing] = useState(false);
  const [reviewError, setReviewError] = useState("");

  const loadSubmission = useCallback(async () => {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        `${API_BASE}/${encodeURIComponent(submissionId)}`,
        {
          credentials: "include",
          headers: {
            Accept: "application/json",
          },
        },
      );

      if (!response.ok) {
        throw new Error(
          `Control Room API returned ${response.status}.`,
        );
      }

      const data = await response.json();

      setSubmission(data.submission);
      setEvents(data.events || []);
    } catch (loadError) {
      setSubmission(null);
      setEvents([]);
      setError(loadError.message);
    } finally {
      setLoading(false);
    }
  }, [submissionId]);

  useEffect(() => {
    document.title =
      "Submission | Control Room | OpenLLMWorks";

    loadSubmission();

    return () => {
      document.title = "OpenLLMWorks";
    };
  }, [loadSubmission]);

  const canReview =
    submission?.status === "validated" &&
    submission?.validation_status === "passed" &&
    !submission?.review_decision;

  const resetReviewForm = () => {
    setReviewMode(null);
    setReasonCode("");
    setReasonDetail("");
    setReviewError("");
  };

  const submitReview = async (decision) => {
    if (reviewing) {
      return;
    }

    if (
      decision === "declined" &&
      !reasonCode
    ) {
      setReviewError(
        "Select a decline reason before continuing.",
      );
      return;
    }

    if (
      decision === "declined" &&
      reasonCode === "other" &&
      !reasonDetail.trim()
    ) {
      setReviewError(
        "Add details when using the Other decline reason.",
      );
      return;
    }

    if (
      decision === "approved" &&
      !window.confirm(
        "Approve this submission? This review decision cannot currently be changed in the Control Room.",
      )
    ) {
      return;
    }

    if (
      decision === "declined" &&
      !window.confirm(
        "Decline this submission? This review decision cannot currently be changed in the Control Room.",
      )
    ) {
      return;
    }

    setReviewing(true);
    setReviewError("");

    try {
      const payload = {
        decision,
      };

      if (decision === "declined") {
        payload.reason_code = reasonCode;

        if (reasonDetail.trim()) {
          payload.reason_detail =
            reasonDetail.trim();
        }
      }

      const response = await fetch(
        `${API_BASE}/${encodeURIComponent(submissionId)}/review`,
        {
          method: "POST",
          credentials: "include",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload),
        },
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.message ||
            `Control Room API returned ${response.status}.`,
        );
      }

      resetReviewForm();
      await loadSubmission();
    } catch (reviewRequestError) {
      setReviewError(reviewRequestError.message);
    } finally {
      setReviewing(false);
    }
  };

  return (
    <div className="control-room">
      <header className="control-room-header">
        <p className="control-room-eyebrow">
          OpenLLMWorks
        </p>

        <Link
          className="control-room-back-link"
          to="/admin"
        >
          ← Back to Control Room
        </Link>

        <h1>Submission Detail</h1>

        <p>
          Operational state and event history for{" "}
          <code>{submissionId}</code>
        </p>
      </header>

      {loading && (
        <section className="control-room-login">
          <h2>Loading Submission</h2>
          <p>
            Retrieving operational state through
            Cloudflare Access...
          </p>
        </section>
      )}

      {!loading && error && (
        <section className="control-room-login">
          <h2>Unable to Load Submission</h2>

          <p className="control-room-error">
            {error}
          </p>

          <button
            type="button"
            onClick={loadSubmission}
          >
            Retry
          </button>
        </section>
      )}

      {!loading && submission && (
        <>
          <section className="control-room-detail-grid">
            <article>
              <span>Status</span>
              <strong>{submission.status}</strong>
            </article>

            <article>
              <span>Validation</span>
              <strong>
                {submission.validation_status || "—"}
              </strong>
            </article>

            <article>
              <span>Review</span>
              <strong>
                {submission.review_decision || "—"}
              </strong>
            </article>

            <article>
              <span>Result ID</span>
              <strong>
                {submission.result_id || "—"}
              </strong>
            </article>
          </section>

          <section className="control-room-panel control-room-detail-panel">
            <div className="control-room-panel-header">
              <div>
                <h2>Submission</h2>
                <p>
                  Current operations database record.
                </p>
              </div>

              <button
                type="button"
                onClick={loadSubmission}
                disabled={loading}
              >
                Refresh
              </button>
            </div>

            <dl className="control-room-detail-list">
              <div>
                <dt>Submission ID</dt>
                <dd>
                  <code>
                    {submission.submission_id}
                  </code>
                </dd>
              </div>

              <div>
                <dt>R2 Object</dt>
                <dd>
                  <code>{submission.object_key}</code>
                </dd>
              </div>

              <div>
                <dt>Received</dt>
                <dd>
                  {formatDate(submission.received_at)}
                </dd>
              </div>

              <div>
                <dt>Validation Started</dt>
                <dd>
                  {formatDate(
                    submission.validation_started_at,
                  )}
                </dd>
              </div>

              <div>
                <dt>Validated</dt>
                <dd>
                  {formatDate(submission.validated_at)}
                </dd>
              </div>

              <div>
                <dt>Reviewed</dt>
                <dd>
                  {formatDate(submission.reviewed_at)}
                </dd>
              </div>

              <div>
                <dt>Imported</dt>
                <dd>
                  {formatDate(submission.imported_at)}
                </dd>
              </div>

              <div>
                <dt>Published</dt>
                <dd>
                  {formatDate(submission.published_at)}
                </dd>
              </div>

              <div>
                <dt>Updated</dt>
                <dd>
                  {formatDate(submission.updated_at)}
                </dd>
              </div>
            </dl>

            {submission.validation_error && (
              <div className="control-room-validation-error">
                <h3>Validation Error</h3>
                <pre>
                  {submission.validation_error}
                </pre>
              </div>
            )}
          </section>

          <section className="control-room-panel control-room-review-panel">
            <div className="control-room-panel-header">
              <div>
                <h2>Review Submission</h2>
                <p>
                  Record the maintainer review decision.
                </p>
              </div>
            </div>

            {canReview && !reviewMode && (
              <div className="control-room-review-ready">
                <div>
                  <strong>
                    Validation passed. Ready for review.
                  </strong>
                  <p>
                    Approve the submission or decline it
                    with a structured reason.
                  </p>
                </div>

                <div className="control-room-review-actions">
                  <button
                    type="button"
                    className="control-room-button-danger"
                    onClick={() => {
                      setReviewMode("decline");
                      setReviewError("");
                    }}
                  >
                    Decline
                  </button>

                  <button
                    type="button"
                    className="control-room-button-primary"
                    onClick={() =>
                      submitReview("approved")
                    }
                    disabled={reviewing}
                  >
                    {reviewing
                      ? "Saving..."
                      : "Approve"}
                  </button>
                </div>
              </div>
            )}

            {canReview &&
              reviewMode === "decline" && (
                <div className="control-room-decline-form">
                  <label htmlFor="decline-reason">
                    Decline reason
                  </label>

                  <select
                    id="decline-reason"
                    value={reasonCode}
                    onChange={(event) => {
                      setReasonCode(
                        event.target.value,
                      );
                      setReviewError("");
                    }}
                    disabled={reviewing}
                  >
                    <option value="">
                      Select a reason...
                    </option>

                    {DECLINE_REASONS.map(
                      (reason) => (
                        <option
                          key={reason.value}
                          value={reason.value}
                        >
                          {reason.label}
                        </option>
                      ),
                    )}
                  </select>

                  <label htmlFor="decline-detail">
                    Additional details
                    {reasonCode === "other"
                      ? " *"
                      : ""}
                  </label>

                  <textarea
                    id="decline-detail"
                    rows="5"
                    maxLength="2000"
                    value={reasonDetail}
                    onChange={(event) =>
                      setReasonDetail(
                        event.target.value,
                      )
                    }
                    placeholder={
                      reasonCode === "other"
                        ? "Describe why this submission should be declined."
                        : "Optional context for this review decision."
                    }
                    disabled={reviewing}
                  />

                  <div className="control-room-review-actions">
                    <button
                      type="button"
                      onClick={resetReviewForm}
                      disabled={reviewing}
                    >
                      Cancel
                    </button>

                    <button
                      type="button"
                      className="control-room-button-danger"
                      onClick={() =>
                        submitReview("declined")
                      }
                      disabled={reviewing}
                    >
                      {reviewing
                        ? "Saving..."
                        : "Decline Submission"}
                    </button>
                  </div>
                </div>
              )}

            {!canReview &&
              submission.review_decision && (
                <div className="control-room-review-complete">
                  <span>Review decision</span>

                  <strong>
                    {submission.review_decision}
                  </strong>

                  <p>
                    Reviewed{" "}
                    {formatDate(
                      submission.reviewed_at,
                    )}
                  </p>
                </div>
              )}

            {!canReview &&
              !submission.review_decision && (
                <div className="control-room-review-unavailable">
                  <strong>
                    Not ready for maintainer review.
                  </strong>

                  <p>
                    This submission must reach
                    validated / passed before a review
                    decision can be recorded.
                  </p>
                </div>
              )}

            {reviewError && (
              <p className="control-room-error">
                {reviewError}
              </p>
            )}
          </section>

          <section className="control-room-panel control-room-events-panel">
            <div className="control-room-panel-header">
              <div>
                <h2>Event History</h2>
                <p>
                  Recorded lifecycle events for this
                  submission.
                </p>
              </div>
            </div>

            <div className="control-room-events">
              {events.length === 0 && (
                <p>No events recorded.</p>
              )}

              {events.map((event) => (
                <article
                  className="control-room-event"
                  key={event.event_id}
                >
                  <div className="control-room-event-marker" />

                  <div className="control-room-event-content">
                    <div className="control-room-event-header">
                      <strong>
                        {event.event_type}
                      </strong>

                      <time>
                        {formatDate(event.created_at)}
                      </time>
                    </div>

                    <p>
                      Actor: <code>{event.actor}</code>
                    </p>

                    {event.details && (
                      <pre>
                        {formatEventDetails(
                          event.details,
                        )}
                      </pre>
                    )}
                  </div>
                </article>
              ))}
            </div>
          </section>
        </>
      )}
    </div>
  );
}

export default AdminSubmission;
