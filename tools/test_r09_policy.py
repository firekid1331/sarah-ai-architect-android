import csv,hashlib,pathlib,subprocess,sys,tempfile,shutil
root=pathlib.Path(__file__).resolve().parents[1]
probes=['app/keys/release.JKS.bkp','app/keys/release.PEM.copy','app/keys/release.KEY.swp','app/keys/release.p12.disabled','app/keys/release.pfx.old.1','app/keys/credentials.json.copy','tools/__pycache__/verify_source_manifest.cpython-311.pyc','tests/__pycache__/test_source_boundary.cpython-311.pyc','audit_harness/__pycache__/test.pyc']
with tempfile.TemporaryDirectory() as td:
 for i,rel in enumerate(probes):
  work=pathlib.Path(td)/str(i);shutil.copytree(root,work)
  target=work/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b'SYNTHETIC_TEST_ONLY')
  with (work/'SHA256_MANIFEST.csv').open('a',newline='') as f:csv.writer(f).writerow([rel,hashlib.sha256(target.read_bytes()).hexdigest()])
  out=subprocess.run([sys.executable,'-B',str(work/'tools/verify_source_manifest.py')],capture_output=True,text=True)
  assert out.returncode != 0,(rel,out.stdout,out.stderr)
  print('PASS reject',rel)
 # Symlink in excluded tree must also be rejected
 work=pathlib.Path(td)/'symlink';shutil.copytree(root,work)
 cache=work/'tools/__pycache__';cache.mkdir();(cache/'outside.pyc').symlink_to(work/'README.md')
 out=subprocess.run([sys.executable,'-B',str(work/'tools/verify_source_manifest.py')],capture_output=True,text=True)
 assert out.returncode != 0,(out.stdout,out.stderr)
 print('PASS reject symlinked bytecode')
print('R09_POLICY PASS 10/10')
