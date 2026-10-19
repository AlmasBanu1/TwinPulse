from pathlib import Path

import numpy as np
import pandas as pd
import wfdb

ROOT = Path(r"C:\Projects\TwinPulse\data\raw\SHAREE")
OUTPUT = Path(r"C:\Projects\TwinPulse\ml\data\processed\sharee_hrv_features_v2.csv")

LOWER_RR_MS = 300.0
UPPER_RR_MS = 2000.0
MAX_FILTERED_PERCENT_FOR_GOOD_FLAG = 5.0

rows = []

for hea_path in sorted(ROOT.glob("*.hea")):
    record_id = hea_path.stem
    dat_path = ROOT / f"{record_id}.dat"

    # Process only records whose signal files are available.
    if not dat_path.exists():
        continue

    try:
        header = wfdb.rdheader(str(ROOT / record_id))
        annotation = wfdb.rdann(str(ROOT / record_id), "qrs")

        fs = float(header.fs)
        samples = np.asarray(annotation.sample, dtype=np.int64)

        if fs <= 0 or len(samples) < 3:
            raise ValueError("Invalid sampling frequency or too few annotations")

        # Keep the original ordering; do not compress the sequence before
        # calculating successive RR differences.
        rr_ms = np.diff(samples).astype(float) * 1000.0 / fs

        finite = np.isfinite(rr_ms)
        positive = finite & (rr_ms > 0)
        rr_valid = positive & (
            (rr_ms >= LOWER_RR_MS) & (rr_ms <= UPPER_RR_MS)
        )

        rr_accepted = rr_ms[rr_valid]
        total_rr = len(rr_ms)

        if total_rr == 0 or len(rr_accepted) == 0:
            raise ValueError("No RR intervals within preliminary bounds")

        # Successive metrics only use pairs that were adjacent in the
        # original RR sequence and where both intervals pass the filter.
        valid_pairs = rr_valid[:-1] & rr_valid[1:]
        successive_differences = np.diff(rr_ms)[valid_pairs]

        mean_rr = float(np.mean(rr_accepted))
        median_rr = float(np.median(rr_accepted))

        rows.append({
            "record_id": record_id,
            "sampling_frequency_hz": fs,
            "annotation_count": len(samples),
            "rr_interval_count": total_rr,

            # Descriptive statistics over all positive, finite intervals.
            "median_rr_all_ms": float(np.median(rr_ms[positive])),
            "rr_below_300_percent": float(
                np.mean(rr_ms[positive] < LOWER_RR_MS) * 100
            ),
            "rr_above_2000_percent": float(
                np.mean(rr_ms[positive] > UPPER_RR_MS) * 100
            ),

            # Features from intervals within the preliminary bounds.
            "accepted_rr_count": len(rr_accepted),
            "rr_filtered_percent": float(
                100 * (1 - len(rr_accepted) / total_rr)
            ),
            "mean_hr_bpm": float(60000.0 / mean_rr),
            "median_hr_bpm": float(60000.0 / median_rr),
            "mean_nn_ms": mean_rr,
            "median_nn_ms": median_rr,
            "sdnn_ms": float(np.std(rr_accepted, ddof=1))
                if len(rr_accepted) >= 2 else np.nan,
            "rmssd_ms": float(np.sqrt(np.mean(
                successive_differences ** 2
            ))) if len(successive_differences) else np.nan,
            "pnn50_percent": float(
                np.mean(np.abs(successive_differences) > 50) * 100
            ) if len(successive_differences) else np.nan,
            "valid_successive_pair_count": len(successive_differences),
            "nn_iqr_ms": float(
                np.percentile(rr_accepted, 75)
                - np.percentile(rr_accepted, 25)
            ),

            # This is a heuristic data-quality flag, not a clinical label.
            "quality_flag": (
                "review"
                if 100 * (1 - len(rr_accepted) / total_rr)
                   > MAX_FILTERED_PERCENT_FOR_GOOD_FLAG
                else "preliminary"
            ),
            "annotation_caveat": "QRS annotations are unaudited",
        })

        print(
            f"{record_id}: "
            f"accepted={len(rr_accepted)}/{total_rr}, "
            f"filtered={100 * (1 - len(rr_accepted) / total_rr):.1f}%, "
            f"quality={rows[-1]['quality_flag']}"
        )

    except Exception as exc:
        print(f"{record_id}: ERROR: {exc}")
        rows.append({
            "record_id": record_id,
            "quality_flag": "error",
            "annotation_caveat": str(exc),
        })

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
pd.DataFrame(rows).to_csv(OUTPUT, index=False)

print(f"\nRecords processed: {len(rows)}")
print(f"Output: {OUTPUT}")
