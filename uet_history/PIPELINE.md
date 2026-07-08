# UET History Pipeline

The UET history workspace uses a three-layer pipeline.

```text
1_raw      -> 2_digest      -> 3_publish
local only    public-safe       public-facing
```

## Layer 1: Raw

Raw inputs include AI conversations, personal notes, transcripts, external
sources, media, old project snapshots, and unreviewed drafts.

Raw content is local-first and is not committed to the public repository unless
it has been reviewed for size, privacy, provenance, and publication safety.

## Layer 2: Digest

`2_digest/` contains summaries, indexes, evidence notes, and structured digests
that can point back to raw sources without publishing the raw sources themselves.

Digest outputs should be factual, source-aware, and conservative about claims.

## Layer 3: Publish

`3_publish/` contains public-facing narrative work such as book outlines,
chapter drafts, article drafts, web-ready summaries, and proposal-ready text.

Publish outputs should not claim more than the digest/source chain supports.

## Public Repository Rule

The public repository may include digest and publish layers. Raw folders stay
out unless a separate review explicitly approves a small, safe source file.