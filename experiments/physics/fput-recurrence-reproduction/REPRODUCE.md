# Reproduce this result

Everything below runs from the extracted evidence package or from an observatory
checkout. No path in this package depends on the author's home directory; the only
absolute paths you will type are the throwaway `/tmp` locations you choose.

## 0. Verify the package

```sh
tar xzf fput-reproduction-<protocol>-<run>.tar.gz -C /tmp/fput-evidence
cd /tmp/fput-evidence
python3 - <<'PY'
import hashlib, json, pathlib
manifest = json.load(open("MANIFEST.json"))
bad = [m["name"] for m in manifest["members"]
       if hashlib.sha256(pathlib.Path(m["name"]).read_bytes()).hexdigest() != m["sha256"]]
print("members:", len(manifest["members"]), "mismatched:", bad)
PY
grep -rE '/(home|Users|root)/' . && echo 'LEAKED ABSOLUTE PATH' || echo 'no home-directory paths'
```

The same two checks are what `run.py export --check` performs inside the repository.

## 1. Fetch and verify the source figure (optional, for provenance)

The LA-1940 PDF is deliberately **not** included. `environment/README.md` carries its
public URL, DOI, byte size and SHA-256, and the repository's data manifest carries the
exact fetch and verify commands:

```sh
curl -L --fail -o /tmp/la-1940.pdf https://www.osti.gov/servlets/purl/4376203
echo "3155813b1851da4fa6fba5818986718b197d68873d38965f3cd7489c14f396f1  /tmp/la-1940.pdf" | sha256sum -c -
```

`reference/README.md` documents how `reference/la-1940-fig1.png` and
`reference/fig1-digitized.csv` were produced from that PDF, including the
digitization uncertainty.

## 2. Create the environment

The workspace lock that the run used is `environment/uv.lock`; its SHA-256 is recorded
in `run/run.json` (`uv_lock_sha256`) and in `MANIFEST.json`. The baseline itself needs
only NumPy (Matplotlib is used for the figure); `run/run.json` records the exact
versions that produced the archived result.

```sh
uv venv /tmp/fput-repro-env
versions=$(python3 -c 'import json;r=json.load(open("run/run.json"))["runtime"];print(r["numpy"],r["matplotlib"])')
uv pip install --python /tmp/fput-repro-env/bin/python \
  "numpy==${versions% *}" "matplotlib==${versions#* }"
```

`metrics.json` and `energies.csv` depend only on the NumPy version; `figure.png` is a
rendered image and also depends on the Matplotlib version, which is why both are pinned.

To reproduce the whole environment instead of the two packages the runner imports, use
the workspace lock from an observatory checkout: `uv sync --extra research`.

## 3. Run the one baseline command

The runner is `experiments/physics/fput-recurrence-reproduction/run.py` in the
observatory repository at the revision recorded in `run/run.json` (`git_revision`).
`reproduction/commands.txt` lists the exact commands that produced this package.

```sh
git -C <observatory-checkout> checkout <git_revision from run/run.json>
cd <observatory-checkout>
/tmp/fput-repro-env/bin/python experiments/physics/fput-recurrence-reproduction/run.py \
  baseline --output-root /tmp/fput-repro-out
```

The run is deterministic: fixed initial state, no seeds, IEEE-754 float64, no adaptive
stepping. It takes about a second and exits 0 for a completed run, 10 for inconclusive
and 20 for a failed one.

## 4. Compare

```sh
python3 - <<'PY'
import json, pathlib
archived = json.load(open("/tmp/fput-evidence/run/metrics.json"))
fresh_dir = sorted(pathlib.Path("/tmp/fput-repro-out").glob("baseline-*"))[-1]
fresh = json.load(open(fresh_dir / "metrics.json"))
print("identical:", fresh == archived)
for key in ("M1", "M2", "M3", "M4", "C1", "C2", "C3"):
    if fresh[key] != archived[key]:
        print("differs:", key, archived[key], "->", fresh[key])
PY
```

`metrics.json` must match byte-for-byte on the same architecture and NumPy version
(`energies.csv` too; `figure.png` also needs the recorded Matplotlib version).
A difference is a finding, not a nuisance: record it rather than re-running until the
numbers agree. The protocol is frozen (`protocol/v2.md`); a changed method needs a new
protocol version, never an edit to a frozen one.
