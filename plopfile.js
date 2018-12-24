
const inquirerRecursive = require('inquirer-recursive');
const shell = require('shelljs');
const SerialPort = require('serialport');

const confirmRerquiredSoftware = function(){
  if (!shell.which('esptool.py.exe')) {
    shell.echo('Sorry, this script requires esptool.py.exe');
    shell.exit(1);
  }

  if (!shell.which('ampy.exe')) {
    shell.echo('Sorry, this script requires ampy.exe');
    shell.exit(1);
  }
}

const comport_prompt =  {
  type: 'list',
  name: 'comport',
  message: 'specify the comport e.g dev/ttyUSB0 or COM1',
  choices:function(){
    const result = []
    return new Promise((resolve, reject) => {
      SerialPort.list(function (err, ports) {
        ports.forEach(function(port) {
          result.push(port.comName)
        });
        resolve(result);
      });
    });

  }
}

const selectproductfolder_prompt = {
  type: 'list',
  name: 'foldername',
  message: 'select the product folder',

  choices:function(){
    const foldernames = []
    shell.ls('-d','./src/*').forEach(function (file) {
      foldernames.push(file.split('/').pop())
    })
    return foldernames
  }
}

const selectcorefile_prompt = {
    type: 'list',
    name: 'filename',
    message: 'select the core file',

    choices:function(){
      const filenames = []
      shell.ls('./internals/core/*').forEach(function (file) {
        filenames.push(file.split('/').pop())
      })
      return filenames
    }
}

const  selectfirmware_prompt = {
  type: 'list',
  name: 'flashfile',
  message: 'Select the firmware for your product',
  choices:function(){

    const filenames = []
    shell.ls('./internals/bin/*').forEach(function (file) {
      filenames.push(file)
    })
    return filenames

  }
}


module.exports = function (plop) {
    // WireUP product 
    
    confirmRerquiredSoftware()

    plop.setPrompt('recursive', inquirerRecursive);
    plop.setHelper('typename',(txt) => txt.toLowerCase().replace(/\s/g,''));
    plop.setHelper('lowercase',(txt) => txt.toLowerCase().replace(/\s/g,''));
    plop.setHelper('indexadjust',(index) => Number(index) + 4);
    plop.setHelper('pseudorandomkey',() => Math.random().toString(36).replace(/[^a-z]+/g, '').substr(0, 15) );

    plop.setHelper('stringAssist', function (value) {
        switch(typeof value){
              case 'number': return value;
              case 'boolean': return value ? "True" : "False"
              case 'string': return "'"+value+"'";
        }
    });



    plop.setGenerator('flash', {
      description: 'choose the interpreter to flash to the ESP8266',
      prompts: [
        selectfirmware_prompt,
        comport_prompt
      ],
      actions:function(answers){
        var actions = [];

        process.stdout.write('Flashing firmware');
        if (shell.exec(

        'esptool.py.exe --port '+answers.comport+' --baud 460800 write_flash --flash_size=detect 0 '+answers.flashfile

        ).code !== 0) {
          shell.echo('\nError: could not flash software');
          shell.exit(1);
        }

        return actions
      }
    }
  )

  plop.setGenerator('erase', {
    description: 'erases the entire flash of the ESP8266',
    prompts: [ comport_prompt ],
    actions:function(answers){
      var actions = [];

      process.stdout.write('Erasing Flash');
      if (shell.exec(

      'esptool.py.exe --port '+answers.comport+' --baud 460800 erase_flash'

      ).code !== 0) {
        shell.echo('\nError: could not erease flash');
        shell.exit(1);
      }

      return actions
    }
  }
)    


plop.setGenerator('upload', {
  description: 'upload a code',
  prompts: [
    selectproductfolder_prompt,
    comport_prompt
  ],
  actions:function(answers){
    var actions = [];

    const filenames = []
    
    shell.ls('./src/'+answers.foldername).forEach(function (file) {
      filenames.push(file)
    })

    process.stdout.write('\nuploading')
    
    filenames.forEach((filename) => {
      process.stdout.write('\n'+filename)
        if (shell.exec(
          'ampy -p '+answers.comport+' -b 115200 put ./src/'+answers.foldername+'/'+filename
        ).code !== 0) {
          shell.echo('\nError: could not upload file', filename);
          shell.exit(1);
        }
    })

    process.stdout.write('\nstarting terminal');
    shell.exec('D:/putty/putty.exe -serial '+answers.comport+' -sercfg 115200,8,n,1,N')

    return actions
  }
}
)



plop.setGenerator('removefile', {
  description: 'remove a file from the device',
  prompts: [
    selectcorefile_prompt,
    comport_prompt
  ],
  actions:function(answers){
    var actions = [];

    process.stdout.write('\nremoving '+answers.filename)

    if (shell.exec(
      'ampy -p '+answers.comport+' -b 115200 rm '+answers.filename
    ).code !== 0) {
      shell.echo('\nError: could not upload file', answers.filename);
      shell.exit(1);
    }

    return actions
  }
}
)

plop.setGenerator('list', {
description: 'files on the device',
prompts: [ comport_prompt ],
actions:function(answers){
  var actions = [];

  if (shell.exec(
    'ampy -p '+answers.comport+' -b 115200 ls'
  ).code !== 0) {
    shell.echo('\nError: could not list files', answers.flashfile);
    shell.exit(1);
  }

  return actions
}
}
)



}; // Plot function end
