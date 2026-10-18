#!/usr/bin/env python3
"""Strict host evidence contract. Never infer success from substrings."""
import hashlib,json,pathlib,re,sys,csv
# Load sibling verifier by exact path only after its pinned digest is checked.
# Do not add checkout paths to sys.path under isolated Python startup.
import importlib.util
SOURCE_VERIFIER_SHA256 = "e0db83c0583c686876beccdd77220c0b810aa04172d2800849f3f2c05d918047"
source_verifier_file = pathlib.Path(__file__).resolve().with_name('verify_source_manifest.py')
if hashlib.sha256(source_verifier_file.read_bytes()).hexdigest() != SOURCE_VERIFIER_SHA256:
    raise ValueError('source verifier checksum mismatch')
spec = importlib.util.spec_from_file_location('_sarah_pinned_source_verifier', source_verifier_file)
if spec is None or spec.loader is None:
    raise ValueError('source verifier import unavailable')
source_verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(source_verifier)
MANIFEST, inventory = source_verifier.MANIFEST, source_verifier.inventory

def verify(folder, sha, run_id, attempt):
    p=pathlib.Path(folder)
    files={'source-manifest-verification.txt':r'SOURCE_MANIFEST PASS files=([1-9][0-9]*)\n?',
           'manifest-negative-tests.txt':None,
           'r07-policy-tests.txt':None,
           'r08-chained-policy-tests.txt':None,
           'r09-policy-tests.txt':None,
           'r10-policy-tests.txt':None,
           'host-regressions.txt':r'HOST_REGRESSIONS PASS\n?'}
    # Exact evidence artifact contract: seven reports plus one attestation, no extras.
    allowed=set(files)|{'host-attestation.json'}
    if not p.is_dir() or p.is_symlink():
        raise ValueError('unsafe evidence directory')
    actual={entry.name for entry in p.iterdir()}
    if actual!=allowed:
        raise ValueError('unexpected or missing evidence members: '+repr(sorted(actual ^ allowed)))
    if any(entry.is_symlink() or not entry.is_file() for entry in p.iterdir()):
        raise ValueError('unsafe evidence member')
    data={}
    for name,pat in files.items():
        f=p/name
        if not f.is_file() or f.is_symlink() or f.stat().st_size>200000: raise ValueError('missing/unsafe evidence '+name)
        data[name]=f.read_bytes()
        if pat and not re.fullmatch(pat,data[name].decode('utf-8')): raise ValueError('forged/contradictory evidence '+name)
    if data['r07-policy-tests.txt'].decode('utf-8').splitlines() != ['PASS reject '+x for x in ['app/keys/.env.production','app/keys/.ENV.STAGING','app/keys/signing.properties','app/keys/keystore.properties.bak','app/keys/key.properties.backup','app/keys/google-services.json','app/keys/service-account-prod.json','app/keys/aws-credentials.ini','app/keys/release.jks.backup','app/keys/release.p12.old']] + ['R07_CREDENTIAL_ALIASES PASS 10/10']:
        raise ValueError('R07 policy transcript missing or forged')
    if data['r08-chained-policy-tests.txt'].decode('utf-8').splitlines() != ['PASS reject '+x for x in ['app/keys/release.jks.backup.old', 'app/src/main/assets/google-services.json.old.bak', 'app/keys/credentials.json.old.backup', 'app/keys/release.p12~.old', 'app/keys/Id_Rsa.BAK.OLD', 'app/keys/service-account-prod.json.old.bak', 'app/src/main/assets/aws-credentials.ini.old.bak', 'app/keys/release.pem.bak.old', 'app/keys/release.jks.old.bak', 'app/keys/release.jks.backup.old.bak', 'app/keys/release.key~.bak', 'app/keys/release.pfx.old.backup']] + ['R08_CHAINED_CREDENTIAL_POLICY PASS 12/12']:
        raise ValueError('R08 policy transcript missing or forged')
    if data['r09-policy-tests.txt'].decode('utf-8').splitlines() != ['PASS reject '+x for x in ['app/keys/release.JKS.bkp','app/keys/release.PEM.copy','app/keys/release.KEY.swp','app/keys/release.p12.disabled','app/keys/release.pfx.old.1','app/keys/credentials.json.copy','tools/__pycache__/verify_source_manifest.cpython-311.pyc','tests/__pycache__/test_source_boundary.cpython-311.pyc','audit_harness/__pycache__/test.pyc']] + ['PASS reject symlinked bytecode','R09_POLICY PASS 10/10']:
        raise ValueError('R09 policy transcript missing or forged')
    expected_r10=['app/keys/release.jks.swo','app/keys/release.pem.swx','app/keys/release.p12.temp','app/keys/release.key.bak2','app/keys/release.pfx.backup_2','app/keys/release.jks.bak_2','app/keys/release.pem.bak20261017','app/keys/release.key.backup-2026-10-17']
    if data['r10-policy-tests.txt'].decode('utf-8').splitlines() != ['PASS '+x for x in expected_r10]+['R10_POLICY PASS 8/8']:
        raise ValueError('R10 policy transcript missing or forged')
    negatives=data['manifest-negative-tests.txt'].decode('utf-8').splitlines()
    expected=['unaltered','modified-source','unlisted-file','missing-row','duplicate-row','empty-manifest','corrupt-csv','traversal','invalid-header','extra-field','invalid-hash','symlink','excluded-cache','asset-apk','asset-class','asset-nested-build','asset-nested-pycache','asset-symlink','local-properties','signing-material'] + ['signing-valid-manifest-'+ext for ext in ('p12','pem','key','pfx','pk8','asc','JKS','Keystore')] + ['credentials-json','mixedcase-key-properties']
    if len(negatives)!=31 or negatives[-1]!='ADVERSARIAL_MANIFEST PASS 30/30': raise ValueError('negative suite incomplete')
    for line,label in zip(negatives[:-1],expected):
        expected_exit=0 if label in ('unaltered',) else 1
        if line!=f'PASS {label} exit {expected_exit}': raise ValueError('negative suite forged '+label)
    att=p/'host-attestation.json'
    if att.is_symlink() or not att.is_file() or att.stat().st_size>16384:
        raise ValueError('missing/unsafe host attestation')
    meta=json.loads(att.read_text(encoding='utf-8'))
    if set(meta)!={'schema','sha','run_id','attempt','digests'} or meta['schema']!=1 or (meta['sha'],str(meta['run_id']),str(meta['attempt']))!=(sha,str(run_id),str(attempt)): raise ValueError('cross-run or invalid provenance')
    if meta['digests']!={k:hashlib.sha256(v).hexdigest() for k,v in data.items()}: raise ValueError('evidence digest mismatch')
    reported=int(re.fullmatch(files['source-manifest-verification.txt'],data['source-manifest-verification.txt'].decode()).group(1))
    # Cross-check against actual checked-out source, not the attested text alone.
    with MANIFEST.open(newline='',encoding='utf-8-sig') as f:
        rows=list(csv.reader(f,strict=True))
    if not rows or rows[0]!=['path','sha256'] or len(rows)<2:
        raise ValueError('invalid canonical source inventory')
    canonical_count=len(rows)-1
    if reported!=canonical_count or reported!=len(inventory()):
        raise ValueError('host evidence source count disagrees with checkout')
    return reported
if __name__=='__main__':
    try:
        count=verify(*sys.argv[1:]);print('HOST_EVIDENCE PASS files='+str(count))
    except (ValueError,OSError,UnicodeError,KeyError,TypeError,IndexError,json.JSONDecodeError) as e:
        print('HOST_EVIDENCE FAIL: '+str(e),file=sys.stderr);sys.exit(1)
