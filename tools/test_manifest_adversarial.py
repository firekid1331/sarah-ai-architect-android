#!/usr/bin/env python3
"""Independent-process negative verifier checks on isolated source copies."""
import csv
import hashlib
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]

def check(label, mutate, expected=1):
    with tempfile.TemporaryDirectory(prefix='sarah-manifest-') as td:
        target = pathlib.Path(td) / 'source'
        shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns('__pycache__', '*.pyc', '.pytest_cache', 'build', '.gradle'))
        mutate(target)
        result = subprocess.run([sys.executable, '-B', str(target/'tools/verify_source_manifest.py')],
                                cwd=target, capture_output=True, text=True, timeout=20)
        if (result.returncode == 0) != (expected == 0):
            raise AssertionError(label + ': exit=' + str(result.returncode) + ' ' + result.stdout + result.stderr)
        print('PASS', label, 'exit', result.returncode)

def rows(root):
    with (root/'SHA256_MANIFEST.csv').open(newline='') as f:
        return list(csv.reader(f))

def put(root, entries):
    with (root/'SHA256_MANIFEST.csv').open('w', newline='') as f:
        csv.writer(f).writerows(entries)

def altered(root):
    with (root/'app/build.gradle').open('a') as f: f.write('\n// tamper\n')

def added(root):
    (root/'app/src/main/EXTRA.txt').write_text('unlisted')

def missing(root):
    r=rows(root);put(root,r[:-1])

def duplicate(root):
    r=rows(root);put(root,r+[r[1]])

def empty(root):
    (root/'SHA256_MANIFEST.csv').write_text('')

def corrupt(root):
    (root/'SHA256_MANIFEST.csv').write_text('path,sha256\n"unterminated')

def traversal(root):
    r=rows(root);r.append(['../escape', '0'*64]);put(root,r)

def bad_header(root):
    r=rows(root);r[0]=['sha256','path'];put(root,r)

def extra_field(root):
    r=rows(root);r[1].append('extra');put(root,r)

def bad_hash(root):
    r=rows(root);r[1][1]='notsha';put(root,r)

def symlink(root):
    (root/'app/src/main/source-link').symlink_to(root/'README.md')

def ignored_cache(root):
    d=root/'tests/__pycache__';d.mkdir();(d/'foo.pyc').write_bytes(b'cache')

def inject(rel, content=b'attack'):
    def fn(root):
        dest=root/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(content)
    return fn

def signed_with_valid_manifest(rel):
    def fn(root):
        dest = root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(b'SARAH_HOST_ONLY_SENTINEL_NOT_A_KEY')
        manifest = rows(root)
        manifest.append([rel, hashlib.sha256(dest.read_bytes()).hexdigest()])
        put(root, manifest)
    return fn

def nested_symlink(root):
    (root/'app/src/main/assets').mkdir(exist_ok=True)
    (root/'app/src/main/assets/link').symlink_to(root/'README.md')

for name, fn, status in [
    ('unaltered',lambda r:None,0),('modified-source',altered,1),('unlisted-file',added,1),
    ('missing-row',missing,1),('duplicate-row',duplicate,1),('empty-manifest',empty,1),
    ('corrupt-csv',corrupt,1),('traversal',traversal,1),('invalid-header',bad_header,1),
    ('extra-field',extra_field,1),('invalid-hash',bad_hash,1),('symlink',symlink,1),
    ('excluded-cache',ignored_cache,1),
    ('asset-apk',inject('app/src/main/assets/injected.apk'),1),
    ('asset-class',inject('app/src/main/assets/injected.class'),1),
    ('asset-nested-build',inject('app/src/main/assets/build/injected.txt'),1),
    ('asset-nested-pycache',inject('app/src/main/assets/__pycache__/injected.pyc'),1),
    ('asset-symlink',nested_symlink,1),
    ('local-properties',inject('local.properties'),1),
    ('signing-material',inject('app/secret.jks'),1),
    *[('signing-valid-manifest-'+ext, signed_with_valid_manifest('app/keys/release.'+ext),1)
      for ext in ('p12','pem','key','pfx','pk8','asc','JKS','Keystore')],
    ('credentials-json',signed_with_valid_manifest('app/keys/credentials.json'),1),
    ('mixedcase-key-properties',signed_with_valid_manifest('app/keys/Key.Properties'),1)]:
    check(name,fn,status)
print('ADVERSARIAL_MANIFEST PASS 30/30')
