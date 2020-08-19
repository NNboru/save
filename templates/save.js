
async function loadfiles(){
    showloader('loading...');
    let resp = await fetch('https://save.pythonanywhere.com/allfiles');
    if(!resp.ok)
        showerror('Some error occurred while connecting to server');
    else{
        let dict = await resp.json();
        if(dict['code'])
            showerror(dict['msg']);
        else{
            files=dict['msg'];
            for(let f of files)
                tab.insertAdjacentHTML('beforeEnd',`
                    <tr>
                        <td><a href='https://save.pythonanywhere.com/load/${f[4]}'>${f[1]}</a></td>
                        <td>${f[2]}</td>
                        <td>${f[3]}</td>
                        <td><a href='https://save.pythonanywhere.com/load/${f[4]}' target='_blank' download='${f[1]}'>download</a></td>
                    </tr>
                `);
        }
    }
    hideloader();
}
loadfiles();

async function upload(files){
    for(let i=0;i<files.length;++i){
        if(files[i].size>1024*1024*100){
            showerror(`size of file "${files[i].name}" is > 100mb. Too large!!`);
            continue;
        }
        showloader('uploading file - ' + files[i].name);
        let obj= new FormData();
        obj.append('file',files[i],files[i].name);
        obj.append('size',getsize(files[i].size));
        
        let resp = await fetch('https://save.pythonanywhere.com/save', { method:'POST', body:obj });
        if(!resp.ok)
        showerror('Some error occurred!');
        else{
            let dict = await resp.json();
            if(dict['code'])
            showerror(dict['msg']);
            else{
                tab.insertAdjacentHTML('beforeEnd',`
                    <tr>
                        <td><a href='https://save.pythonanywhere.com/load/${dict['msg']}'>${files[i].name}</a></td></td>
                        <td>${getsize(files[i].size)}</td>
                        <td>${dict['date']}</td>
                        <td><a href='https://save.pythonanywhere.com/load/${dict['msg']}' target='_blank'
                            download='${files[i].name}'>download</a></td>
                    </tr>
                `);
            }
        }
        hideloader();
    }
}

function getsize(s){
    if(s<1024)
    return s+' bytes';
    s=Math.round(s/10.24)/100;
    if(s<1024)
    return s+' kb';
    s=Math.round(s/10.24)/100;
    return s+' mb';
}

function showerror(msg){
    error.innerHTML=msg;
    error.classList.remove('hide');
    setTimeout(()=>error.classList.add('hide'),5000);
}

function showloader(msg){
    loader.innerHTML=msg;
    loader.classList.remove('hide');
}
function hideloader(){
    loader.classList.add('hide');
}


frmfile.onchange=()=>upload(frmfile.files);

bdy.ondrop=e=>{
    e.preventDefault();
    upload(e.dataTransfer.files);
    droping.classList.add('hide');
}
bdy.ondragover=e=>{
    e.preventDefault();
    console.dir('yo');
    droping.classList.remove('hide');
}

loader.onclick=error.onclick=droping.onclick=e=>{e.target.classList.add('hide')};
