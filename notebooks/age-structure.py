import marimo

__generated_with = "0.19.9"
app = marimo.App()


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Age-structured population models

    ## [Models in Population Biology](http://modelspopbiol.yoavram.com)
    ## Yoav Ram

    We use **Orca** (`Orcinus_orca`) life-table data to build an age-structured demographic model.
    """)
    return


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from age_structure_model import (
        DATA_DIR,
        STAGE_SPEC,
        behavioral_checks,
        build_lefkovitch_matrix,
        clean_life_table,
        dominant_demography,
        finite_sensitivity_elasticity,
        load_orca_data,
        long_run_growth_factor,
        make_init_vectors,
        matrix_checks,
        project_periodic_bad_years,
        project_population,
        summarize_stages,
        threshold_frontier,
    )

    sns.set_context("talk")
    sns.set_palette("colorblind")
    return (
        DATA_DIR,
        STAGE_SPEC,
        behavioral_checks,
        build_lefkovitch_matrix,
        clean_life_table,
        dominant_demography,
        finite_sensitivity_elasticity,
        load_orca_data,
        long_run_growth_factor,
        make_init_vectors,
        matrix_checks,
        mo,
        np,
        pd,
        plt,
        project_periodic_bad_years,
        project_population,
        sns,
        summarize_stages,
        threshold_frontier,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Age structure matters because two populations with the same total size can have very different futures.

    We use a discrete-time projection model:

    $$ \mathbf{n}_{t+1} = \mathbf{A}\mathbf{n}_t $$

    where $\mathbf{n}_t$ is the stage-abundance vector and $\mathbf{A}$ is a Lefkovitch/Leslie-style projection matrix.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Data and life table

    We read Orca snapshots from repository-local CSV files extracted from MALDDABA.
    """)
    return


@app.cell
def _(load_orca_data):
    lt_raw, metric_raw, data_used_raw = load_orca_data()
    return data_used_raw, lt_raw, metric_raw


@app.cell
def _(clean_life_table, lt_raw):
    lt_clean, data_checks = clean_life_table(lt_raw)
    return data_checks, lt_clean


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Quick integrity checks:
    """)
    return


@app.cell
def _(data_checks):
    data_checks
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Data provenance and reported demographic summary from MALDDABA:
    """)
    return


@app.cell
def _(data_used_raw, metric_raw):
    metric_raw, data_used_raw
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Life-table quantities across ages:
    """)
    return


@app.cell
def _(lt_clean, plt, sns):
    fig_life, _axes = plt.subplots(1, 2, figsize=(13, 4), sharex=True)

    _axes[0].plot(lt_clean["Age"], lt_clean["Sx"], lw=2)
    _axes[0].set(xlabel="Age", ylabel="Annual survival $S_x$", title="Survival schedule")

    _axes[1].plot(lt_clean["Age"], lt_clean["mx"], lw=2)
    _axes[1].set(xlabel="Age", ylabel="Fecundity $m_x$", title="Fecundity schedule")

    fig_life.tight_layout()
    sns.despine()
    fig_life
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Stage aggregation for teaching model

    We aggregate ages into four classes:
    1. Juvenile: 0-10
    2. Early reproductive: 11-24
    3. Prime reproductive: 25-44
    4. Older/post-reproductive: 45+
    """)
    return


@app.cell
def _(STAGE_SPEC):
    stage_spec = STAGE_SPEC.copy()
    return (stage_spec,)


@app.cell
def _(lt_clean, stage_spec, summarize_stages):
    stage_summary = summarize_stages(lt_clean, stage_spec)
    return (stage_summary,)


@app.cell
def _(stage_summary):
    stage_summary
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Leslie/Lefkovitch matrix model

    We use a stage-structured projection matrix with within-stage stasis and between-stage maturation.
    """)
    return


@app.cell
def _(build_lefkovitch_matrix, stage_summary):
    A_base = build_lefkovitch_matrix(stage_summary)
    return (A_base,)


@app.cell
def _(A_base, pd, stage_summary):
    _labels = stage_summary["stage"].tolist()
    A_base_df = pd.DataFrame(A_base, index=_labels, columns=_labels)
    A_base_df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Asymptotic theory

    From the dominant eigenvalue/eigenvectors of $\mathbf{A}$ we get:

    $$ \lambda = \text{dominant eigenvalue of } \mathbf{A} $$

    $$ \mathbf{w} = \text{stable stage distribution (right eigenvector)} $$

    $$ \mathbf{v} = \text{reproductive value (left eigenvector)} $$
    """)
    return


@app.cell
def _(A_base, dominant_demography, pd, stage_summary):
    lambda_base, stable_stage, reproductive_value = dominant_demography(A_base)
    asymptotic_df = pd.DataFrame(
        {
            "stage": stage_summary["stage"],
            "stable_stage": stable_stage,
            "reproductive_value": reproductive_value,
        }
    )
    asymptotic_df
    return asymptotic_df, lambda_base, reproductive_value, stable_stage


@app.cell
def _(A_base, lambda_base, matrix_checks, pd, stable_stage):
    matrix_check_df = matrix_checks(A_base, stable_stage, lambda_base)
    matrix_check_df
    return (matrix_check_df,)


@app.cell
def _(lambda_base, metric_raw, mo, np):
    _r = float(metric_raw.loc[0, "r"])
    _lambda_empirical = float(np.exp(_r))
    mo.md(
        rf"""
        Baseline dominant growth factor is **$\lambda = {lambda_base:.4f}$**.

        MALDDABA summary gives **$r = {_r:.5f}$**, which implies **$e^r = {_lambda_empirical:.4f}$**.
        """
    )
    return


@app.cell
def _(asymptotic_df, plt, sns):
    fig_asym, _axes = plt.subplots(1, 2, figsize=(12, 4))

    _axes[0].bar(asymptotic_df["stage"], asymptotic_df["stable_stage"])
    _axes[0].set(title="Stable stage distribution", ylabel="Proportion")
    _axes[0].tick_params(axis="x", rotation=20)

    _axes[1].bar(asymptotic_df["stage"], asymptotic_df["reproductive_value"])
    _axes[1].set(title="Reproductive value", ylabel="Relative value")
    _axes[1].tick_params(axis="x", rotation=20)

    fig_asym.tight_layout()
    sns.despine()
    fig_asym
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Transient dynamics

    We compare multiple initial compositions with the same total $N_0$.
    """)
    return


@app.cell
def _(mo):
    n0_ui = mo.ui.slider(100, 20000, step=100, value=4000, label="Initial total N0")
    years_ui = mo.ui.slider(20, 200, step=5, value=120, label="Projection years")
    mo.hstack([n0_ui, years_ui], justify="start", gap=1.0)
    return n0_ui, years_ui


@app.cell
def _(make_init_vectors, n0_ui, stable_stage):
    _n0 = float(n0_ui.value)
    init_vectors = make_init_vectors(stable_stage, _n0)
    return init_vectors


@app.cell
def _(A_base, init_vectors, np, project_population, stable_stage, years_ui):
    trajectories = {}
    totals = {}
    composition_distance = {}

    for _name, _n0 in init_vectors.items():
        _traj, _tot = project_population(A_base, _n0, years_ui.value)
        trajectories[_name] = _traj
        totals[_name] = _tot
        _comp = _traj / np.clip(_traj.sum(axis=1, keepdims=True), 1e-12, None)
        _dist = np.abs(_comp - stable_stage[None, :]).sum(axis=1)
        composition_distance[_name] = _dist

    return composition_distance, totals, trajectories


@app.cell
def _(composition_distance, np, plt, sns, totals):
    _years = np.arange(len(next(iter(totals.values()))))
    fig_transient, _axes = plt.subplots(1, 2, figsize=(13, 4))

    for _name, _series in totals.items():
        _axes[0].plot(_years, _series, lw=2, label=_name)
    _axes[0].set(xlabel="Year", ylabel="Total abundance", title="Transient abundance")
    _axes[0].legend()

    for _name, _series in composition_distance.items():
        _axes[1].plot(_years, _series, lw=2, label=_name)
    _axes[1].set(
        xlabel="Year",
        ylabel="L1 distance to stable distribution",
        title="Convergence to stable composition",
    )

    fig_transient.tight_layout()
    sns.despine()
    fig_transient
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Sensitivity and elasticity

    We perturb each nonzero matrix element and approximate:

    $$ s_{ij} = \frac{\partial \lambda}{\partial a_{ij}} $$

    $$ e_{ij} = \frac{a_{ij}}{\lambda} \frac{\partial \lambda}{\partial a_{ij}} $$
    """)
    return


@app.cell
def _(A_base, finite_sensitivity_elasticity, np, pd, stage_summary):
    sensitivity_mat, elasticity_mat = finite_sensitivity_elasticity(A_base)

    _labels = stage_summary["stage"].tolist()
    sensitivity_df = pd.DataFrame(sensitivity_mat, index=_labels, columns=_labels)
    elasticity_df = pd.DataFrame(elasticity_mat, index=_labels, columns=_labels)

    _records = []
    _n = A_base.shape[0]
    for _i in range(_n):
        for _j in range(_n):
            if np.isnan(elasticity_mat[_i, _j]):
                continue
            _records.append(
                {
                    "to_stage": _labels[_i],
                    "from_stage": _labels[_j],
                    "sensitivity": sensitivity_mat[_i, _j],
                    "elasticity": elasticity_mat[_i, _j],
                }
            )
    elasticity_long = pd.DataFrame(_records).sort_values("elasticity", ascending=False)
    return elasticity_df, elasticity_long, sensitivity_df


@app.cell
def _(elasticity_df, plt, sns):
    fig_elas, _ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(elasticity_df, annot=True, fmt=".3f", cmap="YlGnBu", ax=_ax)
    _ax.set(title="Elasticity of $\\lambda$ to matrix elements")
    fig_elas.tight_layout()
    fig_elas
    return


@app.cell
def _(elasticity_long):
    elasticity_long.head(8)
    return


@app.cell
def _(behavioral_checks, stage_summary):
    validation_df = behavioral_checks(stage_summary)
    validation_df
    return (validation_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Scientific question 1

    Which vital-rate intervention gives the largest increase in long-run growth?

    We compare equal proportional effort (5% increase) applied separately to:
    1. Juvenile survival
    2. Adult survival
    3. Maturation transition from juvenile stage
    4. Fertility
    """)
    return


@app.cell
def _(build_lefkovitch_matrix, dominant_demography, lambda_base, pd, stage_summary):
    _lever_specs = {
        "juvenile_survival": dict(juvenile_survival_mult=1.05),
        "adult_survival": dict(adult_survival_mult=1.05),
        "maturation": dict(maturation_mult=1.05),
        "fertility": dict(fertility_mult=1.05),
    }

    _rows = []
    for _lever, _kwargs in _lever_specs.items():
        _a = build_lefkovitch_matrix(stage_summary, **_kwargs)
        _lam, _, _ = dominant_demography(_a)
        _rows.append(
            {
                "lever": _lever,
                "lambda": _lam,
                "delta_lambda": _lam - lambda_base,
                "percent_change_lambda": 100.0 * (_lam / lambda_base - 1.0),
            }
        )

    lever_rank_df = pd.DataFrame(_rows).sort_values("delta_lambda", ascending=False)
    lever_rank_df
    return (lever_rank_df,)


@app.cell
def _(mo):
    juvenile_survival_ui = mo.ui.slider(
        0.70, 1.30, step=0.01, value=1.00, label="Juvenile survival multiplier"
    )
    adult_survival_ui = mo.ui.slider(
        0.70, 1.30, step=0.01, value=1.00, label="Adult survival multiplier"
    )
    maturation_ui = mo.ui.slider(
        0.70, 1.30, step=0.01, value=1.00, label="Maturation multiplier"
    )
    fertility_ui = mo.ui.slider(
        0.70, 1.30, step=0.01, value=1.00, label="Fertility multiplier"
    )

    mo.vstack(
        [
            juvenile_survival_ui,
            adult_survival_ui,
            maturation_ui,
            fertility_ui,
        ],
        gap=0.6,
    )
    return adult_survival_ui, fertility_ui, juvenile_survival_ui, maturation_ui


@app.cell
def _(
    build_lefkovitch_matrix,
    dominant_demography,
    stage_summary,
    adult_survival_ui,
    fertility_ui,
    juvenile_survival_ui,
    maturation_ui,
):
    A_intervention = build_lefkovitch_matrix(
        stage_summary,
        juvenile_survival_mult=juvenile_survival_ui.value,
        adult_survival_mult=adult_survival_ui.value,
        maturation_mult=maturation_ui.value,
        fertility_mult=fertility_ui.value,
    )
    lambda_intervention, _, _ = dominant_demography(A_intervention)
    return A_intervention, lambda_intervention


@app.cell
def _(A_base, A_intervention, init_vectors, np, plt, project_population, sns, years_ui):
    _n0 = init_vectors["Stable"]
    _, _baseline_total = project_population(A_base, _n0, years_ui.value)
    _, _intervention_total = project_population(A_intervention, _n0, years_ui.value)

    _years = np.arange(_baseline_total.size)
    fig_q1, _ax = plt.subplots(figsize=(8, 4))
    _ax.plot(_years, _baseline_total, lw=2, label="Baseline")
    _ax.plot(_years, _intervention_total, lw=2, label="Intervention")
    _ax.set(xlabel="Year", ylabel="Total abundance", title="Question 1: baseline vs intervention")
    _ax.legend()
    sns.despine()
    fig_q1.tight_layout()
    fig_q1
    return


@app.cell
def _(lambda_base, lambda_intervention, mo):
    _delta = lambda_intervention - lambda_base
    _pct = 100.0 * (lambda_intervention / lambda_base - 1.0)
    mo.md(
        rf"Intervention gives $\lambda = {lambda_intervention:.4f}$ (change $\Delta\lambda = {_delta:.4f}$, {_pct:.2f}% vs baseline)."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Periodic environmental forcing (deterministic)

    Every $k$ years, we apply a deterministic bad year that reduces juvenile survival and fertility.
    """)
    return


@app.cell
def _(mo):
    bad_period_ui = mo.ui.slider(2, 12, step=1, value=4, label="Bad-year period (years)")
    bad_juvenile_ui = mo.ui.slider(
        0.40, 1.00, step=0.01, value=0.80, label="Bad-year juvenile survival multiplier"
    )
    bad_fertility_ui = mo.ui.slider(
        0.40, 1.00, step=0.01, value=0.90, label="Bad-year fertility multiplier"
    )
    mo.hstack([bad_period_ui, bad_juvenile_ui, bad_fertility_ui], justify="start", gap=1.0)
    return bad_fertility_ui, bad_juvenile_ui, bad_period_ui


@app.cell
def _(
    bad_fertility_ui,
    bad_juvenile_ui,
    bad_period_ui,
    init_vectors,
    long_run_growth_factor,
    project_periodic_bad_years,
    stage_summary,
    years_ui,
):
    periodic_traj, periodic_total, _, _ = project_periodic_bad_years(
        stage_summary,
        init_vectors["Stable"],
        years_ui.value,
        bad_period_ui.value,
        bad_juvenile_ui.value,
        bad_fertility_ui.value,
    )
    periodic_growth = long_run_growth_factor(periodic_total)
    return periodic_growth, periodic_total, periodic_traj


@app.cell
def _(A_base, init_vectors, np, periodic_total, plt, project_population, sns):
    _, _baseline_total = project_population(A_base, init_vectors["Stable"], len(periodic_total) - 1)
    _years = np.arange(periodic_total.size)

    fig_periodic, _ax = plt.subplots(figsize=(8, 4))
    _ax.plot(_years, _baseline_total, lw=2, label="Baseline")
    _ax.plot(_years, periodic_total, lw=2, label="Periodic bad years")
    _ax.set(xlabel="Year", ylabel="Total abundance", title="Deterministic periodic stress")
    _ax.legend()
    sns.despine()
    fig_periodic.tight_layout()
    fig_periodic
    return


@app.cell
def _(mo, periodic_growth):
    mo.md(rf"Estimated long-run multiplicative growth under periodic forcing: **{periodic_growth:.4f}**")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Scientific question 2

    Under repeated bad years, where is the recovery-vs-decline threshold?
    """)
    return


@app.cell
def _(
    init_vectors,
    long_run_growth_factor,
    np,
    pd,
    project_periodic_bad_years,
    stage_summary,
    years_ui,
):
    _period_grid = np.arange(2, 13, 1)
    _severity_grid = np.linspace(0.40, 1.00, 13)

    _rows = []
    for _period in _period_grid:
        for _severity in _severity_grid:
            _, _tot, _, _ = project_periodic_bad_years(
                stage_summary,
                init_vectors["Stable"],
                years_ui.value,
                _period,
                _severity,
                1.0,
            )
            _growth = long_run_growth_factor(_tot)
            _rows.append(
                {
                    "bad_period": _period,
                    "juvenile_survival_multiplier": _severity,
                    "growth_factor": _growth,
                }
            )

    threshold_df = pd.DataFrame(_rows)
    threshold_pivot = threshold_df.pivot(
        index="juvenile_survival_multiplier", columns="bad_period", values="growth_factor"
    )
    return threshold_df, threshold_pivot


@app.cell
def _(threshold_df, threshold_frontier):
    threshold_frontier_df = threshold_frontier(threshold_df)
    threshold_frontier_df
    return (threshold_frontier_df,)


@app.cell
def _(plt, sns, threshold_pivot):
    fig_threshold, _ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(
        threshold_pivot.sort_index(ascending=False),
        cmap="RdYlGn",
        center=1.0,
        vmin=threshold_pivot.min().min(),
        vmax=threshold_pivot.max().max(),
        cbar_kws={"label": "Long-run growth factor"},
        ax=_ax,
    )
    _ax.set(
        xlabel="Bad-year period (years)",
        ylabel="Bad-year juvenile survival multiplier",
        title="Question 2: recovery (green) vs decline (red)",
    )
    fig_threshold.tight_layout()
    fig_threshold
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Limitations and extensions

    1. This model is density independent.
    2. It is a one-sex approximation.
    3. Process and observation uncertainty are not modeled explicitly.
    4. A natural extension is stochastic forcing and Bayesian inference on vital rates.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # References

    1. Caswell, H. (2001). *Matrix Population Models*.
    2. MALDDABA preprint (bioRxiv): https://www.biorxiv.org/content/10.1101/2025.07.01.662579v1
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Colophon

    Notebook: `notebooks/age-structure.py`.
    Data snapshots: `data/orca_life_table.csv`, `data/orca_demographic_metric.csv`, `data/orca_data_used.csv`.
    """)
    return


if __name__ == "__main__":
    app.run()
