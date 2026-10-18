import hashlib,json,pathlib,subprocess,sys,tempfile,os
root=pathlib.Path(__file__).resolve().parents[1]
verify=root/'tools/verify_host_evidence.py'
with tempfile.TemporaryDirectory() as tmp:
 p=pathlib.Path(tmp)
 source=('SOURCE_MANIFEST PASS files='+str(sum(1 for _ in __import__('csv').reader((root/'SHA256_MANIFEST.csv').open()))-1)+'\n').encode()
 names=['unaltered','modified-source','unlisted-file','missing-row','duplicate-row','empty-manifest','corrupt-csv','traversal','invalid-header','extra-field','invalid-hash','symlink','excluded-cache','asset-apk','asset-class','asset-nested-build','asset-nested-pycache','asset-symlink','local-properties','signing-material'] + ['signing-valid-manifest-'+ext for ext in ('p12','pem','key','pfx','pk8','asc','JKS','Keystore')] + ['credentials-json','mixedcase-key-properties']
 negative=''.join('PASS '+n+' exit '+str(0 if n in ('unaltered',) else 1)+'\n' for n in names).encode()+b'ADVERSARIAL_MANIFEST PASS 30/30\n'
 files={'source-manifest-verification.txt':source,'manifest-negative-tests.txt':negative,'host-regressions.txt':b'HOST_REGRESSIONS PASS\n', 'r07-policy-tests.txt':(''.join('PASS reject '+x+'\n' for x in ['app/keys/.env.production','app/keys/.ENV.STAGING','app/keys/signing.properties','app/keys/keystore.properties.bak','app/keys/key.properties.backup','app/keys/google-services.json','app/keys/service-account-prod.json','app/keys/aws-credentials.ini','app/keys/release.jks.backup','app/keys/release.p12.old'])+'R07_CREDENTIAL_ALIASES PASS 10/10\n').encode(), 'r08-chained-policy-tests.txt':(''.join('PASS reject '+x+'\n' for x in ['app/keys/release.jks.backup.old', 'app/src/main/assets/google-services.json.old.bak', 'app/keys/credentials.json.old.backup', 'app/keys/release.p12~.old', 'app/keys/Id_Rsa.BAK.OLD', 'app/keys/service-account-prod.json.old.bak', 'app/src/main/assets/aws-credentials.ini.old.bak', 'app/keys/release.pem.bak.old', 'app/keys/release.jks.old.bak', 'app/keys/release.jks.backup.old.bak', 'app/keys/release.key~.bak', 'app/keys/release.pfx.old.backup'])+'R08_CHAINED_CREDENTIAL_POLICY PASS 12/12\n').encode(), 'r09-policy-tests.txt':(''.join('PASS reject '+x+'\n' for x in ['app/keys/release.JKS.bkp','app/keys/release.PEM.copy','app/keys/release.KEY.swp','app/keys/release.p12.disabled','app/keys/release.pfx.old.1','app/keys/credentials.json.copy','tools/__pycache__/verify_source_manifest.cpython-311.pyc','tests/__pycache__/test_source_boundary.cpython-311.pyc','audit_harness/__pycache__/test.pyc'])+'PASS reject symlinked bytecode\nR09_POLICY PASS 10/10\n').encode()}
 files['r10-policy-tests.txt']=(''.join('PASS '+x+'\n' for x in ['app/keys/release.jks.swo','app/keys/release.pem.swx','app/keys/release.p12.temp','app/keys/release.key.bak2','app/keys/release.pfx.backup_2','app/keys/release.jks.bak_2','app/keys/release.pem.bak20261017','app/keys/release.key.backup-2026-10-17'])+'R10_POLICY PASS 8/8\n').encode()
 def seal():
  (p/'host-attestation.json').write_text(json.dumps({'schema':1,'sha':'a'*40,'run_id':'42','attempt':'1','digests':{n:hashlib.sha256((p/n).read_bytes()).hexdigest() for n in files}}))
 def run(expect):
  z=subprocess.run([sys.executable,'-B',str(verify),str(p),'a'*40,'42','1'],capture_output=True,text=True)
  assert (z.returncode==0)==expect,(z.stdout,z.stderr)
 for n,v in files.items(): (p/n).write_bytes(v)
 seal();run(True);print('PASS valid')
 files['source-manifest-verification.txt']=b'SOURCE_MANIFEST PASS files=1\n'
 for n,v in files.items(): (p/n).write_bytes(v)
 seal();run(False);print('PASS reject positive-but-wrong-count')
 files['source-manifest-verification.txt']=source
 cases=[('forged-zero','source-manifest-verification.txt',b'SOURCE_MANIFEST PASS files=0\n'),('contradictory','source-manifest-verification.txt',source+b'SOURCE_MANIFEST FAIL\n'),('truncated','manifest-negative-tests.txt',negative[:-40]),('forged-negative','manifest-negative-tests.txt',b'ADVERSARIAL_MANIFEST PASS 0/0\n'),('missing-regressions','host-regressions.txt',None)]
 for label,name,payload in cases:
  for n,v in files.items(): (p/n).write_bytes(v)
  if payload is None:(p/name).unlink()
  else:(p/name).write_bytes(payload)
  seal() if payload is not None else None
  run(False);print('PASS reject',label)
 for n,v in files.items(): (p/n).write_bytes(v)
 seal();meta=json.loads((p/'host-attestation.json').read_text());meta['run_id']='43';(p/'host-attestation.json').write_text(json.dumps(meta));run(False);print('PASS reject cross-run')
 for n,val in files.items(): (p/n).write_bytes(val)
 seal()
 outside=pathlib.Path(tmp)/'outside.json';outside.write_bytes((p/'host-attestation.json').read_bytes())
 (p/'host-attestation.json').unlink();(p/'host-attestation.json').symlink_to(outside);run(False);print('PASS reject attestation-symlink')
 (p/'host-attestation.json').unlink();seal();(p/'host-attestation.json').write_bytes(b'x'*16385);run(False);print('PASS reject attestation-oversize')
 for n,val in files.items(): (p/n).write_bytes(val)
 seal();(p/'r07-policy-tests.txt').write_bytes(b'R07_CREDENTIAL_ALIASES PASS 0/0\n');seal();run(False);print('PASS reject forged-r07-policy')
 for n,val in files.items(): (p/n).write_bytes(val)
 seal();(p/'r08-chained-policy-tests.txt').write_bytes(b'R08_CHAINED_CREDENTIAL_POLICY PASS 0/0\n');seal();run(False);print('PASS reject forged-r08-policy')
 for n,val in files.items(): (p/n).write_bytes(val)
 seal();(p/'unexpected.bin').write_bytes(b'extra');run(False);print('PASS reject unexpected-file')
 (p/'unexpected.bin').unlink()
 seal();outside=pathlib.Path(tmp)/'outside-extra';outside.write_bytes(b'extra')
 (p/'unexpected.bin').symlink_to(outside);run(False);print('PASS reject unexpected-symlink')
 print('HOST_EVIDENCE_ADVERSARIAL PASS 14/14')
