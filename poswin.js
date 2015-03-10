#!/usr/bin/env node

"use strict";

var nconf = require('nconf');
var spawn = require('child_process').spawn;
var osenv = require('osenv');
var path = require('path');
require('es6-promise').polyfill();

/**
 * Retrieve all informations about open windows
 *
 * @returns {Promise}
 */
function get_session() {
  return new Promise(function (resolve, reject) {

    var prc = spawn('wmctrl', ['-lxG']);
    var windows = [];
    // parse wmctrl output
    prc.stdout.setEncoding('utf8');
    prc.stdout.on('data', function (data) {
      var str = data.toString();
      var lines = str.replace(/  +/g, ' ').replace(/  +/g, ' ').trim().split("\n");
      windows = lines.map(function (line) {
        var w_specs = line.split(' ');
        return {
          id: w_specs[0],
          desktop: w_specs[1],
          x: w_specs[2],
          y: w_specs[3],
          width: w_specs[4],
          height: w_specs[5],
          name: w_specs[6]
        };
      });
    });

    prc.on('error', reject);
    prc.on('close', function (code) {
      if (code === 0)
        resolve(windows);
      else
        reject(code);
    });
  });
}

function load_conf() {
  nconf.use('file', {
    file: path.join(osenv.home(), '.poswin.json')
  });
  nconf.load();
  return nconf.get();
}

function save_conf(windows) {
  nconf.use('file', {
    file: path.join(osenv.home(), '.poswin.json')
  });
  nconf.load();
  windows.forEach(function (w) {
    nconf.set(w.name, w);
  });
  nconf.save();
}

function save_session() {
  get_session().then(save_conf).catch(console.error);
}

function restore_win(curr_windows, win_to_restore) {
  console.log("Restoring window: %s ", win_to_restore.name);
  //  console.log(win_to_restore);
  // search if this win exists
  var win_id = curr_windows.reduce(function (pv, cv) {
    return (cv.name === win_to_restore.name ? cv.id : pv);
  });

  if (!win_id) return;
  var args = ['-i', '-r', win_id, '-t', win_to_restore.desktop, '-e',
              ['0', win_to_restore.x, win_to_restore.y, win_to_restore.width,
              win_to_restore.height].join(',')];

  console.log(args.join(' '));

  //move to correct desktop
  spawn('wmctrl', args);

  //restore position and size

}

function load_session() {
  get_session().then(function (curr_windows) {
    var windows = load_conf();
    for (var w_name in windows) {
      if (!windows.hasOwnProperty(w_name)) continue;
      var w = windows[w_name];
      if (w.desktop === "-1" || w.name.indexOf('indicator') > -1) continue;
      restore_win(curr_windows, w);
    }
  }).catch(console.log);
}

if (process.argv.indexOf('save') > -1)
  save_session();
else if (process.argv.indexOf('load') > -1)
  load_session();
else
  console.log("use save or load");
