# Core Concept

DNL is connected Markdown for AI navigation.

It is not a note app, a wiki product, or a fixed company hierarchy. It is an information architecture pattern that helps an AI agent load the right context in the right order.

## The Job

A DNL document should answer one of these questions:

- Where should the agent start?
- What does this domain mean?
- Which project or module owns this topic?
- Which source files or repositories matter?
- Which runbook should be used for this failure?
- Where should rough working notes be promoted after they become reusable?

DNL works best when each page has one job and points to the next useful page.

## The Building Blocks

DNL can use a few simple pieces:

- Markdown files for human-readable context
- folders for coarse structure
- local links for public reader documentation
- YAML path tokens for agent-oriented DNL documents
- `PATHS.md` for local repository path mapping
- `future` areas for active investigation and design work
- authoring rules to keep the layer coherent over time

You do not need all of these on day one.

## The Important Boundary

DNL does not prescribe your hierarchy.

A large organization might use company, product, and project layers. A small open-source project might only need one `DNL/README.md`, a code map, and two runbooks.

The pattern is:

```text
short entrypoint
-> focused router
-> domain or module page
-> source path, runbook, or working note
```

## AI-first, Human-readable

DNL is AI-first because the structure is designed for agents that must choose what to read next.

It is still human-readable because the content is plain Markdown, versioned with Git, and visible in normal editors.

## Read Next

- [How DNL Works](how-dnl-works.md)
- [Getting started](getting-started.md)
- [Repository layout](repository-layout.md)
