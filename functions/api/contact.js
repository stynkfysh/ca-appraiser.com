// Contact endpoint for ca-appraiser.com (same handler as brianward.com).
// (temecula.pro, carlsbadappraiser.pro, sanmarcos.pro, sandiegoappraiser.pro,
//  chula-vista.pro, ocvaluepro.com, riverside-appraiser.com, bw-r.com, ...).
//
// Every sister site posts here with a hidden `source` field identifying itself.
// Two things this endpoint guarantees:
//   1. Brian's notification always says which website the submission came from.
//   2. The submitter always gets an automatic confirmation email back.
//
// Env: RESEND_API_KEY, RESEND_FROM, RESEND_TO

// Domains allowed to post here and be redirected back to.
const ALLOWED_RETURN_HOSTS = [
  "brianward.com",
  "www.brianward.com",
  "temecula.pro",
  "www.temecula.pro",
  "carlsbadappraiser.pro",
  "www.carlsbadappraiser.pro",
  "sanmarcos.pro",
  "www.sanmarcos.pro",
  "sandiegoappraiser.pro",
  "www.sandiegoappraiser.pro",
  "chula-vista.pro",
  "www.chula-vista.pro",
  "ocvaluepro.com",
  "www.ocvaluepro.com",
  "riverside-appraiser.com",
  "www.riverside-appraiser.com",
  "palm-springs-appraiser.com",
  "www.palm-springs-appraiser.com",
  "bw-r.com",
  "www.bw-r.com",
  "ca-appraiser.com",
  "www.ca-appraiser.com",
];

// Send the visitor back to the site they actually submitted from, not to
// brianward.com. Falls back to brianward.com if the origin is unrecognized.
function buildReturnUrl(request, status) {
  const candidate =
    request.headers.get("Origin") || request.headers.get("Referer") || "";
  try {
    const u = new URL(candidate);
    if (ALLOWED_RETURN_HOSTS.includes(u.hostname)) {
      return `${u.origin}/contact?status=${status}`;
    }
  } catch (e) {
    // fall through
  }
  return new URL(`/contact?status=${status}`, request.url).toString();
}

export async function onRequestPost(context) {
  const { request, env } = context;

  const formData = await request.formData();
  const name = formData.get("name") || "";
  const email = formData.get("email") || "";
  const phone = formData.get("phone") || "";
  const streetAddress = formData.get("street-address") || "";
  const city = formData.get("city") || "";
  const zipcode = formData.get("zipcode") || "";
  const appraisalPurpose = formData.get("appraisal-purpose") || "";
  const appraisalType = formData.get("appraisal-type") || "";
  const message = formData.get("message") || "";
  const honeypot = formData.get("website") || "";

  // Prefer the form's declared source; fall back to the actual request origin
  // so a site that forgot its hidden field is still identified correctly.
  let source = formData.get("source") || "";
  if (!source) {
    try {
      const originHost = new URL(
        request.headers.get("Origin") || request.headers.get("Referer") || ""
      ).hostname;
      source = originHost.replace(/^www\./, "") || "ca-appraiser.com";
    } catch (e) {
      source = "ca-appraiser.com";
    }
  }

  const fullAddress = [streetAddress, city, zipcode].filter(Boolean).join(", ");

  // Silently accept-and-drop obvious bots.
  if (honeypot) {
    return Response.redirect(buildReturnUrl(request, "success"), 303);
  }

  if (!name || !email || !appraisalPurpose) {
    return Response.redirect(buildReturnUrl(request, "error"), 303);
  }

  const emailBody = `
New Appraisal Inquiry

SUBMITTED FROM WEBSITE: ${source}

Name: ${name}
Email: ${email}
Phone: ${phone || "Not provided"}
Property Address: ${fullAddress || "Not provided"}
Appraisal Purpose: ${appraisalPurpose}
Appraisal Type: ${appraisalType || "Not selected"}
Message: ${message || "None"}
  `.trim();

  const htmlBody = `
<h2>New Appraisal Inquiry</h2>
<p style="font-size:15px;background:#1a5276;color:#fff;padding:10px 14px;border-radius:4px;font-family:Arial,sans-serif;margin:0 0 14px;">
  Submitted from website: <strong>${escapeHtml(source)}</strong>
</p>
<table style="border-collapse:collapse;font-family:Arial,sans-serif;">
  <tr style="background:#f5f5f5;"><td style="padding:6px 12px;font-weight:bold;">Source Website</td><td style="padding:6px 12px;">${escapeHtml(source)}</td></tr>
  <tr><td style="padding:6px 12px;font-weight:bold;">Name</td><td style="padding:6px 12px;">${escapeHtml(name)}</td></tr>
  <tr style="background:#f5f5f5;"><td style="padding:6px 12px;font-weight:bold;">Email</td><td style="padding:6px 12px;"><a href="mailto:${escapeHtml(email)}">${escapeHtml(email)}</a></td></tr>
  <tr><td style="padding:6px 12px;font-weight:bold;">Phone</td><td style="padding:6px 12px;">${escapeHtml(phone || "Not provided")}</td></tr>
  <tr style="background:#f5f5f5;"><td style="padding:6px 12px;font-weight:bold;">Property Address</td><td style="padding:6px 12px;">${escapeHtml(fullAddress || "Not provided")}</td></tr>
  <tr><td style="padding:6px 12px;font-weight:bold;">Appraisal Purpose</td><td style="padding:6px 12px;">${escapeHtml(appraisalPurpose)}</td></tr>
  <tr style="background:#f5f5f5;"><td style="padding:6px 12px;font-weight:bold;">Appraisal Type</td><td style="padding:6px 12px;">${escapeHtml(appraisalType || "Not selected")}</td></tr>
  <tr><td style="padding:6px 12px;font-weight:bold;">Message</td><td style="padding:6px 12px;">${escapeHtml(message || "None")}</td></tr>
</table>
  `.trim();

  const fromAddress =
    env.RESEND_FROM || "CA-Appraiser <noreply@brianward.com>";

  try {
    const res = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${env.RESEND_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: fromAddress,
        to: [env.RESEND_TO || "brian@brianward.com"],
        reply_to: email,
        subject: `[${source}] New Appraisal Inquiry – ${appraisalPurpose} – ${name}`,
        text: emailBody,
        html: htmlBody,
      }),
    });

    if (!res.ok) {
      const err = await res.text();
      console.error("Resend error:", err);
      return Response.redirect(buildReturnUrl(request, "error"), 303);
    }
  } catch (err) {
    console.error("Send failed:", err);
    return Response.redirect(buildReturnUrl(request, "error"), 303);
  }

  // Confirmation to the person who submitted. Deliberately after the
  // notification and never fatal: if this fails, the inquiry still succeeded.
  try {
    await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${env.RESEND_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: fromAddress,
        to: [email],
        reply_to: "brian@brianward.com",
        subject: `We received your appraisal inquiry — ${source}`,
        text: buildAutoReplyText({
          name,
          email,
          phone,
          fullAddress,
          appraisalPurpose,
          appraisalType,
          message,
          source,
        }),
        html: buildAutoReplyHtml({
          name,
          email,
          phone,
          fullAddress,
          appraisalPurpose,
          appraisalType,
          message,
          source,
        }),
      }),
    });
  } catch (err) {
    console.error("Auto-reply failed (inquiry still received):", err);
  }

  return Response.redirect(buildReturnUrl(request, "success"), 303);
}

function buildAutoReplyText(d) {
  return `
Hi ${d.name},

Thank you for contacting Brian Ward Appraisal through ${d.source}. Your inquiry
has been received.

Brian will get back to you within 24 business hours. If your matter is
time-sensitive, you can reply directly to this email or call (858) 215-1553.

WHAT YOU SENT US
Name: ${d.name}
Email: ${d.email}
Phone: ${d.phone || "Not provided"}
Property Address: ${d.fullAddress || "Not provided"}
Appraisal Purpose: ${d.appraisalPurpose}
Appraisal Type: ${d.appraisalType || "Not selected"}
Message: ${d.message || "None"}

Thank you,
Brian Ward
California Certified Residential Real Estate Appraiser
License No. AR036053

This is an automatic confirmation that your submission on ${d.source} was
received. You do not need to submit the form again.
  `.trim();
}

function buildAutoReplyHtml(d) {
  const row = (label, value) =>
    value
      ? `<tr><td style="padding:6px 12px;font-weight:600;width:150px;vertical-align:top;">${escapeHtml(
          label
        )}</td><td style="padding:6px 12px;">${escapeHtml(value)}</td></tr>`
      : "";

  return `<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;max-width:600px;margin:0 auto;padding:20px;color:#333;">
  <h2 style="color:#1a5276;border-bottom:2px solid #1a5276;padding-bottom:10px;">We received your inquiry</h2>

  <p>Hi ${escapeHtml(d.name)},</p>

  <p>Thank you for contacting Brian Ward Appraisal through <strong>${escapeHtml(
    d.source
  )}</strong>. Your inquiry has been received.</p>

  <p>Brian will get back to you within <strong>24 business hours</strong>. If your matter is time-sensitive, you can reply directly to this email or call <strong>(858) 215-1553</strong>.</p>

  <h3 style="color:#555;margin-top:24px;">What you sent us</h3>
  <table style="width:100%;border-collapse:collapse;background:#f9f9f9;border-radius:6px;">
    ${row("Name", d.name)}
    ${row("Email", d.email)}
    ${row("Phone", d.phone)}
    ${row("Property Address", d.fullAddress)}
    ${row("Appraisal Purpose", d.appraisalPurpose)}
    ${row("Appraisal Type", d.appraisalType)}
    ${row("Message", d.message)}
  </table>

  <p style="margin-top:24px;">Thank you,<br>
  <strong>Brian Ward</strong><br>
  California Certified Residential Real Estate Appraiser<br>
  License No. AR036053</p>

  <p style="margin-top:30px;padding-top:16px;border-top:1px solid #ddd;font-size:13px;color:#888;">
    This is an automatic confirmation that your submission on ${escapeHtml(
      d.source
    )} was received. You do not need to submit the form again.
  </p>
</body>
</html>`;
}

function escapeHtml(str) {
  return String(str == null ? "" : str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
