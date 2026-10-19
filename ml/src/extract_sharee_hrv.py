from pathlib import Path
import csv
import numpy as np
import wfdb

ROOT = Path(r"C:\Projects\TwinPulse\data\raw\SHAREE")
OUT = Path(r"C:\Projects\TwinPulse\ml\data\processed\sharee_hrv_features.csv")

RECORD_IDS = [
    "01911", "02012", "02019", "02020", "02025",
    "02033", "02059", "02068", "02069", "02108",
    "02119", "02121", "02136", "02148", "02184",
    "02185", "02218", "02289", "02294", "02304",
    "02339", "02348", "02373", "02403", "02412",
]

MIN_RR_MS = 300.0
MAX_RR_MS = 2000.0


def calculate_features(record_id):
    header = wfdb.rdheader(str(ROOT / record_id))
    ann = wfdb.rdann(str(ROOT / record_id), "qrs")

    fs = float(header.fs)
    signal_length = int(header.sig_len)

    samples = np.asarray(ann.sample, dtype=np.int64)
    in_bounds = (samples >= 0) & (samples < signal_length)
    samples = samples[in_bounds]

    rr_ms = np.diff(samples) / fs * 1000.0
    plausible = (
        np.isfinite(rr_ms)
        & (rr_ms >= MIN_RR_MS)
        & (rr_ms <= MAX_RR_MS)
    )
    clean_rr = rr_ms[plausible]

    row = {
        "record_id": record_id,
        "sampling_frequency_hz": fs,
        "record_duration_hours": signal_length / fs / 3600.0,
        "annotation_count": len(ann.sample),
        "rr_interval_count": len(rr_ms),
        "rr_valid_count": len(clean_rr),
        "rr_filtered_count": int(len(rr_ms) - len(clean_rr)),
        "rr_filtered_percent": (
            100.0 * (len(rr_ms) - len(clean_rr)) / len(rr_ms)
            if len(rr_ms) else np.nan
        ),
    }

    if len(clean_rr) < 2:
        for key in [
            "mean_hr_bpm", "median_hr_bpm", "mean_nn_ms",
            "sdnn_ms", "rmssd_ms", "pnn50_percent",
            "median_nn_ms", "nn_iqr_ms",
        ]:
            row[key] = np.nan
        row["status"] = "insufficient_valid_rr"
        return row

    # HRV features are computed only on intervals passing the range filter.
    # SDNN/RMSSD are preliminary estimates: gaps caused by filtering are not
    # reconstructed, and results require cautious interpretation.
    successive_differences = np.diff(clean_rr)

    row.update({
        "mean_hr_bpm": float(np.mean(60000.0 / clean_rr)),
        "median_hr_bpm": float(60000.0 / np.median(clean_rr)),
        "mean_nn_ms": float(np.mean(clean_rr)),
        "median_nn_ms": float(np.median(clean_rr)),
        "sdnn_ms": float(np.std(clean_rr, ddof=1)),
        "rmssd_ms": float(np.sqrt(np.mean(successive_differences ** 2))),
        "pnn50_percent": float(
            100.0 * np.mean(np.abs(successive_differences) > 50.0)
        ),
        "nn_iqr_ms": float(
            np.percentile(clean_rr, 75) - np.percentile(clean_rr, 25)
        ),
        "status": "ok",
    })
    return row


def main():
    rows = []
    for record_id in RECORD_IDS:
        try:
            row = calculate_features(record_id)
            rows.append(row)
            print(
                f"{record_id}: status={row['status']}, "
                f"valid RR={row['rr_valid_count']}, "
                f"filtered={row['rr_filtered_percent']:.2f}%"
            )
        except Exception as exc:
            print(f"{record_id}: ERROR: {exc}")

    if not rows:
        raise RuntimeError("No feature rows were generated.")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    columns = list(dict.fromkeys(key for row in rows for key in row))
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nRecords processed: {len(rows)} / {len(RECORD_IDS)}")
    print(f"Output: {OUT}")


if __name__ == "__main__":
    main()
