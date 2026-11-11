# Focused literature and source review

Updated 11 November 2026. This is a focused review supporting the semester scope, not a systematic review or claim of exhaustive coverage.

## Scientific dataset description

Arias Chao et al. (2021), [Data 6(1), 5](https://doi.org/10.3390/data6010005), supplies the scientific basis for the dataset choice. It distinguishes real operating profiles from simulated deterioration/responses, describes variable families and provides physical definitions. This supports RUL regression and explains why operating context belongs beside sensor features.

The older local April 2020 preprint focuses on DS02 and differs from later tables. We used actual file metadata to establish local structure and checked the journal for missing definitions, notably P2. The paper does not establish our models' performance, a business saving, or deployment suitability.

## Course concepts applied

The supplied Industrial Analytics/Data Science slides distinguish descriptive analysis from predictive modeling and emphasize a systematic, context-aware process. Dataset Scales and the lecturer's feature-table notebook guide measurement scales and meaningful operations. We distinguish numeric storage from labels/categories and preserve grouping for dependent engine histories.

Task 5 grouping uses historical RUL for explanation only. It does not make the group label available to a predictive model, and repeated flight observations do not become independent engines merely because they form many rows.

## Technical implementation references

Official scikit-learn documentation guides train-only learned transformations, missing-value handling, standardization and categorical encoding. The linear-regression/random-forest references support the **proposed next-stage algorithm explanations**, not unrun experimental claims. API details and source links are in [references](references.md).

## What this review changes in our project

1. Treat operating conditions as context rather than assume every sensor change is wear.
2. Exclude simulator-only health and target information from physical-sensor predictors.
3. Use engine-group-aware evaluation and explicit feature availability at flight end.
4. Prefer simple baseline comparisons before advanced model complexity.
5. Preserve limits: simulation, small groups, source shift and uncertain cross-subset independence.

Both students should read the source sections relevant to their explanation rather than rely on this summary alone. Actual AI assistance is recorded in [the log](ai-use-log.md).
