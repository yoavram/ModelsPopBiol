from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


REPO_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = REPO_ROOT / "data"

STAGE_SPEC = pd.DataFrame(
    {
        "stage": ["Juvenile", "Early reproductive", "Prime reproductive", "Older/post"],
        "start_age": [0, 11, 25, 45],
        "end_age": [10, 24, 44, np.nan],
    }
)


def load_orca_data(data_dir: Path | None = None) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    root = DATA_DIR if data_dir is None else Path(data_dir)
    lt_raw = pd.read_csv(root / "orca_life_table.csv")
    metric_raw = pd.read_csv(root / "orca_demographic_metric.csv")
    data_used_raw = pd.read_csv(root / "orca_data_used.csv")
    return lt_raw, metric_raw, data_used_raw


def clean_life_table(lt_raw: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    lt_clean = lt_raw.copy()
    lt_clean["Age"] = lt_clean["Age"].astype(int)
    lt_clean["Sx"] = pd.to_numeric(lt_clean["Sx"], errors="coerce")
    lt_clean["lx"] = pd.to_numeric(lt_clean["lx"], errors="coerce")
    lt_clean["mx"] = pd.to_numeric(lt_clean["mx"], errors="coerce")
    lt_clean = lt_clean.sort_values("Age", kind="mergesort").reset_index(drop=True)
    lt_clean["dx"] = lt_clean["lx"] * (1.0 - lt_clean["Sx"])
    lt_clean["female_births"] = lt_clean["mx"]

    age_diff = np.diff(lt_clean["Age"].to_numpy())
    checks = {
        "age_increases_by_1": bool(np.all(age_diff == 1)),
        "sx_in_unit_interval": bool(((lt_clean["Sx"] >= 0) & (lt_clean["Sx"] <= 1)).all()),
        "lx_nonincreasing": bool(np.all(np.diff(lt_clean["lx"].to_numpy()) <= 1e-12)),
        "mx_nonnegative": bool((lt_clean["mx"] >= 0).all()),
        "no_missing_required": bool(not lt_clean[["Age", "Sx", "lx", "mx"]].isna().any().any()),
    }
    data_checks = pd.DataFrame({"check": list(checks.keys()), "pass": list(checks.values())})
    return lt_clean, data_checks


def summarize_stages(
    lt_clean: pd.DataFrame, stage_spec: pd.DataFrame | None = None
) -> pd.DataFrame:
    spec = STAGE_SPEC if stage_spec is None else stage_spec
    rows: list[dict[str, object]] = []
    max_age = int(lt_clean["Age"].max())

    for _, row in spec.iterrows():
        start_age = int(row["start_age"])
        end_age = max_age if pd.isna(row["end_age"]) else int(row["end_age"])
        mask = (lt_clean["Age"] >= start_age) & (lt_clean["Age"] <= end_age)
        subset = lt_clean.loc[mask]

        rows.append(
            {
                "stage": row["stage"],
                "start_age": start_age,
                "end_age": end_age,
                "duration": int(subset.shape[0]),
                "plus_group": bool(pd.isna(row["end_age"])),
                "annual_survival": float(subset["Sx"].mean()),
                "fecundity": float(subset["female_births"].mean()),
            }
        )

    return pd.DataFrame(rows)


def build_lefkovitch_matrix(
    stage_summary: pd.DataFrame,
    juvenile_survival_mult: float = 1.0,
    adult_survival_mult: float = 1.0,
    maturation_mult: float = 1.0,
    fertility_mult: float = 1.0,
) -> np.ndarray:
    n_stage = stage_summary.shape[0]
    matrix_a = np.zeros((n_stage, n_stage), dtype=float)

    survival = stage_summary["annual_survival"].to_numpy(dtype=float)
    fecundity = stage_summary["fecundity"].to_numpy(dtype=float)
    duration = stage_summary["duration"].to_numpy(dtype=float)

    survival_eff = survival.copy()
    survival_eff[0] *= juvenile_survival_mult
    if n_stage > 1:
        survival_eff[1:] *= adult_survival_mult
    survival_eff = np.clip(survival_eff, 0.0, 1.0)

    fecundity_eff = np.clip(fecundity * fertility_mult, 0.0, None)
    matrix_a[0, :] = fecundity_eff

    for j in range(n_stage - 1):
        base_gamma = 1.0 / max(1.0, duration[j])
        gamma = base_gamma * (maturation_mult if j == 0 else 1.0)
        gamma = float(np.clip(gamma, 0.0, 1.0))

        matrix_a[j, j] = survival_eff[j] * (1.0 - gamma)
        matrix_a[j + 1, j] = survival_eff[j] * gamma

    matrix_a[-1, -1] = survival_eff[-1]
    return matrix_a


def dominant_demography(matrix_a: np.ndarray) -> tuple[float, np.ndarray, np.ndarray]:
    eigvals, eigvecs = np.linalg.eig(matrix_a)
    idx = int(np.argmax(eigvals.real))
    lambda_dom = float(eigvals[idx].real)

    stable = np.real(eigvecs[:, idx]).astype(float)
    if stable.sum() < 0:
        stable *= -1.0
    stable = np.abs(stable)
    stable = stable / stable.sum()

    left_vals, left_vecs = np.linalg.eig(matrix_a.T)
    idx_left = int(np.argmax(left_vals.real))
    reproductive = np.real(left_vecs[:, idx_left]).astype(float)
    if np.dot(reproductive, stable) < 0:
        reproductive *= -1.0
    reproductive = reproductive / np.dot(reproductive, stable)
    return lambda_dom, stable, reproductive


def project_population(
    matrix_a: np.ndarray, n0_vector: np.ndarray | list[float], n_years: int
) -> tuple[np.ndarray, np.ndarray]:
    n_years = int(n_years)
    traj = np.zeros((n_years + 1, matrix_a.shape[0]), dtype=float)
    traj[0, :] = np.array(n0_vector, dtype=float)

    for t in range(n_years):
        traj[t + 1, :] = matrix_a @ traj[t, :]

    total = traj.sum(axis=1)
    return traj, total


def project_periodic_bad_years(
    stage_summary: pd.DataFrame,
    n0_vector: np.ndarray | list[float],
    n_years: int,
    bad_period: int,
    bad_juvenile_mult: float,
    bad_fertility_mult: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    good = build_lefkovitch_matrix(stage_summary)
    bad = build_lefkovitch_matrix(
        stage_summary,
        juvenile_survival_mult=bad_juvenile_mult,
        adult_survival_mult=1.0,
        maturation_mult=1.0,
        fertility_mult=bad_fertility_mult,
    )

    n_years = int(n_years)
    traj = np.zeros((n_years + 1, good.shape[0]), dtype=float)
    traj[0, :] = np.array(n0_vector, dtype=float)

    period = int(bad_period)
    for t in range(n_years):
        use_bad = period > 0 and ((t + 1) % period == 0)
        matrix_t = bad if use_bad else good
        traj[t + 1, :] = matrix_t @ traj[t, :]

    total = traj.sum(axis=1)
    return traj, total, good, bad


def long_run_growth_factor(total_series: np.ndarray | list[float]) -> float:
    vals = np.clip(np.asarray(total_series, dtype=float), 1e-12, None)
    log_diff = np.diff(np.log(vals))
    if log_diff.size == 0:
        return float("nan")
    start = log_diff.size // 2
    return float(np.exp(log_diff[start:].mean()))


def finite_sensitivity_elasticity(
    matrix_a: np.ndarray, rel_eps: float = 1e-6
) -> tuple[np.ndarray, np.ndarray]:
    lambda_base, _, _ = dominant_demography(matrix_a)
    sens = np.full_like(matrix_a, np.nan, dtype=float)
    elas = np.full_like(matrix_a, np.nan, dtype=float)

    for i in range(matrix_a.shape[0]):
        for j in range(matrix_a.shape[1]):
            if matrix_a[i, j] <= 0:
                continue
            delta = matrix_a[i, j] * rel_eps
            a_pert = matrix_a.copy()
            a_pert[i, j] += delta
            lambda_pert, _, _ = dominant_demography(a_pert)
            s_ij = (lambda_pert - lambda_base) / delta
            sens[i, j] = s_ij
            elas[i, j] = s_ij * matrix_a[i, j] / lambda_base

    return sens, elas


def make_init_vectors(stable_stage: np.ndarray, n0: float) -> dict[str, np.ndarray]:
    init_compositions = {
        "Stable": stable_stage,
        "Juvenile-heavy": np.array([0.70, 0.20, 0.08, 0.02]),
        "Older-heavy": np.array([0.05, 0.15, 0.35, 0.45]),
    }
    return {name: n0 * vec / vec.sum() for name, vec in init_compositions.items()}


def matrix_checks(matrix_a: np.ndarray, stable_stage: np.ndarray, lambda_dom: float) -> pd.DataFrame:
    checks = {
        "matrix_nonnegative": bool((matrix_a >= 0).all()),
        "lambda_positive_real": bool(np.isfinite(lambda_dom) and lambda_dom > 0),
        "stable_stage_nonnegative": bool((stable_stage >= 0).all()),
        "stable_stage_sums_to_1": bool(np.isclose(stable_stage.sum(), 1.0)),
    }
    return pd.DataFrame({"check": list(checks.keys()), "pass": list(checks.values())})


def behavioral_checks(stage_summary: pd.DataFrame, years: int = 120, n0: float = 4000.0) -> pd.DataFrame:
    matrix_base = build_lefkovitch_matrix(stage_summary)
    lambda_base, stable_stage, _ = dominant_demography(matrix_base)
    init_vectors = make_init_vectors(stable_stage, n0)

    lambda_juvenile, _, _ = dominant_demography(
        build_lefkovitch_matrix(stage_summary, juvenile_survival_mult=1.05)
    )
    lambda_adult, _, _ = dominant_demography(
        build_lefkovitch_matrix(stage_summary, adult_survival_mult=1.05)
    )

    _, total_mild, _, _ = project_periodic_bad_years(
        stage_summary, init_vectors["Stable"], years, 6, 0.9, 0.95
    )
    _, total_harsh, _, _ = project_periodic_bad_years(
        stage_summary, init_vectors["Stable"], years, 2, 0.5, 0.7
    )
    growth_mild = long_run_growth_factor(total_mild)
    growth_harsh = long_run_growth_factor(total_harsh)

    _, stable_total = project_population(matrix_base, init_vectors["Stable"], years)
    _, juvenile_total = project_population(matrix_base, init_vectors["Juvenile-heavy"], years)

    checks = {
        "juvenile_survival_increase_non_decreasing_lambda": bool(lambda_juvenile >= lambda_base),
        "adult_survival_increase_non_decreasing_lambda": bool(lambda_adult >= lambda_base),
        "more_frequent_harsher_bad_years_do_not_help_growth": bool(growth_harsh <= growth_mild),
        "different_initial_composition_changes_short_run": bool(
            not np.isclose(stable_total[5], juvenile_total[5])
        ),
    }
    return pd.DataFrame({"check": list(checks.keys()), "pass": list(checks.values())})


def threshold_frontier(threshold_df: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, float]] = []
    for bad_period, subset in threshold_df.groupby("bad_period", sort=True):
        recovering = subset.loc[subset["growth_factor"] >= 1.0].sort_values(
            "juvenile_survival_multiplier"
        )
        threshold = float(recovering["juvenile_survival_multiplier"].min()) if not recovering.empty else np.nan
        rows.append(
            {
                "bad_period": float(bad_period),
                "minimum_recovery_juvenile_survival_multiplier": threshold,
            }
        )
    return pd.DataFrame(rows)
