const video = document.getElementById("video");

navigator.mediaDevices.getUserMedia({

video:true

})

.then(stream=>{

video.srcObject=stream;

})

.catch(()=>{

alert("Camera not working")

});

function capture(){

const canvas=document.getElementById("canvas");
const ctx=canvas.getContext("2d");

canvas.width=video.videoWidth;
canvas.height=video.videoHeight;

ctx.drawImage(video,0,0);

canvas.toBlob(blob=>{

let form=new FormData();

form.append("image",blob);

fetch("http://127.0.0.1:5000/api/detect",{

method:"POST",
body:form

})

.then(res=>res.json())

.then(data=>{

console.log(data);

if(!data.success){

document.getElementById("result").innerHTML="No Waste Found";
return;

}

let top=data.top;

document.getElementById("result").innerHTML=

`

<h2>Detected Object</h2>

<h3>${top.label}</h3>

<p>Confidence : ${(top.confidence*100).toFixed(1)}%</p>

<p>Category : ${top.category}</p>

<p>Bin : ${top.disposal.bin}</p>

<p>Instruction : ${top.disposal.instruction}</p>

`;

})

.catch(()=>{

document.getElementById("result").innerHTML="Backend Not Connected"

});

});

}