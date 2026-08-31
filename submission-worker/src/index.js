const MAX_UPLOAD_BYTES = 10 * 1024 * 1024;

function jsonResponse(body, status = 200, extraHeaders = {}) {
	return new Response(JSON.stringify(body, null, 2), {
		status,
		headers: {
			"Content-Type": "application/json; charset=utf-8",
			...extraHeaders,
		},
	});
}

function createSubmissionId() {
	return `sub_${crypto.randomUUID()}`;
}

export default {
	async fetch(request, env) {
		const url = new URL(request.url);

		if (url.pathname !== "/v1/submissions") {
			return jsonResponse(
				{
					error: "not_found",
					message: "The requested endpoint does not exist.",
				},
				404,
			);
		}

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

		const contentType = request.headers.get("Content-Type");

		if (contentType !== "application/zip") {
			return jsonResponse(
				{
					error: "unsupported_media_type",
					message: "Submission uploads must use application/zip.",
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
						contentType:
							"application/zip",
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

		return jsonResponse(
			{
				submission_id: submissionId,
				status: "received",
			},
			201,
		);
	},
};