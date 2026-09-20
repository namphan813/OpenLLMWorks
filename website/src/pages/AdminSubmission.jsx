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
      `Submission | Control Room | OpenLLMWorks`;

    loadSubmission();

    return () => {
      document.title = "OpenLLMWorks";
    };
  }, [loadSubmission]);

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
