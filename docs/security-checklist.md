# Endpoint security checklist

- Use fictional training data only. Do not paste names, account IDs, passwords,
  MFA codes, tokens, cookies, email bodies, private file paths or raw logs.
- Inspect network configuration locally; redact identifiers before any sharing.
- Verify authorization, scope and consent before testing an endpoint. This lab
  does not authorize access to any employer's network or account.
- Observe approved antivirus/firewall/update status. Escalate alerts; never
  disable protection, change exclusions or weaken certificate checks.
- Use official sign-in and recovery channels privately. Follow identity
  verification policy; this program cannot reset or unlock accounts.
- Treat suspicious messages as potential evidence. Do not click, open or forward
  them here. Report through the authorized security mechanism promptly.
- Keep software patched under the relevant maintenance policy. Save work before
  any authorized restart; never schedule automatic updates through this lab.
- Use least privilege. Do not elevate ordinary diagnostics automatically.
- Keep stores out of version control and protect their filesystem permissions.
  Plaintext JSON has no application encryption or authentication. Free-text
  validation is not a secret detector; the user must enforce the fictional-data rule.
- Before publication, review all staged files and use `git diff --cached`.
  No credentials or system-specific network output belong in a public repository.
