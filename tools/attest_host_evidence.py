import hashlib,json,os,pathlib
names=['source-manifest-verification.txt','manifest-negative-tests.txt','host-regressions.txt','r07-policy-tests.txt','r08-chained-policy-tests.txt','r09-policy-tests.txt', 'r10-policy-tests.txt']
meta={'schema':1,'sha':os.environ['GITHUB_SHA'],'run_id':os.environ['GITHUB_RUN_ID'],'attempt':os.environ['GITHUB_RUN_ATTEMPT'],'digests':{n:hashlib.sha256(pathlib.Path(n).read_bytes()).hexdigest() for n in names}}
pathlib.Path('host-attestation.json').write_text(json.dumps(meta,sort_keys=True)+'\n')
