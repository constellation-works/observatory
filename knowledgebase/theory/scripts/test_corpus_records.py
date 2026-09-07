"""Whole-owner scientific preservation and native activation regressions."""
from collections import Counter
from copy import deepcopy
import datetime as dt
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import corpus_records as corpus
import wide_binary_records as pilot
from orbit_research import validate, protocol_digest
from orbit_research.contract import reference, revision_digest
from orbit_research.native import Owner
from test_wide_binary_records import pointer


class CorpusTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest, cls.active, cls.records = corpus.read_history(corpus.ROOT)
        cls.by = {corpus.key(r): r for r in cls.records}
        cls.views = corpus.project(corpus.ROOT, cls.active, cls.active, cls.records)

    def record(self, ref):
        return self.by[corpus.refkey(ref)]

    def test_complete_exact_scientific_roundtrip(self):
        self.assertEqual(len(self.active['programs']), 10)
        self.assertEqual(len(self.active['protocols']), 4)
        self.assertEqual(len(self.views), 110)
        for path, data in self.views.items():
            self.assertEqual(data, (corpus.ROOT / path).read_bytes(), path)
            self.assertEqual(data, corpus.git(corpus.ROOT, 'show', f'{corpus.BASE}:{path}'), path)
            self.assertEqual(data, corpus.git(corpus.ROOT, 'show', f'{pilot.BASE}:{path}'), path)
        self.assertEqual(set(corpus.local_paths(corpus.ROOT)),
                         {s['path'] for s in self.manifest['sources'] if s['repository'] == 'principia'})
        statuses = Counter()
        for slug, entry in self.active['programs'].items():
            original = json.loads(self.views[f'theory/{slug}/claims.json'])
            for row, cr, ar in zip(original['claims'], entry['claims'], entry['assessments']):
                claim, assessment = self.record(cr), self.record(ar)
                self.assertEqual(row, claim['legacy'])
                self.assertEqual(row['claim'], claim['payload']['statement'])
                self.assertEqual(row['status'], assessment['payload']['legacy_verdict'])
                self.assertEqual(assessment['payload']['inference'], 'historical')
                self.assertEqual(assessment['payload']['claim'], cr)
                statuses[row['status']] += 1
        self.assertEqual(statuses, dict(supported=45, mixed=26, refuted=23, untested=18, conjecture=9))

    def test_every_source_field_and_prose_span_is_located(self):
        by_source = {}
        for item in self.manifest['accounting']:
            source = self.record(item['source'])['legacy']['text']
            selector = item['selector']
            if selector == '$bytes':
                value = source
            elif selector.startswith('text:'):
                _, a, b = selector.split(':')
                value = source[int(a):int(b)]
            else:
                value = pointer(json.loads(source), selector)
            target = pointer(self.record(item['target']), item['pointer'])
            if item.get('decode') == 'json':
                target = pointer(json.loads(target), selector)
            elif selector.startswith('text:'):
                target = target[int(a):int(b)]
            self.assertEqual(value, target, selector)
            self.assertEqual(corpus.digest(corpus.encoded(value)), item['value_digest'])
            by_source.setdefault(corpus.refkey(item['source']), []).append(selector)
        for item in self.manifest['sources']:
            record = json.loads((corpus.ROOT / corpus.AUTHORITY / item['record']).read_bytes())
            selectors = by_source[corpus.key(record)]
            self.assertIn('$bytes', selectors)
            if item['repository'] == 'principia' and item['path'].endswith('.json'):
                self.assertLessEqual({p for p, _ in pilot.leaves(json.loads(record['legacy']['text']))}, set(selectors))
            elif item['path'].endswith('.md'):
                spans = [tuple(map(int, s.split(':')[1:])) for s in selectors if s.startswith('text:')]
                self.assertEqual(spans[0][0], 0)
                self.assertEqual(spans[-1][1], len(record['legacy']['text']))
                self.assertTrue(all(a[1] == b[0] for a, b in zip(spans, spans[1:])))

    def test_retirement_and_refutation_do_not_erase_verdicts(self):
        for slug, entry in self.active['programs'].items():
            raw = json.loads(self.views[f'theory/{slug}/claims.json'])
            program = self.record(entry['program'])
            if raw['status'] in {'retired', 'refuted', 'resolved'}:
                self.assertEqual(raw['live_fronts'], [])
                self.assertEqual(program['activity'], {'retired': 'retired', 'refuted': 'paused', 'resolved': 'resolved'}[raw['status']])
            for cr in entry['claims']:
                c = self.record(cr)
                if c['legacy']['kind'] == 'postulate':
                    self.assertEqual(c['payload']['role'], 'postulate')
                    self.assertIn('expires', c['legacy'])
                    self.assertNotEqual(c['legacy']['status'], 'supported')
        wall = json.loads(self.views['schema/wall.json'])['refuted_ids']
        claims = {self.record(r)['aliases'][0]: self.record(r) for e in self.active['programs'].values() for r in e['claims']}
        self.assertEqual(len(wall), 18)
        self.assertTrue(all(claims[c]['legacy']['status'] == 'refuted' for c in wall))
        self.assertEqual(sum(bool(json.loads(self.views[f'theory/{s}/claims.json'])['live_fronts']) for s in self.active['programs']), 2)

    def test_conditional_model_scope_and_failed_controls_stay_limited(self):
        for r in self.records:
            self.assertEqual(validate(r), [], r['id'])
            if r['kind'] == 'assessment':
                self.assertEqual(r['payload']['inference'], 'historical')
            if r['kind'] == 'protocol':
                self.assertEqual(r['payload']['freeze'], 'historical-unverified')
                self.assertIsNone(r['payload']['frozen_at'])
                self.assertEqual(r['revision_id'], protocol_digest(r['payload']['semantic']))
                changed = deepcopy(r['payload']['semantic'])
                changed['test_changed_normative_control'] = 'different comparator'
                self.assertNotEqual(r['revision_id'], protocol_digest(changed))
        mixed = [self.record(r) for r in self.active['programs'][pilot.FAMILY]['assessments']]
        self.assertEqual([r['payload']['controls'] for r in mixed], ['failed'] * 4 + ['passed'])
        # Complete conditional hypotheses, control_ran and domain restrictions survive
        # as exact legacy fields and source prose (also checked individually above).
        text = self.views['theory/two-substance-vortex-vacuum/photon-mode-obstruction.md'].decode()
        self.assertIn('conditional', text.lower())

    def test_missing_evidence_never_becomes_reconciled(self):
        self.assertEqual(len(self.manifest['pending_reconciliation']), 78)
        for pending in self.manifest['pending_reconciliation']:
            self.assertIsNone(pending['id'])
            self.assertIsNone(pending['revision_id'])
            self.assertEqual(pending['status'], 'pending')
        for link in self.manifest['links']:
            self.assertEqual(link['status'], 'pending')
            self.assertTrue(link['selector'])
        for path in ('source-manifest.json', 'archival-manifest.json'):
            self.assertEqual(validate(json.loads((corpus.ROOT / corpus.AUTHORITY / path).read_bytes())), [])

    def test_policy_behavior_survives_on_projected_records(self):
        checker = corpus.policy()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for path, data in self.views.items():
                out = root / path
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(data)
            docs, gates, errors, wall = checker.load_corpus(root)
            self.assertFalse(errors)
            external = checker.external_roots(corpus.ROOT)
            self.assertFalse(checker.check_docs(root, docs, dt.date(2026, 9, 6), external))
            def reject(mutate, expected, cross=False, date=dt.date(2026, 9, 6)):
                d, g, w = deepcopy(docs), deepcopy(gates), deepcopy(wall)
                mutate(d, g, w)
                errors = checker.check_cross(d, g, w, root) if cross else checker.check_docs(root, d, date, external)
                self.assertIn(expected, '\n'.join(errors))
            reject(lambda d,g,w: d[0].update(live_fronts=['forbidden']), 'must have empty live_fronts')
            reject(lambda d,g,w: d[0]['claims'][0].update(family='another-family'), 'not in doc families')
            reject(lambda d,g,w: d[0]['claims'][0].update(links=['../../studies/missing-source.md']), 'link does not resolve')
            reject(lambda d,g,w: w['refuted_ids'].append('missing-wall-id'), 'wall id missing-wall-id missing', cross=True)
            # Active named postulate, supported hook without its coupling-off control.
            def alter_kind(d,g,w,kind,**changes):
                c = next(c for doc in d if doc['status'] == 'exploratory' for c in doc['claims'] if c['kind'] == kind)
                c.update(changes)
            reject(lambda d,g,w: alter_kind(d,g,w,'postulate',status='supported'), 'a postulate cannot be supported')
            reject(lambda d,g,w: alter_kind(d,g,w,'postulate',expires='2020-01-01'), 'postulate expired')
            reject(lambda d,g,w: alter_kind(d,g,w,'hook',status='supported',control_ran=False), 'hook cannot be supported')

    def test_native_source_activation_and_rollback_preserve_all_appends(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            subprocess.run(['git', '-C', str(root), '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                            'commit', '-q', '--allow-empty', '-m', 'fixture'], check=True)
            path = f'theory/{pilot.FAMILY}/related.md'
            data = self.views[path] + b'\n<!-- Native owner workflow fixture: no scientific changes. -->\n'
            locator = f'research/content/{corpus.digest(data)[7:]}.md'
            content = root / locator
            content.parent.mkdir(parents=True)
            content.write_bytes(data)
            request = dict(request_id='native-source-fixture', id='native-source-fixture', expected_heads=[],
                reason='Exercise future native prose authoring without altering historical objects.', scope='literature',
                payload=dict(role='source', availability='available', snapshot_digest=corpus.digest(data), locator=locator, media_type='text/markdown'),
                references=[self.active['sources'][path]], orbit_links=[dict(host='fixture', workspace='fixture', task='fixture', run='fixture')])
            req = root / 'request.json'
            req.write_bytes(corpus.encoded(request))
            cmd = [sys.executable, '-m', 'orbit_research', 'artifact', '--owner-root', str(root), '--repository', 'principia', '--request', str(req)]
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            native = json.loads(result.stdout)
            self.assertEqual(native['schema_version'], 2)
            self.assertIsNone(native['legacy'])
            self.assertEqual(json.loads(subprocess.run(cmd, check=True, capture_output=True, text=True).stdout), native)
            active = deepcopy(self.active)
            active['sources'][path] = reference(native)
            views = corpus.project(root, active, self.active, self.records)
            self.assertEqual(views[path], data)
            before = {p: p.read_bytes() for p in (root / 'research').rglob('*') if p.is_file()}
            rollback = corpus.project(root, self.active, self.active, self.records)
            self.assertEqual(rollback, self.views)
            self.assertEqual(before, {p: p.read_bytes() for p in (root / 'research').rglob('*') if p.is_file()})
            content.write_bytes(data + b'corruption')
            with self.assertRaisesRegex(ValueError, 'source digest mismatch'):
                corpus.project(root, active, self.active, self.records)

    def test_activation_cannot_drop_identity_or_reopen_closed_work(self):
        changed = deepcopy(self.active)
        del changed['programs']['gravity-as-scarcity']
        with self.assertRaisesRegex(ValueError, 'retain every programs'):
            corpus.project(corpus.ROOT, changed, self.active, self.records)
        changed = deepcopy(self.active)
        changed['programs'][pilot.FAMILY]['claims'][0]['revision_id'] = 'sha256:' + '0' * 64
        with self.assertRaisesRegex(ValueError, 'missing'):
            corpus.project(corpus.ROOT, changed, self.active, self.records)
        # A valid framework record still cannot reactivate a retired program.
        ref = self.active['programs']['gravity-as-scarcity']['program']
        record = deepcopy(self.record(ref))
        record['activity'] = 'active'
        record['legacy']['status'] = 'exploratory'
        record['revision_id'] = revision_digest(record)
        self.assertEqual(validate(record), [])
        changed = deepcopy(self.active)
        changed['programs']['gravity-as-scarcity']['program'] = reference(record)
        with self.assertRaisesRegex(ValueError, 'cannot reactivate'):
            corpus.project(corpus.ROOT, changed, self.active, self.records + [record])

    def test_native_claim_and_assessment_generate_both_views(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            subprocess.run(['git', '-C', str(root), '-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                            'commit', '-q', '--allow-empty', '-m', 'fixture'], check=True)
            owner = Owner(root, 'principia')
            original = self.active['programs'][pilot.FAMILY]
            old = self.record(original['claims'][0])
            common = dict(expected_heads=[], scope='synthetic-calibration',
                          reason='Native fixture only; no live science is authored.',
                          orbit_links=[dict(host='fixture', workspace='fixture', task='fixture', run='fixture')])
            claim = owner.apply('claim', dict(common, request_id='claim-fixture', id=old['aliases'][0],
                payload=dict(old['payload'], statement=old['payload']['statement'] + ' Fixture-only qualification.'),
                references=[original['claims'][0]]))
            assessment = owner.apply('assess', dict(common, request_id='assessment-fixture', id='assessment-fixture',
                payload=dict(claim=reference(claim), verdict='inconclusive', legacy_verdict=None,
                    inference='exploratory', controls='failed', basis='scientific-evidence',
                    rationale='Fixture: controls remain unresolved; no new evidence.', evidence=[], evidence_summary='inconclusive')))
            active = deepcopy(self.active)
            active['programs'][pilot.FAMILY]['claims'][0] = reference(claim)
            active['programs'][pilot.FAMILY]['assessments'][0] = reference(assessment)
            projected = corpus.project(root, active, self.active, self.records)
            row = json.loads(projected[pilot.CLAIMS])['claims'][0]
            self.assertEqual(row['claim'], claim['payload']['statement'])
            self.assertEqual(row['status'], 'mixed')
            self.assertEqual(row['evidence'], assessment['payload']['rationale'])
            self.assertIn(row['claim'], projected[f'{pilot.THEORY}/evidence-ledger.md'].decode())
            self.assertIn(row['evidence'], projected[f'{pilot.THEORY}/evidence-ledger.md'].decode())
            self.assertEqual(self.record(original['claims'][0]), old)
            self.assertEqual(corpus.project(root, self.active, self.active, self.records), self.views)
            bad = owner.apply('assess', dict(common, request_id='bad-control-fixture', id='bad-control-fixture',
                payload=dict(assessment['payload'], verdict='supported', evidence_summary='supports')))
            active['programs'][pilot.FAMILY]['assessments'][0] = reference(bad)
            with self.assertRaisesRegex(ValueError, 'failed or unrun controls'):
                corpus.project(root, active, self.active, self.records)

    def test_source_commit_mapping_and_view_corruption_fail_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(corpus.ROOT / 'research', root / 'research')
            for path, data in self.views.items():
                out = root / path
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_bytes(data)
            source_path = root / corpus.AUTHORITY / self.manifest['sources'][0]['record']
            original = source_path.read_bytes()
            for member, suffix, message in [('text', 'changed source', 'source bytes changed'),
                                             ('commit_object', 'changed metadata', 'commit object changed')]:
                source = json.loads(original)
                source['legacy'][member] += suffix
                source_path.write_bytes(corpus.encoded(source))
                with self.assertRaisesRegex(ValueError, message):
                    corpus.read_history(root)
                source_path.write_bytes(original)
            manifest_path = root / corpus.AUTHORITY / 'migration.json'
            original = manifest_path.read_bytes()
            manifest = json.loads(original)
            manifest['accounting'][0]['pointer'] = '/not-the-original-location'
            manifest_path.write_bytes(corpus.encoded(manifest))
            with self.assertRaisesRegex(ValueError, 'immutable mapping drift'):
                corpus.read_history(root)
            manifest_path.write_bytes(original)
            view = root / 'schema/wall.json'
            view.write_bytes(b'{"refuted_ids": []}\n')
            with self.assertRaisesRegex(ValueError, 'compatibility drift'):
                corpus.inspect(root)
            view.write_bytes(self.views['schema/wall.json'])
            (root / 'studies/unaccounted.md').write_text('Unregistered science.\n')
            with self.assertRaisesRegex(ValueError, 'unaccounted scientific file'):
                corpus.inspect(root)

    def test_rollback_export_is_exact_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / 'rollback'
            pilot.export(corpus.ROOT, target, self.views)
            self.assertEqual({p.relative_to(target).as_posix(): p.read_bytes() for p in target.rglob('*') if p.is_file()}, self.views)
            with self.assertRaisesRegex(ValueError, 'must not exist'):
                pilot.export(corpus.ROOT, target, self.views)


if __name__ == '__main__':
    unittest.main()
