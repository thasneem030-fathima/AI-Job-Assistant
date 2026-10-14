async function analyze(){
 let resume = document.getElementById('resume').value;
 let job = document.getElementById('job').value;
 document.getElementById('result').innerHTML = "Analyzing... ⏳";
 try{
  let res = await fetch('http://127.0.0.1:5000/analyze', {
   method:'POST',
   headers:{'Content-Type':'application/json'},
   body: JSON.stringify({resume:resume, job_description:job})
  });
  let data = await res.json();
  document.getElementById('result').innerHTML = `<h3>Match: ${data.match_score}%</h3><p>${data.analysis}</p>`;
 }catch(e){
  document.getElementById('result').innerHTML = "Backend not running! Start backend terminal: cd backend -> python app.py";
 }
}