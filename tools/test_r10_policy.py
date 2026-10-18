import csv,hashlib,pathlib,subprocess,sys,tempfile,shutil,os
root=pathlib.Path(__file__).resolve().parents[1]
probes=['app/keys/release.jks.swo','app/keys/release.pem.swx','app/keys/release.p12.temp','app/keys/release.key.bak2','app/keys/release.pfx.backup_2','app/keys/release.jks.bak_2','app/keys/release.pem.bak20261017','app/keys/release.key.backup-2026-10-17']
with tempfile.TemporaryDirectory() as td:
 for i,rel in enumerate(probes):
  work=pathlib.Path(td)/str(i);shutil.copytree(root,work)
  target=work/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b'SYNTHETIC_ONLY')
  with (work/'SHA256_MANIFEST.csv').open('a',newline='') as f:csv.writer(f).writerow([rel,hashlib.sha256(target.read_bytes()).hexdigest()])
  p=subprocess.run([sys.executable,'-I','-S','-B',str(work/'tools/verify_source_manifest.py')],capture_output=True,text=True)
  assert p.returncode!=0,(rel,p.stdout,p.stderr)
  print('PASS',rel)
 print('R10_POLICY PASS 8/8')
