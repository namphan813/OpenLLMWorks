const MAX_UPLOAD_BYTES = 10 * 1024 * 1024;

const GITHUB_OWNER = "namphan813";
const GITHUB_REPOSITORY = "OpenLLMWorks";
const GITHUB_WORKFLOW = "validate-submission.yml";
const GITHUB_REF = "main";

const SUBMISSION_ID_PATTERN =
	/^sub_[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$/;

function jsonResponse(body, status = 200, extraHeaders = {}) {
	return new Response(JSON.stringify(body, null, 2), {
		status,
		headers: {
			"Content-Type": "application/json; charset=utf-8",
			...extraHeaders,
		},
	});
}

function adminCorsHeaders(request) {
        const origin = request.headers.get("Origin");

        const allowedOrigins = new Set([
                "http://localhost:5173",
                "https://openllmworks.com",
        ]);

        if (allowedOrigins.has(origin)) {
                return {
                        "Access-Control-Allow-Origin": origin,
                        "Access-Control-Allow-Credentials": "true",
                        "Access-Control-Allow-Headers": "Authorization, Content-Type",
                        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                        "Vary": "Origin",
                };
        }

        return {};
}

function createSubmissionId() {
	return `sub_${crypto.randomUUID()}`;
}

function isValidSubmissionId(submissionId) {
	return SUBMISSION_ID_PATTERN.test(submissionId);
}

async function recordSubmissionReceived(
	submissionId,
	objectKey,
	env,
) {
	if (!env.OPERATIONS_DB) {
		console.warn(
			"Submission operations state was not recorded because " +
				"OPERATIONS_DB is not configured.",
			{
				submissionId,
				objectKey,
			},
		);

		return false;
	}

	const receivedAt = new Date().toISOString();

	const eventDetails = JSON.stringify({
		object_key: objectKey,
		source: "direct_submission",
	});

	try {
		await env.OPERATIONS_DB.batch([
			env.OPERATIONS_DB
				.prepare(
					`
					INSERT INTO submissions (
						submission_id,
						status,
						object_key,
						received_at,
						updated_at
					)
					VALUES (?, 'received', ?, ?, ?)
					`,
				)
				.bind(
					submissionId,
					objectKey,
					receivedAt,
					receivedAt,
				),

			env.OPERATIONS_DB
				.prepare(
					`
					INSERT INTO submission_events (
						submission_id,
						event_type,
						actor,
						details
					)
					VALUES (?, 'received', 'submission_worker', ?)
					`,
				)
				.bind(
					submissionId,
					eventDetails,
				),
		]);

		console.log(
			"Submission operations state recorded.",
			{
				submissionId,
				status: "received",
				objectKey,
			},
		);

		return true;
	} catch (error) {
		console.error(
			"Submission operations state recording failed.",
			{
				submissionId,
				objectKey,
				error,
			},
		);

		return false;
	}
}

async function triggerValidation(submissionId, env) {
	if (!env.GITHUB_ACTIONS_TOKEN) {
		console.warn(
			"Automatic validation was not triggered because " +
				"GITHUB_ACTIONS_TOKEN is not configured.",
			{
				submissionId,
			},
		);

		return;
	}

	const workflowUrl =
		`https://api.github.com/repos/${GITHUB_OWNER}/` +
		`${GITHUB_REPOSITORY}/actions/workflows/` +
		`${GITHUB_WORKFLOW}/dispatches`;

	try {
		const response = await fetch(workflowUrl, {
			method: "POST",
			headers: {
				Authorization: `Bearer ${env.GITHUB_ACTIONS_TOKEN}`,
				Accept: "application/vnd.github+json",
				"Content-Type": "application/json",
				"User-Agent": "OpenLLMWorks-Submission-Worker",
				"X-GitHub-Api-Version": "2022-11-28",
			},
			body: JSON.stringify({
				ref: GITHUB_REF,
				inputs: {
					submission_id: submissionId,
					test_rejection: "false",
				},
			}),
		});

		if (!response.ok) {
			const responseText = await response.text();

			console.error(
				"Automatic validation trigger failed.",
				{
					submissionId,
					status: response.status,
					statusText: response.statusText,
					responseBody: responseText,
				},
			);

			return;
		}

		console.log(
			"Automatic validation requested.",
			{
				submissionId,
			},
		);
	} catch (error) {
		console.error(
			"Automatic validation trigger encountered an error.",
			{
				submissionId,
				error,
			},
		);
	}
}

async function handleValidationCallback(
	request,
	submissionId,
	env,
) {
	if (request.method !== "POST") {
		return jsonResponse(
			{
				error: "method_not_allowed",
				message: "This endpoint accepts POST requests only.",
			},
			405,
			{
				Allow: "POST",
			},
		);
	}

	if (!isValidSubmissionId(submissionId)) {
		return jsonResponse(
			{
				error: "invalid_submission_id",
				message: "The submission ID is invalid.",
			},
			400,
		);
	}

	if (!env.VALIDATION_CALLBACK_TOKEN) {
		console.error(
			"VALIDATION_CALLBACK_TOKEN is not configured.",
		);

		return jsonResponse(
			{
				error: "server_configuration_error",
				message:
					"Validation callback authentication is unavailable.",
			},
			500,
		);
	}

	const authorization =
		request.headers.get("Authorization");

	const expectedAuthorization =
		`Bearer ${env.VALIDATION_CALLBACK_TOKEN}`;

	if (authorization !== expectedAuthorization) {
		return jsonResponse(
			{
				error: "unauthorized",
				message: "Invalid validation callback credential.",
			},
			401,
		);
	}

	const contentType =
		request.headers.get("Content-Type") || "";

	if (
		!contentType
			.toLowerCase()
			.startsWith("application/json")
	) {
		return jsonResponse(
			{
				error: "unsupported_media_type",
				message:
					"Validation callbacks must use application/json.",
			},
			415,
		);
	}

	let payload;

	try {
		payload = await request.json();
	} catch {
		return jsonResponse(
			{
				error: "invalid_json",
				message: "The callback body is not valid JSON.",
			},
			400,
		);
	}

	const status = payload?.status;

	if (
		status !== "validating" &&
		status !== "validated" &&
		status !== "rejected"
	) {
		return jsonResponse(
			{
				error: "invalid_status",
				message:
					"Validation status must be validating, validated, or rejected.",
			},
			400,
		);
	}

	const existingSubmission =
		await env.OPERATIONS_DB
			.prepare(
				`
				SELECT submission_id
				FROM submissions
				WHERE submission_id = ?
				LIMIT 1
				`,
			)
			.bind(submissionId)
			.first();

	if (!existingSubmission) {
		return jsonResponse(
			{
				error: "submission_not_found",
				message:
					"The submission does not exist in the operations database.",
			},
			404,
		);
	}

	const now = new Date().toISOString();

	let validationStatus = null;
	let validationError = null;
	let eventType = status;

	if (status === "validated") {
		validationStatus = "passed";
	}

	if (status === "rejected") {
		validationStatus = "failed";
		validationError =
			typeof payload.validation_error === "string"
				? payload.validation_error.slice(0, 4000)
				: "Canonical validation failed.";
	}

	const eventDetails = JSON.stringify({
		source: "github_actions",
		validation_status: validationStatus,
		validation_error: validationError,
	});

	try {
		if (status === "validating") {
			await env.OPERATIONS_DB.batch([
				env.OPERATIONS_DB
					.prepare(
						`
						UPDATE submissions
						SET
							status = 'validating',
							validation_started_at =
								COALESCE(validation_started_at, ?),
							validation_status = NULL,
							validation_error = NULL,
							updated_at = ?
						WHERE submission_id = ?
						`,
					)
					.bind(
						now,
						now,
						submissionId,
					),

				env.OPERATIONS_DB
					.prepare(
						`
						INSERT INTO submission_events (
							submission_id,
							event_type,
							actor,
							details
						)
						VALUES (?, ?, 'github_actions', ?)
						`,
					)
					.bind(
						submissionId,
						eventType,
						eventDetails,
					),
			]);
		} else {
			await env.OPERATIONS_DB.batch([
				env.OPERATIONS_DB
					.prepare(
						`
						UPDATE submissions
						SET
							status = ?,
							validated_at = ?,
							validation_status = ?,
							validation_error = ?,
							updated_at = ?
						WHERE submission_id = ?
						`,
					)
					.bind(
						status,
						now,
						validationStatus,
						validationError,
						now,
						submissionId,
					),

				env.OPERATIONS_DB
					.prepare(
						`
						INSERT INTO submission_events (
							submission_id,
							event_type,
							actor,
							details
						)
						VALUES (?, ?, 'github_actions', ?)
						`,
					)
					.bind(
						submissionId,
						eventType,
						eventDetails,
					),
			]);
		}
	} catch (error) {
		console.error(
			"Validation state update failed.",
			{
				submissionId,
				status,
				error,
			},
		);

		return jsonResponse(
			{
				error: "operations_database_error",
				message:
					"The validation state could not be recorded.",
			},
			500,
		);
	}

	console.log(
		"Validation state recorded.",
		{
			submissionId,
			status,
			validationStatus,
		},
	);

	return jsonResponse(
		{
			submission_id: submissionId,
			status,
			validation_status: validationStatus,
		},
		200,
	);
}

async function requireControlRoomAccess(ctx) {
	if (!ctx?.access) {
		return {
			authorized: false,
			response: jsonResponse(
				{
					error: "unauthorized",
					message:
						"Cloudflare Access authentication is required.",
				},
				401,
			),
		};
	}

	try {
		const identity = await ctx.access.getIdentity();

		if (!identity) {
			return {
				authorized: false,
				response: jsonResponse(
					{
						error: "unauthorized",
						message:
							"Cloudflare Access identity is unavailable.",
					},
					401,
				),
			};
		}

		return {
			authorized: true,
			identity,
		};
	} catch (error) {
		console.error(
			"Control Room Access identity check failed.",
			{
				error,
			},
		);

		return {
			authorized: false,
			response: jsonResponse(
				{
					error: "unauthorized",
					message:
						"Cloudflare Access authentication could not be verified.",
				},
				401,
			),
		};
	}
}

async function handleAdminSubmissions(
	request,
	env,
	ctx,
) {
	if (request.method !== "GET") {
		return jsonResponse(
			{
				error: "method_not_allowed",
				message: "This endpoint accepts GET requests only.",
			},
			405,
			{
				Allow: "GET",
			},
		);
	}

	const access =
		await requireControlRoomAccess(ctx);

	if (!access.authorized) {
		return access.response;
	}

	try {
		const submissionsResult =
			await env.OPERATIONS_DB
				.prepare(
					`
					SELECT
						submission_id,
						status,
						object_key,
						received_at,
						validation_started_at,
						validated_at,
						validation_status,
						validation_error,
						updated_at
					FROM submissions
					ORDER BY received_at DESC
					LIMIT 100
					`,
				)
				.all();

		const countsResult =
			await env.OPERATIONS_DB
				.prepare(
					`
					SELECT
						status,
						COUNT(*) AS count
					FROM submissions
					GROUP BY status
					`,
				)
				.all();

		const counts = {
			total: 0,
			received: 0,
			validating: 0,
			validated: 0,
			rejected: 0,
		};

		for (const row of countsResult.results || []) {
			const count = Number(row.count) || 0;

			counts.total += count;

			if (
				Object.prototype.hasOwnProperty.call(
					counts,
					row.status,
				)
			) {
				counts[row.status] = count;
			}
		}

		return jsonResponse(
			{
				counts,
				submissions:
					submissionsResult.results || [],
			},
			200,
		);
	} catch (error) {
		console.error(
			"Control Room submissions query failed.",
			{
				error,
			},
		);

		return jsonResponse(
			{
				error: "operations_database_error",
				message:
					"Control Room submissions could not be loaded.",
			},
			500,
		);
	}
}

async function handleAdminSubmissionDetail(
	request,
	submissionId,
	env,
	ctx,
) {
	if (request.method !== "GET") {
		return jsonResponse(
			{
				error: "method_not_allowed",
				message: "This endpoint accepts GET requests only.",
			},
			405,
			{
				Allow: "GET",
			},
		);
	}

	const access =
		await requireControlRoomAccess(ctx);

	if (!access.authorized) {
		return access.response;
	}

	if (!isValidSubmissionId(submissionId)) {
		return jsonResponse(
			{
				error: "invalid_submission_id",
				message: "The submission ID is invalid.",
			},
			400,
		);
	}

	try {
		const submission =
			await env.OPERATIONS_DB
				.prepare(
					`
					SELECT
						submission_id,
						status,
						object_key,
						received_at,
						updated_at,
						validation_started_at,
						validated_at,
						validation_status,
						validation_error,
						reviewed_at,
						review_decision,
						imported_at,
						published_at,
						result_id,
						created_at
					FROM submissions
					WHERE submission_id = ?
					LIMIT 1
					`,
				)
				.bind(submissionId)
				.first();

		if (!submission) {
			return jsonResponse(
				{
					error: "submission_not_found",
					message:
						"The submission does not exist in the operations database.",
				},
				404,
			);
		}

		const eventsResult =
			await env.OPERATIONS_DB
				.prepare(
					`
					SELECT
						event_id,
						event_type,
						actor,
						details,
						created_at
					FROM submission_events
					WHERE submission_id = ?
					ORDER BY created_at ASC, event_id ASC
					`,
				)
				.bind(submissionId)
				.all();

		return jsonResponse(
			{
				submission,
				events:
					eventsResult.results || [],
			},
			200,
		);
	} catch (error) {
		console.error(
			"Control Room submission detail query failed.",
			{
				submissionId,
				error,
			},
		);

		return jsonResponse(
			{
				error: "operations_database_error",
				message:
					"Control Room submission details could not be loaded.",
			},
			500,
		);
	}
}

const REVIEW_DECLINE_REASON_CODES = new Set([
	"incomplete_evidence",
	"protocol_mismatch",
	"hardware_mismatch",
	"duplicate_submission",
	"suspicious_result",
	"unsupported_configuration",
	"other",
]);

async function handleAdminSubmissionReview(
	request,
	submissionId,
	env,
	ctx,
) {
	if (request.method !== "POST") {
		return jsonResponse(
			{
				error: "method_not_allowed",
				message: "This endpoint accepts POST requests only.",
			},
			405,
			{
				Allow: "POST",
			},
		);
	}

	const access =
		await requireControlRoomAccess(ctx);

	if (!access.authorized) {
		return access.response;
	}

	if (!isValidSubmissionId(submissionId)) {
		return jsonResponse(
			{
				error: "invalid_submission_id",
				message: "The submission ID is invalid.",
			},
			400,
		);
	}

	const contentType =
		request.headers.get("Content-Type") || "";

	if (
		!contentType
			.toLowerCase()
			.startsWith("application/json")
	) {
		return jsonResponse(
			{
				error: "unsupported_media_type",
				message:
					"Review requests must use application/json.",
			},
			415,
		);
	}

	let payload;

	try {
		payload = await request.json();
	} catch {
		return jsonResponse(
			{
				error: "invalid_json",
				message: "The review body is not valid JSON.",
			},
			400,
		);
	}

	const decision = payload?.decision;

	if (
		decision !== "approved" &&
		decision !== "declined"
	) {
		return jsonResponse(
			{
				error: "invalid_review_decision",
				message:
					"Review decision must be approved or declined.",
			},
			400,
		);
	}

	let reasonCode = null;
	let reasonDetail = null;

	if (decision === "declined") {
		reasonCode =
			typeof payload.reason_code === "string"
				? payload.reason_code.trim()
				: "";

		if (
			!REVIEW_DECLINE_REASON_CODES.has(
				reasonCode,
			)
		) {
			return jsonResponse(
				{
					error: "invalid_decline_reason",
					message:
						"A valid decline reason code is required.",
				},
				400,
			);
		}

		if (typeof payload.reason_detail === "string") {
			reasonDetail =
				payload.reason_detail
					.trim()
					.slice(0, 2000);

			if (reasonDetail === "") {
				reasonDetail = null;
			}
		}

		if (
			reasonCode === "other" &&
			!reasonDetail
		) {
			return jsonResponse(
				{
					error: "decline_detail_required",
					message:
						"Additional details are required when the decline reason is other.",
				},
				400,
			);
		}
	}

	let submission;

	try {
		submission =
			await env.OPERATIONS_DB
				.prepare(
					`
					SELECT
						submission_id,
						status,
						validation_status,
						review_decision
					FROM submissions
					WHERE submission_id = ?
					LIMIT 1
					`,
				)
				.bind(submissionId)
				.first();
	} catch (error) {
		console.error("Control Room review lookup failed.", {
			submissionId,
			error,
		});

		return jsonResponse(
			{
				error: "operations_database_error",
				message:
					"The submission review state could not be loaded.",
			},
			500,
		);
	}

	if (!submission) {
		return jsonResponse(
			{
				error: "submission_not_found",
				message:
					"The submission does not exist in the operations database.",
			},
			404,
		);
	}

	if (submission.review_decision) {
		return jsonResponse(
			{
				error: "submission_already_reviewed",
				message:
					"This submission already has a review decision.",
				review_decision:
					submission.review_decision,
			},
			409,
		);
	}

	if (
		submission.status !== "validated" ||
		submission.validation_status !== "passed"
	) {
		return jsonResponse(
			{
				error: "submission_not_reviewable",
				message:
					"Only validated submissions with passed validation can be reviewed.",
				status: submission.status,
				validation_status:
					submission.validation_status,
			},
			409,
		);
	}

	const now = new Date().toISOString();

	const eventDetails = JSON.stringify({
		source: "control_room",
		decision,
		reason_code: reasonCode,
		reason_detail: reasonDetail,
	});

	try {
		await env.OPERATIONS_DB.batch([
			env.OPERATIONS_DB
				.prepare(
					`
					UPDATE submissions
					SET
						status = ?,
						review_decision = ?,
						reviewed_at = ?,
						updated_at = ?
					WHERE submission_id = ?
					`,
				)
				.bind(
					decision,
					decision,
					now,
					now,
					submissionId,
				),

			env.OPERATIONS_DB
				.prepare(
					`
					INSERT INTO submission_events (
						submission_id,
						event_type,
						actor,
						details
					)
					VALUES (?, ?, 'maintainer', ?)
					`,
				)
				.bind(
					submissionId,
					decision,
					eventDetails,
				),
		]);
	} catch (error) {
		console.error("Control Room review update failed.", {
			submissionId,
			decision,
			error,
		});

		return jsonResponse(
			{
				error: "operations_database_error",
				message:
					"The review decision could not be recorded.",
			},
			500,
		);
	}

	return jsonResponse(
		{
			submission_id: submissionId,
			status: decision,
			review_decision: decision,
			reviewed_at: now,
		},
		200,
	);
}

async function handleSubmissionUpload(
	request,
	env,
	ctx,
) {
	if (request.method !== "POST") {
		return jsonResponse(
			{
				error: "method_not_allowed",
				message: "This endpoint accepts POST requests only.",
			},
			405,
			{
				Allow: "POST",
			},
		);
	}

	const contentType =
		request.headers.get("Content-Type");

	if (contentType !== "application/zip") {
		return jsonResponse(
			{
				error: "unsupported_media_type",
				message:
					"Submission uploads must use application/zip.",
			},
			415,
		);
	}

	const contentLengthHeader =
		request.headers.get("Content-Length");

	if (contentLengthHeader !== null) {
		const contentLength =
			Number(contentLengthHeader);

		if (
			!Number.isFinite(contentLength) ||
			contentLength <= 0
		) {
			return jsonResponse(
				{
					error: "invalid_request",
					message:
						"The submission upload has an invalid Content-Length.",
				},
				400,
			);
		}

		if (contentLength > MAX_UPLOAD_BYTES) {
			return jsonResponse(
				{
					error: "payload_too_large",
					message:
						"The submission ZIP exceeds the maximum allowed size.",
				},
				413,
			);
		}
	}

	if (request.body === null) {
		return jsonResponse(
			{
				error: "invalid_request",
				message: "The submission upload is empty.",
			},
			400,
		);
	}

	const submissionId =
		createSubmissionId();

	const objectKey =
		`incoming/${submissionId}.zip`;

	try {
		await env.SUBMISSIONS_BUCKET.put(
			objectKey,
			request.body,
			{
				httpMetadata: {
					contentType: "application/zip",
				},
				customMetadata: {
					submissionId,
					status: "received",
				},
			},
		);
	} catch (error) {
		console.error(
			"Submission storage failed:",
			error,
		);

		return jsonResponse(
			{
				error: "storage_error",
				message:
					"The submission could not be stored.",
			},
			500,
		);
	}

	await recordSubmissionReceived(
		submissionId,
		objectKey,
		env,
	);

	ctx.waitUntil(
		triggerValidation(
			submissionId,
			env,
		),
	);

	return jsonResponse(
		{
			submission_id: submissionId,
			status: "received",
		},
		201,
	);
}

export default {
	async fetch(request, env, ctx) {
		const url = new URL(request.url);

		if (url.pathname === "/v1/submissions") {
			return handleSubmissionUpload(
				request,
				env,
				ctx,
			);
		}

		const adminPathParts =
			url.pathname.split("/");

		const isAdminSubmissionsRoute =
			url.pathname === "/v1/admin/submissions";

		const isAdminSubmissionReviewRoute =
			adminPathParts.length === 6 &&
			adminPathParts[1] === "v1" &&
			adminPathParts[2] === "admin" &&
			adminPathParts[3] === "submissions" &&
			adminPathParts[4] !== "" &&
			adminPathParts[5] === "review";

		const isAdminSubmissionDetailRoute =
			adminPathParts.length === 5 &&
			adminPathParts[1] === "v1" &&
			adminPathParts[2] === "admin" &&
			adminPathParts[3] === "submissions" &&
			adminPathParts[4] !== "";

		if (
			isAdminSubmissionsRoute ||
			isAdminSubmissionDetailRoute ||
			isAdminSubmissionReviewRoute
		) {
			const corsHeaders =
				adminCorsHeaders(request);

			if (request.method === "OPTIONS") {
				return new Response(null, {
					status: 204,
					headers: corsHeaders,
				});
			}

			let response;

			if (isAdminSubmissionReviewRoute) {
				response =
					await handleAdminSubmissionReview(
						request,
						adminPathParts[4],
						env,
						ctx,
					);
			} else if (
				isAdminSubmissionDetailRoute
			) {
				response =
					await handleAdminSubmissionDetail(
						request,
						adminPathParts[4],
						env,
						ctx,
					);
			} else {
				response =
					await handleAdminSubmissions(
						request,
						env,
						ctx,
					);
			}


			const headers =
				new Headers(response.headers);

			for (
				const [name, value] of
					Object.entries(corsHeaders)
			) {
				headers.set(name, value);
			}

			return new Response(
				response.body,
				{
					status: response.status,
					statusText: response.statusText,
					headers,
				},
			);
		}

        const pathParts = url.pathname.split("/");

        const isValidationRoute =
            pathParts.length === 5 &&
            pathParts[1] === "v1" &&
            pathParts[2] === "submissions" &&
            pathParts[4] === "validation";

        if (isValidationRoute) {
            return handleValidationCallback(
                request,
                pathParts[3],
                env,
            );
        }

		return jsonResponse(
			{
				error: "not_found",
				message:
					"The requested endpoint does not exist.",
			},
			404,
		);
	},
};
