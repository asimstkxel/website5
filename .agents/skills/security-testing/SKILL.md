---
name: security-testing
description: Security testing, vulnerability assessment, and secure code review. Use for identifying security flaws, testing authentication/authorization, reviewing code for OWASP Top 10 vulnerabilities, and ensuring secure configurations.
---

# Security Testing

## Use this skill when

- Reviewing code for security vulnerabilities (XSS, SQL injection, CSRF, etc.)
- Testing authentication and authorization flows
- Assessing input validation and output encoding
- Checking secure headers, CORS, and cookie configurations
- Reviewing dependency vulnerabilities
- Performing security checklists before deployment
- Hardening APIs and form endpoints

## Do not use this skill when

- The task is purely functional testing without security implications (route to qa)
- The task is about writing new features (route to frontend or backend)
- The task is about business requirements (route to business-analyst)

## Security Testing Principles

- **Defense in depth**: Never rely on a single security control. Layer protections.
- **Least privilege**: Every component should have the minimum permissions needed.
- **Fail secure**: When something breaks, it should deny access, not grant it.
- **Trust no input**: All user-supplied data is untrusted until validated and sanitized.
- **Security by default**: Secure configurations should be the default, not opt-in.

## OWASP Top 10 Review Checklist

### 1. Injection (SQL, NoSQL, Command, LDAP)

```
- [ ] All database queries use parameterized statements or prepared queries
- [ ] No string concatenation in SQL/NoSQL queries with user input
- [ ] OS commands are avoided; if necessary, inputs are strictly validated
- [ ] ORM usage does not allow raw query injection
- [ ] Error messages do not expose database structure or query details
```

**What to look for in code:**
```javascript
// VULNERABLE — string concatenation
const query = `SELECT * FROM users WHERE email = '${req.body.email}'`;

// SECURE — parameterized query
const query = 'SELECT * FROM users WHERE email = $1';
const result = await db.query(query, [req.body.email]);
```

### 2. Broken Authentication

```
- [ ] Passwords are hashed with bcrypt/scrypt/argon2 (not MD5/SHA1)
- [ ] Session tokens are cryptographically random and sufficiently long
- [ ] Session tokens are invalidated on logout
- [ ] Failed login attempts are rate-limited
- [ ] Password reset tokens expire and are single-use
- [ ] Multi-factor authentication is available for sensitive operations
- [ ] Default credentials are not present
```

### 3. Sensitive Data Exposure

```
- [ ] Sensitive data is encrypted in transit (HTTPS/TLS)
- [ ] Sensitive data is encrypted at rest
- [ ] API responses do not leak unnecessary fields (passwords, tokens, internal IDs)
- [ ] Error messages and stack traces are not exposed to users
- [ ] Sensitive data is not logged (passwords, tokens, PII)
- [ ] Cache-Control headers prevent caching of sensitive responses
- [ ] Autocomplete is disabled on sensitive form fields
```

### 4. XML External Entities (XXE)

```
- [ ] XML parsers disable external entity processing
- [ ] XML input is validated against a schema
- [ ] JSON is preferred over XML where possible
```

### 5. Broken Access Control

```
- [ ] Every API endpoint checks authorization (not just authentication)
- [ ] Users cannot access other users' data by changing IDs in URLs
- [ ] Admin functions are restricted to admin roles
- [ ] CORS is configured to allow only trusted origins
- [ ] Directory listing is disabled on the web server
- [ ] File uploads validate type, size, and do not allow path traversal
```

### 6. Security Misconfiguration

```
- [ ] Security headers are set (see Security Headers section below)
- [ ] Default accounts and passwords are removed
- [ ] Directory listing is disabled
- [ ] Error handling does not reveal stack traces
- [ ] Unused HTTP methods are disabled
- [ ] Server version headers are removed or obscured
- [ ] Debug mode is disabled in production
```

### 7. Cross-Site Scripting (XSS)

```
- [ ] All user input rendered in HTML is escaped/encoded
- [ ] Content-Security-Policy header is configured
- [ ] DOM manipulation uses safe methods (textContent, not innerHTML with user data)
- [ ] JavaScript frameworks' built-in XSS protections are not bypassed
- [ ] URL parameters are not reflected in the page without encoding
- [ ] Rich text editors sanitize output (e.g., DOMPurify)
```

**What to look for in code:**
```javascript
// VULNERABLE — innerHTML with user data
element.innerHTML = userInput;

// SECURE — textContent for plain text
element.textContent = userInput;

// SECURE — sanitize if HTML is needed
element.innerHTML = DOMPurify.sanitize(userInput);
```

### 8. Insecure Deserialization

```
- [ ] Untrusted data is not deserialized without validation
- [ ] JSON.parse is preferred over eval for JSON data
- [ ] Serialized objects from cookies/hidden fields are integrity-checked
```

### 9. Using Components with Known Vulnerabilities

```
- [ ] Dependencies are regularly audited (npm audit, pip audit, etc.)
- [ ] No dependencies with known critical/high CVEs
- [ ] Unused dependencies are removed
- [ ] Lock files are committed and reviewed
- [ ] Automated dependency update tools are configured (Dependabot, Renovate)
```

### 10. Insufficient Logging & Monitoring

```
- [ ] Authentication events are logged (login, logout, failed attempts)
- [ ] Authorization failures are logged
- [ ] Input validation failures are logged
- [ ] Logs do not contain sensitive data (passwords, tokens)
- [ ] Logs are tamper-resistant and stored securely
- [ ] Alerting is configured for suspicious patterns
```

## Security Headers Checklist

```
- [ ] Content-Security-Policy — restricts resource loading sources
- [ ] X-Content-Type-Options: nosniff — prevents MIME type sniffing
- [ ] X-Frame-Options: DENY or SAMEORIGIN — prevents clickjacking
- [ ] Strict-Transport-Security — enforces HTTPS
- [ ] Referrer-Policy: strict-origin-when-cross-origin — limits referrer leakage
- [ ] Permissions-Policy — restricts browser features (camera, microphone, geolocation)
- [ ] X-XSS-Protection: 0 — disabled (CSP is the modern replacement)
```

## Static Site Security Review

For static HTML/CSS/JS sites (no backend):

```
- [ ] No sensitive data hardcoded in HTML/JS (API keys, tokens, credentials)
- [ ] Third-party scripts loaded from trusted CDNs with integrity hashes (SRI)
- [ ] Forms with action URLs use HTTPS endpoints
- [ ] External links use rel="noopener noreferrer" on target="_blank"
- [ ] No inline event handlers that eval user-controlled data
- [ ] Google Tag Manager / analytics scripts are from verified accounts
- [ ] Contact forms do not expose email addresses to scraping
- [ ] No commented-out code containing sensitive information
- [ ] Images and assets do not leak metadata (EXIF data)
```

## Client-Side Security Patterns

### Form Validation
```javascript
// Always validate on BOTH client and server
// Client-side is for UX, server-side is for security

// Email validation (basic client-side)
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
if (!emailRegex.test(input)) {
  showError('Please enter a valid email address');
}

// Sanitize before inserting into DOM
function sanitizeForDisplay(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}
```

### Subresource Integrity (SRI)
```html
<!-- Always use integrity hashes for third-party scripts -->
<script
  src="https://cdn.example.com/library.js"
  integrity="sha384-abc123..."
  crossorigin="anonymous">
</script>
```

### Content Security Policy (meta tag for static sites)
```html
<meta http-equiv="Content-Security-Policy"
  content="default-src 'self'; script-src 'self'; style-src 'self' https://fonts.googleapis.com; font-src https://fonts.gstatic.com; img-src 'self' https:; frame-ancestors 'none';">
```

## Vulnerability Report Format

When reporting security findings:

```
## Security Assessment: [target]
**Date:** [date]
**Scope:** [what was tested]
**Risk Level:** Critical | High | Medium | Low | Informational

### Findings

#### [VULN-001] [Title]
**Severity:** Critical | High | Medium | Low
**Category:** [OWASP category]
**Location:** [file:line or URL]
**Description:** [what the vulnerability is]
**Impact:** [what an attacker could do]
**Reproduction steps:**
  1. [step]
  2. [step]
**Recommendation:** [how to fix it]
**References:** [relevant CWE/CVE/OWASP links]

### Summary
**Total findings:** [count by severity]
**Critical/High requiring immediate action:** [count]
**Recommendation:** [ship / fix before shipping / block deployment]
```

## Process

1. **Scope** — Define what is being tested and the threat model
2. **Review** — Examine code against OWASP checklist and security patterns
3. **Test** — Attempt to exploit identified weaknesses
4. **Report** — Document findings with severity, impact, and remediation
5. **Verify** — Confirm fixes resolve the vulnerabilities without regression
