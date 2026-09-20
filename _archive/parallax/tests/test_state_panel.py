"""Offline tests for the R03 state covariate panel. No network."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

import pytest

from parallax.consumer_goods.data import state_panel as sp


def test_state_coverage_is_fifty_states_plus_dc():
    assert len(sp.STATE_FIPS) == 51
    assert len(sp.FIPS_STATE) == 51
    assert sp.STATE_FIPS["CA"] == "06"
    assert sp.FIPS_STATE["36"] == "NY"


def test_laus_series_id_layout():
    series = sp.laus_series_id("AL", seasonally_adjusted=True)
    assert series == "LASST010000000000003"
    assert len(series) == 20
    assert sp.laus_series_id("AL", seasonally_adjusted=False).startswith("LAUST01")
    assert sp.laus_series_id("CA")[5:7] == "06"


def _laus_payload() -> bytes:
    document = {
        "status": "REQUEST_SUCCEEDED",
        "Results": {
            "series": [
                {
                    "seriesID": "LASST060000000000003",
                    "data": [
                        {"year": "2024", "period": "M02", "value": "5.3"},
                        {"year": "2024", "period": "M01", "value": "5.2"},
                        {"year": "2024", "period": "M13", "value": "5.25"},
                    ],
                }
            ]
        },
    }
    return json.dumps(document).encode()


def test_parse_laus_extracts_months_and_drops_annual_average():
    rows = sp.parse_laus(_laus_payload())
    assert len(rows) == 2, "M13 is the annual average and must not enter a monthly panel"
    assert {r["month"] for r in rows} == {1, 2}
    assert all(r["usps"] == "CA" for r in rows)
    assert rows[0]["unemployment_rate"] == 5.3


def test_parse_laus_concatenated_chunks():
    combined = _laus_payload() + b"\n" + _laus_payload()
    assert len(sp.parse_laus(combined)) == 4


# The three fixtures below are shaped from the *live* 2026-08-04 BLS payload, not from
# json.dumps(). json.dumps() emits newline-free JSON; the real API does not, and the original
# newline-splitting parser passed its tests and failed on first contact with real data.
_REAL_SHAPED_LAUS = (
    b'{"status":"REQUEST_SUCCEEDED","responseTime":258,"message":[],"Results":{\n'
    b'"series":\n'
    b'[{"seriesID":"LASST060000000000003","data":['
    b'{"year":"2026","period":"M06","periodName":"June","latest":"true","value":"5.2",'
    b'"footnotes":[{"code":"P","text":"Preliminary."}]},'
    b'{"year":"2026","period":"M05","periodName":"May","value":"-","footnotes":[{}]},'
    b'{"year":"2025","period":"M12","periodName":"December","value":"5.4",'
    b'"footnotes":[{"code":"R","text":"Data were subject to revision on April 8, 2026."}]}'
    b"]}]\n}}"
)


def test_parse_laus_handles_newlines_inside_the_json():
    """Live responses embed newlines in the document; splitting on them shreds it."""
    rows = sp.parse_laus(_REAL_SHAPED_LAUS)
    assert len(rows) == 3
    assert all(r["usps"] == "CA" for r in rows)


def test_parse_laus_maps_the_dash_sentinel_to_none():
    """BLS writes "-" for suppressed observations. float() raises; 0.0 would silently bias."""
    rows = {(r["year"], r["month"]): r for r in sp.parse_laus(_REAL_SHAPED_LAUS)}
    assert rows[(2026, 5)]["unemployment_rate"] is None
    assert rows[(2026, 6)]["unemployment_rate"] == 5.2


def test_parse_laus_carries_vintage_footnotes():
    """Latest-vintage values include revisions nobody knew at the time — lookahead bias."""
    rows = {(r["year"], r["month"]): r for r in sp.parse_laus(_REAL_SHAPED_LAUS)}
    assert rows[(2026, 6)]["preliminary"] is True and rows[(2026, 6)]["revised"] is False
    assert rows[(2025, 12)]["revised"] is True and rows[(2025, 12)]["preliminary"] is False


def test_iter_concatenated_json_is_delimiter_independent():
    payload = _REAL_SHAPED_LAUS + b"\n\n  " + _REAL_SHAPED_LAUS + _REAL_SHAPED_LAUS
    assert len(list(sp.iter_concatenated_json(payload))) == 3
    assert len(sp.parse_laus(payload)) == 9


def test_parse_laus_raises_on_failed_request():
    bad = json.dumps({"status": "REQUEST_NOT_PROCESSED", "message": ["rate limited"]}).encode()
    with pytest.raises(ValueError, match="BLS request failed"):
        sp.parse_laus(bad)


def test_parse_acs_derives_female_share_and_skips_territories():
    header = ["NAME", *sp.ACS_VARIABLES.keys(), "state"]
    body = [
        ["California", "39000000", "37.0", "19000000", "20000000", "91000", "06"],
        ["Puerto Rico", "3200000", "43.0", "1500000", "1700000", "22000", "72"],
    ]
    rows = sp.parse_acs(json.dumps([header, *body]).encode(), year=2023)
    assert len(rows) == 1
    row = rows[0]
    assert row["usps"] == "CA" and row["year"] == 2023
    assert row["median_age"] == 37.0
    assert row["female_share"] == pytest.approx(20 / 39)


def test_parse_acs_maps_census_null_sentinel_to_none():
    header = ["NAME", *sp.ACS_VARIABLES.keys(), "state"]
    body = [["Wyoming", "580000", "38.0", "290000", "290000", "-666666666", "56"]]
    row = sp.parse_acs(json.dumps([header, *body]).encode(), year=2023)[0]
    assert row["median_household_income"] is None
    assert row["female_share"] == pytest.approx(0.5)


# Fixtures below are written as explicit literals laid out by the *documented* byte positions in
# NOAA's state-readme.txt, deliberately not built by a helper that mirrors the parser. A helper
# would encode the same assumption the parser does, so the test would pass whether or not the
# layout was right -- which is exactly how the original 2-character DIVISION bug survived.
#
#            1-3        4          5-6        7-10        11-17 ...
#            STATE   DIVISION   ELEMENT      YEAR        JAN ... DEC  (f7.2, right justified)
_CA_2024_TEMP = (
    "0040022024  48.30  52.10  55.00  58.90  63.20  68.40  73.10  73.80  70.20  63.50  54.10 -99.90"
)
_CA_2024_PRECIP = (
    "0040012024   3.10   2.80   2.20   1.10   0.40   0.10   0.00   0.10   0.30   0.90   1.80   2.60"
)
_CA_DIVISION_3 = (
    "0043022024  40.00  41.00  42.00  43.00  44.00  45.00  46.00  47.00  48.00  49.00  50.00  51.00"
)


def test_climdiv_fixture_matches_documented_field_positions():
    """Pin the fixture itself against the readme, so a bad fixture cannot mask a bad parser."""
    assert _CA_2024_TEMP[0:3] == "004"  # STATE-CODE, positions 1-3
    assert _CA_2024_TEMP[3:4] == "0"  # DIVISION-NUMBER, position 4 -- one character
    assert _CA_2024_TEMP[4:6] == "02"  # ELEMENT-CODE, positions 5-6
    assert _CA_2024_TEMP[6:10] == "2024"  # YEAR, positions 7-10
    assert _CA_2024_TEMP[10:17] == "  48.30"  # JAN-VALUE, positions 11-17
    assert len(_CA_2024_TEMP) == 10 + 12 * 7 == 94  # DEC-VALUE ends at position 94


def test_parse_climdiv_statewide_only_and_missing_sentinel():
    rows = sp.parse_climdiv("\n".join([_CA_2024_TEMP, _CA_DIVISION_3]).encode())
    assert len(rows) == 12, "divisional records must not enter a statewide panel"
    assert rows[0]["temp_f"] == 48.3
    assert rows[0]["month"] == 1 and rows[0]["year"] == 2024
    assert rows[6]["temp_f"] == 73.1, "July must land on the seventh field, not a shifted one"
    assert rows[11]["temp_f"] is None, "-99.90 is the missing sentinel, not a temperature"


def test_parse_climdiv_filters_by_element_code():
    rows = sp.parse_climdiv("\n".join([_CA_2024_TEMP, _CA_2024_PRECIP]).encode())
    assert len(rows) == 12, "precipitation shares the layout and must not be read as temperature"
    assert rows[0]["temp_f"] == 48.3


def test_resolve_climdiv_filename_picks_latest_version():
    listing = b"""
    <a href="climdiv-tmpcst-v1.0.0-20240105">climdiv-tmpcst-v1.0.0-20240105</a>
    <a href="climdiv-tmpcst-v1.0.0-20260105">climdiv-tmpcst-v1.0.0-20260105</a>
    <a href="climdiv-pcpnst-v1.0.0-20260105">climdiv-pcpnst-v1.0.0-20260105</a>
    """
    assert sp.resolve_climdiv_filename(listing) == "climdiv-tmpcst-v1.0.0-20260105"


def test_resolve_climdiv_filename_raises_when_absent():
    with pytest.raises(ValueError, match="no climdiv-tmpcst"):
        sp.resolve_climdiv_filename(b"<html>nothing here</html>")


def test_forward_fill_annual_carries_last_known_vintage():
    annual = [
        {"usps": "CA", "year": 2022, "median_age": 37.0},
        {"usps": "CA", "year": 2023, "median_age": 37.4},
    ]
    rows = sp.forward_fill_annual(annual, 2022, 2024, ["median_age"])
    assert len(rows) == 3 * 12
    by_year = {r["year"]: r["median_age"] for r in rows}
    assert by_year[2022] == 37.0
    assert by_year[2023] == 37.4
    assert by_year[2024] == 37.4, "2024 has no vintage yet; carry 2023 forward"


def test_join_panel_keeps_only_fully_observed_cells():
    left = [{"usps": "CA", "year": 2024, "month": 1, "unemployment_rate": 5.2}]
    right = [
        {"usps": "CA", "year": 2024, "month": 1, "temp_f": 55.0},
        {"usps": "NY", "year": 2024, "month": 1, "temp_f": 31.0},
    ]
    joined = sp.join_panel(left, right)
    assert len(joined) == 1, "NY has temperature but no unemployment; an inner join drops it"
    assert joined[0]["unemployment_rate"] == 5.2 and joined[0]["temp_f"] == 55.0


def test_store_raw_is_immutable(tmp_path: Path):
    artefact = sp.store_raw(tmp_path, "laus", "https://example.test", b"payload", notes="first")
    assert artefact.sha256 == ("239f59ed55e737c77147cf55ad0c1b030b6d7ee748a7426952f9b852d5a935e5")
    assert artefact.n_bytes == 7
    with pytest.raises(FileExistsError):
        sp.store_raw(tmp_path, "laus", "https://example.test", b"different")


def test_store_raw_appends_manifest(tmp_path: Path):
    sp.store_raw(tmp_path, "laus", "https://example.test/a", b"one")
    sp.store_raw(tmp_path, "acs", "https://example.test/b", b"two")
    manifest = (tmp_path / date.today().isoformat() / "manifest.jsonl").read_text()
    entries = [json.loads(line) for line in manifest.splitlines()]
    assert {e["source"] for e in entries} == {"laus", "acs"}
    assert all(e["fetched_on"] == date.today().isoformat() for e in entries)


def test_write_panel_stable_columns(tmp_path: Path):
    rows = [
        {"usps": "CA", "year": 2024, "month": 1, "temp_f": 55.0, "unemployment_rate": 5.2},
        {"usps": "NY", "year": 2024, "month": 1, "temp_f": None, "unemployment_rate": 4.1},
    ]
    target = sp.write_panel(rows, tmp_path / "panel.csv")
    lines = target.read_text().strip().splitlines()
    assert lines[0] == "usps,year,month,temp_f,unemployment_rate"
    assert lines[2] == "NY,2024,1,,4.1", "missing values write as empty, never as 0"


def test_write_panel_refuses_empty(tmp_path: Path):
    with pytest.raises(ValueError, match="empty panel"):
        sp.write_panel([], tmp_path / "panel.csv")


# ---------------------------------------------------------------------------------------
# CDC obesity
# ---------------------------------------------------------------------------------------


def _cdc_record(**overrides: str) -> dict[str, str]:
    """One record shaped like a live data.cdc.gov row, verified against the API on 2026-08-04.

    Note ``stratificationcategoryid1`` is ``OVR`` while ``stratificationid1`` is ``OVERALL``.
    Transposing the two selects nothing, and an empty obesity column reads downstream as
    'no heterogeneity' rather than as missing data.
    """
    record = {
        "yearstart": "2023",
        "yearend": "2023",
        "locationabbr": "CA",
        "locationdesc": "California",
        "datasource": "Behavioral Risk Factor Surveillance System",
        "question": "Percent of adults aged 18 years and older who have obesity",
        "questionid": "Q036",
        "data_value": "28.1",
        "stratificationcategory1": "Total",
        "stratificationcategoryid1": "OVR",
        "stratificationid1": "OVERALL",
    }
    record.update(overrides)
    return record


def test_parse_cdc_obesity_keeps_overall_stratum_only():
    payload = json.dumps(
        [
            _cdc_record(),
            _cdc_record(stratificationcategoryid1="AGEYR", stratificationid1="AGEYR2534"),
            _cdc_record(stratificationcategoryid1="SEX", stratificationid1="FEMALE"),
            _cdc_record(locationabbr="PR"),
        ]
    ).encode()
    rows = sp.parse_cdc_obesity(payload)
    assert len(rows) == 1, "stratified rows would multiply each state by its stratum count"
    assert rows[0] == {"usps": "CA", "year": 2023, "obesity_prevalence": 28.1}


def test_parse_cdc_obesity_rejects_the_overweight_question():
    """Q037 shares every other field with Q036 and is a different measure."""
    payload = json.dumps(
        [
            _cdc_record(),
            _cdc_record(
                questionid="Q037",
                question="Percent of adults aged 18 years and older who have an "
                "overweight classification",
                data_value="35.0",
            ),
        ]
    ).encode()
    rows = sp.parse_cdc_obesity(payload)
    assert [r["obesity_prevalence"] for r in rows] == [28.1]


def test_parse_cdc_obesity_raises_when_filter_selects_nothing():
    payload = json.dumps([_cdc_record(stratificationid1="MALE")]).encode()
    with pytest.raises(ValueError, match="selecting nothing"):
        sp.parse_cdc_obesity(payload)


def test_parse_cdc_obesity_raises_on_schema_drift():
    payload = json.dumps([{"year": "2023", "state": "CA", "value": "28.1"}]).encode()
    with pytest.raises(ValueError, match="schema changed"):
        sp.parse_cdc_obesity(payload)


def test_parse_cdc_obesity_raises_on_empty():
    with pytest.raises(ValueError, match="confirm the dataset id"):
        sp.parse_cdc_obesity(b"[]")


def test_fetch_acs_requires_a_key():
    """A keyless Census request returns an HTML error page, not JSON. Fail before the parser."""
    with pytest.raises(ValueError, match="requires a key"):
        sp.fetch_acs(2023, api_key=None)


# ---------------------------------------------------------------------------------------
# Guards
# ---------------------------------------------------------------------------------------


def test_climdiv_codes_are_not_fips():
    """The whole point of the mapping: nClimDiv orders states its own way."""
    assert sp.NCLIMDIV_STATE_CODES_VERIFIED is True
    assert len(sp.NCLIMDIV_STATE_CODE_TO_USPS) == 50
    assert sp.NCLIMDIV_STATE_CODE_TO_USPS["002"] == "AZ", (
        "FIPS 02 is Alaska; nClimDiv 002 is Arizona"
    )
    assert sp.NCLIMDIV_STATE_CODE_TO_USPS["004"] == "CA", "FIPS 04 is Arizona; nClimDiv 004 is CA"
    assert sp.NCLIMDIV_STATE_CODE_TO_USPS["050"] == "AK"
    assert sp.NCLIMDIV_STATE_CODE_TO_USPS["049"] == "HI"
    assert "DC" not in set(sp.NCLIMDIV_STATE_CODE_TO_USPS.values()), (
        "the readme's state table has no District of Columbia"
    )
    assert set(sp.NCLIMDIV_STATE_CODE_TO_USPS.values()) == set(sp.STATE_FIPS) - {"DC"}


def test_map_climdiv_drops_regional_aggregates():
    rows = sp.map_climdiv_to_usps(
        [
            {"climdiv_state_code": "004", "year": 2024, "month": 1, "temp_f": 48.3},
            {"climdiv_state_code": "110", "year": 2024, "month": 1, "temp_f": 33.0},
        ]
    )
    assert len(rows) == 1, "110 is the national aggregate, not a state"
    assert rows[0]["usps"] == "CA"
    assert "climdiv_state_code" not in rows[0]


def test_build_from_raw_assembles_laus_and_annual(tmp_path: Path):
    (tmp_path / "laus.raw").write_bytes(_laus_payload())
    header = ["NAME", *sp.ACS_VARIABLES.keys(), "state"]
    body = [["California", "39000000", "37.0", "19000000", "20000000", "91000", "06"]]
    (tmp_path / "acs_2024.raw").write_bytes(json.dumps([header, *body]).encode())

    rows = sp.build_from_raw(tmp_path, 2024, 2024)
    assert len(rows) == 2, "inner join keeps only the two months LAUS observed"
    assert {r["month"] for r in rows} == {1, 2}
    assert all(r["median_age"] == 37.0 for r in rows)
    assert all(r["usps"] == "CA" for r in rows)


def test_build_from_raw_joins_temperature(tmp_path: Path):
    (tmp_path / "laus.raw").write_bytes(_laus_payload())  # California, Jan and Feb 2024
    (tmp_path / "climdiv.raw").write_bytes(_CA_2024_TEMP.encode())
    rows = sp.build_from_raw(tmp_path, 2024, 2024)
    assert len(rows) == 2, "LAUS observed two months; the inner join keeps those"
    assert rows[0]["temp_f"] == 48.3 and rows[0]["unemployment_rate"] == 5.2
    assert rows[1]["temp_f"] == 52.1 and rows[1]["unemployment_rate"] == 5.3


def test_build_from_raw_raises_when_nothing_recognised(tmp_path: Path):
    (tmp_path / "unrelated.txt").write_text("noise")
    with pytest.raises(FileNotFoundError, match="no recognised raw artefacts"):
        sp.build_from_raw(tmp_path, 2024, 2024)
