# PUI89 AI Security Gateway v1

**Status:** implemented on the isolated branch `security/pui89-ai-security-gateway-v1`; not merged, not integrated into runtime agents, and not independently validated.

## Cost and dependency boundary

- Python standard library only; no third-party package additions.
- No model/API calls, subscriptions, cloud services, downloads, network access, scheduled jobs or GitHub Actions workflow changes.
- No installation or CI execution is required to add these source files.
- The gateway stores no raw prompt or response content in its decision object; it returns a SHA-256 digest and character count.

## Initial controls

1. Input and output text inspection.
2. Transparent prompt-injection indicator rules on inputs.
3. Secret-like string detection on inputs and outputs.
4. Content length and type checks with fail-closed handling.
5. Explicit tool allowlist; unknown tools are blocked.
6. High-impact tool names require human review.
7. All allowlisted tool calls still require caller-side authorization.
8. Machine-readable decision metadata and explicit limitations.

## Decision semantics

- `ALLOW`: no configured deterministic rule triggered. This is not a guarantee of safety or truth.
- `REVIEW`: a configured risk indicator or human-approval requirement applies.
- `BLOCK`: invalid/oversized content, secret-like material, or a tool not explicitly allowlisted.

## Safety limitations

- Regex rules are a small baseline and can miss novel, obfuscated, multilingual or context-dependent prompt injection.
- Secret patterns are illustrative, not exhaustive DLP.
- Tool-name matching is not a substitute for a typed capability registry or OS-level sandbox.
- This module does not sanitize, execute, authorize, or route any tool call.
- It does not validate model output truthfulness, malware, attachments, images, MCP protocol semantics, or physical safety.
- No physical actuation is possible or permitted through this module.

## Verification required before merge

Run the focused standard-library tests in a controlled local environment with no package installation:

```powershell
python -m unittest discover -s tests -p "test_pui89_ai_security_gateway.py" -v
```

Record the Python version, command, output, and commit. Do not mark tests passed until they have actually run. Then review false positives/negatives and threat-model coverage before integrating adapters into other PUI89 projects.
