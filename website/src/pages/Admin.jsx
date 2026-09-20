import {
    useCallback,
    useEffect,
    useState,
} from "react";

import {
    Link,
} from "react-router-dom";

import "./Admin.css";

const API_URL =
    "https://api.openllmworks.com/v1/admin/submissions";

function formatDate(value) {
    if (!value) {
        return "—";
    }

    return new Date(value).toLocaleString();
}

function Admin() {
    const [submissions, setSubmissions] = useState([]);
    const [counts, setCounts] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    const loadSubmissions = useCallback(async () => {
        setLoading(true);
        setError("");

        try {
            const response = await fetch(API_URL, {
                credentials: "include",
                headers: {
                    Accept: "application/json",
                },
            });

            if (!response.ok) {
                throw new Error(
                    `Control Room API returned ${response.status}.`,
                );
            }

            const data = await response.json();

            setCounts(data.counts);
            setSubmissions(data.submissions || []);
        } catch (loadError) {
            setCounts(null);
            setSubmissions([]);
            setError(loadError.message);
        } finally {
            setLoading(false);
        }
    }, []);

    useEffect(() => {
        document.title = "Control Room | OpenLLMWorks";

        loadSubmissions();

        return () => {
            document.title = "OpenLLMWorks";
        };
    }, [loadSubmissions]);

    return (
        <div className="control-room">
            <header className="control-room-header">
                <div>
                    <p className="control-room-eyebrow">
                        OpenLLMWorks
                    </p>

                    <h1>Control Room</h1>

                    <p>
                        Submission operations and validation state.
                    </p>
                </div>
            </header>

            {!counts && (
                <section className="control-room-login">
                    <h2>
                        {loading
                            ? "Loading Operations"
                            : "Unable to Load Operations"}
                    </h2>

                    <p>
                        {loading
                            ? "Connecting through Cloudflare Access..."
                            : "The Control Room could not reach the operations API."}
                    </p>

                    {error && (
                        <p className="control-room-error">
                            {error}
                        </p>
                    )}

                    {!loading && (
                        <button
                            type="button"
                            onClick={loadSubmissions}
                        >
                            Retry
                        </button>
                    )}
                </section>
            )}

            {counts && (
                <>
                    <section className="control-room-stats">
                        <article>
                            <span>Total</span>
                            <strong>{counts.total}</strong>
                        </article>

                        <article>
                            <span>Validated</span>
                            <strong>{counts.validated}</strong>
                        </article>

                        <article>
                            <span>Validating</span>
                            <strong>{counts.validating}</strong>
                        </article>

                        <article>
                            <span>Received</span>
                            <strong>{counts.received}</strong>
                        </article>

                        <article>
                            <span>Rejected</span>
                            <strong>{counts.rejected}</strong>
                        </article>
                    </section>

                    <section className="control-room-panel">
                        <div className="control-room-panel-header">
                            <div>
                                <h2>Recent Submissions</h2>
                                <p>
                                    Latest operational state from D1.
                                </p>
                            </div>

                            <button
                                type="button"
                                onClick={loadSubmissions}
                                disabled={loading}
                            >
                                {loading
                                    ? "Refreshing..."
                                    : "Refresh"}
                            </button>
                        </div>

                        {error && (
                            <p className="control-room-error">
                                {error}
                            </p>
                        )}

                        <div className="control-room-table-wrap">
                            <table className="control-room-table">
                                <thead>
                                    <tr>
                                        <th>Submission</th>
                                        <th>Status</th>
                                        <th>Validation</th>
                                        <th>Received</th>
                                        <th>Updated</th>
                                    </tr>
                                </thead>

                                <tbody>
                                    {submissions.map((submission) => (
                                        <tr
                                            key={
                                                submission.submission_id
                                            }
                                        >
                                            <td>
                                                <Link
                                                    className="control-room-submission-link"
                                                    to={`/admin/submissions/${submission.submission_id}`}
                                                >
                                                    <code>
                                                        {submission.submission_id}
                                                    </code>
                                                </Link>
                                            </td>

                                            <td>
                                                {submission.status}
                                            </td>

                                            <td>
                                                {
                                                    submission.validation_status ||
                                                    "—"
                                                }
                                            </td>

                                            <td>
                                                {formatDate(
                                                    submission.received_at,
                                                )}
                                            </td>

                                            <td>
                                                {formatDate(
                                                    submission.updated_at,
                                                )}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </section>
                </>
            )}
        </div>
    );
}

export default Admin;