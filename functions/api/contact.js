// Contact endpoint for ca-appraiser.com.
//
// Layered spam defence: honeypot, HMAC form token, dwell time and content
// scoring. Only CLEAN submissions trigger the confirmation auto-reply.

const ALLOWED_RETURN_HOSTS = [
  "brianward.com", "www.brianward.com",
  "temecula.pro", "www.temecula.pro",
  "carlsbadappraiser.pro", "www.carlsbadappraiser.pro",
  "sanmarcos.pro", "www.sanmarcos.pro",
  "sandiegoappraiser.pro", "www.sandiegoappraiser.pro",
  "chula-vista.pro", "www.chula-vista.pro",
  "ocvaluepro.com", "www.ocvaluepro.com",
  "riverside-appraiser.com", "www.riverside-appraiser.com",
  "palm-springs-appraiser.com", "www.palm-springs-appraiser.com",
  "bw-r.com", "www.bw-r.com",
  "ca-appraiser.com", "www.ca-appraiser.com",
  "palmdesertappraiser.com", "www.palmdesertappraiser.com",
];

const DEFAULT_SOURCE = "ca-appraiser.com";
const DEFAULT_FROM = "CA-Appraiser <contact@brianward.com>";
const DEFAULT_TO = "brian@brianward.com";

// ---------------------------------------------------------------------------
// Spam scoring. Shared by every Brian Ward site's contact endpoint.
//
// Design rule: a real lead must never be silently lost. Scores land in three
// bands -- deliver, deliver-but-flag, drop -- and only overwhelming evidence
// reaches the drop band. Anything uncertain is still delivered, just marked.
//
// The auto-reply is gated on the CLEAN band only. Spammers submit harvested
// third-party addresses, so replying to an unverified submission means mailing
// strangers on the attacker's behalf and burning the sending domain.
// ---------------------------------------------------------------------------

const CLEAN = 'clean';
const SUSPECT = 'suspect';
const SPAM = 'spam';

const DROP_AT = 90;
const FLAG_AT = 50;

// Free-mail domains heavily used by form-spam tooling.
const BAD_EMAIL_DOMAINS = [
  'bk.ru', 'mail.ru', 'list.ru', 'inbox.ru', 'rambler.ru', 'yandex.ru',
  'internet.ru', 'bigpind.com', 'outllook.com',
];

// Placeholder locality tokens seen across this campaign.
const JUNK_PLACES = [
  'leo', 'tro', 'mtskheta', 'lilongwe', 'porsgrunn', 'shekhupura',
  'lac la biche', 'tbilisi', 'kralupy', 'gujranwala',
];

const VALID_PURPOSES = [
  'bankruptcy', 'date-of-death', 'divorce', 'estate', 'tax', 'before-buying',
  'before-selling', 'family-transaction', 'insurance-dispute', 'pmi-removal',
  'bonds', 'other',
];

function scoreSubmission(f) {
  const reasons = [];
  let score = 0;
  const add = (n, why) => { score += n; reasons.push(`${why} (+${n})`); };

  const name = (f.name || '').trim();
  const email = (f.email || '').trim();
  const phone = (f.phone || '').trim();
  const street = (f.street || '').trim();
  const city = (f.city || '').trim();
  const zip = (f.zip || '').trim();
  const message = (f.message || '').trim();
  const purpose = (f.purpose || '').trim();
  const all = [name, email, phone, street, city, zip, message].join(' ');

  // --- Hard signal: only an automated client fills a hidden field ---
  if (f.honeypot) add(100, 'hidden honeypot field was filled');

  // --- Cloudflare Turnstile (skipped entirely when not configured) ---
  if (f.turnstile === 'failed') add(60, 'failed Cloudflare Turnstile');
  if (f.turnstile === 'passed') {
    // Strong proof of a real browser and a real person.
    score -= 40;
    reasons.push('passed Cloudflare Turnstile (-40)');
  }

  // --- Proof the submission came from a real page load ---
  // Deliberately NOT stacked on top of a Turnstile failure. Both the token
  // and the Turnstile widget depend on JavaScript, so a visitor with scripts
  // blocked fails both at once. Charging for both would push an ordinary
  // client over the drop threshold on a single underlying cause and lose a
  // real lead. Counted only when Turnstile has not already spoken.
  if (!f.tokenValid && f.turnstile !== 'passed' && f.turnstile !== 'failed') {
    add(40, 'no valid form token (posted directly to the API)');
  }
  if (f.dwellMs != null && f.dwellMs < 3000) add(40, 'submitted under 3s after page load');

  // --- Non-Latin script in a California appraisal form ---
  if (/[Ѐ-ӿ؀-ۿ一-鿿]/.test(all)) add(50, 'non-Latin script');

  // --- Contact details ---
  const digits = phone.replace(/\D/g, '');
  if (digits.length === 11 && digits[0] !== '1') add(35, 'phone is 11 digits not starting with 1');
  else if (digits.length > 11) add(25, 'phone has more than 11 digits');

  const domain = (email.split('@')[1] || '').toLowerCase();
  if (BAD_EMAIL_DOMAINS.includes(domain)) add(40, `email domain ${domain}`);

  if (name && !/\s/.test(name) && name.length >= 8) add(25, 'single-token name');

  // --- Address plausibility ---
  if (street && city && street.toLowerCase() === city.toLowerCase()) {
    add(30, 'street and city are identical');
  }
  if (street && !/\d/.test(street)) add(25, 'street address contains no number');
  if (JUNK_PLACES.includes(city.toLowerCase()) || JUNK_PLACES.includes(street.toLowerCase())) {
    add(30, 'known placeholder locality');
  }
  if (zip && !/^\d{5}(-\d{4})?$/.test(zip)) add(20, 'zip is not a US 5-digit code');

  // --- Payload ---
  if (/https?:\/\/|www\.|\[url|\[link|<a\s/i.test(message)) add(35, 'message contains a link');
  if (purpose && !VALID_PURPOSES.includes(purpose.toLowerCase().replace(/\s+/g, '-'))) {
    add(20, 'appraisal purpose is not one of the form options');
  }

  if (score < 0) score = 0;

  let verdict = CLEAN;
  if (score >= DROP_AT) verdict = SPAM;
  else if (score >= FLAG_AT) verdict = SUSPECT;

  return { score, verdict, reasons };
}

// --- Cloudflare Turnstile -------------------------------------------------
// Free, unlimited. Managed mode: real visitors normally see a brief self-
// resolving box and never click anything.
//
// Two deliberate design choices:
//
// 1. DORMANT UNTIL CONFIGURED. With no TURNSTILE_SECRET_KEY set, this is a
//    no-op and scoring behaves exactly as before. Deploying the code cannot
//    break a form before the keys exist.
//
// 2. FAILURE IS SCORED, NOT FATAL. A failed or missing Turnstile token adds
//    weight rather than hard-rejecting, so a real client on a flaky network or
//    with a blocked third-party script still reaches Brian, flagged. Losing a
//    genuine estate lead costs far more than glancing at a flagged one.
//
// Two secrets are supported because the free plan caps a widget at 10
// hostnames and the brianward.com endpoint serves more than that across the
// market-area sites.

async function verifyTurnstile(token, ip, env) {
  const secrets = [env.TURNSTILE_SECRET_KEY, env.TURNSTILE_SECRET_KEY_2].filter(Boolean);
  if (!secrets.length) return 'unconfigured';
  if (!token) return 'failed';

  for (const secret of secrets) {
    try {
      const body = new FormData();
      body.append('secret', secret);
      body.append('response', token);
      if (ip) body.append('remoteip', ip);
      const r = await fetch(
        'https://challenges.cloudflare.com/turnstile/v0/siteverify',
        { method: 'POST', body }
      );
      const d = await r.json();
      if (d.success) return 'passed';
    } catch (e) {
      // Network trouble reaching Cloudflare must not decide the outcome.
      console.error('Turnstile verify error:', e.message);
      return 'unconfigured';
    }
  }
  return 'failed';
}

// --- Form token: proves a real browser loaded the page before submitting ----
// HMAC-signed timestamp. Bots that POST straight at the endpoint have none.

async function hmac(secret, data) {
  const key = await crypto.subtle.importKey(
    'raw', new TextEncoder().encode(secret),
    { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']
  );
  const sig = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(data));
  return [...new Uint8Array(sig)].map(b => b.toString(16).padStart(2, '0')).join('');
}

function formSecret(env) {
  return env.FORM_SECRET || env.RESEND_API_KEY || 'fallback-secret';
}

async function issueToken(env) {
  const ts = Date.now();
  const nonce = crypto.randomUUID();
  const sig = await hmac(formSecret(env), `${ts}.${nonce}`);
  return `${ts}.${nonce}.${sig}`;
}

// Returns { valid, dwellMs }
async function verifyToken(token, env) {
  if (!token || typeof token !== 'string') return { valid: false, dwellMs: null };
  const parts = token.split('.');
  if (parts.length !== 3) return { valid: false, dwellMs: null };
  const [ts, nonce, sig] = parts;
  const expected = await hmac(formSecret(env), `${ts}.${nonce}`);
  if (sig !== expected) return { valid: false, dwellMs: null };
  const age = Date.now() - Number(ts);
  if (!(age >= 0 && age < 7200000)) return { valid: false, dwellMs: age };
  return { valid: true, dwellMs: age };
}

// ---------------------------------------------------------------------------
// Request handling
// ---------------------------------------------------------------------------

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

async function sendMail(env, payload) {
  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${env.RESEND_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(await res.text());
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

  // Honeypots: hidden inputs no human ever sees, let alone fills.
  const honeypot =
    formData.get("website") || formData.get("company_url") || formData.get("fax") || "";

  let source = formData.get("source") || "";
  if (!source) {
    try {
      const originHost = new URL(
        request.headers.get("Origin") || request.headers.get("Referer") || ""
      ).hostname;
      source = originHost.replace(/^www\./, "") || DEFAULT_SOURCE;
    } catch (e) {
      source = DEFAULT_SOURCE;
    }
  }

  const fullAddress = [streetAddress, city, zipcode].filter(Boolean).join(", ");

  if (!name || !email || !appraisalPurpose) {
    return Response.redirect(buildReturnUrl(request, "error"), 303);
  }

  const turnstile = await verifyTurnstile(
    formData.get('cf-turnstile-response'),
    request.headers.get('CF-Connecting-IP'),
    env
  );

  const { valid: tokenValid, dwellMs } = await verifyToken(
    formData.get("form_token"),
    env
  );

  const { score, verdict, reasons } = scoreSubmission({
    name, email, phone,
    street: streetAddress, city, zip: zipcode,
    message, purpose: appraisalPurpose,
    honeypot, tokenValid, dwellMs, turnstile,
  });

  // --- SPAM: drop without sending anything. No notification, no auto-reply,
  // no Resend credit consumed. The bot still gets a success page so it has no
  // signal to adapt against.
  if (verdict === SPAM) {
    console.log(
      JSON.stringify({ blocked: true, source, name, email, score, reasons })
    );
    return Response.redirect(buildReturnUrl(request, "success"), 303);
  }

  const flagged = verdict === SUSPECT;

  const emailBody = `
New Appraisal Inquiry${flagged ? " [POSSIBLE SPAM]" : ""}

SUBMITTED FROM WEBSITE: ${source}
${flagged ? `\nFLAGGED AS POSSIBLE SPAM (score ${score}): ${reasons.join("; ")}\n` : ""}
Name: ${name}
Email: ${email}
Phone: ${phone || "Not provided"}
Property Address: ${fullAddress || "Not provided"}
Appraisal Purpose: ${appraisalPurpose}
Appraisal Type: ${appraisalType || "Not selected"}
Message: ${message || "None"}
  `.trim();

  const flagBanner = flagged
    ? `<p style="font-size:14px;background:#fbe9e7;border:1px solid #d32f2f;color:#c62828;padding:10px 14px;border-radius:4px;font-family:Arial,sans-serif;margin:0 0 14px;">
  <strong>Possible spam (score ${score}).</strong> Delivered so you can judge it yourself. No confirmation email was sent to the submitter.<br>
  <span style="font-size:12px;">${escapeHtml(reasons.join("; "))}</span>
</p>`
    : "";

  const htmlBody = `
<h2>New Appraisal Inquiry</h2>
${flagBanner}
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
    env.RESEND_FROM || DEFAULT_FROM;

  try {
    await sendMail(env, {
      from: fromAddress,
      to: [env.RESEND_TO || DEFAULT_TO],
      reply_to: email,
      subject: `${flagged ? "[POSSIBLE SPAM] " : ""}[${source}] New Appraisal Inquiry – ${appraisalPurpose} – ${name}`,
      text: emailBody,
      html: htmlBody,
    });
  } catch (err) {
    console.error("Resend error:", err.message);
    return Response.redirect(buildReturnUrl(request, "error"), 303);
  }

  // --- Auto-reply ONLY for clean submissions.
  // Spam uses harvested third-party addresses; replying to an unverified
  // submission means mailing strangers on the spammer's behalf, burning both
  // Resend credit and the sending domain's reputation.
  if (verdict === CLEAN) {
    try {
      await sendMail(env, {
        from: fromAddress,
        to: [email],
        reply_to: "brian@brianward.com",
        subject: `We received your appraisal inquiry — ${source}`,
        text: buildAutoReplyText({
          name, email, phone, fullAddress, appraisalPurpose, appraisalType, message, source,
        }),
        html: buildAutoReplyHtml({
          name, email, phone, fullAddress, appraisalPurpose, appraisalType, message, source,
        }),
      });
    } catch (err) {
      console.error("Auto-reply failed (inquiry still received):", err.message);
    }
  }

  return Response.redirect(buildReturnUrl(request, "success"), 303);
}

export async function onRequestOptions(context) {
  const origin = context.request.headers.get("Origin") || "";
  let allow = "https://www.brianward.com";
  try {
    const u = new URL(origin);
    if (ALLOWED_RETURN_HOSTS.includes(u.hostname)) allow = u.origin;
  } catch (e) { /* default */ }
  return new Response(null, {
    headers: {
      "Access-Control-Allow-Origin": allow,
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    },
  });
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
      ? `<tr><td style="padding:6px 12px;font-weight:600;width:150px;vertical-align:top;">${escapeHtml(label)}</td><td style="padding:6px 12px;">${escapeHtml(value)}</td></tr>`
      : "";

  return `<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;max-width:600px;margin:0 auto;padding:20px;color:#333;">
  <h2 style="color:#1a5276;border-bottom:2px solid #1a5276;padding-bottom:10px;">We received your inquiry</h2>

  <p>Hi ${escapeHtml(d.name)},</p>

  <p>Thank you for contacting Brian Ward Appraisal through <strong>${escapeHtml(d.source)}</strong>. Your inquiry has been received.</p>

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
    This is an automatic confirmation that your submission on ${escapeHtml(d.source)} was received.
    You do not need to submit the form again.
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
