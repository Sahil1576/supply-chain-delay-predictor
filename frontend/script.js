const $ = id => document.getElementById(id);
let file = null, markdown = "";

/* theme */
const root = document.documentElement;
const setTheme = t => { root.dataset.theme = t; $("themeBtn").textContent = t === "dark" ? "☀️" : "🌙"; localStorage.setItem("theme", t); };
setTheme(localStorage.getItem("theme") || (matchMedia("(prefers-color-scheme:dark)").matches ? "dark" : "light"));
$("themeBtn").onclick = () => setTheme(root.dataset.theme === "dark" ? "light" : "dark");

/* file selection */
const drop = $("drop"), input = $("fileInput");
drop.onclick = () => input.click();
drop.onkeydown = e => (e.key === "Enter" || e.key === " ") && input.click();
["dragenter","dragover"].forEach(ev => drop.addEventListener(ev, e => { e.preventDefault(); drop.classList.add("over"); }));
["dragleave","drop"].forEach(ev => drop.addEventListener(ev, e => { e.preventDefault(); drop.classList.remove("over"); }));
drop.addEventListener("drop", e => setFile(e.dataTransfer.files[0]));
input.onchange = () => setFile(input.files[0]);
$("clearBtn").onclick = () => setFile(null);

function setFile(f){
  showError("");
  if (f && !f.name.toLowerCase().endsWith(".csv")) { showError("Please choose a .csv file."); return; }
  file = f || null; input.value = "";
  $("fileBox").classList.toggle("show", !!file);
  $("runBtn").disabled = !file;
  if (file){ $("fileName").textContent = file.name; $("fileMeta").textContent = (file.size/1024).toFixed(1) + " KB"; }
}

function showError(msg){ const e = $("error"); e.textContent = msg; e.classList.toggle("show", !!msg); }

/* progress steps */
let timers = [];
function setStep(n){
  [...$("steps").children].forEach((li,i) => { li.className = i < n ? "done" : i === n ? "active" : ""; li.firstChild.textContent = i < n ? "✓" : ""; });
}
function startSteps(){
  $("status").classList.add("show"); setStep(0);
  timers = [setTimeout(() => setStep(1), 1200), setTimeout(() => setStep(2), 4000)];
}
function stopSteps(ok){
  timers.forEach(clearTimeout);
  if (ok) setStep(3); else $("status").classList.remove("show");
}

/* run */
$("runBtn").onclick = async () => {
  if (!file) return;
  showError(""); $("results").classList.remove("show");
  $("runBtn").disabled = true; $("runBtn").textContent = "Analyzing…";
  startSteps();
  try{
    const fd = new FormData(); fd.append("file", file);
    const res = await fetch($("apiUrl").value.replace(/\/$/,"") + "/predict", { method:"POST", body:fd });
    if (!res.ok){
      let detail = res.statusText;
      try { const j = await res.json(); detail = typeof j.detail === "string" ? j.detail : JSON.stringify(j.detail || j); } catch {}
      throw new Error(`Server returned ${res.status}: ${detail}`);
    }
    const data = await res.json();
    markdown = typeof data === "string" ? data : (data.report || JSON.stringify(data, null, 2));
    stopSteps(true);
    render(markdown);
  }catch(err){
    stopSteps(false);
    showError(err instanceof TypeError ? "Could not reach the API. Check that the server is running, the URL is correct, and CORS is enabled." : err.message);
  }finally{
    $("runBtn").disabled = !file; $("runBtn").textContent = "Generate report";
  }
};

/* render */
function render(md){
  const html = DOMPurify.sanitize(marked.parse(md));
  const box = $("report"); box.innerHTML = html;
  box.querySelectorAll("table").forEach(t => { const w = document.createElement("div"); w.className = "tbl"; t.replaceWith(w); w.appendChild(t); });
  const toc = $("toc"); toc.innerHTML = "";
  box.querySelectorAll("h2").forEach((h,i) => {
    h.id = "sec" + i;
    const a = document.createElement("a"); a.href = "#sec" + i; a.textContent = h.textContent.replace(/^\d+\.\s*/,"");
    toc.appendChild(a);
  });
  $("results").classList.add("show");
  $("results").scrollIntoView({ behavior:"smooth", block:"start" });
}

/* scroll spy */
addEventListener("scroll", () => {
  const hs = [...document.querySelectorAll("#report h2")]; let cur = null;
  hs.forEach(h => { if (h.getBoundingClientRect().top < 120) cur = h.id; });
  document.querySelectorAll("#toc a").forEach(a => a.classList.toggle("on", a.getAttribute("href") === "#" + cur));
});

/* actions */
$("copyBtn").onclick = async e => { await navigator.clipboard.writeText(markdown); e.target.textContent = "Copied ✓"; setTimeout(() => e.target.textContent = "Copy", 1500); };
$("mdBtn").onclick = () => { const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob([markdown], {type:"text/markdown"})); a.download = "delay-report.md"; a.click(); URL.revokeObjectURL(a.href); };
$("pdfBtn").onclick = () => print();
