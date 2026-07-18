# Stack profiles

The core template is stack-agnostic. Profiles add concrete commands, structure, tests, and security guidance without replacing root standards.

Available profiles:

- [`node-typescript.md`](node-typescript.md)
- [`nextjs-react.md`](nextjs-react.md)
- [`python.md`](python.md)
- [`docker.md`](docker.md)
- [`postgresql.md`](postgresql.md)
- [`terraform.md`](terraform.md)

A project may select multiple profiles in `project.yml`. Implement profile commands behind the stable Task interface and add nested `AGENTS.md` only when a directory needs materially different local rules.
