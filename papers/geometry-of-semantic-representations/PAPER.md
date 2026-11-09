---
name: "geometry-of-semantic-representations"
title: "Meaning Geometry: Representation Spaces, Distinguishability, and the Limits of Similarity"
short_title: "Meaning Geometry"
subtitle: "Representation Spaces, Distinguishability, and the Limits of Similarity"
artifact: "scientific-paper"
edition: "1.1"
author: "Pavel Valentov"
language: "en"
license: "CC-BY-4.0"
status: "research-draft"
description: "Task-relative observation spaces, quotient metrics, partial information and the limits of similarity-based knowledge use."
sources:
  - "Knowledge Contract project corpus and publication edition"
  - "Hamming 1950 Codes"
  - "Gardenfors 2000 Conceptual Spaces"
  - "Coecke Sadrzadeh Clark 2010 Meaning"
---

# Meaning Geometry: Representation Spaces, Distinguishability, and the Limits of Similarity

**Author:** Pavel Valentov · **Publication edition:** 1.1

## Abstract

A representation can be close to another representation while differing on a condition that determines whether it may be used. Conversely, different expressions can agree on every observation required by a particular task. This paper asks what a geometry of meaning representations can establish when its objects, observations, context and comparison rule are explicit. We define an observation profile and derive a weighted pseudometric on its objects, with a metric on the corresponding observational equivalence classes. Conditional propositions describe information loss in representations, refinement and normalization, preservation under transformations, sound distance envelopes for incomplete observations, and bounded change across aligned contexts. Constructed countermodels distinguish threshold proximity from equivalence, symmetric distance from directed entailment, and agreement of unknown markers from established content. A cosine example shows that a commonly used dissimilarity does not automatically satisfy the triangle inequality. The mathematical constructions are elementary and are not claimed as a new universal geometry or a theory of human experience. The contribution is a common, inspectable boundary between comparison, transformation and knowledge admission: similarity can organize candidate search, while validity, applicability and authority remain separate obligations. Exact finite examples accompany the deductions. They do not validate semantic annotations, measure an embedding model or demonstrate production performance.

**Keywords:** semantic representation; observation profile; pseudometric; contextual equivalence; incomplete information; knowledge admission.

## 1. Question, method and contribution

A numerical similarity score has a meaning only after specifying what is compared and what distinctions the score can retain. A vector may represent a string, a possible interpretation, an assessed claim or a task-specific artifact. Those objects are not interchangeable. Changing a representation, its comparison context or the selected observations can change which differences are visible without changing the source text.

Our question is **which conclusions about represented content follow from a declared geometry, and which require additional evidence**. The method is deductive. We define a bounded representation profile, prove its properties, and construct examples that fail when a premise is removed. Finite verification checks selected instances of this model; it does not give a formal semantics to arbitrary language.

The [human-meaning foundation](../human-meaning-and-computable-knowledge/PAPER.md) separates human expression, interpretation, representation and permitted use. [Meaning in Context](../semantic-objects-and-context/PAPER.md) makes context and applicability explicit. This paper uses those distinctions to define comparison on selected observations. It does not replace human understanding by a vector or identify an author's intention with a model-generated encoding.

The resulting contributions are a precise comparison profile; explicit interaction between equivalence, projection and transformation; conservative treatment of incomplete observations; and an interface in which similarity helps retrieve candidates without granting their use. The mathematical components are standard kinds of construction, with proofs supplied to expose the assumptions needed here. No priority claim over conceptual-space or compositional-semantics research is made.

## 2. Related approaches and the scope of the construction

Hamming's work on error-detecting and error-correcting codes [1] provides the historical background for disagreement counts. We use a positive weighted version on declared observations and prove the exact property needed below. Naming a distance after this construction does not establish that its coordinates express the distinctions relevant to a knowledge task.

Gärdenfors's conceptual-spaces programme models representations through geometrical structures and quality dimensions [2]. It makes geometry relevant to conceptual representation rather than treating it as a display of an arbitrary graph. Our profile is narrower: its coordinates are explicitly selected observations, and it makes no assumption that all concepts form convex regions or that one set of dimensions captures human cognition.

Coecke, Sadrzadeh and Clark combine distributional vector-space meaning with a compositional treatment of grammatical types [3]. Their work provides a substantive precedent for connecting algebraic structure and represented meaning. The present account does not reproduce that categorical construction or inherit its guarantees. It asks what remains justified when a task's protected distinctions, partial information and admission conditions are recorded separately from its numerical comparison.

These comparisons identify neighbouring approaches, not an exhaustive literature survey or a finding that our profile is empirically superior. The proofs below are self-contained. Whether a learned representation reliably approximates the declared observations is a separate measurement question.

## 3. Observation profiles and equivalence

Fix a context \(c\). A comparison profile specifies an object set \(X_c\), a finite nonempty question index set \(Q\), an answer alphabet \(A_q\) for each question, interpretation functions

\[
f_{q,c}:X_c\to A_q,
\]

and positive weights \(w_q\) with \(\sum_{q\in Q}w_q=1\). The joint observation map is

\[
\Phi_c(x)=(f_{q,c}(x))_{q\in Q}.
\]

The question index identifies a defined observation, not merely a keyword. Answer equality needs an explicit interpretation: identical unit labels, for example, are not automatically equal physical quantities. The functions in this section are total and single-valued on the declared carrier. Ambiguous or unavailable semantic values are treated in Section 6 rather than silently resolved by a plausible guess.

Define observational equivalence by

\[
x\sim_c y\quad\Longleftrightarrow\quad\Phi_c(x)=\Phi_c(y).
\]

Equality makes this relation reflexive, symmetric and transitive. It is relative to the chosen questions, context and interpretation functions. Two equivalent objects may have different wording, provenance or omitted properties. If one of those differences matters to the task, the profile must expose it or the admission process must check it separately.

The context record fixes the interpretation assumptions and revisions under which observations are compared. The mathematical definition does not certify the correctness of that record. A mistaken extraction can supply a perfectly well-defined value to a metric. Geometry alone cannot reveal that the value was extracted incorrectly.

### Proposition 1. Observation distance is a pseudometric and induces a quotient metric

For the fixed profile define

\[
d_c(x,y)=\sum_{q\in Q}w_q\,
\mathbf 1[f_{q,c}(x)\ne f_{q,c}(y)].
\]

Then \(d_c\) is a pseudometric with values in \([0,1]\). Moreover, \(d_c(x,y)=0\) exactly when \(x\sim_c y\), and

\[
\bar d_c([x],[y])=d_c(x,y)
\]

is a metric on \(X_c/\!\sim_c\).

**Proof.** Each summand is nonnegative, vanishes on the diagonal and is symmetric. For any three answers \(a,b,e\),

\[
\mathbf 1[a\ne e]\leq
\mathbf 1[a\ne b]+\mathbf 1[b\ne e].
\]

Multiplying by positive weights and summing proves the triangle inequality. Normalization gives the upper bound one. Positivity makes a zero sum equivalent to agreement in every coordinate. Replacing an object by an equivalent representative leaves every summand unchanged, so the quotient expression is well-defined. On the quotient, zero distance therefore implies equality of classes. ∎

The conclusion concerns distinguishability within a profile. It is not a proof that equivalent objects express the same meaning for every task. If zero-weight coordinates were allowed, the zero-distance relation would ignore them; it could no longer be identified with agreement on all declared questions. An empty question set supplies no discrimination and is excluded from this normalized profile.

## 4. Representation loss and transformations

Suppose an encoder \(e:X_c\to Z\) is used instead of the original objects. Let \(p:X_c\to O\) be a protected observation, possibly the whole vector \(\Phi_c\).

### Proposition 2. Recoverability requires agreement on representation fibres

There exists a function \(h:e(X_c)\to O\) with \(p=h\circ e\) if and only if

\[
e(x)=e(y)\Rightarrow p(x)=p(y)
\quad\text{for all }x,y\in X_c.
\]

**Proof.** Necessity follows by applying \(h\) to the equal representations. Conversely, assign to each attained representation the observation of any preimage. The stated implication makes that assignment independent of the chosen preimage. ∎

This is a set-theoretic factorization criterion, consistent with the representation boundary in the human-meaning foundation. It does not construct an efficient decoder, establish access to that decoder, or verify the observation values. If two objects collide under the encoder while differing on a mandatory observation, no function of that encoding alone can recover the observation for both. Adding a source reference or residual may separate the cases, but that changes the information supplied to the consumer.

A relation-preserving transformation needs similarly explicit premises. Let \(g:D\to Y\) be a partial transformation, with \(D\subseteq X_c\), and let the output profile have observation functions \(f'_q\) in the same alphabets and the same weights. Assume

\[
f'_q(g(x))=f_{q,c}(x)
\quad\text{for every }x\in D,\ q\in Q.
\]

### Proposition 3. Observation-preserving transformations are isometries on admitted classes

Under these assumptions,

\[
d'(g(x),g(y))=d_c(x,y)
\quad\text{for }x,y\in D.
\]

If \(D\) is a union of observational equivalence classes, \(g\) induces a well-defined isometric map from the admitted classes of \(X_c/\!\sim_c\) into the output quotient.

**Proof.** Preservation makes the input and output disagreement indicators equal coordinate by coordinate, giving the distance equality. Equivalent input representatives have identical output observations. Saturation of \(D\) makes admission independent of representative choice. These facts define the quotient map; its distance equality proves it is isometric and hence injective on classes. ∎

Neither surjectivity onto the output space nor injectivity on original objects is claimed. A transformation can merge differently labelled objects already equivalent in this profile. Without domain saturation, the distance equality still holds for admitted pairs, but membership of an entire input class is not well-defined: one representative may be admitted while another equivalent one is refused.

This connects geometry to the conditions of [Knowledge Transformations](../constrained-transformations/PAPER.md). Calling an operation a semantic transformation does not establish its preservation premise. For nondeterministic operations, any corresponding guarantee must quantify over every admitted output, not only one favourable sample.

## 5. Changing the observations and the context

Projection and refinement affect both equivalence and numerical distances. They need not preserve the interpretation of a threshold.

### Proposition 4. Restriction and refinement have different normalization effects

For a nonempty subset \(I\subseteq Q\), write

\[
W_I=\sum_{q\in I}w_q,
\qquad
d_I^*(x,y)=\sum_{q\in I}w_q\mathbf 1[f_{q,c}(x)\ne f_{q,c}(y)].
\]

Then \(d_I^*\leq d_c\). If the restricted profile is renormalized to total weight one, its distance is \(d_I=d_I^*/W_I\), so \(d_I\leq d_c/W_I\); it need not be at most \(d_c\).

For two fixed profiles on the same carrier, with distances \(d_Q,d_R\), the disjoint labelled union with weight mixture \(0<\alpha<1\) gives

\[
d_{\mathrm{ref}}=(1-\alpha)d_Q+\alpha d_R.
\]

Its zero-distance relation is the intersection of the two profile equivalences, and \(|d_{\mathrm{ref}}-d_Q|\leq\alpha\).

**Proof.** Restriction deletes nonnegative summands; division by \(W_I>0\) gives the normalized formula. For refinement, the mixture is the definition of the combined weights. Both positive terms vanish exactly when both profile distances vanish. Finally, \(|d_{\mathrm{ref}}-d_Q|=\alpha|d_R-d_Q|\leq\alpha\), since both distances lie in \([0,1]\). ∎

For two equally weighted coordinates, objects differing only in the first coordinate have distance \(1/2\). Restriction to that coordinate without normalization still gives \(1/2\), but renormalization gives one. Thus, discarding information can increase a normalized numerical distance. A smaller feature set is not itself evidence of greater semantic similarity.

Refinement can expose a difference that the original profile hid. Its mixture bound does not justify silently reusing a ranking or a decision threshold: cases near the threshold can change classification. Nor does counting several correlated questions establish several independent pieces of evidence. The weights define the comparison convention; their usefulness requires a separate task-based argument.

### Proposition 5. Aligned context changes bound distance changes

Suppose objects \(x,y\) can be interpreted in contexts \(c,c'\), with the same question meanings, answer alphabets and weights. Let \(d\) denote the weighted disagreement metric on the common product of answer alphabets. Define

\[
\epsilon_x=d(\Phi_c(x),\Phi_{c'}(x)),
\qquad
\epsilon_y=d(\Phi_c(y),\Phi_{c'}(y)).
\]

Then

\[
|d_c(x,y)-d_{c'}(x,y)|\leq\epsilon_x+\epsilon_y.
\]

**Proof.** The triangle inequality along the product-space path from \(\Phi_c(x)\) through \(\Phi_{c'}(x)\) and \(\Phi_{c'}(y)\) to \(\Phi_c(y)\) gives \(d_c(x,y)\leq\epsilon_x+d_{c'}(x,y)+\epsilon_y\). Interchanging the contexts proves the reverse bound. ∎

The alignment premise is essential to the interpretation of this result. Identical coordinate positions do not prove identical questions, referents or units. Without an explicit cross-context identification, applying the same arithmetic compares encodings whose meanings may have changed. Even under alignment, a stable distance does not show that an authorization or a material condition remains valid.

## 6. Incomplete observations and conservative distance envelopes

An unknown marker may be a valid recorded observation. Two records containing the same marker then have zero recorded disagreement in that coordinate. This does not establish equality of the underlying unknown values.

To compare possible semantic values, assign each object a nonempty set \(A_q(x)\) of allowed answers at each coordinate. Let \(\Gamma_{xy}\) be a nonempty set of admissible joint completions, contained in

\[
\left(\prod_{q\in Q}A_q(x)\right)
\times
\left(\prod_{q\in Q}A_q(y)\right).
\]

The completion set can encode dependencies between coordinates or between the objects. The interpretation of its members must be stated: possibilities allowed by an assessment are not automatically probabilities or established facts.

### Proposition 6. Coordinate envelopes are sound, with conditional attainability

Define

\[
L(x,y)=\sum_qw_q\mathbf 1[A_q(x)\cap A_q(y)=\varnothing]
\]

and

\[
U(x,y)=\sum_qw_q\mathbf 1[\text{the two answer sets are not the same singleton}].
\]

For every \((u,v)\in\Gamma_{xy}\), the completed distance satisfies

\[
L(x,y)\leq d(u,v)\leq U(x,y).
\]

If \(\Gamma_{xy}\) is exactly the full product of the displayed answer sets, both endpoints are attained.

**Proof.** Disjoint coordinate sets force disagreement; identical singletons force agreement. Every other coordinate can contribute at most its weight and at least zero, giving the bounds for any permitted completion. In the full-product case, choose a common answer in each nonempty intersection to attain the lower bound, and choose unequal answers in every pair of sets other than identical singletons to attain the upper bound. These choices can be combined independently because the profile is finite and the completion set is the full product. ∎

Joint constraints can make an endpoint unattainable. For two binary coordinates, allow only the completion pairs \((00,00)\) and \((11,11)\). Every marginal answer set is \(\{0,1\}\), so the coordinate upper envelope is one, but each admissible joint distance is zero. The coordinate envelope remains sound; it is not an exact optimization over joint constraints.

An empty completion set is an inconsistency or an unsatisfied modelling condition, not an established zero distance. Treating an impossible set of premises as a favourable comparison would hide the problem. Conversely, two independent unknown binary values admit both agreement and disagreement: the correct range is \([0,1]\), although two displayed unknown markers are identical.

At threshold \(\tau\), the condition \(U\leq\tau\) suffices for every admissible completion to be near, and \(L>\tau\) suffices for every completion to be far. Otherwise these envelopes alone do not settle the comparison. That reporting rule is conservative; it does not assert that a stronger joint analysis could not decide the case.

## 7. Similarity is not equivalence, entailment or permission

Several familiar shortcuts fail even on small exact examples.

**Threshold proximity is not transitive.** On two binary coordinates with equal weights, let \(x=00\), \(y=01\), \(z=11\) and \(\tau=1/2\). Both adjacent distances equal \(1/2\), whereas \(d(x,z)=1\). Consequently, the relation \(d\leq\tau\) is not an equivalence relation. Taking its transitive closure can join endpoints farther apart than the threshold. A clustering rule must state whether that is intentional rather than calling each cluster a class of identical meaning.

**Symmetric distance does not encode directed entailment by itself.** Under ordinary Boolean semantics, \(a\land b\) entails \(a\), but \(a\) does not entail \(a\land b\): the assignment with \(a\) true and \(b\) false is a counterexample. Any symmetric distance gives the same number in the two directions. A symmetric threshold alone therefore cannot implement this asymmetric entailment relation. An additional logical interpretation or directed assessment is necessary.

**One minus cosine similarity is not automatically a metric.** Consider unit vectors at angles \(0\), \(\pi/3\) and \(2\pi/3\). The adjacent dissimilarities \(1-\cos\theta\) are both \(1/2\), but the endpoint dissimilarity is \(3/2\). The triangle inequality would require \(3/2\leq1\), which is false. This refutes that axiom for this particular dissimilarity, not the usefulness of cosine ranking, Euclidean metrics or angular metrics under their own definitions. Algorithms requiring metric axioms need a measure that actually satisfies them.

**A small distance does not discharge a mandatory obligation.** Give an authorization coordinate weight \(1/100\) and all other coordinates total weight \(99/100\). Two records identical everywhere except allow versus deny then have distance \(1/100\). They can be near under a threshold of \(1/10\), but the permission decision is different. Raising predicted utility or adding many agreeing coordinates does not remove the denial. The same mathematical issue applies to any indispensable condition assigned a small weight.

These are countermodels to unconditional shortcuts. They do not refute a theorem whose premises include the missing condition. Nor do they estimate how often a particular encoder makes these errors.

## 8. Interface to Knowledge Contract and evaluation

Geometry has a constructive but limited role: it can order or filter candidates relative to a declared comparison profile. A downstream consumer still checks source identity, relevant interpretation, support, applicability, transformations, current authority, delivery and budget under the task's contract. Approximate retrieval additionally needs a stated recall and stopping boundary; a high-scoring returned item is not evidence that no necessary omitted item exists.

A comparison record should identify the object revisions, context and profile, question definitions, answer interpretations, weights, representation map, comparison rule and any incomplete-observation envelope. It should distinguish an observed value from a hypothesized value. An implementation claim also needs the actual encoder/checker version and evidence connecting its outputs to the declared functions. Storing this record makes a claim inspectable; it does not itself validate the claim.

The [context-composition paper](../retrieval-and-context-composition/PAPER.md) supplies a separate account of mandatory coverage and delivery. The [evidence paper](../evidence-and-falsification/PAPER.md) distinguishes proof, finite verification and empirical observation. The [controlled-reuse paper](../controlled-knowledge-reuse/PAPER.md) adds the obligations for using an earlier artifact in another request. These connections do not make distance a replacement for those requirements or require a geometric method in every retrieval implementation.

The companion [verification record](../../reviews/meaning-geometry/RESULTS.md) reports eight groups of newly executed exact synthetic checks. The [program](../../tools/check_meaning_geometry.py) enumerates a declared binary carrier and constructed partial-information cases using rational arithmetic. In one group, sixteen labelled objects produce eight observation classes; its 4,096 ordered triples test the triangle inequality on that carrier. Other groups check restrictions, refinement, preserving transformations, representation collisions, completion envelopes, similarity countermodels, hard-condition separation and aligned context changes. Counts have different denominators and are not pooled into an empirical success rate.

The program supplies regression controls for these examples, not a replacement for the proofs, an independent review or a test of learned semantic extraction. A useful empirical study would separately assess observation fidelity, candidate recall, decision errors, costs and sensitivity to profile choice, using a declared baseline and held-out cases. No such model comparison is reported here.

## 9. Limitations

The profile selects rather than discovers the distinctions relevant to a task. Observation functions, alphabets, context alignment and admissible completions are premises whose real-world adequacy requires evidence. Positive weights make the quotient result exact, but do not make the chosen weights psychologically or operationally calibrated. Equality within an answer alphabet can itself require a justified normalization.

Finite discrete coordinates do not describe every continuous, perceptual, pragmatic or social aspect of meaning. More general component metrics can be studied, but their axioms and aggregate properties must be established for their own domains. We do not infer convex concepts, a universal embedding, an optimum dimension or a general algorithm for resolving ambiguity from this model.

The set-theoretic factorization and quotient arguments do not establish computability, accessible decoders or efficient search. Coordinate envelopes can be loose when completion constraints are correlated. The finite program checks its own explicit synthetic inputs and shares the author's modelling choices; its successful exit is not independent confirmation of the entire semantic account.

Finally, a geometry of represented content is not a truth theory or an authority service. Those boundaries are deliberate requirements of the proposed interface, not empirical properties automatically enforced by an existing agent system.

## 10. Conclusion

A defensible geometry of meaning representations begins with a declared carrier, context, observations and comparison convention. Within a fixed finite observation profile, weighted disagreement yields a pseudometric and an exact metric on observational equivalence classes. Representation collisions limit recoverability; transformations preserve geometry only under explicit observation and domain conditions. Refinement, normalization and context change can alter distances, while incomplete observations require conservative envelopes rather than convenient equality of unknown markers.

The countermodels show why proximity, equivalence, entailment and permission must remain distinct. Geometry can help find material worth checking. It cannot by itself establish that the material is true, applicable, complete or authorized for a particular use. Connecting that limited geometric role to explicit transformation and admission obligations gives a testable interface between the scientific account and Knowledge Contract implementations.

## References

1. Hamming, R. W. “Error Detecting and Error Correcting Codes.” *Bell System Technical Journal* 29(2), 1950, 147–160. <https://doi.org/10.1002/j.1538-7305.1950.tb00463.x>. [Bell Labs publication record](https://www.nokia.com/bell-labs/publications-and-media/publications/error-detecting-and-error-correcting-codes/).
2. Gärdenfors, P. *Conceptual Spaces: The Geometry of Thought*. MIT Press, 2000. [Author's institutional publication record](https://portal.research.lu.se/en/publications/conceptual-spaces-the-geometry-of-thought/).
3. Coecke, B., Sadrzadeh, M., and Clark, S. “Mathematical Foundations for a Compositional Distributional Model of Meaning.” 2010. <https://arxiv.org/abs/1003.4394>.
