import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {evidenceRef,exportNotes} from '../src/domain.js';
import {parseCapturedEvidence} from '../src/provenance.js';
const read=p=>readFileSync(new URL(p,import.meta.url),'utf8');
const raw=read('../public/evidence/bundle.json'),bundle=JSON.parse(raw),reviews=JSON.parse(read('../src/reviews.json'));
const sha=s=>createHash('sha256').update(s).digest('hex');

test('changed captured sources or fresh reviews stop the review from loading',async()=>{
  assert.equal((await parseCapturedEvidence('bundle.json',raw)).runId,bundle.runId);
  const fresh=read('../public/evidence/fresh-reviews.json');
  await parseCapturedEvidence('fresh-reviews.json',fresh);
  await assert.rejects(parseCapturedEvidence('bundle.json',raw.replace('active rooms','all rooms')),/evidence has changed/);
  await assert.rejects(parseCapturedEvidence('fresh-reviews.json',fresh+' '),/evidence has changed/);
});

test('snapshot identities agree with all embedded and standalone source bytes',()=>{
  for(const [milestone,snapshot] of Object.entries(bundle.milestones)){
    const entries=Object.entries(snapshot.files).sort(([a],[b])=>a<b?-1:a>b?1:0);
    for(const [path,file] of entries){
      assert.equal(sha(file.text),file.sha256,path);
      assert.equal(read(`../public/evidence/snapshots/milestone-${milestone}/${path}`),file.text,path);
    }
    assert.equal(sha(entries.map(([path,f])=>path+'\0'+f.sha256+'\n').join('')),snapshot.fingerprint);
  }
});

test('published package hashes and separate evidence copies agree',()=>{
  const publication=JSON.parse(read('../public/evidence/publication.json'));
  const manifest=JSON.parse(read('../public/evidence/manifest.json'));
  assert.equal(manifest.bundleSha256,sha(raw));
  assert.equal(manifest.localOnly,false);
  for(const [name,record] of Object.entries(publication.artifacts))
    assert.equal(sha(read('../public/evidence/'+name)),record.publishedSha256,name);
  for(const [m,fingerprint] of Object.entries(publication.snapshotFingerprints))
    assert.equal(fingerprint,bundle.milestones[m].fingerprint);
  const fresh=JSON.parse(read('../public/evidence/fresh-reviews.json'));
  assert.equal(fresh['3'].report,read('../public/evidence/fresh-review.md'));
  assert.equal(fresh['4'].report,read('../public/evidence/fresh-review-m4.md'));
  assert.equal(fresh['4'].execution,read('../public/evidence/m4-reproduction.log'));
  assert.equal(fresh['4'].test,read('../public/evidence/reviewer_active_totals_test.exs'));
  assert.equal(fresh['4'].environment,read('../public/evidence/reproduction-environment.md'));
});

test('each change distinguishes the correct base, task, and submitted source versions',()=>{
  let count=0;
  const validate=r=>{count++;const f=bundle.milestones[String(r.m)]?.files[r.path];assert.ok(f,JSON.stringify(r));assert.ok(r.start>=1&&r.end>=r.start&&r.end<=f.lines,JSON.stringify(r));};
  for(const [key,c] of Object.entries(reviews)){
    const m=Number(key);
    assert.equal(c.baseFingerprint,bundle.milestones[String(m-1)].fingerprint);
    assert.equal(c.headFingerprint,bundle.milestones[key].fingerprint);
    for(const x of c.changes){
      for(const [kind,version] of [['before',m-1],['requirement',m],['after',m]]){
        assert.ok(x.refs[kind].length>0,`${x.id} ${kind}`);
        for(const r of x.refs[kind]){assert.equal(r.m,version);validate(r);}
      }
      x.refs.tests.forEach(validate);x.implementationSteps.forEach(s=>validate(s.ref));
    }
    for(const mod of c.modules)mod.refs.forEach(validate);
  }
  assert.ok(count>150);
});

test('execution view values exist in captured reviewer output rather than a UI simulation',()=>{
  const fresh=JSON.parse(read('../public/evidence/fresh-reviews.json'));
  const evidence=JSON.parse(fresh['4'].execution.split('\n').find(l=>l.startsWith('REVIEW_EVIDENCE ')).slice(16));
  assert.equal(evidence.active_rooms,0);
  assert.equal(evidence.after_last.deposit_due_cents,10500);
  assert.equal(evidence.after_last.deposit_paid_cents,1000);
  assert.equal(evidence.ledger.cash_held_cents,0);
  assert.ok(fresh['4'].test.includes('op-cancel-last'));
  assert.ok(fresh['4'].execution.includes('Failed: 1 test'));
  for(const needle of ['returns the original applied result and applies nothing twice','object key order is irrelevant','is rejected and does not replace the original record','an exact retry of a stale operation reports the original actual revision','an unexpected fault rolls the operation back and aborts the batch']){
    const r=evidenceRef(bundle,3,'test/group_stay_web/controllers/idempotency_test.exs',needle);
    assert.ok(!r.missing&&!r.missingNeedle,needle);
  }
});

test('note and assessment exports retain their own snapshot provenance',()=>{
  const out=exportNotes({bundle,notes:[{m:4,subject:'Contract',kind:'Context',createdAt:'2026-09-06',fingerprint:'original-note-snapshot',source:'request.md:31',text:'External clients need historical totals.'}],decisions:{'m4-totals':{value:'Needs clarification',fingerprint:'original-assessment-snapshot',createdAt:'2026-09-06'}}});
  for(const str of ['original-note-snapshot','original-assessment-snapshot','request.md:31','Needs clarification',bundle.runId])assert.ok(out.includes(str));
});
