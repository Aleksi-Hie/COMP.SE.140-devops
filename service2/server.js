const dns = require('dns');
const {exec} = require('child_process');
const {createServer} = require('http');

const serviceName = process.env.SERVICE_NAME || 'service2'
const port = 8200
function IpLookup(){
    return new Promise((resolve, reject) => {
        dns.lookup(serviceName, (err, address, family) => {
            if(err){
                reject(err)
            }
            else{
                resolve(address)
            }
        });
    });

}

async function getIp(){
    const ip = await IpLookup(serviceName)
    return ip
}

function sendShellCommand(command){
    return new Promise((resolve, reject) =>{
        exec(command, (err, stdout, stderr) =>{
            if(err){
                reject(err)
            }else{
                resolve(stdout);
            }
        })
    })
}

async function getProcesses(){
    const processes = await sendShellCommand("ps -ax")
    //console.log(processes)
    return processes;
}
async function getDiskSpace(){
    const diskSpace = await sendShellCommand("df")
    //console.log(diskSpace)
    return diskSpace;
}

async function getRebootTime(){
    const rebootTime = await sendShellCommand("uptime -p")
    //console.log(rebootTime)
    return rebootTime
}

async function getData(){
    let object = {ip: await getIp(),
                  processes: await getProcesses(),
                  diskspace:await getDiskSpace(),
                  reboottime:await getRebootTime()
    };
    return object;
}


const server = createServer((req, res) => {
    console.log(req.url)
    if (req.url === '/shutdown/') {
        res.statusCode = 200;
        res.end();
        process.exit(0);
    }

    res.statusCode = 200;
    getData().then((data) => {
        res.setHeader('Content-Type', 'application/json');
        res.write(JSON.stringify(data))
        res.end();
    })
});

server.listen(port, "0.0.0.0")

