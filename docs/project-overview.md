# Project overview

This is a local training application, not a production support platform.
It connects four skills: gathering evidence, interpreting network symptoms,
recording simulated incidents and escalating safely.

`models.py` validates ticket records and creates collision-resistant UUID IDs.
`ticket_manager.py` separates business rules from persistence behind a service
class: reads validate the complete store, writes lock, serialize to a temporary
file, flush and atomically replace. No separate database dependency is needed.
`cli.py` parses choices, formats JSON and translates expected failures into
exit codes. It never constructs a shell command from free text.
`network_diagnostics.py` validates destinations and bounds subprocesses; injected
runners and resolvers make offline tests possible. `knowledge_base.py` validates
article fields and matches all search words case-insensitively.

Data flow: user -> CLI -> service/model -> local storage. Diagnostics print to
the terminal and never feed raw network output into ticket persistence.
Knowledge-base fixtures and simulated tickets live under data/; the default
mutable ticket store lives under the user's home directory.

Scope: undergraduate IT support practice, Windows client procedures and awareness
of enterprise ownership boundaries. Success means runnable workflows and accurate
interpretation, not proving external internet access or administering a tenant.
