# BASALT Enterprise API Specification (v1.0.0)

BASALT is proprietary technology authored by Argelys Samuel Oriach and created within Seven Eighty Three (Lab 783). Commercial licensing inquiries: licensing@basalt.fm.

Base URL: `https://api.basalt.fm`

## 1. Authentication & Security
All calibration requests require a valid tenant key passed in the HTTP header:
`X-BASALT-KEY: <YOUR_ISSUED_API_KEY>`

Audio payloads are processed exclusively in ephemeral memory-backed temporary directories and purged immediately upon stream completion. BASALT retains zero copies of uploaded master recordings.

## 2. Health & Parity Check
`GET /health`

Returns current node availability and oscillator lock status.

**Response (`200 OK`):**
```json
{
  "status": "ONLINE",
  "lock": "7.83 HZ",
  "version": "1.0.0"
}
```
