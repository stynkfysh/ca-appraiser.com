// Cloudflare Pages Function — CA-Appraiser.com contact form handler.
// POSTs the form, emails the lead via Resend, then redirects back with a status.
// Env vars (set in Cloudflare Pages → Settings → Environment variables):
//   RESEND_API_KEY  — Resend API key
//   RESEND_FROM     — verified sender, e.g. "CA-Appraiser <noreply@brianward.com>"
//   RESEND_TO       — destination inbox, e.g. "brian@brianward.com"

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

  const fullAddress = [streetAddress, city, zipcode].filter(Boolean).join(", ");

  if (!name || !email || !appraisalPurpose) {
    return Response.redirect(new URL("/contact?status=error", request.url), 303);
  }

  const emailBody = `
New Appraisal Inquiry from CA-Appraiser.com

Name: ${name}
Email: ${email}
Phone: ${phone || "Not provided"}
Property Address: ${fullAddress || "Not provided"}
Appraisal Purpose: ${appraisalPurpose}
Appraisal Type: ${appraisalType || "Not selected"}
Message: ${message || "None"}
  `.trim();

  const htmlBody = `
<h2>New Appraisal Inquiry — CA-Appraiser.com</h2>
<table style="border-collapse:collapse;font-family:Arial,sans-serif;">
  <tr><td style="padding:6px 12px;font-weight:bold;">Name</td><td style="padding:6px 12px;">${escapeHtml(name)}</td></tr>
  <tr><td style="padding:6px 12px;font-weight:bold;">Email</td><td style="padding:6px 12px;"><a href="mailto:${escapeHtml(email)}">${escapeHtml(email)}</a></td></tr>
  <tr><td style="padding:6px 12px;font-weight:bold;">Phone</td><td style="padding:6px 12px;">${escapeHtml(phone || "Not provided")}</td></tr>
  <tr><td style="padding:6px 12px;font-weight:bold;">Property Address</td><td style="padding:6px 12px;">${escapeHtml(fullAddress || "Not provided")}</td></tr>
  <tr><td style="padding:6px 12px;font-weight:bold;">Appraisal Purpose</td><td style="padding:6px 12px;">${escapeHtml(appraisalPurpose)}</td></tr>
  <tr><td style="padding:6px 12px;font-weight:bold;">Appraisal Type</td><td style="padding:6px 12px;">${escapeHtml(appraisalType || "Not selected")}</td></tr>
  <tr><td style="padding:6px 12px;font-weight:bold;">Message</td><td style="padding:6px 12px;">${escapeHtml(message || "None")}</td></tr>
</table>
  `.trim();

  try {
    const res = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${env.RESEND_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: env.RESEND_FROM || "CA-Appraiser.com <noreply@date-of-death.com>",
        to: [env.RESEND_TO || "contact@ca-appraiser.com"],
        reply_to: email,
        subject: `New Appraisal Inquiry – ${appraisalPurpose} – ${name}`,
        text: emailBody,
        html: htmlBody,
      }),
    });

    if (!res.ok) {
      const err = await res.text();
      console.error("Resend error:", err);
      return Response.redirect(new URL("/contact?status=error", request.url), 303);
    }

    return Response.redirect(new URL("/contact?status=success", request.url), 303);
  } catch (err) {
    console.error("Send failed:", err);
    return Response.redirect(new URL("/contact?status=error", request.url), 303);
  }
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
