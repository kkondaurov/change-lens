// This account is bound to the published capture described in docs/PROVENANCE.md.
// A new import requires a new review, not just replacement JSON.
export const evidenceHashes = {
  "bundle.json": "4a1df271db7072513c433f26309abd87940a0f825b753ff9e3abf6c914bc7d52",
  "fresh-reviews.json": "b27513386a6323e3307d6eff9705bc69ef8d302ae58ff9021835e54129b15b87"
};

export async function parseCapturedEvidence(name, text) {
  const digest = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  const actual = Array.from(new Uint8Array(digest), b => b.toString(16).padStart(2,'0')).join('');
  if (!evidenceHashes[name] || actual !== evidenceHashes[name]) {
    throw new Error('The captured evidence has changed. This explanation and review belong to an earlier snapshot. Regenerate and review the narrative before updating its evidence lock.');
  }
  return JSON.parse(text);
}
