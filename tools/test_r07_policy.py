import csv,hashlib,pathlib,subprocess,sys,tempfile,shutil
root=pathlib.Path(__file__).resolve().parents[1]
probes=['app/keys/.env.production','app/keys/.ENV.STAGING','app/keys/signing.properties','app/keys/keystore.properties.bak','app/keys/key.properties.backup','app/keys/google-services.json','app/keys/service-account-prod.json','app/keys/aws-credentials.ini','app/keys/release.jks.backup','app/keys/release.p12.old']
with tempfile.TemporaryDirectory() as td:
 for i,rel in enumerate(probes):
  work=pathlib.Path(td)/str(i);shutil.copytree(root,work,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
  target=work/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b'SYNTHETIC_NO_SECRET')
  with (work/'SHA256_MANIFEST.csv').open('a',newline='') as f:csv.writer(f).writerow([rel,hashlib.sha256(target.read_bytes()).hexdigest()])
  out=subprocess.run([sys.executable,'-B',str(work/'tools/verify_source_manifest.py')],capture_output=True,text=True)
  assert out.returncode!=0,(rel,out.stdout,out.stderr)
  print('PASS reject',rel)
print('R07_CREDENTIAL_ALIASES PASS 10/10')
