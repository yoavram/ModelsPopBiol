from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = REPO_ROOT / "notebooks"
if str(NOTEBOOK_DIR) not in sys.path:
    sys.path.insert(0, str(NOTEBOOK_DIR))

from age_structure_model import (  # noqa: E402
    behavioral_checks,
    build_lefkovitch_matrix,
    clean_life_table,
    dominant_demography,
    load_orca_data,
    make_init_vectors,
    matrix_checks,
    project_periodic_bad_years,
    summarize_stages,
    threshold_frontier,
)


def main() -> int:
    lt_raw, metric_raw, data_used_raw = load_orca_data()
    lt_clean, data_checks = clean_life_table(lt_raw)
    stage_summary = summarize_stages(lt_clean)
    matrix_a = build_lefkovitch_matrix(stage_summary)
    lambda_dom, stable_stage, _ = dominant_demography(matrix_a)
    matrix_check_df = matrix_checks(matrix_a, stable_stage, lambda_dom)
    behavior_df = behavioral_checks(stage_summary)
    init_vectors = make_init_vectors(stable_stage, 4000.0)

    _, total_good, _, _ = project_periodic_bad_years(
        stage_summary, init_vectors["Stable"], 120, 4, 0.8, 0.9
    )
    _, total_bad, _, _ = project_periodic_bad_years(
        stage_summary, init_vectors["Stable"], 120, 2, 0.5, 0.7
    )

    threshold_rows = []
    for period in range(2, 13):
        for severity in [0.4, 0.6, 0.8, 1.0]:
            _, totals, _, _ = project_periodic_bad_years(
                stage_summary, init_vectors["Stable"], 120, period, severity, 1.0
            )
            growth = totals[-1] / totals[-2]
            threshold_rows.append(
                {
                    "bad_period": period,
                    "juvenile_survival_multiplier": severity,
                    "growth_factor": growth,
                }
            )
    frontier_df = threshold_frontier(pd.DataFrame(threshold_rows))

    assert data_checks["pass"].all(), data_checks
    assert matrix_check_df["pass"].all(), matrix_check_df
    assert behavior_df["pass"].all(), behavior_df
    assert len(lt_clean) == 91, len(lt_clean)
    assert stage_summary["duration"].sum() == len(lt_clean), stage_summary
    assert lambda_dom > 1.0, lambda_dom
    assert total_bad[-1] < total_good[-1], (total_bad[-1], total_good[-1])
    assert frontier_df["bad_period"].nunique() == 11, frontier_df
    assert not metric_raw.empty
    assert not data_used_raw.empty

    print("age-structure validation passed")
    print(f"lambda={lambda_dom:.6f}")
    print(stage_summary[["stage", "duration", "annual_survival", "fecundity"]].to_string(index=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
