export function evidenceRef(bundle,m,path,needle='',length=12) {
  const file=bundle.milestones[String(m)]?.files[path];
  if(!file) return {m,path,start:1,end:1,missing:true};
  const rows=file.text.split('\n');
  const index=needle?rows.findIndex(l=>l.includes(needle)):0;
  return {m,path,start:index<0?1:index+1,end:Math.min(rows.length,(index<0?0:index)+length),missingNeedle:index<0};
}

export function exportNotes({notes,decisions,bundle}) {
  const lines=['# Change Lens — review handoff','',`Source run: ${bundle.runId}`,'','This is a local human review handoff. No comments have been submitted to an MR.',''];
  for (const m of [3,4]) {
    const selected=notes.filter(n=>n.m===m);
    lines.push(`## Milestone ${m-1} → ${m}`,`Snapshot: ${bundle.milestones[String(m)].fingerprint}`,'');
    if(m===4&&decisions['m4-totals']) {const d=decisions['m4-totals'];lines.push(`Finding disposition: ${d.value||d}`,`Snapshot at assessment: ${d.fingerprint||'Not captured in earlier prototype'}`,`Assessed at: ${d.createdAt||'Not captured'}`,'');}
    if(!selected.length) lines.push('No human notes saved.','');
    for(const n of selected) lines.push(`### ${n.subject}`,`Type: ${n.kind} · ${n.createdAt}`,`Snapshot at note creation: ${n.fingerprint}`,n.source?`Source: ${n.source}`:'', '',n.text,'');
  }
  return lines.join('\n');
}
