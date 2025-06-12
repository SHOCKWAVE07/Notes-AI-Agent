async function send(url, body) {
  const res = await fetch(url, body);
  const data = await res.json();
  alert(JSON.stringify(data));
  loadNotes();
}

function recordVoice() {
  navigator.mediaDevices.getUserMedia({audio: true})
    .then(stream => {
      const rec = new MediaRecorder(stream);
      const chunks = [];
      rec.ondataavailable = e => chunks.push(e.data);
      rec.onstop = async () => {
        const b = new Blob(chunks, {type: "audio/wav"});
        const form = new FormData();
        form.append("file", b, "voice.wav");
        await send("http://localhost:8000/voice-command", {method:"POST",body:form});
      };
      rec.start();
      setTimeout(() => rec.stop(), 4000);
    });
}

document.getElementById("voiceBtn").onclick = recordVoice;
document.getElementById("textBtn").onclick = () => {
  const text = document.getElementById("textInput").value;
  send("http://localhost:8000/text-command", {method:"POST",headers:{"Content-Type":"application/json"}, body: JSON.stringify({"msg": text})});
};

async function loadNotes() {
  const res = await fetch("http://localhost:8000/notes");
  const notes = await res.json();
  const out = notes.map(n => `
    <div class="p-4 border rounded shadow">
      <div class="text-gray-500 text-sm">${n.created_at}${n.updated_at ? " (edited)" : ""}</div>
      <div>${n.text}</div>
      <div class="text-blue-500 text-sm">[${n.tags.join(", ")}]</div>
    </div>`).join("");
  document.getElementById("notes").innerHTML = out;
}
loadNotes();
