
import { useEffect, useState } from "react";
import {
  Activity,
  AlertCircle,
  CheckCircle2,
  ChevronDown,
  Clock3,
  HeartPulse,
  LoaderCircle,
  Plus,
  RefreshCw,
  ShieldCheck,
  Stethoscope,
  Waves,
  Zap,
} from "lucide-react";
import "./App.css";

const API = "http://127.0.0.1:8000";

type Patient = {
  age: number | null;
  bmi: number | null;
  sbp: number | null;
  dbp: number | null;
  imt_max: number | null;
  lvmi: number | null;
  ef: number | null;
  gender: string;
  smoker: string;
};

type EventRecord = {
  version: number;
  timestamp: string;
  event_type: string;
  payload: Record<string, unknown>;
};

type Twin = {
  patient_id: string;
  version: number;
  created_at: string;
  updated_at: string;
  clinical_state: Patient;
  physiological_state: {
    heart_rate_bpm?: number;
    mean_rr_ms?: number;
    sdnn_ms?: number;
    rmssd_ms?: number;
    source?: string;
  };
  prediction: Record<string, unknown> | null;
  history: EventRecord[];
};

const initialPatient: Patient = {
  age: 60,
  bmi: 27,
  sbp: 145,
  dbp: 90,
  imt_max: 0.9,
  lvmi: 110,
  ef: 60,
  gender: "M",
  smoker: "No",
};

const fieldLabels: Record<string, string> = {
  age: "Age",
  bmi: "BMI",
  sbp: "Systolic BP",
  dbp: "Diastolic BP",
  imt_max: "Maximum IMT",
  lvmi: "LV mass index",
  ef: "Ejection fraction",
};

function display(value: unknown, suffix = "") {
  if (value === null || value === undefined || value === "") return "—";
  return `${String(value)}${suffix}`;
}

function timeLabel(value?: string) {
  if (!value) return "Not available";
  return new Date(value).toLocaleString();
}

function getErrorMessage(error: unknown) {
  return error instanceof Error ? error.message : "Something went wrong";
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  let response: Response;

  try {
    response = await fetch(`${API}${path}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options?.headers,
      },
    });
  } catch {
    throw new Error(
      "Cannot connect to the backend. Check that FastAPI is running at 127.0.0.1:8000.",
    );
  }

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    const detail = data.detail;
    throw new Error(
      typeof detail === "string"
        ? detail
        : `Request failed with status ${response.status}`,
    );
  }

  return data as T;
}

export default function App() {
  const [patientId, setPatientId] = useState("DEMO-001");
  const [form, setForm] = useState<Patient>(initialPatient);
  const [twin, setTwin] = useState<Twin | null>(null);
  const [apiOnline, setApiOnline] = useState(false);
  const [busy, setBusy] = useState("");
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [heartRate, setHeartRate] = useState(76);
  const [sdnn, setSdnn] = useState(42);
  const [rmssd, setRmssd] = useState(31);

  useEffect(() => {
    let active = true;

    const checkApiHealth = async () => {
      try {
        const result = await request<{
          success: boolean;
          model_loaded: boolean;
          digital_twin_engine_loaded: boolean;
        }>("/api/health");

        if (active) {
          setApiOnline(
            result.success &&
              result.model_loaded &&
              result.digital_twin_engine_loaded,
          );
        }
      } catch {
        if (active) {
          setApiOnline(false);
        }
      }
    };

    void checkApiHealth();

    return () => {
      active = false;
    };
  }, []);

  const runAction = async (label: string, action: () => Promise<void>) => {
    setBusy(label);
    setError("");
    setNotice("");

    try {
      await action();
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setBusy("");
    }
  };

  const loadTwin = async () => {
    const id = patientId.trim();
    if (!id) throw new Error("Enter a patient ID first.");

    const result = await request<{ twin: Twin }>(
      `/api/twins/${encodeURIComponent(id)}`,
    );

    setTwin(result.twin);
    setForm(result.twin.clinical_state);
    setNotice("Digital Twin state refreshed.");
  };

  const createTwin = () =>
    runAction("create", async () => {
      const id = patientId.trim();
      if (!id) throw new Error("Enter a patient ID first.");

      const result = await request<{ twin: Twin; message: string }>(
        `/api/twins/${encodeURIComponent(id)}`,
        {
          method: "POST",
          body: JSON.stringify(form),
        },
      );

      setTwin(result.twin);
      setNotice(result.message);
    });

  const refreshTwin = () =>
    runAction("refresh", async () => {
      await loadTwin();
    });

  const predict = () =>
    runAction("predict", async () => {
      const id = patientId.trim();
      if (!id) throw new Error("Enter a patient ID first.");

      if (!twin || twin.patient_id !== id) {
        const result = await request<{ twin: Twin }>(
          `/api/twins/${encodeURIComponent(id)}`,
        );
        setTwin(result.twin);
      }

      const result = await request<{ twin: Twin; disclaimer: string }>(
        `/api/twins/${encodeURIComponent(id)}/predict`,
        { method: "POST" },
      );

      setTwin(result.twin);
      setNotice("Exploratory model prediction completed.");
    });

  const updatePhysiology = () =>
    runAction("physiology", async () => {
      const id = patientId.trim();
      if (!twin || twin.patient_id !== id) {
        throw new Error("Create or load this patient's Digital Twin first.");
      }

      const result = await request<{ twin: Twin }>(
        `/api/twins/${encodeURIComponent(id)}/physiology`,
        {
          method: "POST",
          body: JSON.stringify({
            heart_rate_bpm: heartRate,
            mean_rr_ms: Math.round(60000 / heartRate),
            sdnn_ms: sdnn,
            rmssd_ms: rmssd,
            source: "demo_simulation",
          }),
        },
      );

      setTwin(result.twin);
      setNotice("Simulated physiological observation added to the twin.");
    });

  const prediction = twin?.prediction;
  const score = Number(
    prediction?.exploratory_score ??
      prediction?.probability ??
      prediction?.risk_probability,
  );
  const hasScore = Number.isFinite(score);
  const scorePercent = hasScore ? `${(score * 100).toFixed(1)}%` : "—";

  const predictionClass =
    prediction?.prediction ?? prediction?.predicted_class;
  const hasPrediction =
    predictionClass !== undefined && predictionClass !== null;

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">
            <HeartPulse size={25} strokeWidth={2.2} />
          </div>
          <div>
            <div className="brand-name">TwinPulse</div>
            <div className="brand-caption">CARDIOVASCULAR DIGITAL TWIN</div>
          </div>
        </div>

        <div className="side-section-label">WORKSPACE</div>
        <div className="side-link active">
          <Activity size={18} />
          <span>Patient overview</span>
        </div>
        <div className="side-link">
          <Waves size={18} />
          <span>Physiological state</span>
          <span className="side-tag">DEMO</span>
        </div>
        <div className="side-link">
          <ShieldCheck size={18} />
          <span>Risk assessment</span>
        </div>

        <div className="sidebar-bottom">
          <div className="research-mark">
            <Stethoscope size={18} />
            <div>
              <strong>Research prototype</strong>
              <span>Not for clinical decisions</span>
            </div>
          </div>
          <div className="sidebar-footer">TwinPulse · Challenge 2026</div>
        </div>
      </aside>

      <main className="main-area">
        <header className="topbar">
          <div className="breadcrumb">
            <span>Workspace</span>
            <span className="crumb-separator">/</span>
            <strong>Patient overview</strong>
          </div>
          <div className="topbar-right">
            <span className={`status-pill ${apiOnline ? "online" : "offline"}`}>
              <span className="status-dot" />
              {apiOnline ? "API connected" : "API unavailable"}
            </span>
            <button
              className="icon-button"
              title="Check backend status"
              onClick={() => {
                void (async () => {
                  try {
                    const result = await request<{
                      success: boolean;
                      model_loaded: boolean;
                      digital_twin_engine_loaded: boolean;
                    }>("/api/health");

                    setApiOnline(
                      result.success &&
                        result.model_loaded &&
                        result.digital_twin_engine_loaded,
                    );
                  } catch {
                    setApiOnline(false);
                  }
                })();
              }}
            >
              <RefreshCw size={17} />
            </button>
          </div>
        </header>

        <div className="page-content">
          <section className="page-heading">
            <div>
              <div className="eyebrow">DIGITAL HEALTH · RESEARCH ENVIRONMENT</div>
              <h1>Patient overview</h1>
              <p>
                Explore a virtual patient state and its experimental model output.
              </p>
            </div>
            <div className="research-chip">
              <span className="research-chip-dot" />
              Research mode
            </div>
          </section>

          <section className="notice-banner">
            <div className="notice-icon">
              <AlertCircle size={19} />
            </div>
            <div>
              <strong>Research prototype — not clinically validated</strong>
              <p>
                Model outputs are experimental and must not be used for diagnosis,
                treatment, or medical decisions.
              </p>
            </div>
          </section>

          {error && (
            <div className="feedback error-feedback" role="alert">
              <AlertCircle size={17} />
              <span>{error}</span>
              <button onClick={() => setError("")}>Dismiss</button>
            </div>
          )}

          {notice && (
            <div className="feedback success-feedback" role="status">
              <CheckCircle2 size={17} />
              <span>{notice}</span>
              <button onClick={() => setNotice("")}>Dismiss</button>
            </div>
          )}

          <section className="overview-grid">
            <article className="metric-card">
              <div className="metric-top">
                <span>Digital Twin state</span>
                <div className="metric-icon purple">
                  <Activity size={18} />
                </div>
              </div>
              <div className="metric-value">
                {twin ? "Active" : "Not loaded"}
              </div>
              <div className="metric-foot">
                <span className={`tiny-dot ${twin ? "green-dot" : ""}`} />
                {twin ? `Version ${twin.version}` : "Create or load a patient"}
              </div>
            </article>

            <article className="metric-card">
              <div className="metric-top">
                <span>Heart rate</span>
                <div className="metric-icon rose">
                  <HeartPulse size={18} />
                </div>
              </div>
              <div className="metric-value">
                {display(twin?.physiological_state?.heart_rate_bpm)}
                <span className="metric-unit">
                  {twin?.physiological_state?.heart_rate_bpm != null
                    ? " bpm"
                    : ""}
                </span>
              </div>
              <div className="metric-foot">Most recent recorded observation</div>
            </article>

            <article className="metric-card">
              <div className="metric-top">
                <span>Model output</span>
                <div className="metric-icon blue">
                  <ShieldCheck size={18} />
                </div>
              </div>
              <div className="metric-value">
                {hasScore ? scorePercent : "Pending"}
              </div>
              <div className="metric-foot">Exploratory model score</div>
            </article>

            <article className="metric-card">
              <div className="metric-top">
                <span>State events</span>
                <div className="metric-icon amber">
                  <Clock3 size={18} />
                </div>
              </div>
              <div className="metric-value">{twin?.history?.length ?? 0}</div>
              <div className="metric-foot">Recorded twin updates</div>
            </article>
          </section>

          <section className="content-grid">
            <article className="panel patient-panel">
              <div className="panel-heading">
                <div>
                  <div className="panel-kicker">PATIENT RECORD</div>
                  <h2>Clinical profile</h2>
                  <p>Enter clinical values to create a virtual patient.</p>
                </div>
                <div className="panel-heading-icon">
                  <Stethoscope size={20} />
                </div>
              </div>

              <label className="input-label" htmlFor="patient-id">
                Patient identifier
              </label>
              <div className="patient-id-row">
                <input
                  id="patient-id"
                  value={patientId}
                  onChange={(e) => setPatientId(e.target.value)}
                  placeholder="e.g. DEMO-001"
                />
                <button
                  className="button button-secondary button-square"
                  onClick={() => void refreshTwin()}
                  disabled={!!busy}
                  title="Load existing patient"
                >
                  {busy === "refresh" ? (
                    <LoaderCircle className="spin" size={17} />
                  ) : (
                    <RefreshCw size={17} />
                  )}
                </button>
              </div>

              <div className="form-grid">
                {(
                  [
                    ["age", 18, 120, 1],
                    ["bmi", 10, 100, 0.1],
                    ["sbp", 50, 300, 1],
                    ["dbp", 30, 200, 1],
                    ["imt_max", 0, 5, 0.01],
                    ["lvmi", 0, 1000, 1],
                    ["ef", 0, 100, 1],
                  ] as const
                ).map(([key, min, max, step]) => (
                  <div className="form-field" key={key}>
                    <label htmlFor={key}>{fieldLabels[key]}</label>
                    <input
                      id={key}
                      type="number"
                      min={min}
                      max={max}
                      step={step}
                      value={form[key] ?? ""}
                      onChange={(e) =>
                        setForm((previous) => ({
                          ...previous,
                          [key]:
                            e.target.value === ""
                              ? null
                              : Number(e.target.value),
                        }))
                      }
                    />
                  </div>
                ))}

                <div className="form-field">
                  <label htmlFor="gender">Gender</label>
                  <select
                    id="gender"
                    value={form.gender}
                    onChange={(e) =>
                      setForm({ ...form, gender: e.target.value })
                    }
                  >
                    <option value="M">Male (M)</option>
                    <option value="F">Female (F)</option>
                  </select>
                </div>

                <div className="form-field">
                  <label htmlFor="smoker">Smoking status</label>
                  <select
                    id="smoker"
                    value={form.smoker}
                    onChange={(e) =>
                      setForm({ ...form, smoker: e.target.value })
                    }
                  >
                    <option value="No">No</option>
                    <option value="Yes">Yes</option>
                    <option value="Unknown">Unknown</option>
                  </select>
                </div>
              </div>

              <div className="form-actions">
                <button
                  className="button button-primary"
                  onClick={() => void createTwin()}
                  disabled={!!busy || !apiOnline}
                >
                  {busy === "create" ? (
                    <LoaderCircle className="spin" size={17} />
                  ) : (
                    <Plus size={17} />
                  )}
                  Create Digital Twin
                </button>
              </div>
            </article>

            <div className="right-stack">
              <article className="panel prediction-panel">
                <div className="panel-heading">
                  <div>
                    <div className="panel-kicker">EXPERIMENTAL INFERENCE</div>
                    <h2>Risk model output</h2>
                  </div>
                  <div className="panel-heading-icon blue">
                    <Zap size={20} />
                  </div>
                </div>

                <div className="prediction-score">
                  <div>
                    <div className="score-label">Exploratory score</div>
                    <div className="score-number">{scorePercent}</div>
                  </div>
                  <div className="score-symbol">
                    <Activity size={23} />
                  </div>
                </div>

                <div className="score-track">
                  <div
                    className="score-fill"
                    style={{
                      width: `${hasScore ? Math.min(100, Math.max(0, score * 100)) : 0}%`,
                    }}
                  />
                </div>

                <div className="score-scale">
                  <span>0%</span>
                  <span>100%</span>
                </div>

                <div className="prediction-result">
                  <span>Model class</span>
                  <strong>
                    {hasPrediction ? String(predictionClass) : "No prediction"}
                  </strong>
                </div>

                <div className="prediction-result">
                  <span>Model</span>
                  <strong>
                    {String(
                      prediction?.model ??
                        prediction?.model_name ??
                        "Logistic Regression",
                    )}
                  </strong>
                </div>

                <button
                  className="button button-primary full-button"
                  onClick={() => void predict()}
                  disabled={!!busy || !apiOnline || !twin}
                >
                  {busy === "predict" ? (
                    <LoaderCircle className="spin" size={17} />
                  ) : (
                    <Zap size={17} />
                  )}
                  Run exploratory prediction
                </button>

                <p className="micro-disclaimer">
                  This score is not clinically validated and must not guide
                  diagnosis or treatment. It is not a calibrated clinical risk.
                </p>
              </article>

              <article className="panel physiology-panel">
                <div className="panel-heading">
                  <div>
                    <div className="panel-kicker">SIMULATED INPUT</div>
                    <h2>Physiological state</h2>
                    <p>Update the twin with demo observations.</p>
                  </div>
                  <div className="panel-heading-icon rose">
                    <Waves size={20} />
                  </div>
                </div>

                <div className="physiology-control">
                  <div>
                    <label htmlFor="heart-rate">Heart rate</label>
                    <strong>
                      {heartRate} <small>bpm</small>
                    </strong>
                  </div>
                  <input
                    id="heart-rate"
                    type="range"
                    min="40"
                    max="150"
                    value={heartRate}
                    onChange={(e) => setHeartRate(Number(e.target.value))}
                  />
                </div>

                <div className="physiology-control">
                  <div>
                    <label htmlFor="sdnn">SDNN</label>
                    <strong>
                      {sdnn} <small>ms</small>
                    </strong>
                  </div>
                  <input
                    id="sdnn"
                    type="range"
                    min="5"
                    max="150"
                    value={sdnn}
                    onChange={(e) => setSdnn(Number(e.target.value))}
                  />
                </div>

                <div className="physiology-control">
                  <div>
                    <label htmlFor="rmssd">RMSSD</label>
                    <strong>
                      {rmssd} <small>ms</small>
                    </strong>
                  </div>
                  <input
                    id="rmssd"
                    type="range"
                    min="5"
                    max="150"
                    value={rmssd}
                    onChange={(e) => setRmssd(Number(e.target.value))}
                  />
                </div>

                <button
                  className="button button-secondary full-button"
                  onClick={() => void updatePhysiology()}
                  disabled={!!busy || !twin || !apiOnline}
                >
                  {busy === "physiology" ? (
                    <LoaderCircle className="spin" size={17} />
                  ) : (
                    <Waves size={17} />
                  )}
                  Add simulated observation
                </button>
                <p className="micro-disclaimer">
                  Demo values only. These controls do not read a wearable or
                  process a live ECG stream.
                </p>
              </article>
            </div>
          </section>

          <section className="panel state-panel">
            <div className="panel-heading">
              <div>
                <div className="panel-kicker">DIGITAL TWIN ENGINE</div>
                <h2>Patient state &amp; activity</h2>
                <p>
                  {twin
                    ? `Last updated ${timeLabel(twin.updated_at)}`
                    : "Create or load a patient to view the state and activity log."}
                </p>
              </div>
              <button
                className="button button-secondary"
                onClick={() => void refreshTwin()}
                disabled={!!busy || !apiOnline}
              >
                <RefreshCw size={16} />
                Refresh state
              </button>
            </div>

            <div className="state-summary">
              <div className="state-summary-item">
                <span>Patient ID</span>
                <strong>{twin?.patient_id ?? "—"}</strong>
              </div>
              <div className="state-summary-item">
                <span>State version</span>
                <strong>{twin?.version ?? "—"}</strong>
              </div>
              <div className="state-summary-item">
                <span>Created</span>
                <strong>{twin ? timeLabel(twin.created_at) : "—"}</strong>
              </div>
              <div className="state-summary-item">
                <span>Physiology source</span>
                <strong>
                  {twin?.physiological_state?.source === "demo_simulation"
                    ? "Demo simulation"
                    : twin?.physiological_state?.source ?? "Not recorded"}
                </strong>
              </div>
            </div>

            <div className="subheading-row">
              <h3>Clinical measurements</h3>
              <span>Current twin state</span>
            </div>

            <div className="clinical-values">
              {Object.entries(fieldLabels).map(([key, label]) => (
                <div className="clinical-value" key={key}>
                  <span>{label}</span>
                  <strong>
                    {display(
                      twin?.clinical_state?.[key as keyof Patient],
                      key === "bmi"
                        ? " kg/m²"
                        : key === "sbp" || key === "dbp"
                          ? " mmHg"
                          : key === "imt_max"
                            ? " mm"
                            : key === "ef"
                              ? "%"
                              : "",
                    )}
                  </strong>
                </div>
              ))}
            </div>

            <div className="subheading-row history-heading">
              <h3>Recent activity</h3>
              <span>{twin?.history?.length ?? 0} events</span>
            </div>

            {!twin?.history?.length ? (
              <div className="empty-state">
                <div className="empty-icon">
                  <Clock3 size={22} />
                </div>
                <strong>No activity yet</strong>
                <p>Create a Digital Twin to begin recording state changes.</p>
              </div>
            ) : (
              <div className="history-list">
                {[...twin.history].reverse().map((event) => (
                  <div
                    className="history-row"
                    key={`${event.version}-${event.timestamp}`}
                  >
                    <div className="history-icon">
                      {event.event_type === "prediction_update" ? (
                        <Zap size={17} />
                      ) : event.event_type === "physiological_update" ? (
                        <Waves size={17} />
                      ) : (
                        <Activity size={17} />
                      )}
                    </div>
                    <div className="history-details">
                      <strong>{event.event_type.replaceAll("_", " ")}</strong>
                      <span>{timeLabel(event.timestamp)}</span>
                    </div>
                    <div className="history-version">v{event.version}</div>
                    <ChevronDown className="history-chevron" size={16} />
                  </div>
                ))}
              </div>
            )}
          </section>

          <footer className="page-footer">
            <div>
              <HeartPulse size={16} />
              <span>TwinPulse</span>
              <span className="footer-separator">·</span>
              <span>Digital Twin Challenge 2026</span>
            </div>
            <span>Research &amp; educational prototype</span>
          </footer>
        </div>
      </main>
    </div>
  );
}
