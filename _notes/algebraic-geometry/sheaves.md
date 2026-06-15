---
title: Sheaves
topic: Algebraic Geometry
order: 1
tags: [sheaves, schemes]
summary: "层的基本定义、限制映射与粘合条件。"
---

# Sheaves

A presheaf $\mathcal F$ on a topological space $X$ assigns to every open set $U\subseteq X$ an object $\mathcal F(U)$ and to every inclusion $V\subseteq U$ a restriction map

\[
\rho_{UV}:\mathcal F(U)\to \mathcal F(V).
\]

A sheaf is a presheaf satisfying the locality and gluing axioms.

## Motivation

A sheaf should be thought of as a device which records local data and remembers when such data can be glued globally.
