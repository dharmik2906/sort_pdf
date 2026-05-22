
let inputFile = document.getElementById('input_file');
let logoImg = document.getElementById('logo_img');
let pdfImg = document.getElementById('pdf_img');
let loading = document.getElementById('loading_img');
let msg_succ= document.getElementById('msg_succ');

inputFile.addEventListener('change', function(){
    if(inputFile.files.length > 0){
        setTimeout(() => {
            alert('pdf uploded')
            loading.style.display = 'none'
            pdfImg.style.display = 'block';     
        }, 2000);
        logoImg.style.display = 'none';
        loading.style.display = 'block'
    }
    else{
        logoImg.style.display = 'block';
        pdfImg.style.display = 'none';
    }
});

let reset = document.getElementById('btn_reset');
reset.addEventListener('click',function(){
    logoImg.style.display = 'block';
    pdfImg.style.display = 'none';
    loading.style.display = 'none'

})