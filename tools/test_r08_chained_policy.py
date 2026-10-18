import csv,hashlib,pathlib,subprocess,sys,tempfile,shutil
root=pathlib.Path(__file__).resolve().parents[1]
probes=['app/keys/release.jks.backup.old', 'app/src/main/assets/google-services.json.old.bak', 'app/keys/credentials.json.old.backup', 'app/keys/release.p12~.old', 'app/keys/Id_Rsa.BAK.OLD', 'app/keys/service-account-prod.json.old.bak', 'app/src/main/assets/aws-credentials.ini.old.bak', 'app/keys/release.pem.bak.old', 'app/keys/release.jks.old.bak', 'app/keys/release.jks.backup.old.bak', 'app/keys/release.key~.bak', 'app/keys/release.pfx.old.backup']
with tempfile.TemporaryDirectory() as td:
 for i,rel in enumerate(probes):
  work=pathlib.Path(td)/str(i);shutil.copytree(root,work,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
  target=work/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b'SYNTHETIC_NO_SECRET')
  with (work/'SHA256_MANIFEST.csv').open('a',newline='') as f:csv.writer(f).writerow([rel,hashlib.sha256(target.read_bytes()).hexdigest()])
  out=subprocess.run([sys.executable,'-B',str(work/'tools/verify_source_manifest.py')],capture_output=True,text=True)
  assert out.returncode!=0,(rel,out.stdout,out.stderr)
  print('PASS reject',rel)
print('R08_CHAINED_CREDENTIAL_POLICY PASS 12/12')
