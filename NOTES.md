# Gmail setup status (2026-10-23)
- VM: nemoclaw-gmail-vm, project capstone-project-512419, zone us-central1-a
- Sandbox: gmail-agent, model nvidia/nemotron-3.5-super-vl-120b-a12b
- Gmail preset applied: policy add gmail --yes
- Credential: /sandbox/hand/gmail_config.json (host copy ~/gmail_config.json, chmod 600)
- WORKING: send_email_proxy.py (sandbox has no direct DNS; goes via proxy)
- FAILED: send_email.py (name resolution error); needs the proxy
- Test email received. Script may hang after sending; press Ctrl-C.
- Snapshot: gmail-working
- Open: port 18789 dashboard forward warning on recover; Slack not set up;
  Snowflake not set up; report script not built; cron not scheduled.
