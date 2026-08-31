# Repository relation

Decision date: 2026-08-30.

## Decision

`Sodelin/new-math-discovery` and `Sodelin/ai-math-discovery` remain **distinct
repositories with distinct roles**.  `new-math-discovery` does not migrate
under or replace `ai-math-discovery`.

- `new-math-discovery` is the formal evolution engine: Lean definitions and
  theorems, executable attacks, counterexamples, and bounded claim matrices.
- `ai-math-discovery` is the canonical public discovery and audit lane.
- A result moves between them by an explicit commit-pinned import or
  cross-link after review.  Repository histories, issue boards, and candidate
  publication layers are not duplicated.

The first durability example is
`NewMathDiscovery.BlindnessRealization.blind_iff_below_generator`, frozen in
`new-math-discovery` commit `7910bd4`.  A later public packet may cite that
commit; the theorem is not silently copied into a second evolving source of
truth.

## Evidence

At the decision point:

- local `origin` was `https://github.com/Sodelin/new-math-discovery.git`;
- its `main` and local pre-freeze `HEAD` were
  `e0312af07d774b300525dbcf4380c317dce5eaac`;
- `ai-math-discovery/main` was
  `8d1777d31d230d57d9f871167414b8abba24245d`;
- PR 2 contained the canonical packet commit
  `fed566996600cee2375ac0fd4426de29f11001f7` and had fetched head
  `fc126ae25ab8d9039e517682d0963c80436d6304`;
- `git merge-base` found no common ancestor between the
  `new-math-discovery` canonical commit and either `ai-math-discovery/main` or
  PR 2;
- the root commits were distinct:
  `00114cc4e914c6e1e175204e4fefeb5a3ebf0f52` for
  `new-math-discovery` and
  `4b6f4c1a610058a1391a96e45ae5b055b1ec8c87` for
  `ai-math-discovery`.

This is a portfolio-role decision, not a claim that the repositories could
never be merged technically.  Any future migration requires an explicit new
decision, a history-preservation plan, and a deduplication audit.
