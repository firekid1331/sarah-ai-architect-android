#!/usr/bin/env python3
"""Fail-closed complete inventory SHA256 verifier; never modifies source."""
import csv
import hashlib
import pathlib
import re
import sys

# Reject redirection before resolving the verifier's own path.
VERIFIER_PATH = pathlib.Path(__file__).absolute()
if VERIFIER_PATH.is_symlink() or (VERIFIER_PATH.parent).is_symlink():
    raise SystemExit('SOURCE_MANIFEST FAIL: symlinked verifier path')
ROOT = VERIFIER_PATH.parent.parent
if ROOT.is_symlink():
    raise SystemExit('SOURCE_MANIFEST FAIL: symlinked source root')
MANIFEST = ROOT / 'SHA256_MANIFEST.csv'
MAX_MANIFEST = 256 * 1024
MAX_FILES = 4096
MAX_FILE_BYTES = 100 * 1024 * 1024
# Exclusions are exact known generated roots, never arbitrary nested components.
SAFE_GENERATED = ('app/build/', '.gradle/', '.git/', '.idea/', '.pytest_cache/',)
ALLOWED_ROOT_FILES = {'.gitignore', 'README.md', 'settings.gradle', 'build.gradle', 'gradle.properties'}
ALLOWED_TREES = {'app', 'audit_harness', 'docs', 'tests', 'tools', 'reference', '.github'}

def permitted(rel):
    if rel == 'SHA256_MANIFEST.csv': return False
    if rel == 'local.properties' or rel.endswith('/local.properties'):
        raise ValueError('local.properties forbidden in committed input: ' + rel)
    # Filename/path policy only: does not claim to detect secrets in arbitrary contents.
    lower = rel.casefold()
    components = lower.split('/')
    forbidden_suffixes = ('.jks', '.keystore', '.p12', '.pfx', '.pem', '.key', '.pk8', '.asc',
                          '.p8', '.p7b', '.p7c', '.p7m', '.p7s', '.p10', '.p11', '.p12',
                          '.pfx', '.der', '.crt', '.cer', '.mobileprovision')
    forbidden_names = {'local.properties', 'key.properties', 'keystore.properties',
                       '.env', '.env.local', 'credentials.json', 'service-account.json',
                       'id_rsa', 'id_ed25519', 'known_hosts'}
    # Bounded policy: filename aliases and backup forms are forbidden even if hashed.
    forbidden_aliases = ('signing.properties', 'google-services.json', 'aws-credentials.ini')
    def sensitive_component(c):
        if c.startswith('.env.') or c in forbidden_aliases:
            return True
        if c.startswith(('service-account-', 'credentials-', 'credential-', 'aws-credentials.')) and c.endswith(('.json', '.ini', '.properties', '.yaml', '.yml')):
            return True
        if c.startswith(('key.properties.', 'keystore.properties.', 'signing.properties.')):
            return True
        # Strip *all* chained backup suffixes; reject sensitive originals.
        stripped = c
        backup_suffixes = ('.bak', '.backup', '.old', '.orig', '.save', '.tmp', '.bkp', '.copy', '.swp', '.swo', '.swx', '.disabled', '.temp', '~')
        for _ in range(32):
            matched = next((suffix for suffix in backup_suffixes if stripped.endswith(suffix)), None)
            if matched is None:
                numbered = re.search(r'(?:\.(?:old|bak|backup|bkp|copy|save|tmp|orig)\.[0-9]{1,8}|\.[0-9]{1,8})$', stripped)
                if numbered: matched = numbered.group(0)
                if matched is None:
                    numbered = re.search(r'(?:\.(?:bak|backup|bkp|copy|old|save|tmp|orig)[_-]?[0-9]{1,8}|\.(?:bak|backup|bkp|copy|old|save|tmp|orig)[_-]?[0-9]{4}[-_][0-9]{2}[-_][0-9]{2})$', stripped)
                    if numbered: matched = numbered.group(0)
            if not matched: break
            stripped = stripped[:-len(matched)]
            if stripped.endswith(forbidden_suffixes) or stripped in forbidden_names or stripped in forbidden_aliases or stripped.startswith('.env.') or stripped.startswith(('service-account-', 'credentials-', 'credential-', 'aws-credentials.')):
                return True
        else:
            raise ValueError('excessive backup suffix nesting')
        return False
    if any(sensitive_component(c) for c in components):
        raise ValueError('credential alias or backup forbidden: ' + rel)
    if any(c in {'.android', '.ssh', 'secrets', 'credentials', 'private-keys'} for c in components) or \
       any(c in forbidden_names for c in components) or lower.endswith(forbidden_suffixes):
        raise ValueError('signing/credential-like path forbidden: ' + rel)
    if any(c.casefold() == '__pycache__' or c.casefold().endswith(('.pyc', '.pyo')) for c in rel.split('/')):
        raise ValueError('executable Python cache forbidden: ' + rel)
    if any(rel == prefix[:-1] or rel.startswith(prefix) for prefix in SAFE_GENERATED):
        return False
    return True


def inventory():
    result = {}
    for p in ROOT.rglob('*'):
        rel = p.relative_to(ROOT).as_posix()
        if not permitted(rel):
            continue
        if not (rel in ALLOWED_ROOT_FILES or rel.split('/')[0] in ALLOWED_TREES):
            raise ValueError('unapproved source tree: ' + rel)
        if p.is_symlink():
            raise ValueError('symlink in source: ' + rel)
        if p.is_dir():
            continue
        if not p.is_file():
            raise ValueError('nonregular source: ' + rel)
        if p.stat().st_size > MAX_FILE_BYTES:
            raise ValueError('oversized source: ' + rel)
        result[rel] = hashlib.sha256(p.read_bytes()).hexdigest()
        if len(result) > MAX_FILES:
            raise ValueError('too many source files')
    return result


def verify():
    if len(sys.argv) == 3 and sys.argv[1] == '--expected-root':
        expected = pathlib.Path(sys.argv[2]).absolute()
        if expected.is_symlink() or expected != ROOT or expected.resolve() != ROOT.resolve():
            raise ValueError('expected source root mismatch')
    elif len(sys.argv) != 1:
        raise ValueError('usage: verify_source_manifest.py [--expected-root ABSOLUTE_CHECKOUT]')
    if not MANIFEST.is_file() or MANIFEST.is_symlink() or MANIFEST.stat().st_size > MAX_MANIFEST:
        raise ValueError('manifest absent, symlinked or oversized')
    with MANIFEST.open(newline='', encoding='utf-8-sig') as f:
        rows = csv.reader(f, strict=True)
        if next(rows, None) != ['path', 'sha256']:
            raise ValueError('invalid manifest header')
        entries = {}
        for row in rows:
            if len(row) != 2:
                raise ValueError('invalid manifest row')
            rel, digest = row
            parts = pathlib.PurePosixPath(rel).parts
            if (not rel or rel.startswith('/') or '\\' in rel or
                any(x in ('.', '..', '') for x in rel.split('/')) or
                pathlib.PurePosixPath(rel).as_posix() != rel or
                not permitted(rel)):
                raise ValueError('unsafe or excluded manifest path: ' + rel)
            if rel in entries:
                raise ValueError('duplicate manifest path: ' + rel)
            if not re.fullmatch(r'[0-9a-f]{64}', digest):
                raise ValueError('invalid SHA256: ' + rel)
            entries[rel] = digest
            if len(entries) > MAX_FILES:
                raise ValueError('too many manifest entries')
    actual = inventory()
    if set(entries) != set(actual):
        raise ValueError('inventory mismatch missing=' + repr(sorted(set(actual)-set(entries))) +
                         ' extra=' + repr(sorted(set(entries)-set(actual))))
    bad = sorted(k for k in entries if entries[k] != actual[k])
    if bad:
        raise ValueError('hash mismatch: ' + repr(bad))
    print('SOURCE_MANIFEST PASS files=' + str(len(entries)))


if __name__ == '__main__':
    try:
        verify()
    except (ValueError, OSError, UnicodeError, csv.Error) as exc:
        print('SOURCE_MANIFEST FAIL: ' + str(exc), file=sys.stderr)
        sys.exit(1)
